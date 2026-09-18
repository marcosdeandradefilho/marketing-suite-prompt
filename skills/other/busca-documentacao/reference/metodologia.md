# metodologia.md — the loop, budget, gates, degraded mode

The skill researches GLOBAL tooling (GitHub, docs, changelogs are English-first), but the OUTPUT is
Brazilian Portuguese. Do NOT force `site:.com.br` — that throws away the real prior art. Search in
English for the tool layer; write the report in PT-BR for the reader.

## The input gate (Step 0)
1. Derive the **niche** from `$ARGUMENTS` + chat: a short noun phrase ("gerenciador de senhas",
   "app de notas", "emissor de nota fiscal", "CRM simples"). Translate to the English search term too
   ("password manager", "note-taking app", "invoicing", "CRM") — GitHub/topics are English-keyed.
2. Detect optional inputs:
   - **Manual tool list** ("já conheço o X e o Y"): seed those as the candidate set, validate each is
     real this session (one search/fetch each), then still run discovery to fill gaps + de-dupe.
   - **Angle** (UX / técnico / monetização): lead with + expand that section; shrink the others.
3. Empty/too-vague description → ask **exactly ONE** AskUserQuestion (header "Mira"): *"O que tu vai
   construir? Descreve em 1 frase — ou cola o nome de 1 ferramenta parecida que tu já conhece."* One
   question MAX, ever. If still useless ("sei lá"/"tanto faz"), do NOT guess a niche — say plainly the
   skill needs um alvo e convida a rodar de novo com 1 frase. Never invent a niche to look busy.

## Research budget (assume PRO floor — you can't detect MAX from here)
- ≤ ~10-12 WebSearch and ≤ ~5 WebFetch of FULL PAGES (READMEs, doc/pricing pages) total per run.
- `api.github.com` JSON calls (search/repos/issues/trees) are CHEAP — tiny JSON, not a full page render.
  They don't count against the ~5 full-page-fetch budget; pace them for GitHub's rate limit (~10/min) but
  use them freely as the discovery backbone. (Live test jun/2026: ~18 API calls ran with no rate-limit.)
- Batch GitHub queries: combine 3-4 qualifiers into ONE repo search instead of many narrow ones.
- De-dupe the candidate set BEFORE fetching any README.
- Pre-screen WebSearch snippets before spending a WebFetch — only fetch a page that the snippet says
  is worth it.
- GitHub Search/Topics API is unauthenticated and rate-limited (~10 req/min, ~60/hr observed; exact
  current limit not re-confirmed this run — pace it). On 403/422 from GitHub, suggest the user set an
  OPTIONAL `GITHUB_TOKEN`, but NEVER require it — zero-config is the rule.
- If the budget runs out, ship fewer-but-stronger cards (minimum 1 real one) + the honesty bucket.

## The loop
- **R1 Descobrir** → `reference/descoberta-fontes.md`. Build a comparable set of ~5-12 tools.
- **R2 Extrair** → `reference/extracao.md`. Features (normalized + counted), UX patterns, architecture.
- **R3 Armadilhas** → `reference/armadilhas-monetizacao.md` §gotchas. Real, linked pain only.
- **R4 Monetização** → `reference/armadilhas-monetizacao.md` §monetization. Model + price band.
Narrate between rounds in plain PT-BR, never expose tool names.

## The minimum-N rule (correctness guard for the % output)
- Track N = number of tools you actually READ a real source for this session.
- The headline output "features mais comuns (frequência %)" is only meaningful at N≥3.
- **If N < 3:** SUPPRESS the % table entirely. Emit per-tool observations instead + a banner:
  *"Nicho novo / pouca documentação aberta — achei só N ferramenta(s). Trate como hipótese, não como
  padrão de mercado."* Never present a % computed from 1-2 tools as a market frequency.
- At N≥3, every frequency claim MUST show its denominator and the canonical token counted
  (e.g. *"sync em 6/8 ferramentas"*) — auditable, not asserted. See `reference/extracao.md` §frequência.

## Recurrence / re-run de-dup (Step 0.5)
- On invocation, Glob `.claude/pesquisas/*.md`; match the niche by slug/filename.
- If a prior report exists, Read it. The new run produces a **"O que mudou desde a última pesquisa"**
  block at the top: **Adicionado** (new tools/features found), **Mudou** (renamed, repriced, new version),
  **Removido** (tool died/archived). Surface only deltas — don't reprint the whole report.
- Stamp the report with the run date and a "Fontes conferidas nesta rodada" list so the NEXT run can diff.
- This recurrence is the honest reason the skill earns a monthly Claude Code subscription: a niche's tools
  ship, reprice and die on their own cadence; a saved report goes stale in weeks.

## Degraded mode (make-or-break)
Detect: zero/garbage results, tool errors, repeated 403/Cloudflare, GitHub rate-limit, empty bodies.
1. Retry once with a reformulated or English query.
2. Still down → SAY it in PT-BR: *"A busca não retornou nada confiável agora — pode ser limite do plano
   ou bloqueio das fontes."*
3. Deliver clearly-labeled **"hipóteses pra você confirmar"** cards WITH the exact manual searches to run
   (the literal GitHub/Google queries), and suggest a `GITHUB_TOKEN` if GitHub was the blocker.
4. NEVER present training-data guesses as documentation you read. A hypothesis is labeled a hypothesis.
