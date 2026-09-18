"""Monta cada CENA (um bloco narrativo) como um MP4 mudo, normalizado, com a legenda
ja queimada. O video final so concatena essas cenas (concat -c copy) e muxa o audio.

  python cena.py <pasta-projeto> [--bloco N]

Por que cena = arquivo: 55% mais rapido que re-encodar tudo no fim, e
RETOMAVEL — se cair na cena 27, as 26 anteriores estao prontas e conferidas.

O bloco e uma SEQUENCIA de planos, nao um clipe em loop (mudanca da v1.3.0):
Ate a v1.2 a cena era UM clipe com `-stream_loop -1` esticado ate fechar o tempo do bloco.
Medido no primeiro video de verdade: bloco de 56s com clipe de 5,3s = o mesmo plano 10,5
vezes seguidas; 9 dos 14 blocos repetiam 3x ou mais. Agora a cena e montada com varios
segmentos de ~8s: trechos DIFERENTES dos clipes (offsets espalhados) intercalados com fotos
em Ken Burns. Foto nunca entra parada — sempre com zoom ou travelling, senao a retencao cai.

Pega-ratao do ffmpeg no Windows, todos resolvidos aqui:
- subtitles com caminho do Windows quebra o parser (os ':' viram separador de opcao).
  Solucao: roda com cwd na pasta da legenda e usa NOME RELATIVO.
- libass troca a fonte em silencio se nao acha: fontsdir aponta pra pasta com o .ttf.
- concat -c copy corrompe SEM ERRO se as cenas tiverem formatos diferentes: por isso
  toda cena sai identica (1920x1080, 30fps, yuv420p, mesmo timescale).
- zoompan com -loop 1 nunca termina: Ken Burns e d=1 + -t, com upscale antes pra nao tremer.
- foto gigante (5000px+) estoura a RAM no zoompan: midia.py ja reduz pra 2560.
"""
import math, pathlib, shutil, subprocess, sys
from comum import FFMPEG, V_ARGS, dur, erro, le_json, tem_video

FONTE_SRC = pathlib.Path(__file__).resolve().parent.parent / "assets" / "fontes"
FPS = 30
SEG_MIN = 4.5           # trecho menor que isso nao vira segmento
SEG_MAX_FOTO = 15.0     # foto segurando mais que isso cansa
# Clipe do Pexels e quase sempre UMA tomada continua: 3 trechos dele nao sao 3 planos, sao
# 3 vezes o mesmo lugar. No maximo 2, e so quando o clipe e longo (os pedacos ficam distantes).
MAX_SEG_POR_CLIPE = 2
DUR_PRA_DOIS_TRECHOS = 16.0
# preenche a tela (canal dark nao usa barra preta). increase+crop, nao decrease+pad.
NORM = (f"scale=1920:1080:force_original_aspect_ratio=increase,"
        f"crop=1920:1080,setsar=1,fps={FPS}")


def ken(variante, segundos):
    """Ken Burns com movimento VARIADO — duas fotos seguidas nunca se mexem igual.

    Upscale antes do zoompan pra nao tremer (o zoompan anda em passo de pixel do
    INPUT; com o dobro de resolucao o passo vira meio pixel na saida).
    """
    n = max(2, int(round(segundos * FPS)))
    base = "scale=3840:-2"
    z_max = 1.40   # movimento tem que ser VISIVEL: 1.32 ficava sutil demais num plano de 8s
    inc = (z_max - 1.0) / n
    centro = "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
    v = variante % 5
    if v == 0:      # zoom in, centrado
        zp = f"zoompan=z='min(zoom+{inc:.6f},{z_max})':d=1:{centro}"
    elif v == 1:    # zoom out, centrado
        zp = f"zoompan=z='if(lte(on,1),{z_max},max(zoom-{inc:.6f},1.0))':d=1:{centro}"
    elif v == 2:    # travelling pra direita
        zp = (f"zoompan=z='1.26':d=1:x='(iw-iw/zoom)*on/{n}':"
              f"y='ih/2-(ih/zoom/2)'")
    elif v == 3:    # travelling pra esquerda
        zp = (f"zoompan=z='1.26':d=1:x='(iw-iw/zoom)*(1-on/{n})':"
              f"y='ih/2-(ih/zoom/2)'")
    else:           # zoom in descendo
        zp = (f"zoompan=z='min(zoom+{inc:.6f},{z_max})':d=1:"
              f"x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*on/{n}'")
    return f"{base},{zp}:s=1920x1080:fps={FPS},setsar=1"


def segmentos(itens, alvo, seg):
    """Transforma a lista de midias do bloco numa sequencia de segmentos que cobre `alvo`.

    Um clipe entrega ate MAX_SEG_POR_CLIPE trechos, pegos em OFFSETS espalhados (o começo,
    o meio e o fim de um clipe sao planos diferentes). Foto entrega 1 segmento.
    """
    videos = [i for i in itens if i.get("tipo") == "video"]
    fotos = [i for i in itens if i.get("tipo") == "foto"]

    slots_v = []
    for it in videos:
        d = float(it.get("dur") or 0)
        if d < SEG_MIN:
            continue
        n = MAX_SEG_POR_CLIPE if d >= DUR_PRA_DOIS_TRECHOS else 1
        passo = d / n
        for k in range(n):
            off = k * passo
            slots_v.append({"arq": it["arquivo"], "tipo": "video", "off": round(off, 2),
                            "dur": min(seg, passo), "max": max(SEG_MIN, passo)})
    slots_f = [{"arq": i["arquivo"], "tipo": "foto", "off": 0.0,
                "dur": seg, "max": SEG_MAX_FOTO} for i in fotos]
    if not slots_v and not slots_f:
        return []

    # intercala: as fotos entram espalhadas no meio dos videos, nunca em bloco
    fila = []
    if slots_f and slots_v:
        passo = max(1, math.ceil(len(slots_v) / (len(slots_f) + 1)))
        fi = 0
        for idx, s in enumerate(slots_v):
            fila.append(s)
            if (idx + 1) % passo == 0 and fi < len(slots_f):
                fila.append(slots_f[fi]); fi += 1
        fila.extend(slots_f[fi:])
    else:
        fila = slots_v + slots_f

    # corta no alvo, ou estica o que da pra esticar
    total = sum(s["dur"] for s in fila)
    if total >= alvo:
        saida, acc = [], 0.0
        for s in fila:
            resta = alvo - acc
            if resta <= 0.05:
                break
            s = dict(s); s["dur"] = min(s["dur"], resta)
            saida.append(s); acc += s["dur"]
        if saida and acc < alvo:
            saida[-1]["dur"] += alvo - acc
        return saida

    for _ in range(6):  # distribui a falta respeitando o teto de cada slot
        falta = alvo - sum(s["dur"] for s in fila)
        if falta <= 0.05:
            break
        folga = [s for s in fila if s["max"] - s["dur"] > 0.05]
        if not folga:
            break
        parte = falta / len(folga)
        for s in folga:
            s["dur"] = min(s["max"], s["dur"] + parte)
    falta = alvo - sum(s["dur"] for s in fila)
    if falta > 0.05:  # ultimo recurso: segura a ultima foto/plano (avisa)
        fila[-1]["dur"] += falta
    return fila


def comando(clipdir, segs, ass_rel, saida):
    """Um unico ffmpeg: N entradas -> normaliza cada uma -> concat -> queima legenda."""
    ent, filtros, rotulos = [], [], []
    for i, s in enumerate(segs):
        arq = str((clipdir / s["arq"]).resolve())
        if s["tipo"] == "video":
            ent += ["-ss", f"{s['off']:.3f}", "-t", f"{s['dur']:.3f}", "-i", arq]
            filtros.append(f"[{i}:v]{NORM},setpts=PTS-STARTPTS[v{i}]")
        else:
            ent += ["-loop", "1", "-framerate", str(FPS), "-t", f"{s['dur']:.3f}", "-i", arq]
            filtros.append(f"[{i}:v]{ken(i, s['dur'])},setpts=PTS-STARTPTS[v{i}]")
        rotulos.append(f"[v{i}]")
    fc = ";".join(filtros)
    fc += f";{''.join(rotulos)}concat=n={len(segs)}:v=1:a=0[cat]"
    fc += f";[cat]subtitles={ass_rel}:fontsdir=fontes[out]"
    return ([FFMPEG, "-hide_banner", "-loglevel", "error", "-nostdin", "-y"] + ent +
            ["-filter_complex", fc, "-map", "[out]", "-an", *V_ARGS,
             "-video_track_timescale", "30000", str(saida)])


def ok(mp4, alvo):
    try:
        return abs(dur(mp4) - alvo) <= 0.15
    except Exception:
        return False


def monta(proj, bloco, alvo, legdir, midia):
    clipdir = proj / "03-clipes"
    saida = (proj / "04-cenas" / f"cena-{bloco:02d}.mp4").resolve()
    ass_rel = f"cena-{bloco:02d}.ass"
    if not (legdir / ass_rel).exists():
        erro(f"faltou a legenda {ass_rel}. Rode legenda.py antes.")
    if saida.exists() and ok(saida, alvo):
        print(f"  cena {bloco}: ja pronta (cache)")
        return

    itens = (midia.get("blocos") or {}).get(str(bloco)) or []
    seg = float(midia.get("seg") or 8.0)
    if itens:
        segs = segmentos(itens, alvo, seg)
        if not segs:
            erro(f"bloco {bloco}: midia.json nao tem plano utilizavel. Rode midia.py de novo.")
        subprocess.run(comando(clipdir, segs, ass_rel, saida), check=True, cwd=str(legdir))
        nv = sum(1 for s in segs if s["tipo"] == "video")
        print(f"  cena {bloco}: {alvo:.1f}s em {len(segs)} planos ({nv} video, {len(segs) - nv} foto)")
        return

    # --- compatibilidade: projeto antigo, 1 arquivo por bloco ---
    mp4 = clipdir / f"bloco-{bloco:02d}.mp4"
    jpg = clipdir / f"bloco-{bloco:02d}.jpg"
    vf_base = f"{NORM},subtitles={ass_rel}:fontsdir=fontes"
    if mp4.exists() and tem_video(mp4):
        cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
               "-stream_loop", "-1", "-i", str(mp4.resolve()), "-t", f"{alvo:.3f}",
               "-vf", vf_base]
    elif jpg.exists():
        cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
               "-loop", "1", "-framerate", str(FPS), "-i", str(jpg.resolve()),
               "-t", f"{alvo:.3f}", "-vf", f"{ken(0, alvo)},subtitles={ass_rel}:fontsdir=fontes"]
    else:
        erro(f"bloco {bloco}: sem midia em 03-clipes. Rode midia.py ou jogue arquivos la.")
    cmd += ["-an", *V_ARGS, "-video_track_timescale", "30000", str(saida)]
    subprocess.run(cmd, check=True, cwd=str(legdir))
    print(f"  cena {bloco}: {alvo:.1f}s [modo antigo: 1 clipe em loop]")


def main():
    if len(sys.argv) < 2:
        erro("uso: cena.py <pasta-projeto> [--bloco N]")
    proj = pathlib.Path(sys.argv[1])
    man = le_json(proj / "01-voz" / "manifest.json")
    legdir = (proj / "02-legenda").resolve()
    midia_p = proj / "03-clipes" / "midia.json"
    midia = le_json(midia_p) if midia_p.exists() else {}

    # a fonte VEM COM A SKILL. sem ela o libass troca por uma generica, calado.
    fontes = legdir / "fontes"
    fontes.mkdir(parents=True, exist_ok=True)
    if FONTE_SRC.exists():
        for f in FONTE_SRC.glob("*.ttf"):
            d = fontes / f.name
            if not (d.exists() and d.stat().st_size == f.stat().st_size):
                shutil.copy2(f, d)

    (proj / "04-cenas").mkdir(parents=True, exist_ok=True)
    so = None
    if "--bloco" in sys.argv:
        so = int(sys.argv[sys.argv.index("--bloco") + 1])
    for b in man["blocos"]:
        if so is not None and b["id"] != so:
            continue
        monta(proj, b["id"], b["dur"], legdir, midia)
    print("cenas prontas.")


if __name__ == "__main__":
    main()
