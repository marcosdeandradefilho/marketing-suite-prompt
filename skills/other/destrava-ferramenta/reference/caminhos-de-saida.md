# caminhos-de-saida.md — how to structure the report (triage UX)

Triage is a **decision forum, not a deep technical dive** — keep the report scannable for a
non-programmer. The deep fix steps live BEHIND the chosen path, not dumped in the report
(plane.so/blog/bug-triage-process-how-to-run-it-and-what-to-prioritize). Write it in PT-BR, plain,
anti-guru.

## The 5-part structure

### 1. READ-BACK (one soft line)
Restate what they're stuck on + the emotional read, so they feel heard before any diagnosis:
> *"Beleza — tu travou no [X], tá [frustrado/confuso] e já tentou [Y]. Deixa eu te mostrar o que
> tá acontecendo e os caminhos."*
No label-dump ("detectei que você é tipo C"). Just show you understood.

### 2. DIAGNÓSTICO EM 3 CAMADAS (priority order)
In "stop the bleeding → restore → root cause" order (sre.google/sre-book/managing-incidents):
- **Camada 1 — o que está sangrando agora** (the literal symptom/error).
- **Camada 2 — por que continua travando** (the architectural decision behind it).
- **Camada 3 — a causa de fundo** (scope/context).
It's OK to state impact ("é isso que te trava") before the exact cause is nailed
(emmer.dev/blog/an-effective-incident-runbook-template) — never stall for certainty.

### 3. 2-3 CAMINHOS DE SAÍDA (the core)
Present only genuinely distinct (non-dominated) options — **never 1** (no choice) and **never 6**
(overwhelm). Each path is a mini-runbook (emmer.dev/...): 1-3 "pages" max; if it balloons, it's two
paths — split it. Each path has:
- **Um nome** = the failure mode it addresses (*"Caminho A — volta pro último estado que rodava"*).
- **Passos curtos e ordenados** (the actual moves).
- **Um trade-off de uma linha, A FAVOR e CONTRA** so they can actually choose — option awareness
  (arxiv.org/pdf/2302.12389): *"mais rápido, mas você perde o que fez desde ontem"* /
  *"mais seguro, mas mais lento"* / *"resolve a raiz, mas é o maior dos três."*
- **Um critério de aceite como RESULTADO observável**, ideally Given/When/Then, plain enough for a
  non-programmer to verify the same way an engineer would
  (atlassian.com/work-management/project-management/acceptance-criteria):
  *"Quando você recarregar, o erro some e seus dados aparecem."* NOT a recipe — a checkable result.
- **Um gatilho de desistência (bail trigger):** *"se você já tentou esse caminho com foco e mesmo
  assim não saiu, troca pro Caminho B ou pede ajuda"* — based on the SRE escalation heuristic (an
  event becomes an incident once it resists focused effort — sre.google/sre-book/managing-incidents).
  **Phrase it by EFFORT/condition, NEVER a clock time** ("depois de focar e não sair", not "depois
  de 1 hora") — anti-guru forbids time estimates.

**Path TYPES to choose from** (pick the 2-3 that fit the trava): voltar pro último estado que rodava ·
refatorar o módulo quebrado · fatiar/walking-skeleton · enxugar o que a IA inflou (see
`recuperacao-de-escopo.md`) · the layer-1 debugging move (`playbook-debugging.md`) · and — when the
trava is a WRONG or MANUAL approach — the **CAMINHO DE PESQUISA** (SKILL rule 8): parar de fazer na mão,
usar a forma padrão / uma biblioteca pronta / ver como o open-source resolve, backed by a real search
you ran this session + a "cola isso no Google/Claude" anchor. For a deep prior-art sweep, point them to
`/busca-documentacao`. Don't force the research path on a one-off typo; reach for it when the approach
itself is the problem.

### 4. PRIMEIRO MOVIMENTO RECOMENDADO
Lead with ONE clearly-marked recommended path + a one-line reason.
**Ranking rule:** blocker-first (priority, not severity); tiebreaker = **cheapest-and-most-
reversible-first** — the smallest, most-undoable action, so a non-programmer can try it without
fear of making things worse.

### 5. "TÁ RESOLVIDO DE VERDADE QUANDO..." (overall definition of done)
One line, distinct from each path's acceptance, so they can tell "this path worked" from "the whole
thing is fixed" (atlassian.com/...). Then offer to save the retomada plan and log the trava
(`historico-de-travas.md`), and a calm re-run nudge.

## Tone checks on the written report
- PT-BR end to end; instructions/your reasoning can be English, but everything the USER reads is
  PT-BR.
- No time estimate ("em 10 min você resolve"), no income/"vira dev" promise, no hype.
- R$ only; foreign price as `US$`; never a bare `$`.
- Errors framed as data, process praised over ability (`ler-o-emocional.md`).

## Mini-shape (skeleton, not numbers to copy) — PLAIN TEXT, no emoji/bold/table
The saved retomada plan is read RAW in an editor. So NO emoji, NO `**bold**`, NO pipe tables. Plain
uppercase labels + simple lists only. Skeleton:
```
O QUE ROLOU
[read-back de 1 linha]

DIAGNOSTICO (da mais urgente pra mais de fundo)
Camada 1 (agora): ...
Camada 2 (por que volta): ...
Camada 3 (fundo): ...

O QUE ESSA FERRAMENTA TINHA QUE FAZER
[1-2 linhas: o objetivo da ferramenta, pra mirar no objetivo e não só no sintoma]

CAMINHOS
Caminho A (recomendado): [nome]
   passos: 1) ... 2) ...
   a favor: ...
   contra: ...
   ta ok quando: [resultado observavel]
   se focar e mesmo assim nao sair: vai pro Caminho B
Caminho B: [nome]
   ...
Caminho C (opcional): [nome]
   ...

COMECA POR: Caminho A. [motivo de 1 linha]
TA RESOLVIDO DE VERDADE QUANDO: [resultado geral observavel]
```
