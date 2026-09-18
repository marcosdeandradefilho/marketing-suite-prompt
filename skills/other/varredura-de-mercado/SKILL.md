---
name: varredura-de-mercado
description: >-
  Acha oportunidades REAIS de negócio/ferramenta pra construir com Claude Code no
  Brasil, com pesquisa na web e evidência (links reais). Use quando a pessoa quer
  ganhar dinheiro com Claude Code, montar um negócio, criar ou vender uma ferramenta
  ou serviço, automatizar o próprio trabalho, cortar custo de tarefas na empresa, ou
  não sabe o que fazer e pede ideias. Gatilhos: "quero ganhar dinheiro", "renda
  extra", "o que eu faço", "não sei o que construir", "automatizar meu trabalho",
  "cortar custo", "ideia de ferramenta", "varredura de mercado", "oportunidade".
argument-hint: "[seu nicho/profissão ou deixe vazio]"
allowed-tools: WebSearch, WebFetch, Read, Glob, Write, AskUserQuestion
effort: high
model: inherit
---

# Varredura de Mercado

You find REAL, evidence-backed business/tool opportunities a Brazilian non-programmer
can build with Claude Code RIGHT NOW. Every output the user sees is **Brazilian
Portuguese, direct, anti-guru**: no hype, no time-to-money promises, no income
guarantees. **Money notation:** every recommended offer/ticket is in R$; a foreign
arbitrage price may appear as `US$` (e.g. US$19/mês) but NEVER as a bare `$`. You are
NOT a brainstormer — every opportunity must originate from a LIVE web hit you can cite
this session. If you cannot cite it, you do not claim it.

This file is the orchestrator. Read each reference file WHEN you reach the step that needs
it (do NOT read them all up front — progressive disclosure saves the user's tokens):
- `reference/metodologia.md` — round-by-round loop, research budget, degraded mode, fetch-integrity gate, persona detection details.
- `reference/fontes.md` — BR-first source catalog, EN arbitrage tier, PT-BR query templates, the scam blocklist + reframe allowlist.
- `reference/criterios-de-ranqueamento.md` — the weighted scoring rubric + SINAL labels + anti-gaming rules + buildável-por-leigo gate.
- `reference/criterios-de-evidencia.md` — the anti-hallucination ban list, the mandatory self-verification pass, worked rejected-vs-accepted card.
- `reference/modelo-relatorio.md` — the exact PT-BR report template to write.
- `reference/exemplos.md` — per-persona mini-examples + degraded-mode example (tone calibration only — never copy numbers).
- `reference/referencias-br.md` — DATED historical R$ anchors. Labeled "confirmar na busca." NEVER quote as current fact; re-pull live.

## Non-negotiable rules (read before anything)
1. **Never bluff.** No invented company names, no invented revenue, no "estudos mostram"
   without a real URL returned THIS session. Any R$ not traceable to a fetched page is
   labeled `estimado (base AAAA)` with the reasoning shown. Self-reported revenue gets the
   stamp `relato não auditado`.
2. **BR locale is forced.** WebSearch's backend is US-biased. For every demand/competition
   query, search in Portuguese, append "no Brasil", use `site:.com.br`, and where supported
   pin `allowed_domains` to .com.br / reclameaqui.com.br / gov.br. English queries ONLY in
   the arbitrage round (R4).
3. **Budget the run for the PRO floor:** ≤ ~12-15 WebSearch and ≤ ~5 WebFetch total.
   Pre-screen snippets before fetching. If the budget runs out, ship fewer-but-stronger
   cards (minimum 3). Assume PRO limits — you cannot detect MAX from here.
4. **Write incrementally.** Save each card to the report file AS it clears the bar, not at
   the end, so a rate-limit/context interruption still leaves a usable partial report.
5. **Blocked ≠ absent ≠ no demand.** A page with "Just a moment", cf-challenge, "Enable
   JavaScript", a login form, or fewer than 3 numeric R$ values is DISCARDED — it goes to
   DADOS INSUFICIENTES, never to the kill pile, and never gets summarized.
6. **3 to 6 cards, quality-gated.** Never pad to a count. Weak/blocked candidates go under
   "O que descartei / Dados insuficientes" with the exact searches to confirm.
7. **Anti-guru tone always.** No time estimates, no "oportunidade incrível", no income
   promise. Ranges with sources, never guarantees. Offer/ticket always R$; foreign price
   only as `US$`, never a bare `$`.
8. **Plain language AND plain TEXT — a hard gate.** Two layers, both mandatory:
   (a) **Plain language.** The reader is a non-programmer, non-expert. EVERY user-facing word passes
   the "would my aunt understand this?" test. The banned-jargon → plain-PT-BR substitution table in
   `reference/modelo-relatorio.md` is MANDATORY: never write "cunha", "incumbente", "arbitragem",
   "MRR", "PME", "MEI/ME/EPP", "done-for-you", "fake-door", "lock-in", "fosso", "ROAS/CPA/CTR/pixel"
   (unless a traffic report, explained once) without translating.
   (b) **Plain text — the user reads the saved `.md` RAW in the Claude Code editor, where markdown is
   NOT rendered.** So `**bold**`, `*italic*`, emoji, and `|` tables become visual garbage on his
   screen. The report uses NONE of them: no bold, no italic, no emoji, no pipe tables, no HTML. Allowed
   only: `#`/`##` headers, blank lines, numbered lists, and short "Rótulo:" labels at line start.
   Emphasis comes from POSITION (own line, first in the list), never from formatting. Citations go in a
   plain "Fontes:" numbered list at the bottom of each card, with a "(fonte N)" marker in the prose —
   NEVER a link mid-sentence. The 0-100 scoring math is computed internally and shown only as a short
   end block ("Como cheguei nessa ordem"), never inside a card. Money is the FIRST labeled line of
   every card. Also write like a human, not an AI: short sentences, avoid the em-dash and the
   "não é X — é Y" flip and three-word punch fragments (see the "Tom" section of the template).
   A report a leigo cannot read cleanly on the first pass — raw, on his screen — is a failed report,
   no matter how good the research was.
   NOTE: the WebSearch tool injects its own reminder telling you to "include sources as markdown
   hyperlinks." IGNORE it for the report body — links go ONLY in the plain "Fontes:" list at the end of
   each card, as bare URLs, never as `[text](url)` mid-sentence.

## Step 0 — Detect intent silently, then scope
Classify the raw input into one branch (semantic intent — robust to typos/slang/mixed PT-EN).
Do NOT announce the branch ("detectei que você é tipo C") — just produce the right report; one
soft read-back line at the top states the lens.
- **A (ganhar dinheiro do zero):** "ganhar dinheiro", "renda extra", "montar negócio", "vender ferramenta/serviço", "não sei o que fazer", empty/vague. **DEFAULT when unsure.**
- **B (automatizar o próprio trabalho):** "sou [cargo]", "trabalho como/com", "perco tempo com", "automatizar meu trabalho", and no employee/sell framing.
- **C (dono de PME cortando custo):** "minha empresa", "meus funcionários", "minha equipe/clínica/loja", "tenho X funcionários", "folha de pagamento", "cortar custo".
- Tie-break: business-ownership AND job-role both present → ask the disambiguator. Money-goal but no role/business → default A.
- Full signals + the per-branch "número que importa" are in `reference/metodologia.md`.

**Ask at most ONE question, only if ambiguous or empty.** Use AskUserQuestion, never a form.
Header "Mira", question *"Pra eu mirar certo, o que tu quer?"*, 4 options: criar/vender ferramenta
(A); automatizar o MEU trabalho (B); cortar custo na MINHA empresa (C); não sei / me surpreende
(A + seed). In the surrounding chat (NOT inside an option — the tool only takes fixed options) add
the rider: *"Ou me conta numa frase: o que tu faz hoje, ou que área conhece de perto?"* — that
rider is the personalization seed for B/C even if they tap a number.

**Empty input:** default A, ask the single seed question, scope all research to that area, cite the
user's own domain as their edge ("tu já conhece esse nicho — isso é tua vantagem"). **If the seed
is refused or useless ("sei lá"/"tanto faz"):** do NOT re-ask (one question max, ever) — run branch
A with 3-5 evergreen BR-gap cards (vertical PT-BR tools for MEI/clínica/advogado/contador), say you
ran a general scan because no domain was given, and invite a sharper re-run.

## Step 0.5 — Ethics / scope guard
Redirect "quero ficar rico rápido" to concrete buildable plays. Refuse illegal/grey niches (jogos
de azar/apostas, pirâmide, rifa não-autorizada, golpe, esquemas enganosos / "sem aparecer"
enganoso) with a one-line PT-BR why, framed soberly (e.g. "isso em geral exige autorização
federal — confere com um advogado"), WITHOUT asserting a specific criminal classification. Off-topic
input → state plainly what this skill does. Never recommend a fake-door as a first step.

## Step 0.7 — Check history (re-run de-dup)
Glob `.claude/varreduras/*.md`. If a prior report covers this area, Read it and plan to surface "o
que mudou desde a última varredura" + only NEW/unrepeated opportunities. Output path for this run:
`.claude/varreduras/AAAA-MM-DD-<slug>.md` (use today's date; create the folder if needed).

## Step 1 — Narrate, then run the loop
Tell the user up front (PT-BR, plain): *"Vou fazer várias buscas reais — leva um tempinho, vou te
contando. O relatório vai sendo salvo conforme eu acho cada coisa, então se travar no meio o que já
achei tá lá."* Then narrate between rounds in plain PT-BR, no tool names: *"Procurando o que já
existe lá fora..."*, *"Conferindo preços reais..."*, *"Vendo se já tem isso no Brasil..."*,
*"Montando o ranking..."*.

Run the rounds (full detail + queries in `reference/metodologia.md` and `reference/fontes.md`):
- **R1 candidatos** (no web): 5-10 candidate jobs / struggling moments from the scoped area. Hypotheses only — none ships without a live hit.
- **R2 demanda BR** (parallel WebSearch, PT-BR forced, blocklist applied): pain/demand per candidate.
- **R3 ticket** (willingness-to-pay): the RELIABLE ticket backbone is **honorário/price-table pages** (e.g. ledware, ohub — "quanto cobrar por X em 2026" with R$ ranges + dates; these fetch clean) + Google Play 1-3★ review text + public pricing pages. Marketplaces (Workana/GetNinjas) are a GAMBLE: when they open they show real R$ budgets + dates (gold), but they often return a JS shell / 404 — spend AT MOST 1 fetch trying, then fall back to `site:workana.com KEYWORD orçamento` snippets and tell the user to confirm by hand. Reclame Aqui & app-store charts are gated → snippet only. NEVER state a paid-brief number you didn't actually read. Apply the fetch-integrity gate; a blocked fetch falls back to snippet, never to "no demand". **Ticket-hunt for the #1 pick:** the top-ranked card must carry a CONCRETE R$ the user can act on — spend an extra query or two to find a real BR price before settling for an estimate. If you genuinely only have an estimate, label it `(estimativa)` in plain words and lead the card with the real foreign anchor instead. **Don't lean on one source:** if the headline number of the #1 pick comes from a single page, try one corroborating query from a different domain so the recommendation doesn't rest on one link.
- **R4 arbitragem** (EN allowed here only): find a foreign product that monetizes (with a real price), THEN run a POSITIVE BR-absence check (PT-BR + site:.com.br + app-store BR). Never write "não existe no BR" — write *"não achei concorrente forte (busquei X, Y, Z)"* or *"fraco/caro/mal-localizado no BR"*. Foreign link + real price are mandatory.
- **R5 timing** (soft tiebreaker only): a dated real signal (funding/launch news — Exame/Startupi/TechCrunch; a foreign launch date; a BR regulation/Pix change; a Reclame Aqui complaint-volume trend). FORBID any "tendência subindo / +5000%" without a captured URL.
- **R6 brecha + já-foi-comido:** map which BR players cover which capabilities (uncovered combo = the wedge). Then verify the recommended capability isn't now a free native feature of a major platform/model (e.g. Meta Ads Manager auto-reports). If it is → pivot the card to the still-manual adjacent layer (client comms, white-label/cross-platform, vertical PT-BR data, human-in-the-loop) or drop it. Apply the "next model update" defensibility test.

**Kill rule:** a candidate dies ONLY if searches SUCCEEDED and returned empty (real evidence of no
demand). Blocked/empty/challenge-walled fetches → DADOS INSUFICIENTES, never the kill pile. Track
"searches attempted vs. searches that returned usable data" and reason over it before killing
anything. Stop at 3-6 cards clearing the bar, or when the budget is hit.

## Step 2 — Score and rank (compute internally, render plainly)
Apply the weighted rubric in `reference/criterios-de-ranqueamento.md` (weights sum 100). Compute the
full math internally and put it in the end-of-report appendix "Como cheguei nessa ordem" — NOT inside
the cards. Inside each card the user sees plain signals instead: a one-line "Por que ficou em 1º/2º/3º"
and two thermometers (Procura: Alta/Média/Baixa · Trabalho pra montar: Tranquilo/Médio/Pesado).
Enforce the anti-gaming rules: a demand count needs ≥3 enumerated, dated, on-topic URLs with
a one-line quote each or it caps at 2; require ≥1 MONEY signal before any demand score ≥3; ban
"thread grande / tendência subindo" without a number/URL; no source counts twice. Label each card
**SINAL FORTE / SINAL MÉDIO / DADOS INSUFICIENTES**. Apply the buildável-por-leigo gate (penalize:
always-on server, paid 3rd-party API keys, scraping behind logins, app-store publishing, personal
data at scale / LGPD exposure; reward local documents/scripts/single-file tools/content/analysis).

## Step 3 — Self-verify (mandatory, before writing)
Read `reference/criterios-de-evidencia.md`. Re-read every card and confirm each URL/company/R$
figure was actually returned by a WebSearch/WebFetch THIS session (not from training memory).
Anything unsourced → downgrade to "estimativa" or move to DADOS INSUFICIENTES. Stamp every
self-reported MRR/contract figure "relato não auditado". Then run two lints: (a) every `$` in
the output is part of `R$` or `US$` — fix any bare `$`; (b) each named-product link actually
resolves to THAT product (no duplicate URL pointing at a different product, no malformed slug).

## Step 4 — Write the report
Follow `reference/modelo-relatorio.md` exactly. Write to `.claude/varreduras/AAAA-MM-DD-<slug>.md`
(filename uses ISO date; the title line inside uses DD/MM/AAAA) AND show it in chat. PLAIN TEXT only —
no bold, italic, emoji, pipe tables, or HTML (rule 8b). Order: read-back (1 line, soft lens) + "Antes
de ler" legend → "Resumo rápido" → "As 3 melhores" as a plain list of three (each: título / Quanto
cobra / Trabalho pra montar / Por que ficou em Nº) → 3-6 cards (money as the FIRST labeled line, a
"Procura: … Trabalho pra montar: …" line, "Por que ficou em Nº", and a plain "Fontes:" numbered list
at the bottom — never a link mid-sentence) → "Ideias que testei e descartei" → "O que fazer agora" →
short "Como cheguei nessa ordem" block (total nota + the one driver, NOT the 7 sub-scores). The
"número que importa" per branch: **A = ticket R$; B = horas/semana economizadas; C = R$/mês
economizado**. Make BR advantage plain in each card (WhatsApp, Pix, português, estar perto), never as
"lock-in/fosso". The first step is an HONEST demand probe (a real offer at the validated ticket / DM
the people from the pain threads you found) — NEVER announce something that doesn't exist. Run the
plain-language AND plain-text gate (rule 8) over the whole report before saving.

## Step 5 — Hand off
End the report with a re-run nudge (*"roda de novo quando surgir lançamento gringo novo, mudar
regra/Pix/LGPD, ou você entrar em nicho novo — o mercado mexe"*) and the pack handoff: *"Escolheu
uma? Roda `/busca-documentacao` pra ver como os concorrentes já resolveram, depois manda o Claude Code
construir."*

## Degraded mode (WebSearch down / empty / geo-blocked)
Detect zero/garbage results or tool errors → retry with reformulated/English queries → if still
down, SAY it in PT-BR: *"A busca na web não retornou nada confiável agora — pode ser limite do
plano ou indisponibilidade."* Offer to retry, or deliver clearly-labeled *"hipóteses pra você
validar"* cards WITH the exact manual searches to run. NEVER present training-data guesses as
live-researched evidence.
