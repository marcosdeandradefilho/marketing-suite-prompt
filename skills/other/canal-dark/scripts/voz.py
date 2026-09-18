"""Gera a narracao com edge-tts, FRASE A FRASE, e mede cada uma com ffprobe.

  python voz.py <plano.json> <pasta-projeto> [--voz pt-BR-AntonioNeural]

Por que frase a frase e nao o roteiro inteiro:
1. A legenda sai DETERMINISTICA: o texto ja e conhecido (e o roteiro), o unico
   dado que falta e o TEMPO, e o tempo sai do ffprobe de cada .wav. Erro 0 ms.
   Nao precisa de Whisper, que reescreveria nome proprio.
2. Requisicao curta nunca bate no corte silencioso do edge-tts aos 10:00 (issue #390).

SEM FALLBACK: se o edge-tts estiver fora (403/503), o health-check
falha e o script PARA com erro honesto. Nao entrega audio quebrado nem troca de motor.

Escreve:
  01-voz/b{BB}-f{FF}.wav  (cada frase, 48kHz mono)
  01-voz/narracao.wav     (tudo concatenado, a faixa de voz)
  01-voz/manifest.json    (ini/fim ABSOLUTOS por frase e por bloco -> alimenta legenda e cena)
"""
import asyncio, pathlib, sys, tempfile
from comum import FFMPEG, dur, erro, roda, salva_json, le_json

try:
    import edge_tts
except ImportError:
    erro("edge-tts nao instalado. Rode: pip install edge-tts")

VOZ_PADRAO = "pt-BR-AntonioNeural"   # masculina. feminina: pt-BR-FranciscaNeural


async def sintetiza(texto, voz, saida_mp3):
    """Uma frase -> um MP3. Levanta excecao se o servico devolver audio vazio."""
    com = edge_tts.Communicate(texto, voz)
    recebeu = False
    with open(saida_mp3, "wb") as f:
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
                recebeu = True
    if not recebeu:
        raise RuntimeError("edge-tts nao devolveu audio (rate-limit ou servico fora)")


def mp3_para_wav(mp3, wav):
    roda([FFMPEG, "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
          "-i", str(mp3), "-ac", "1", "-ar", "48000", str(wav)])


async def health_check(voz):
    """Sintetiza 1 frase de teste. Se falhar, PARA aqui, antes de gastar o video inteiro."""
    tmp = pathlib.Path(tempfile.gettempdir()) / "canal-dark-healthcheck.mp3"
    try:
        await sintetiza("teste de voz", voz, tmp)
        if not tmp.exists() or tmp.stat().st_size == 0:
            raise RuntimeError("arquivo de teste vazio")
    except Exception as e:
        erro(f"o servico de voz (edge-tts) esta fora agora: {e}\n"
             "Nao da pra gerar a narracao neste momento. Tente de novo mais tarde. "
             "Esta versao nao tem voz alternativa (decisao de projeto).")
    finally:
        tmp.unlink(missing_ok=True)


async def main():
    if len(sys.argv) < 3:
        erro("uso: voz.py <plano.json> <pasta-projeto> [--voz pt-BR-AntonioNeural]")
    plano = le_json(sys.argv[1])
    proj = pathlib.Path(sys.argv[2])
    voz = plano.get("voz") or VOZ_PADRAO
    if "--voz" in sys.argv:
        voz = sys.argv[sys.argv.index("--voz") + 1]

    print(f"conferindo o servico de voz ({voz})...")
    await health_check(voz)

    vozdir = proj / "01-voz"
    vozdir.mkdir(parents=True, exist_ok=True)
    tmpdir = pathlib.Path(tempfile.mkdtemp(prefix="canal-dark-voz-"))

    frases_out, blocos_out, wavs = [], [], []
    t = 0.0
    total_frases = sum(len(b["frases"]) for b in plano["blocos"])
    feito = 0
    for b in plano["blocos"]:
        bloco_ini = t
        for i, fr in enumerate(b["frases"], 1):
            texto = fr["texto"] if isinstance(fr, dict) else str(fr)
            nome = f"b{b['id']:02d}-f{i:02d}.wav"
            wav = vozdir / nome
            # so (re)gera se ainda nao existe e valido -> retomavel
            if not (wav.exists() and _ok(wav)):
                mp3 = tmpdir / (nome + ".mp3")
                await sintetiza(texto, voz, mp3)
                mp3_para_wav(mp3, wav)
            d = dur(wav)
            frases_out.append({"bloco": b["id"], "idx": i, "arquivo": nome,
                               "texto": texto, "ini": round(t, 3),
                               "fim": round(t + d, 3), "dur": round(d, 3)})
            wavs.append(wav)
            t += d
            feito += 1
            print(f"  voz {feito}/{total_frases}  ({t:.0f}s de narracao)")
        blocos_out.append({"id": b["id"], "funcao": b.get("funcao", ""),
                           "ini": round(bloco_ini, 3), "fim": round(t, 3),
                           "dur": round(t - bloco_ini, 3)})

    # concatena tudo numa faixa de voz unica
    narr = vozdir / "narracao.wav"
    lista = tmpdir / "lista.txt"
    lista.write_text("\n".join(f"file '{w.as_posix()}'" for w in wavs) + "\n", encoding="utf-8")
    roda([FFMPEG, "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
          "-f", "concat", "-safe", "0", "-i", str(lista),
          "-ac", "1", "-ar", "48000", str(narr)])

    salva_json(vozdir / "manifest.json",
               {"voz": voz, "total": round(t, 3), "frases": frases_out, "blocos": blocos_out})
    print(f"narracao: {t / 60:.1f} min, {total_frases} frases, voz {voz}")


def _ok(wav):
    try:
        return dur(wav) > 0.05
    except Exception:
        return False


if __name__ == "__main__":
    asyncio.run(main())
