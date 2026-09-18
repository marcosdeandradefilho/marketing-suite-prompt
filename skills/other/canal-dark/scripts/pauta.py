"""pauta.py — sugere TEMAS de video achando o que ESTOUROU em canais do nicho.

Metodo (tudo gratis, so yt-dlp, sem chave — ver reference/canal.md):
1. Busca o nicho no YouTube (ytsearch) -> videos fortes + os canais que aparecem.
2. Escolhe os canais mais fortes (ou usa os que o usuario deu como referencia no canal.json).
3. Lista os uploads recentes de cada canal (--flat-playlist, barato) e acha OUTLIER:
   video com views >= 3x a MEDIANA do canal (MEDIANA, nao media: um viral so nao distorce).
4. Junta, ranqueia por multiplicador, tira repetido -> temas candidatos.

NAO copia video: entrega o TEMA e por que bombou. O angulo original e sempre do usuario
(requisito da politica de conteudo do YouTube — ver reference/politica-youtube.md).

Degrada com honestidade: se a web cair / yt-dlp tomar 429 / o termo nao tiver base, escreve
'temas' vazio + um aviso, e quem chamou pede o tema direto ao usuario avisando que vai SEM
validacao de demanda.

Uso:
  python scripts/pauta.py <canal_dir> [--nicho "estoicismo"] [--canais url1,url2] [--n 12] [--idioma pt-BR]
Saida: <canal_dir>/pauta-cache.json  +  um resumo no stdout.
"""
import sys, json, subprocess, statistics, pathlib, argparse
from collections import defaultdict

SEP = "\x1f"        # separador raro (unit separator): nao aparece em titulo de video
YTDLP = "yt-dlp"
MULT_OUTLIER = 3.0  # views >= 3x a mediana = outlier (faixa do vidIQ; ver dossie)
BASE_MIN = 5        # menos que isso de video, a mediana nao e confiavel


def _run(args, timeout=90):
    """Roda o yt-dlp. Devolve stdout (str) ou "" em qualquer falha. Nunca levanta."""
    try:
        p = subprocess.run([YTDLP] + args, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return p.stdout if p.returncode == 0 else ""
    except FileNotFoundError:
        print("ERRO: yt-dlp nao encontrado. Instale (winget install yt-dlp  /  pip install yt-dlp).",
              file=sys.stderr)
        sys.exit(2)
    except subprocess.TimeoutExpired:
        return ""


def _int(s):
    s = (s or "").strip()
    try:
        return int(s)
    except ValueError:
        return None


def busca_nicho(nicho, n=15):
    """ytsearch: videos fortes do nicho (flat traz view_count)."""
    tpl = SEP.join(["%(view_count)s", "%(id)s", "%(title)s", "%(channel)s", "%(channel_url)s"])
    out = _run(["--flat-playlist", "--print", tpl, f"ytsearch{n}:{nicho}"])
    vids = []
    for ln in out.splitlines():
        p = ln.split(SEP)
        if len(p) >= 5:
            vids.append({"views": _int(p[0]), "id": p[1], "titulo": p[2],
                         "canal": p[3], "canal_url": p[4]})
    return vids


def uploads_canal(canal_url, ate=40):
    """Uploads recentes de um canal (flat, barato). upload_date vem NA no flat (nao usamos)."""
    url = canal_url.rstrip("/")
    if not url.endswith("/videos"):
        url += "/videos"
    tpl = SEP.join(["%(view_count)s", "%(id)s", "%(title)s"])
    out = _run(["--flat-playlist", "--playlist-end", str(ate), "--print", tpl, url])
    vids = []
    for ln in out.splitlines():
        p = ln.split(SEP)
        if len(p) >= 3 and _int(p[0]) is not None:
            vids.append({"views": _int(p[0]), "id": p[1], "titulo": p[2]})
    return vids


def outliers(vids, mult=MULT_OUTLIER):
    vv = [v["views"] for v in vids if v["views"]]
    if len(vv) < BASE_MIN:
        return []
    med = statistics.median(vv)
    if med <= 0:
        return []
    res = []
    for v in vids:
        if v["views"] and v["views"] >= mult * med:
            o = dict(v)
            o["multiplicador"] = round(v["views"] / med, 1)
            o["mediana_canal"] = int(med)
            res.append(o)
    return sorted(res, key=lambda x: x["multiplicador"], reverse=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canal_dir")
    ap.add_argument("--nicho", default=None)
    ap.add_argument("--canais", default=None, help="csv de URLs de canal de referencia")
    ap.add_argument("--n", type=int, default=12)
    ap.add_argument("--idioma", default=None)
    a = ap.parse_args()

    canal_dir = pathlib.Path(a.canal_dir)
    nicho = a.nicho
    canais = [c.strip() for c in a.canais.split(",") if c.strip()] if a.canais else []

    cj = canal_dir / "canal.json"
    if cj.exists():
        try:
            d = json.loads(cj.read_text(encoding="utf-8-sig"))
            nicho = nicho or d.get("nicho")
            if not canais:
                canais = list(d.get("canais_referencia", []) or [])
        except (ValueError, OSError):
            pass
    if not nicho:
        print("ERRO: sem nicho. Passe --nicho ou tenha um canal.json com o campo 'nicho'.", file=sys.stderr)
        sys.exit(1)

    avisos = []
    nicho_vids = busca_nicho(nicho, 15)
    if not nicho_vids:
        avisos.append("A busca do nicho nao retornou nada (web bloqueada, yt-dlp com 429, ou termo raro). "
                      "Sem demanda medida: peca o tema direto ao usuario e avise que o video vai SEM validacao.")

    # sem canais de referencia? descobre os mais fortes dos resultados do nicho.
    if not canais and nicho_vids:
        peso = defaultdict(int)
        for v in nicho_vids:
            if v["canal_url"]:
                peso[v["canal_url"]] += (v["views"] or 0)
        canais = [u for u, _ in sorted(peso.items(), key=lambda kv: kv[1], reverse=True)[:4]]

    temas, vistos = [], set()
    for cu in canais[:5]:
        for o in outliers(uploads_canal(cu)):
            chave = o["titulo"].lower().strip()
            if chave in vistos:
                continue
            vistos.add(chave)
            temas.append({"titulo": o["titulo"], "canal_url": cu, "views": o["views"],
                          "multiplicador": o["multiplicador"], "mediana_canal": o["mediana_canal"],
                          "url": f"https://www.youtube.com/watch?v={o['id']}",
                          "por_que": f"{o['multiplicador']}x a mediana do proprio canal"})

    # completa com os top da busca do nicho (caso um canal nao liste os uploads)
    for v in sorted([x for x in nicho_vids if x["views"]], key=lambda x: x["views"], reverse=True)[:6]:
        chave = v["titulo"].lower().strip()
        if chave in vistos:
            continue
        vistos.add(chave)
        temas.append({"titulo": v["titulo"], "canal": v["canal"], "views": v["views"],
                      "url": f"https://www.youtube.com/watch?v={v['id']}",
                      "por_que": "forte na busca do nicho"})

    if canais and not temas and nicho_vids:
        avisos.append("Achei canais do nicho mas nenhum outlier claro (>=3x a mediana) nos ultimos uploads. "
                      "Os candidatos abaixo sao os mais vistos da busca, sem o selo de outlier.")

    temas = sorted(temas, key=lambda t: t.get("multiplicador", 0), reverse=True)[:a.n]
    saida = {"nicho": nicho, "idioma": a.idioma, "canais_usados": canais[:5],
             "gerado_por": "pauta.py", "avisos": avisos, "temas": temas}
    canal_dir.mkdir(parents=True, exist_ok=True)
    (canal_dir / "pauta-cache.json").write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"OK pauta-cache.json  nicho='{nicho}'  canais={len(canais[:5])}  temas={len(temas)}  avisos={len(avisos)}")
    for t in temas[:8]:
        m = f"{t['multiplicador']}x" if t.get("multiplicador") else "nicho"
        print(f"  [{m:>5}] {(t.get('views') or 0):>9} views  {t['titulo'][:66]}")
    if avisos:
        for av in avisos:
            print("  AVISO: " + av, file=sys.stderr)


if __name__ == "__main__":
    main()
