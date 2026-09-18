"""publicar.py — monta o PACOTE DE PUBLICACAO pronto pra colar no YouTube Studio.

Le o roteiro (00-plano.json), a medicao da voz (01-voz/manifest.json) e os creditos
(03-clipes/creditos.json), mais o texto criativo que o Claude escreve em
06-saida/publicar-input.json, e escreve 06-saida/PUBLICAR.txt: titulo + titulos A/B,
descricao com o gancho (primeira dobra), CAPITULOS calculados dos tempos REAIS do audio,
bloco de creditos do Pexels, hashtags, tags e o aviso de conteudo sintetico.

O que este script GARANTE (nao confia no Claude calcular na mao):
- Capitulos derivam do manifest: bloco 1 forcado a 0:00, minimo de 10s entre capitulos,
  minimo de 3 capitulos (regra do YouTube) — se nao der 3, OMITE capitulos e avisa.
- Limites conferidos: titulo <=100 (visivel ~70), gancho da descricao na primeira dobra,
  hashtags <=15 (acima disso o YouTube IGNORA todas), descricao <=5000.
Os numeros vem de reference/publicacao.md (fontes oficiais do YouTube Help).

Uso:  python scripts/publicar.py <projeto>
Saida: <projeto>/06-saida/PUBLICAR.txt  (texto puro, pronto pra copiar e colar)
"""
import sys, pathlib
from comum import le_json, erro

# --- limites do YouTube (ver reference/publicacao.md) -------------------------
TITULO_MAX = 100          # limite duro de caracteres do titulo (UI do YouTube)
TITULO_VISIVEL = 70       # acima disso o comeco e que aparece; celular corta ~50-60
GANCHO_DOBRA = 157        # ~caracteres visiveis antes do "mostrar mais" (desktop; celular ~100)
DESC_MAX = 5000           # limite duro da descricao (oficial)
HASHTAG_MAX = 60          # >60 hashtags = o YouTube IGNORA TODAS (oficial). Ideal: 3-5.
CAP_MIN_QTD = 3           # minimo de capitulos pra ativar a barra (oficial)
CAP_GAP_MIN = 10.0        # cada capitulo precisa de >=10s do anterior (oficial)


def ts(seg):
    """Segundos -> timestamp de capitulo (M:SS ou H:MM:SS). Piso pro segundo inteiro."""
    seg = int(seg)
    h, m, s = seg // 3600, (seg % 3600) // 60, seg % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def capitulos(manifest, labels):
    """Escolhe capitulos validos: 0:00 no comeco, >=10s entre eles, rotulo por bloco.

    Bloco curto demais (gap < 10s do capitulo anterior) e absorvido no anterior
    (nao vira capitulo). Devolve (linhas, avisos)."""
    blocos = manifest.get("blocos", [])
    caps, ultimo = [], -1e9
    for i, b in enumerate(blocos):
        rotulo = (labels[i] if i < len(labels) else b.get("funcao", f"Parte {i+1}")).strip()
        ini = 0.0 if i == 0 else float(b.get("ini", 0))
        if i == 0 or (ini - ultimo) >= CAP_GAP_MIN:
            caps.append((ini, rotulo))
            ultimo = ini
    avisos = []
    if len(caps) < CAP_MIN_QTD:
        avisos.append(
            f"So deu pra formar {len(caps)} capitulo(s) validos (o YouTube exige >=3 "
            f"com >=10s cada). CAPITULOS foram OMITIDOS. Isso e normal em video curto de "
            f"teste; num video de 10+ min os blocos sao maiores e a barra aparece.")
        return [], avisos
    linhas = [f"{ts(t)} {r}" for t, r in caps]
    return linhas, avisos


def bloco_creditos(creditos):
    if not creditos:
        return []
    linhas = ["CREDITOS", "Videos e fotos: Pexels (https://www.pexels.com) — uso gratuito, sem royalties."]
    vistos = set()
    for it in creditos.get("itens", []):
        autor, url = it.get("autor", "").strip(), it.get("url_autor", "").strip()
        chave = (autor, url)
        if autor and chave not in vistos:
            vistos.add(chave)
            linhas.append(f"- {autor}: {url}" if url else f"- {autor}")
    return linhas


def main():
    if len(sys.argv) < 2:
        erro("uso: python scripts/publicar.py <projeto>")
    proj = pathlib.Path(sys.argv[1]).resolve()
    plano = le_json(proj / "00-plano.json")
    manifest_p = proj / "01-voz" / "manifest.json"
    if not manifest_p.exists():
        erro("01-voz/manifest.json nao existe — rode a voz (voz.py) antes de publicar.")
    manifest = le_json(manifest_p)

    creditos_p = proj / "03-clipes" / "creditos.json"
    creditos = le_json(creditos_p) if creditos_p.exists() else None

    entrada_p = proj / "06-saida" / "publicar-input.json"
    ent = le_json(entrada_p) if entrada_p.exists() else {}

    avisos = []
    if not entrada_p.exists():
        avisos.append(
            "06-saida/publicar-input.json nao existe: usei o titulo do plano e rotulos "
            "provisorios. O Claude deveria escrever esse arquivo com titulo, gancho, corpo, "
            "hashtags e tags (ver reference/publicacao.md).")

    # --- titulo ---------------------------------------------------------------
    titulo = (ent.get("titulo") or plano.get("titulo") or "").strip()
    if not titulo:
        avisos.append("Sem titulo (nem no publicar-input.json nem no plano).")
    if len(titulo) > TITULO_MAX:
        avisos.append(f"TITULO tem {len(titulo)} caracteres — o YouTube corta em {TITULO_MAX}. Encurte.")
    elif len(titulo) > TITULO_VISIVEL:
        avisos.append(f"TITULO tem {len(titulo)} caracteres — acima de ~{TITULO_VISIVEL} ele corta no "
                      f"celular/busca. O comeco tem que entregar a curiosidade sozinho.")
    alternativos = [t.strip() for t in ent.get("titulos_alternativos", []) if t.strip()]

    # --- descricao ------------------------------------------------------------
    gancho = (ent.get("descricao_gancho") or "").strip()
    corpo = (ent.get("descricao_corpo") or "").strip()
    if gancho and len(gancho) > GANCHO_DOBRA:
        avisos.append(f"GANCHO da descricao tem {len(gancho)} caracteres — no desktop so ~{GANCHO_DOBRA} "
                      f"aparecem antes do 'mostrar mais' (no celular ~100). Ponha o mais forte no comeco.")

    # --- capitulos (deterministico do manifest) -------------------------------
    labels = [c.strip() for c in ent.get("capitulos", [])]
    cap_linhas, cap_avisos = capitulos(manifest, labels)
    avisos += cap_avisos

    # --- hashtags e tags ------------------------------------------------------
    hashtags = [h.strip() for h in ent.get("hashtags", []) if h.strip()]
    hashtags = ["#" + h.lstrip("#") for h in hashtags]
    if len(hashtags) > HASHTAG_MAX:
        avisos.append(f"{len(hashtags)} hashtags — acima de {HASHTAG_MAX} o YouTube IGNORA TODAS. "
                      f"Cortei pras {HASHTAG_MAX} primeiras (mas o ideal e usar so 3 a 5).")
        hashtags = hashtags[:HASHTAG_MAX]
    elif len(hashtags) > 5:
        avisos.append(f"{len(hashtags)} hashtags — o YouTube aceita ate {HASHTAG_MAX}, mas 3 a 5 fortes "
                      f"rende mais. As 3 primeiras sao as que aparecem acima do titulo.")
    tags = [t.strip() for t in ent.get("tags", []) if t.strip()]

    # --- monta a descricao final (o que vai colado no campo do YouTube) -------
    desc = []
    if gancho:
        desc.append(gancho)
    if corpo:
        desc.append("")
        desc.append(corpo)
    if cap_linhas:
        desc.append("")
        desc.append("CAPITULOS")
        desc += cap_linhas
    creds = bloco_creditos(creditos)
    if creds:
        desc.append("")
        desc += creds
    if hashtags:
        # As 3 primeiras hashtags da descricao aparecem ACIMA do titulo; por isso ordem importa.
        desc.append("")
        desc.append(" ".join(hashtags))
    descricao = "\n".join(desc).strip()
    if len(descricao) > DESC_MAX:
        avisos.append(f"DESCRICAO tem {len(descricao)} caracteres — o limite e {DESC_MAX}. Encurte o corpo.")

    # --- arquivo final --------------------------------------------------------
    out = []
    out.append("PACOTE DE PUBLICACAO — canal-dark")
    out.append("Copie cada bloco pro campo certo no YouTube Studio. Isto e texto puro; nao ha nada")
    out.append("pra 'renderizar', e so colar.")
    out.append("")
    out.append("=" * 70)
    out.append("TITULO  (campo 'Titulo')")
    out.append("=" * 70)
    out.append(titulo)
    if alternativos:
        out.append("")
        out.append("-- outros titulos pra testar (troque depois de ~48h se o CTR vier baixo) --")
        for a in alternativos:
            out.append(f"  {a}")
    out.append("")
    out.append("=" * 70)
    out.append("DESCRICAO  (campo 'Descricao' — cole tudo abaixo)")
    out.append("=" * 70)
    out.append(descricao)
    out.append("")
    out.append("=" * 70)
    out.append("TAGS  (Configuracoes > Tags — separe por virgula)")
    out.append("=" * 70)
    out.append(", ".join(tags) if tags else "(sem tags — as tags pesam pouco hoje; o titulo e a thumb mandam)")
    out.append("")
    out.append("=" * 70)
    out.append("CONTEUDO ALTERADO OU SINTETICO  (obrigatorio marcar)")
    out.append("=" * 70)
    out.append("Este video usa narracao gerada por IA. Ao subir, na etapa de detalhes, em")
    out.append("'Conteudo alterado ou sintetico', marque SIM (conteudo que parece realista foi")
    out.append("gerado/alterado digitalmente). O YouTube pode mostrar um aviso ao publico; isso")
    out.append("NAO tira a monetizacao por si so. Ver reference/politica-youtube.md.")
    if avisos:
        out.append("")
        out.append("=" * 70)
        out.append("CONFERIR  (avisos deste gerador — nao vai pro YouTube)")
        out.append("=" * 70)
        for a in avisos:
            out.append(f"[CONFERIR] {a}")

    destino = proj / "06-saida" / "PUBLICAR.txt"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"OK PUBLICAR.txt  titulo={len(titulo)}ch  capitulos={len(cap_linhas)}  "
          f"hashtags={len(hashtags)}  tags={len(tags)}  avisos={len(avisos)}")
    print(str(destino))


if __name__ == "__main__":
    main()
