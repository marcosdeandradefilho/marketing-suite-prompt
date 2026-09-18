"""Gera uma legenda .ass POR CENA a partir do manifest da voz. Sem ASR.

  python legenda.py <pasta-projeto>

O texto ja e conhecido (o roteiro) e o tempo ja foi medido (ffprobe de cada frase),
entao a legenda e deterministica: nada de transcrever, nada de Whisper reescrever
nome proprio. Uma frase longa vira 2 ou mais cartelas, dividindo o tempo da frase
proporcional ao numero de caracteres (aproximacao linear, boa pra long-form).

Tempos REBASEADOS pro zero de cada cena (a cena e renderizada isolada e so depois
concatenada). Legenda de documentario: creme com contorno preto, no maximo 2 linhas,
teto de ~20 caracteres por segundo (Netflix Timed Text Style Guide).

Escreve 02-legenda/cena-{BB}.ass, UTF-8 SEM BOM (o libass come acento se houver BOM).
"""
import pathlib, sys
from comum import erro, le_json

# tema escuro com acento quente. ASS usa BGR, nao RGB.
CREME = "&H00DDECF3"    # #f3ecdd
PRETO = "&H00000000"
L, A = 1920, 1080
FONTE = "Anton"
TAM = 58
MARGEM_V = 90
MAX_LINHA = 42         # chars por linha (Netflix: 42)
MAX_LINHAS = 2         # cartela nunca passa de 2 linhas
CPS = 20               # teto de caracteres por segundo (legibilidade)


def hhmmss(t):
    t = max(0.0, t)
    return f"{int(t // 3600)}:{int((t % 3600) // 60):02d}:{t % 60:05.2f}"


def quebra_linhas(palavras, max_linha):
    linhas, atual = [], ""
    for p in palavras:
        cand = (atual + " " + p).strip()
        if len(cand) > max_linha and atual:
            linhas.append(atual)
            atual = p
        else:
            atual = cand
    if atual:
        linhas.append(atual)
    return linhas


def cartelas_da_frase(texto, ini, fim):
    """Divide a frase em cartelas de <=2 linhas, repartindo o tempo por caractere."""
    linhas = quebra_linhas(texto.split(), MAX_LINHA)
    grupos = [linhas[i:i + MAX_LINHAS] for i in range(0, len(linhas), MAX_LINHAS)]
    total_chars = sum(len(" ".join(g)) for g in grupos) or 1
    out, t = [], ini
    for g in grupos:
        chars = len(" ".join(g))
        share = (fim - ini) * (chars / total_chars)
        out.append(("\\N".join(g), t, t + share))
        t += share
    return out


def cena_ass(frases, bloco_ini):
    cab = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {L}
PlayResY: {A}
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Fala,{FONTE},{TAM},{CREME},{CREME},{PRETO},&H99000000,0,0,0,0,100,100,0,0,1,3,1,2,120,120,{MARGEM_V},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    linhas = []
    for fr in frases:
        for txt, a, b in cartelas_da_frase(fr["texto"], fr["ini"], fr["fim"]):
            ini_local = max(0.0, a - bloco_ini)
            fim_local = max(ini_local + 0.1, b - bloco_ini)
            linhas.append(f"Dialogue: 0,{hhmmss(ini_local)},{hhmmss(fim_local)},Fala,,0,0,0,,{txt}")
    return cab + "\n".join(linhas) + "\n"


def main():
    if len(sys.argv) < 2:
        erro("uso: legenda.py <pasta-projeto>")
    proj = pathlib.Path(sys.argv[1])
    man = le_json(proj / "01-voz" / "manifest.json")
    legdir = proj / "02-legenda"
    legdir.mkdir(parents=True, exist_ok=True)

    por_bloco = {b["id"]: b for b in man["blocos"]}
    frases_por_bloco = {}
    for fr in man["frases"]:
        frases_por_bloco.setdefault(fr["bloco"], []).append(fr)

    for bid, frases in frases_por_bloco.items():
        ass = cena_ass(frases, por_bloco[bid]["ini"])
        saida = legdir / f"cena-{bid:02d}.ass"
        saida.write_text(ass, encoding="utf-8")  # UTF-8 SEM BOM
    print(f"legendas: {len(frases_por_bloco)} cenas -> {legdir.name}")


if __name__ == "__main__":
    main()
