"""Baixa uma SEQUENCIA de midias por bloco (varios videos + algumas fotos), do Pexels.

  python midia.py <plano.json> <pasta-projeto> [--video-pct 75] [--seg 8]

Por que sequencia e nao 1 clipe por bloco (mudanca da v1.3.0):
Um bloco narrativo tem ~40 a 90 segundos e um clipe do Pexels costuma ter 5 a 20. Com um
clipe so, a cena LOOPAVA o mesmo trecho ate fechar o tempo — medido no v01: bloco de 56s com
clipe de 5,3s = 10,5 voltas do mesmo plano. Agora cada bloco recebe midia suficiente pra ser
coberto por segmentos DIFERENTES de ~8s. Foto entra na mistura (vira Ken Burns na cena.py):
enche o tempo sem repetir plano e custa quase nada de banda.

Regras que ficam de pe:
- A troca de plano acontece DENTRO do bloco, mas o BLOCO narrativo continua sendo a unidade.
  Nao se troca de cena a cada frase (gatilho literal de "videos that stitch together unrelated
  clips" na politica do YouTube).
- Nunca repete o mesmo asset no video inteiro (diario de IDs usados).
- O nome do arquivo do Pexels MENTE a resolucao: confere com ffprobe depois de baixar.
- Guideline da API exige credito: grava creditos.json -> vira CREDITOS.md.
- So Pexels. Sem fonte alternativa. Sem a chave, PARA e manda o tutorial.
- Nunca raspa o site: usa a API com a chave (raspar viola os Termos do Pexels).
- Foto do Pexels vem com 5000px+; reduz pra 2560 na hora de salvar (imagem gigante trava o
  render depois — mesmo pega-ratao ja medido na thumbnail).

A chave e procurada em: env PEXELS_API_KEY, depois <projeto>/pexels-key.txt, depois a RAIZ
do canal (<projeto>/../pexels-key.txt — serve todos os videos), depois <skill>/pexels-key.txt.
"""
import json, math, os, pathlib, subprocess, sys, urllib.error, urllib.parse, urllib.request
from comum import FFMPEG, erro, salva_json, le_json, sonda

API_VIDEO = "https://api.pexels.com/videos/search"
API_FOTO = "https://api.pexels.com/v1/search"

SEG_ALVO = 8.0          # duracao alvo de cada segmento visual
SEG_MIN = 4.5           # abaixo disso o plano nem vira segmento
# Um clipe do Pexels quase sempre e UMA tomada continua: pegar 3 trechos dele nao da 3 planos,
# da 3 vezes o mesmo lugar. Por isso no maximo 2 trechos, e so quando o clipe e longo o
# bastante pros dois pedacos ficarem de fato distantes.
MAX_SEG_POR_CLIPE = 2
DUR_PRA_DOIS_TRECHOS = 16.0
MAX_CLIPES_BLOCO = 4
MAX_FOTOS_BLOCO = 5
LARGURA_FOTO = 2560     # foto maior que isso trava o render (medido)

TUTORIAL = ("Sem a chave do Pexels nao da pra buscar os videos de fundo.\n"
            "Como pegar (gratis, sem cartao, 2 minutos): abra pexels.com/api, "
            "clique em 'Get Started', faca login, copie a chave (API Key) e cole "
            "num arquivo chamado pexels-key.txt dentro da pasta do projeto. "
            "Passo a passo com telas no LEIA-PRIMEIRO.md desta skill.")


def acha_chave(proj):
    if os.environ.get("PEXELS_API_KEY"):
        return os.environ["PEXELS_API_KEY"].strip()
    proj = pathlib.Path(proj)
    for cand in (proj / "pexels-key.txt",
                 proj.parent / "pexels-key.txt",  # raiz do canal (uma pasta acima do video)
                 pathlib.Path(__file__).resolve().parent.parent / "pexels-key.txt"):
        if cand.exists():
            k = cand.read_text(encoding="utf-8-sig").strip()
            if k:
                return k
    erro(TUTORIAL)


def pega(url, chave):
    req = urllib.request.Request(url, headers={"Authorization": chave,
                                               "User-Agent": "canal-dark-skill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 401:
            erro("a chave do Pexels foi recusada (401). Confira se colou a chave certa.\n" + TUTORIAL)
        if e.code == 429:
            erro("o Pexels bateu o limite de requisicoes (429). Espere uma hora e rode de novo. "
                 "O limite gratuito e 200 por hora.")
        raise


def melhor_video(item):
    """O melhor arquivo <=1080p em paisagem. Devolve (url, w, h) ou None."""
    cands = [f for f in item.get("video_files", []) if (f.get("height") or 0) <= 1080
             and (f.get("width") or 0) >= (f.get("height") or 0)]
    if not cands:
        cands = item.get("video_files", [])
    if not cands:
        return None
    f = max(cands, key=lambda x: (x.get("width") or 0) * (x.get("height") or 0))
    return f["link"], f.get("width"), f.get("height")


def baixa(url, saida):
    req = urllib.request.Request(url, headers={"User-Agent": "canal-dark-skill/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r, open(saida, "wb") as f:
        while True:
            chunk = r.read(1 << 16)
            if not chunk:
                break
            f.write(chunk)


def reduz_foto(bruta, alvo):
    """Foto do Pexels vem enorme. Reduz pra LARGURA_FOTO antes de guardar."""
    cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-nostdin", "-y", "-i", str(bruta),
           "-vf", f"scale='min({LARGURA_FOTO},iw)':-2", "-q:v", "2", str(alvo)]
    subprocess.run(cmd, check=True)
    try:
        bruta.unlink()
    except OSError:
        pass


def luma(arquivo, e_video):
    """Media e desvio do brilho de um frame representativo (0-255).

    Existe porque o Pexels devolve muito clipe "night fire" que na pratica e uma chama
    minuscula num quadro PRETO: medido no v01, um bloco ficou ~20s praticamente preto.
    Quadro chapado (preto, branco ou liso) nao segura ninguem assistindo.
    """
    vf = "thumbnail,scale=64:36,format=gray" if e_video else "scale=64:36,format=gray"
    cmd = [FFMPEG, "-v", "error", "-nostdin", "-i", str(arquivo), "-vf", vf,
           "-frames:v", "1", "-f", "rawvideo", "-"]
    try:
        out = subprocess.run(cmd, capture_output=True, timeout=90).stdout
    except Exception:
        return None
    if len(out) < 64:
        return None
    m = sum(out) / len(out)
    dp = (sum((b - m) ** 2 for b in out) / len(out)) ** 0.5
    return m, dp


def quadro_pobre(arquivo, e_video):
    """True se o quadro e escuro demais, estourado, ou chapado (sem informacao)."""
    r = luma(arquivo, e_video)
    if r is None:
        return False  # nao deu pra medir: nao reprova por isso
    m, dp = r
    return m < 26 or m > 238 or dp < 12


# Marcadores no titulo/alt do Pexels que quase sempre estragam um canal dark de historia:
# gente moderna no quadro e cenario moderno. Nao e censura de tema — e continuidade.
STOP = ("selfie", "tourist", "tourists", "posing", "smiling", "portrait of", "influencer",
        "vlogger", "photographer taking", "couple ", "family ", "businessman", "office",
        "laptop", "smartphone", "car ", "cars ", "traffic", "construction worker",
        "modern building", "playground", "supermarket", "kitchen",
        # pegos no teste: um bombeiro de uniforme laranja "Jakarta" na queda de Ninive
        "firefighter", "fireman", "fire brigade", "firefighters", "rescue", "ambulance",
        "police", "helmet", "high visibility", "uniform", "worker", "workers", "protest")


def texto_do_item(item):
    return " ".join(str(x) for x in (item.get("alt") or "", item.get("url") or "",
                                     item.get("description") or "")).lower().replace("-", " ")


def suspeito(item, termo):
    t = texto_do_item(item)
    termo = termo.lower()
    return any(s in t and s.strip() not in termo for s in STOP)


def termos_do_bloco(b):
    t = b.get("termos_busca")
    if isinstance(t, list) and t:
        return [x for x in t if x]
    um = b.get("termo_busca") or b.get("funcao") or "cinematic"
    return [um]


def busca(cache, api, termo, chave, chave_lista):
    """Busca com cache por (api, termo) — o mesmo termo nao gasta 2 requisicoes."""
    k = (api, termo)
    if k not in cache:
        q = urllib.parse.urlencode({"query": termo, "per_page": 20, "orientation": "landscape"})
        cache[k] = pega(f"{api}?{q}", chave).get(chave_lista, [])
    return cache[k]


def quanto_cobre(dur_clipe, seg=SEG_ALVO):
    """Quantos segundos de plano DIFERENTE um clipe consegue entregar."""
    if dur_clipe < SEG_MIN:
        return 0.0
    n = MAX_SEG_POR_CLIPE if dur_clipe >= DUR_PRA_DOIS_TRECHOS else 1
    return n * seg


def livre(nome_base, dst, existentes, queimados):
    """Proximo nome livre pro bloco.

    Nome de arquivo REPROVADO nunca volta: se voltasse, a folha de contato da rodada
    seguinte mostraria 'b04-f02.jpg' de novo com outra imagem dentro e ninguem saberia
    se foi trocado ou nao.
    """
    i = 1
    while (f"{nome_base}{i:02d}" in existentes or f"{nome_base}{i:02d}" in queimados
           or (dst / f"{nome_base}{i:02d}.mp4").exists()
           or (dst / f"{nome_base}{i:02d}.jpg").exists()):
        i += 1
    return f"{nome_base}{i:02d}"


def contato(dst, mapa):
    """Folha de contato: 1 quadro por midia baixada, na ordem, pro Claude OLHAR e reprovar.

    Sem legenda escrita na imagem de proposito (drawtext com caminho do Windows e um
    pega-ratao); a ordem sai impressa no terminal e casa com a grade.
    """
    ordem, tmp = [], dst / "_contato"
    tmp.mkdir(exist_ok=True)
    for f in tmp.glob("*.jpg"):
        f.unlink()
    n = 0
    for bid in sorted(mapa, key=lambda x: int(x)):
        for it in mapa[bid]:
            src = dst / it["arquivo"]
            if not src.exists():
                continue
            alvo = tmp / f"c_{n:03d}.jpg"
            # TAMANHO FIXO: o filtro tile exige todos os quadros iguais. Foto 3:2 e video 16:9
            # misturados quebravam a folha (so entravam 2 quadros). Medido.
            enquadra = ("scale=360:202:force_original_aspect_ratio=decrease,"
                        "pad=360:202:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1")
            vf = f"thumbnail,{enquadra}" if it["tipo"] == "video" else enquadra
            try:
                subprocess.run([FFMPEG, "-v", "error", "-nostdin", "-y", "-i", str(src),
                                "-vf", vf, "-frames:v", "1", str(alvo)], check=True, timeout=120)
            except Exception:
                continue
            ordem.append((n + 1, bid, it["arquivo"], it["termo"]))
            n += 1
    if not n:
        return None, []
    cols = 5
    saida = dst / "contato.png"
    try:
        subprocess.run([FFMPEG, "-v", "error", "-nostdin", "-y",
                        "-start_number", "0", "-i", str(tmp / "c_%03d.jpg"),
                        "-filter_complex", f"tile={cols}x{max(1, math.ceil(n / cols))}:"
                                           "margin=4:padding=4:color=0x181818",
                        "-frames:v", "1", str(saida)], check=True, timeout=300)
    except Exception:
        return None, ordem
    return saida, ordem


def main():
    if len(sys.argv) < 3:
        erro("uso: midia.py <plano.json> <pasta-projeto> [--video-pct 75] [--seg 8] "
             "[--rejeitar arq1.mp4,arq2.jpg]")
    plano = le_json(sys.argv[1])
    proj = pathlib.Path(sys.argv[2])
    pct_video = 75
    if "--video-pct" in sys.argv:
        pct_video = max(50, min(100, int(sys.argv[sys.argv.index("--video-pct") + 1])))
    seg = SEG_ALVO
    if "--seg" in sys.argv:
        seg = max(5.0, min(15.0, float(sys.argv[sys.argv.index("--seg") + 1])))
    rejeitar = set()
    if "--rejeitar" in sys.argv:
        rejeitar = {x.strip() for x in sys.argv[sys.argv.index("--rejeitar") + 1].split(",") if x.strip()}

    chave = acha_chave(proj)
    dst = proj / "03-clipes"
    dst.mkdir(parents=True, exist_ok=True)

    # duracao real de cada bloco: sai do manifest da voz (voz.py roda antes)
    duracoes = {}
    man_p = proj / "01-voz" / "manifest.json"
    if man_p.exists():
        for b in le_json(man_p)["blocos"]:
            duracoes[b["id"]] = b["dur"]

    midia_p = dst / "midia.json"
    ja = le_json(midia_p)["blocos"] if midia_p.exists() else {}
    banidos_p = dst / "rejeitados.json"
    _rej = le_json(banidos_p) if banidos_p.exists() else {}
    banidos = set(_rej.get("pexels_ids") or [])
    queimados = set(_rej.get("arquivos") or [])

    # --- aplica a reprovacao do gate visual: apaga o arquivo e bane o id ---
    if rejeitar:
        for bid, itens in list(ja.items()):
            mantem = []
            for it in itens:
                if it["arquivo"] in rejeitar:
                    banidos.add(it.get("pexels_id"))
                    queimados.add(pathlib.Path(it["arquivo"]).stem)
                    try:
                        (dst / it["arquivo"]).unlink()
                    except OSError:
                        pass
                    print(f"  reprovado: {it['arquivo']} (bloco {bid}) — vou buscar outro")
                else:
                    mantem.append(it)
            ja[bid] = mantem
        salva_json(banidos_p, {"pexels_ids": sorted(x for x in banidos if x),
                               "arquivos": sorted(queimados)})

    usados, creditos, mapa = set(banidos), [], {}
    for v in ja.values():
        for it in v:
            if it.get("pexels_id"):
                usados.add(it["pexels_id"])

    cache = {}
    for b in plano["blocos"]:
        bid = b["id"]
        chave_b = str(bid)
        alvo = duracoes.get(bid)
        if not alvo:
            print(f"  bloco {bid}: [CONFERIR] sem duracao no manifest da voz. Rode voz.py antes.")
            alvo = 45.0

        termos = termos_do_bloco(b)
        itens = [it for it in ja.get(chave_b, []) if (dst / it["arquivo"]).exists()]
        nomes = {pathlib.Path(it["arquivo"]).stem for it in itens}
        cobertura = sum(quanto_cobre(it["dur"], seg) if it["tipo"] == "video" else seg
                        for it in itens)
        n_video_ja = sum(1 for it in itens if it["tipo"] == "video")
        n_foto_ja = len(itens) - n_video_ja

        n_seg = max(2, int(round(alvo / seg)))
        n_foto = min(MAX_FOTOS_BLOCO, int(round(n_seg * (100 - pct_video) / 100.0)))
        seg_video = max(1, n_seg - n_foto)
        alvo_video = seg_video * seg

        if cobertura >= alvo - 0.5 and itens:
            mapa[chave_b] = itens
            print(f"  bloco {bid}: ja tenho {len(itens)} midias (cache)")
            continue

        # --- videos: baixa ate cobrir os segmentos de video ---
        cob_video = sum(quanto_cobre(it["dur"], seg) for it in itens if it["tipo"] == "video")
        for i in range(MAX_CLIPES_BLOCO - n_video_ja):
            if cob_video >= alvo_video:
                break
            termo = termos[(i + n_video_ja) % len(termos)]
            escolhido = None
            for item in busca(cache, API_VIDEO, termo, chave, "videos"):
                if item["id"] in usados or (item.get("duration") or 0) < SEG_MIN:
                    continue
                if suspeito(item, termo):
                    continue
                mv = melhor_video(item)
                if not mv or (mv[1] or 0) < 1280:
                    continue
                escolhido = (item, mv, termo)
                break
            if not escolhido:
                break
            item, mv, termo = escolhido
            nome = livre(f"b{bid:02d}-v", dst, nomes, queimados) + ".mp4"
            baixa(mv[0], dst / nome)
            if quadro_pobre(dst / nome, True):  # quadro preto/estourado/chapado: descarta
                print(f"  bloco {bid}: descartei um clipe de '{termo}' (quadro sem informacao)")
                usados.add(item["id"])
                try:
                    (dst / nome).unlink()
                except OSError:
                    pass
                continue
            real = sonda(dst / nome)  # o nome mente a resolucao; confere de verdade
            usados.add(item["id"])
            nomes.add(pathlib.Path(nome).stem)
            cob_video += quanto_cobre(real["duracao"], seg)
            cobertura += quanto_cobre(real["duracao"], seg)
            itens.append({"arquivo": nome, "tipo": "video", "dur": round(real["duracao"], 2),
                          "termo": termo, "pexels_id": item["id"],
                          "resolucao": f"{real['largura']}x{real['altura']}"})
            creditos.append({"bloco": bid, "termo": termo, "tipo": "video", "arquivo": nome,
                             "autor": item.get("user", {}).get("name", ""),
                             "url_autor": item.get("user", {}).get("url", ""),
                             "url": item.get("url", ""),
                             "resolucao": f"{real['largura']}x{real['altura']}"})

        # Se o video nao cobriu tudo (clipe curto, termo pobre), a FOTO cobre a diferenca em
        # vez de deixar um plano esticado. Melhor uma imagem com movimento do que 20s parado.
        falta = alvo - cobertura - max(0, n_foto - n_foto_ja) * seg
        if falta > 0:
            n_foto = min(MAX_FOTOS_BLOCO, max(n_foto, n_foto_ja + int(math.ceil(falta / seg))))

        # --- fotos: cada uma vira UM segmento com movimento (Ken Burns) ---
        for i in range(max(0, n_foto - n_foto_ja)):
            termo = termos[(i + n_foto_ja + 1) % len(termos)]
            escolhido = None
            for item in busca(cache, API_FOTO, termo, chave, "photos"):
                if item["id"] in usados or (item.get("width") or 0) < 1600:
                    continue
                if suspeito(item, termo):
                    continue
                escolhido = (item, termo)
                break
            if not escolhido:
                break
            item, termo = escolhido
            nome = livre(f"b{bid:02d}-f", dst, nomes, queimados) + ".jpg"
            bruta = dst / (nome + ".bruta")
            baixa(item["src"]["original"], bruta)
            reduz_foto(bruta, dst / nome)
            usados.add(item["id"])
            if quadro_pobre(dst / nome, False):
                print(f"  bloco {bid}: descartei uma foto de '{termo}' (quadro sem informacao)")
                try:
                    (dst / nome).unlink()
                except OSError:
                    pass
                continue
            nomes.add(pathlib.Path(nome).stem)
            itens.append({"arquivo": nome, "tipo": "foto", "dur": seg, "termo": termo,
                          "pexels_id": item["id"]})
            creditos.append({"bloco": bid, "termo": termo, "tipo": "foto", "arquivo": nome,
                             "autor": item.get("photographer", ""),
                             "url_autor": item.get("photographer_url", ""),
                             "url": item.get("url", "")})

        if not itens:
            print(f"  bloco {bid}: [CONFERIR] nada no Pexels pros termos {termos}. "
                  "Troque os termos_busca no plano ou jogue arquivos proprios em 03-clipes/.")
        else:
            nv = sum(1 for x in itens if x["tipo"] == "video")
            nf = len(itens) - nv
            cobre = sum(quanto_cobre(x["dur"], seg) if x["tipo"] == "video" else seg for x in itens)
            marca = "" if cobre >= alvo - 0.5 else "  [CONFERIR] pode faltar plano (vai esticar)"
            print(f"  bloco {bid}: {nv} video + {nf} foto  ~{cobre:.0f}s pra {alvo:.0f}s{marca}")
        mapa[chave_b] = itens

    salva_json(midia_p, {"seg": seg, "video_pct": pct_video, "blocos": mapa})
    antigos = le_json(dst / "creditos.json")["itens"] if (dst / "creditos.json").exists() else []
    vivos = {it["arquivo"] for v in mapa.values() for it in v}
    vistos = {(c.get("arquivo"), c.get("url")) for c in creditos}
    creditos = creditos + [c for c in antigos
                           if (c.get("arquivo"), c.get("url")) not in vistos
                           and c.get("arquivo") in vivos]
    salva_json(dst / "creditos.json", {"fonte": "Pexels (https://www.pexels.com)", "itens": creditos})
    total = sum(len(v) for v in mapa.values())
    print(f"midia: {total} arquivos em {len(mapa)} blocos. midia.json + creditos.json salvos.")

    folha, ordem = contato(dst, mapa)
    if folha:
        print("\nGATE VISUAL — abra a folha de contato e OLHE cada quadro:")
        print(f"  {folha}   (grade de 5 colunas, na ordem abaixo)")
        for n, bid, arq, termo in ordem:
            print(f"  {n:>3}. bloco {bid:>2}  {arq:<16} {termo}")
        print("  Reprove o que nao combina com o assunto/epoca (gente moderna, predio moderno,")
        print("  civilizacao errada) com:  python midia.py <plano> <projeto> --rejeitar arq1,arq2")


if __name__ == "__main__":
    main()
