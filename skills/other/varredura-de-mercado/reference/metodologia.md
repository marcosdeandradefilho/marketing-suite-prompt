# Metodologia — o loop de varredura

> Detalhe operacional do loop que o `SKILL.md` orquestra. Instruções em inglês, queries/exemplos em PT-BR.

## Research budget (PRO floor — assume PRO, you cannot detect MAX)
- Hard cap: ~12-15 WebSearch + ~5 WebFetch total per run. Track the counter as a checklist.
- Pre-screen search snippets BEFORE any WebFetch. Fetch only high-value pages.
- If the budget runs out: ship fewer-but-stronger cards (minimum 3). Better 3 cited cards than 6 half-fetched.
- Write each card to the report file AS it clears the bar (incremental), so an interruption leaves a usable partial.

## Persona detection (silent, semantic, typo/slang/mixed-PT-EN robust)
- **A (ganhar dinheiro do zero):** money-without-a-job. DEFAULT for empty/ambiguous.
- **B (automatizar o próprio trabalho):** first-person-job language, no employee/sell framing.
- **C (dono de PME):** possessive-business, headcount/cost language.
- Tie-break: business + role both present → ask. Money-goal, no role/business → A.
- NEVER announce the branch. One read-back line states the lens softly.

## Per-persona JTBD frame + "número que importa"
- **A:** zero → a sellable thing fast. Número = R$ ticket (one-off + recurring). Rank by ticket × speed-to-first-money × defensibility. Favors productized-service / arbitrage plays via marketplaces. Reject commodity ChatGPT-wrapper ideas (must pass the "next model update" test).
- **B:** keep the job, kill drudgery / add capacity. Número = horas/semana economizadas (+ extra clients a freelancer/agency can take on). Name the user's actual role tasks back to them (per-role taxonomy in `referencias-br.md`). The user's drudge tasks live in their head, not on the web, so **pivot B's web sweep to the arbitrage / vira-produto angle** — what tools exist abroad for this profession's tasks, what BR peers in this profession complain about / pay for — so the live-evidence engine still earns its keep. Apply the platform-ate-the-task warning.
- **C:** cut cost without hiring. Número = R$/mês economizado vs REAL BR labor cost (pulled live). Ethical anti-guru framing: *"automatiza a tarefa repetitiva, libera/realoca a pessoa"* — NOT "demita amanhã".

## The one disambiguating question (only if ambiguous/empty) — AskUserQuestion, never a form
Header "Mira". *"Pra eu mirar certo, o que tu quer?"* Options: criar/vender ferramenta (A);
automatizar o MEU trabalho (B); cortar custo na MINHA empresa (C); não sei / me surpreende (A +
seed). In the surrounding chat add the rider *"Ou me conta numa frase: o que tu faz hoje, ou que
área conhece de perto?"* = personalization seed (the tool only takes fixed options, so the rider
must be plain chat text, not an option).
- **Empty input:** default A, ask the seed question, scope to that area, cite the user's domain as their edge.
- **Seed refused/useless:** do NOT re-ask; run A with 3-5 evergreen BR-gap cards.

## The rounds
- **R1 candidatos** (no web): 5-10 candidate jobs / struggling moments. Hypotheses only — none ships without a live hit.
- **R2 demanda BR** (parallel WebSearch, PT-BR forced): pain/demand per candidate. Force locale: Portuguese + "no Brasil" + `site:.com.br` + `allowed_domains` .com.br/reclameaqui/gov.br where supported. Apply blocklist + allowlist (`fontes.md`).
- **R3 ticket** (willingness-to-pay): reliable backbone = **honorário/price-table pages** (ledware, ohub-type "quanto cobrar por X 2026" with dated R$ ranges — these fetch clean) + Google Play 1-3★ review text + public pricing pages. Marketplaces (Workana/GetNinjas) are a GAMBLE — sometimes raw R$ budgets+dates, often a JS shell or 404; spend ≤1 fetch, then `site:workana.com KEYWORD orçamento` snippet + "confirm by hand". Reclame Aqui (SPA) and Apple charts (bot-gated) → snippet only, never assert live numbers. Triangulate the #1 ticket across 2+ independent sources; date-stamp every figure. NEVER state a paid-brief number you didn't actually read. Apply the fetch-integrity gate; blocked fetch → snippet fallback, never "no demand".
- **R4 arbitragem** (EN allowed): a foreign product that monetizes (real price) on ProductHunt/G2/Capterra/Indie Hackers/app stores. THEN a positive BR-absence check (PT-BR + `site:.com.br` + app-store BR + "KEYWORD brasil" / "KEYWORD preço R$"). Never "não existe no BR"; write "não achei concorrente forte (busquei X, Y, Z)" or "fraco/caro/mal-localizado". Foreign link + price mandatory; BR-absence = a claim-with-its-searches, never a verdict.
- **R5 timing** (soft tiebreaker): ONE dated real signal (Exame/Startupi/TechCrunch funding/launch; a foreign launch date; a BR regulation/Pix change; a Reclame Aqui complaint trend). FORBID "tendência subindo / +5000%" without a captured URL — Google Trends is not reliably accessible zero-config.
- **R6 brecha + já-foi-comido:** map BR players' capability coverage (uncovered combo = the wedge). Verify the capability isn't now a free native feature of a major platform/model (e.g. Meta Ads Manager auto-reports). If it is → pivot to the still-manual adjacent layer (client comms, white-label, vertical PT-BR data, human-in-the-loop) or drop. Apply the "next model update" defensibility test.

## Fetch-integrity gate (mandatory)
DISCARD (never summarize) any fetched page containing: "Just a moment", `cf-challenge`, "Enable
JavaScript", a login form, or fewer than 3 numeric R$ values. The candidate → DADOS INSUFICIENTES
with the failed source under "verificar manualmente". Blocked ≠ no demand.

## Kill rule (guard against false negatives)
A candidate dies ONLY if searches SUCCEEDED and returned empty. Blocked/empty fetches → DADOS
INSUFICIENTES, never the kill pile. Track "searches attempted vs. searches that returned usable
data" and reason over it before killing. Stop at 3-6 cards clearing the bar, or at budget.

## Degraded mode (WebSearch down/empty/geo-blocked)
Detect zero/garbage/tool-error → retry reformulated/English queries → if still down, SAY in PT-BR
(*"a busca na web não retornou nada confiável agora — pode ser limite do plano ou
indisponibilidade"*), offer retry OR deliver clearly-labeled "hipóteses pra validar" WITH the manual
searches. NEVER present training-data guesses as live evidence.

## Persistence / re-run
Output path `.claude/varreduras/AAAA-MM-DD-<slug>.md`. On invocation, glob prior reports for the
same area, Read them, and surface "o que mudou" + only new/unrepeated opportunities.
