"""Junta as cenas + o audio no MP4 final, pronto pro YouTube.

  python montar.py <pasta-projeto>

As cenas ja saem identicas (1920x1080, 30fps, mesmo timescale), entao o concat e por
COPIA de fluxo (instantaneo, sem perda). Depois muxa o audio e poe o moov na frente
(+faststart) pra o video comecar a tocar sem baixar inteiro.

Escreve 06-saida/video.mp4 (master 1080p).
"""
import glob, pathlib, subprocess, sys, tempfile
from comum import A_ARGS, FFMPEG, dur, erro, escreve_lista_concat


def main():
    if len(sys.argv) < 2:
        erro("uso: montar.py <pasta-projeto>")
    proj = pathlib.Path(sys.argv[1])
    cenadir = (proj / "04-cenas").resolve()
    cenas = sorted(glob.glob(str(cenadir / "cena-*.mp4")))
    if not cenas:
        erro("nenhuma cena em 04-cenas. Rode cena.py antes.")
    mix = proj / "05-audio" / "mix.m4a"
    if not mix.exists():
        erro("faltou 05-audio/mix.m4a. Rode audio.py antes.")

    outdir = proj / "06-saida"
    outdir.mkdir(parents=True, exist_ok=True)
    saida = (outdir / "video.mp4").resolve()

    # concat -c copy (roda com cwd na pasta das cenas: lista com nomes RELATIVOS, sem BOM)
    lista = escreve_lista_concat(cenadir / "_cenas.txt", cenas)
    mudo = pathlib.Path(tempfile.gettempdir()) / "canal-dark-mudo.mp4"
    subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
                    "-f", "concat", "-safe", "0", "-i", lista.name,
                    "-c", "copy", str(mudo)], check=True, cwd=str(cenadir))

    # muxa audio + faststart. -shortest corta no fim da faixa mais curta (a voz manda).
    subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
                    "-i", str(mudo), "-i", str(mix),
                    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", *A_ARGS,
                    "-movflags", "+faststart", "-shortest", str(saida)], check=True)
    mudo.unlink(missing_ok=True)
    d = dur(saida)
    print(f"MASTER pronto: {d / 60:.1f} min ({int(d)}s) -> {saida}")
    if d < 500:
        print("[AVISO] o video ficou abaixo de 8min20s. Sem mid-roll: o YouTube so libera "
              "anuncio no meio a partir de 8 minutos. Considere esticar o desenvolvimento.")


if __name__ == "__main__":
    main()
