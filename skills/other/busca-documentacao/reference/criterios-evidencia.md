# criterios-evidencia.md — anti-bluff: the gates that keep it honest

The spec's whole differentiator is *"lê documentação REAL, não memória do treinamento"*. If the skill
fabricates a feature, a gotcha or a price, it's worse than useless — it sends the builder down a wrong
path with false confidence. These gates are not optional.

## Gate 1 — Fetch-integrity (discard blocked/garbage pages)
A fetched page is DISCARDED — never summarized, never read as evidence — if it contains any of:
- "Just a moment" / Cloudflare `cf-challenge` / "Enable JavaScript" / "Checking your browser"
- a login/sign-in wall where the content should be
- an empty or near-empty body (no real content)
Discarded pages go to the report's **"Fontes que não consegui ler"** bucket with the URL + a one-line
manual-check instruction. **Blocked ≠ absent ≠ feature-missing.** A walled doc never becomes "a ferramenta
não tem essa feature" and never becomes a fabricated summary.
Known-walled (don't even WebFetch): alternativeto.net, producthunt.com, saashub.com → `site:` search only.

## Gate 2 — Mandatory self-verify (before writing the report)
Re-read every tool card and confirm each of these came from a fetch/search THIS session:
- the tool exists and the link resolves to THAT tool (no duplicate URL pointing at a different product);
- each feature is in the doc/README you read (not assumed from the tool's reputation);
- each gotcha has a real issue/post/review link;
- each price/monetization label came from the actual pricing page (or is marked inferred);
- if a repo is recommended as a fork/absorb base, its license came from the GitHub API (`license.spdx_id`)
  and was translated to plain permission — NOT guessed. `null`/`NOASSERTION` → "confira o arquivo LICENSE",
  never a permission claim.
Anything that fails → move it to **"não confirmado / verificar"** with the exact search to run, or drop it.
Do NOT present training-memory facts as documentation you read.

## Gate 3 — Labeling claims (4-class + "relato não auditado")
For any claim, the reader must know how firm it is. Use the status classes:
- **Confirmado** — read directly in an official source this session (cite it).
- **Parcial** — partially supported / one weak source.
- **Inferido** — reasoned from indirect signal (e.g. architecture inferred from pricing, not code) —
  always labeled as inference.
- **Não confirmado** — couldn't verify → goes to the verify bucket, never stated as fact.
Self-reported numbers (a user's "tenho 10k usuários", a vendor's testimonial MRR) get stamped
**"relato não auditado"**. Never write "estudos mostram" without a real URL returned this session.

## Gate 4 — Citation discipline
- Every per-tool card carries exactly one real **`Fonte:`** line (URL + the surface: README / changelog /
  pricing / issue).
- Every table claim is traceable back to a card.
- **Never invent a URL.** If you don't have one, write "não encontrado" — a blank or a guessed link is a
  failure, not a placeholder.

## Gate 5 — Notation lint (run before writing)
- Every `$` in the output is part of `R$` (BR price) or `US$` (foreign price) — fix any bare `$`.
- Foreign price bands stay `US$`; don't silently convert to R$ (the reader sets their own R$ price).
- No time-to-money, no income guarantee, no hype adjective ("incrível", "revolucionário"). Ranges with
  sources, never guarantees.
