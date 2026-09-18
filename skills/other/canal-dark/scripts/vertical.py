"""Corta um trecho do master num vertical 9:16 pro Shorts/Reels/TikTok.

  python vertical.py <master.mp4> <saida.mp4> <inicio_seg> <duracao_seg>

IMPORTANTE: isto e o CORTE tecnico. A ESCOLHA e a reescrita do trecho
(gancho proprio nos primeiros 3s) sao decisao de conteudo, feita pelo Claude no
SKILL.md antes de chamar este script. Um pedaco aleatorio de 60s de um video de 12min
nao tem comeco nem fim e morre de retencao.

Como o master e 1080p, cortar 9:16 viraria upscale e amoleceria a imagem. Entao usa
fundo desfocado (o proprio frame borrado atras) + o video centralizado por cima. A
legenda que ja esta queimada no master continua legivel no centro.
Limite oficial de Shorts: ate 3 minutos, 1080p.
"""
import pathlib, subprocess, sys
from comum import A_ARGS, FFMPEG, V_ARGS, dur, erro

FILTRO = (
    "[0:v]split=2[bg][fg];"
    "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=25[bg];"
    "[fg]scale=1080:-2[fg];"
    "[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,fps=30[v]"
)


def main():
    if len(sys.argv) < 5:
        erro("uso: vertical.py <master.mp4> <saida.mp4> <inicio_seg> <duracao_seg>")
    master = pathlib.Path(sys.argv[1]).resolve()
    saida = pathlib.Path(sys.argv[2]).resolve()
    ini = float(sys.argv[3].replace(",", "."))
    d = float(sys.argv[4].replace(",", "."))
    if not master.exists():
        erro(f"nao achei {master}")
    if d > 180:
        erro("Shorts vai ate 3 minutos. Escolha um trecho menor.")

    saida.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
                    "-ss", f"{ini:.3f}", "-i", str(master), "-t", f"{d:.3f}",
                    "-filter_complex", FILTRO, "-map", "[v]", "-map", "0:a:0",
                    *V_ARGS, *A_ARGS, "-movflags", "+faststart", str(saida)], check=True)
    print(f"vertical: {dur(saida):.1f}s -> {saida}")


if __name__ == "__main__":
    main()
