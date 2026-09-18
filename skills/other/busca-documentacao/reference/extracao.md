# extracao.md — features, UX patterns, architecture (R2)

The deliverable a builder needs is not a feature checklist — it's the niche's **mental model**: what
workflow the tools optimize for, what's table-stakes vs differentiator, and which patterns are reusable.
A feature table alone is a spreadsheet, not analysis (Olushad). Extract the WHY: every shipped feature =
weeks of engineering someone bet on (customer demand, a lost deal, a churn driver) (trackmore.io).

## 1. Features → canonical tokens → frequency
Raw headings differ across tools for the SAME capability ("Features" vs "Everything you need" vs "Why X";
"real-time sync" vs "live sync" vs "cloud sync"). So:
1. Pull each tool's feature list (README heading skeleton, or `/docs` nav, or `/changelog`).
2. **Normalize** each raw feature into a canonical verb-noun token BEFORE counting. Collapse synonyms:
   `real-time sync` / `live sync` / `cloud sync` → `sync`. Keep a small synonym map per run.
3. Build a tools × canonical-feature matrix mentally (or in a scratch list): rows = tools, cols =
   canonical features, cell = 1/0.
4. **Frequency = column-count / N** (N = tools read). Tier the output:
   - **CORE** (≥70% present) = table-stakes a non-programmer MUST clone.
   - **COMUM** (40-70%) = differentiators worth considering.
   - **RARO** (<40%) = niche / skippable.

### §frequência — the auditable-% rule (correctness guard)
Every frequency claim shows its **denominator and the canonical token**: write *"sync — 6/8 ferramentas"*,
never a bare *"75% têm sync"*. If N<3, the % is suppressed entirely (see `reference/metodologia.md`
minimum-N rule) — emit per-tool observations instead.
> The synonym normalization is judgment-based and was NOT calibrated end-to-end on a real 8-10 tool set
> in the build research — so always SHOW the denominator and the token counted so the reader can audit
> the number, and never round a small-N count into a confident market %.

## 2. UX / onboarding / first-run patterns
Look for these recurring patterns and report them with the same frequency treatment as features:
- **Onboarding / time-to-first-value:** read the README "Quick Start" and `/docs` "Getting Started".
  Count steps to first value. A single `docker run` / one-binary path = the "one-command first run"
  pattern (memos and most OSS ship this).
- **First-run without signup:** a "Try the Live Demo" heading/link = the demo-without-signup pattern.
- **Pricing-page UX:** free self-host + paid cloud tier (memos, twenty, joplin); freemium gating on
  sync/collaboration/storage (Obsidian: editor free, Sync + Publish are paid add-ons).
Translate every UX observation into plain PT-BR for the reader — no jargon dumps.

## 3. Architecture concepts a non-programmer can ask Claude to mimic
By DEFAULT, get the reusable skeleton CHEAPLY from the README "Stack" heading + the install
instructions — no need to read source code for this. (Reading the actual code is the OPTIONAL deeper
path in §5 below / SKILL.md R5, only when the user opts to fork a specific repo.)
- **Single-binary / single `docker run`** (memos) → *"um programa só que você roda com um comando"*.
- **Local-first + optional sync** (joplin, obsidian) → *"os dados ficam num arquivo local, a sincronização
  é um extra"*.
- **Plugin / extension architecture** (obsidian community plugins) → *"um núcleo simples + plugins"*.
- **Web UI + REST API split** (twenty, memos) → *"uma tela web e uma API por trás"*.
Phrase each as a plain-language instruction the reader can paste into Claude Code, e.g.
*"faz um programa só que eu rodo com um comando e guarda tudo num arquivo local"*.

## 4. No-open-source fallback (edge case: niche is all closed SaaS)
When GitHub yields nothing (no repos), you CANNOT read the code or a "Stack" heading. Then:
- Pivot architecture extraction to **closed-source-readable surfaces**: public docs, API reference,
  integration/connector pages, status pages, and `/pricing` tier-gating (which features are locked
  reveals the capability map).
- **DOWNGRADE** the report's architecture section to *"padrões inferidos da doc pública (não do código)"*
  with an explicit confidence label.
- State plainly when a concept can't be verified rather than inventing it. A closed SaaS's internals are
  not knowable from outside — say so; don't fabricate an architecture.

## The depth test (did the extraction go deep enough?)
Before writing, you should be able to complete: *"o jeito que esse nicho resolve é ___, e o que quase
ninguém faz bem é ___"*. The second blank is the gap — the most valuable thing for the builder. If you
can't fill both from real sources, dig one more tool or say the evidence is thin.

## §licenças — license → plain permission (surface whenever a repo is a fork candidate)
A non-programmer who "absorbs a codebase and sells on top" can land in legal trouble. So for EVERY
open-source repo on the table as a possible base, get `license.spdx_id` from `https://api.github.com/repos/OWNER/REPO`
and translate it to plain permission (PT-BR, for the reader):
- **MIT / Apache-2.0 / BSD-2/3-Clause / MPL-2.0 / ISC / Unlicense** → "pode usar, modificar e VENDER em
  cima, num produto fechado. Só mantém o aviso de copyright/licença (Apache também pede listar as mudanças)."
- **LGPL** → "pode usar como biblioteca num produto fechado, mas se mexer NO código da própria lib, essa
  parte tem que ficar aberta. Caso de dúvida, conferir com cuidado."
- **GPL-2.0 / GPL-3.0** → "copyleft: se DISTRIBUIR um produto com esse código, tem que abrir o código do
  produto. Incompatível com produto fechado distribuído (instalável). Como SERVIÇO web puro, a GPL não
  dispara — mas é arriscado pra leigo, evita."
- **AGPL-3.0** → "copyleft FORTE: pega até quando você só roda como serviço web (SaaS). Te obriga a abrir
  TODO o seu código pros usuários. Pra vender ferramenta fechada, NÃO absorva código AGPL — só inspiração."
- **Sem licença / `NOASSERTION` / `null`** → "todos os direitos reservados por padrão. Pode LER e se
  inspirar, mas copiar o código pro seu produto é juridicamente cinzento. Reescreva você mesmo, ou peça
  ao autor pra adicionar uma licença." NEVER read `null` as "pode usar"; never guess the permission.
- **Dual-license / 'commercial license available'** → "tem versão paga pra uso comercial fechado — uma
  opção, mas custa; veja o preço com o autor."
Always cite where the license came from (the GitHub API repo endpoint). If the API returns `NOASSERTION`
(license file exists but isn't a standard SPDX), say "licença não padrão — abra o arquivo LICENSE pra
confirmar" instead of asserting a permission.

## §5 — optional code dive (SKILL.md R5, only on opt-in)
Run ONLY when the path recommendation is "partir de um repo" AND the user accepted the Step 4 offer. Then:
1. Confirm the license (§licenças) FIRST — if it forbids a closed product and the user wants to sell one,
   say so up front and stop, or pivot to "reference only".
2. Fetch the file tree: `https://api.github.com/repos/OWNER/REPO/git/trees/HEAD?recursive=1` — get the
   shape (how many files, the main folders, the entry point).
3. Read 1-2 CORE files (the entry point + the file that does the main job) via raw.githubusercontent.com.
4. Report in plain PT-BR what the code actually does, whether it really matches the idea, and whether it's
   small/readable enough for a non-programmer to modify with Claude Code (or a giant codebase that's risky
   to fork). Honest verdict: "dá pra partir dele" vs "é grande/complicado demais, melhor só de referência".
Keep it to the PRO budget — 1 tree call + 1-2 file fetches per repo, not a full audit.
