"""Funcoes compartilhadas do pipeline /canal-dark.

Tudo que os outros scripts precisam pra sobreviver ao Windows: sondar arquivo,
medir duracao sem cair no locale pt-BR, escrever lista de concat UTF-8 SEM BOM,
e o padrao de erro honesto.
"""
import json, pathlib, subprocess, sys

FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"

# saida pro YouTube (doc oficial de upload). GOP = metade do fps, closed.
V_ARGS = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
          "-profile:v", "high", "-g", "15", "-keyint_min", "15", "-sc_threshold", "0", "-bf", "2"]
A_ARGS = ["-c:a", "aac", "-b:a", "256k", "-ac", "2", "-ar", "48000"]


def erro(msg):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def roda(cmd, **kw):
    """Roda um comando e devolve o CompletedProcess. Nunca joga stdout gigante no contexto."""
    return subprocess.run(cmd, check=True, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", **kw)


def dur(arquivo):
    """Duracao em segundos. Blinda contra ffprobe devolver virgula no locale pt-BR."""
    out = roda([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                "-of", "csv=p=0", str(arquivo)]).stdout.strip()
    return float(out.replace(",", "."))


def sonda(video):
    """largura, altura, fps, duracao, e se e vertical."""
    out = roda([FFPROBE, "-v", "error", "-select_streams", "v:0",
                "-show_entries", "stream=width,height,r_frame_rate",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1", str(video)]).stdout
    d = dict(l.split("=", 1) for l in out.strip().splitlines() if "=" in l)
    num, den = (d.get("r_frame_rate", "30/1").split("/") + ["1"])[:2]
    return {
        "largura": int(d["width"]),
        "altura": int(d["height"]),
        "fps": round(float(num) / float(den or 1), 3),
        "duracao": float(d.get("duration", "0").replace(",", ".")),
        "vertical": int(d["height"]) > int(d["width"]),
    }


def tem_video(arquivo):
    """True se o arquivo tem stream de video (distingue clipe de foto/audio)."""
    try:
        out = roda([FFPROBE, "-v", "error", "-select_streams", "v:0",
                    "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(arquivo)]).stdout
        return "video" in out
    except subprocess.CalledProcessError:
        return False


def salva_json(caminho, obj):
    """JSON em UTF-8 SEM BOM (o resto do pipeline le com o mesmo pressuposto)."""
    p = pathlib.Path(caminho)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")


def le_json(caminho):
    return json.loads(pathlib.Path(caminho).read_text(encoding="utf-8-sig"))


def escreve_lista_concat(caminho, arquivos):
    """Lista do concat demuxer do ffmpeg, UTF-8 SEM BOM.

    Os dois modos de falha do Windows, os dois mudos:
    - Set-Content grava ANSI (CP1252) e o ffmpeg nao abre nome com acento.
    - Out-File -Encoding utf8 grava COM BOM e o ffmpeg le '<BOM>file' como keyword.
    Escrevendo os bytes daqui, em Python, os dois somem. Nome relativo + aspas
    simples escapadas pra sobreviver a apostrofo no nome.
    """
    p = pathlib.Path(caminho)
    linhas = []
    for a in arquivos:
        nome = pathlib.Path(a).name.replace("'", "'\\''")
        linhas.append(f"file '{nome}'")
    p.write_text("\n".join(linhas) + "\n", encoding="utf-8")  # sem BOM
    return p
