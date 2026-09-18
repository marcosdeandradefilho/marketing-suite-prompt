"""Monta a faixa de audio final: voz + musica (se houver) com ducking e loudness -14 LUFS.

  python audio.py <pasta-projeto>

A voz vem de 01-voz/narracao.wav. A musica, se existir, de 05-audio/musica/*.mp3
(o usuario poe na mao: a skill NAO baixa musica, pra nao tomar Content ID).
Se nao houver musica, so normaliza a voz.

Detalhes que nao sao obvios:
- '-stream_loop -1' ANTES do '-i' da musica e O(1) de memoria (loopa sem bufferizar).
- 'normalize=0' no amix e obrigatorio, senao a voz cai 6 dB sozinha.
- 'asplit' duplica a voz pra alimentar o amix E a cadeia lateral do ducking.
- alvo -14 LUFS, true peak -1.5 (consenso de mercado; o Google nao publica numero oficial).

Saida: 05-audio/mix.m4a (AAC 256k estereo 48kHz).
"""
import glob, pathlib, subprocess, sys
from comum import FFMPEG, dur, erro

FILTRO_COM_MUSICA = (
    "[1:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,volume=0.30[bg];"
    "[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,asplit=2[voz][sc];"
    "[bg][sc]sidechaincompress=threshold=0.02:ratio=12:attack=15:release=350:level_sc=1[bgduck];"
    "[voz][bgduck]amix=inputs=2:duration=first:normalize=0,"
    "loudnorm=I=-14:TP=-1.5:LRA=11[a]"
)


def main():
    if len(sys.argv) < 2:
        erro("uso: audio.py <pasta-projeto>")
    proj = pathlib.Path(sys.argv[1])
    voz = proj / "01-voz" / "narracao.wav"
    if not voz.exists():
        erro("faltou 01-voz/narracao.wav. Rode voz.py antes.")
    outdir = proj / "05-audio"
    outdir.mkdir(parents=True, exist_ok=True)
    saida = outdir / "mix.m4a"

    musicas = sorted(glob.glob(str(outdir / "musica" / "*.mp3")) +
                     glob.glob(str(outdir / "musica" / "*.m4a")) +
                     glob.glob(str(outdir / "musica" / "*.wav")))

    if musicas:
        print(f"mixando voz + musica ({pathlib.Path(musicas[0]).name}) com ducking...")
        cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
               "-i", str(voz), "-stream_loop", "-1", "-i", musicas[0],
               "-filter_complex", FILTRO_COM_MUSICA, "-map", "[a]",
               "-c:a", "aac", "-b:a", "256k", "-ac", "2", "-ar", "48000", str(saida)]
    else:
        print("sem musica em 05-audio/musica/ — normalizando so a voz.")
        cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
               "-i", str(voz), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
               "-c:a", "aac", "-b:a", "256k", "-ac", "2", "-ar", "48000", str(saida)]
    subprocess.run(cmd, check=True)
    print(f"audio: {dur(saida):.1f}s -> {saida.name}")


if __name__ == "__main__":
    main()
