---
name: crm-leads
description: >-
  Transforma sua lista de leads num painel visual (kanban) que roda no seu computador: cada lead
  vira um card que você arrasta de Novos para Contatado, Proposta e Fechado, com dossiê completo,
  marcas (quente/frio/não perturbe), anotações e próxima ação. Os leads novos de cada prospecção
  entram sempre no MESMO painel, sem duplicar e sem apagar o que você já mexeu. Também importa
  planilha que você já tem e devolve um relatório do funil. Não faz a prospecção em si (isso é a
  /prospector) — ela ORGANIZA e ACOMPANHA os leads. Gatilhos: "abre o painel de leads", "meu CRM",
  "kanban de leads", "joga os leads no painel", "como tá meu funil", "quantos leads eu tenho",
  "importa minha planilha de leads", "acompanhar prospecção", "mover lead", "crm-leads".
argument-hint: "[abrir | importar <arquivo> | funil | vazio pra ele decidir]"
allowed-tools: Read, Write, Edit, Glob, Bash, AskUserQuestion
model: inherit
---

# CRM de leads (painel kanban local)

You turn a pile of leads into a **visual board the user actually works from**: a local kanban with a
per-lead dossiê, funnel stages, marks, notes and next action. Everything runs **on the user's own
machine** — no account, no cloud, no API key. Every word the user sees is **Brazilian Portuguese,
direct, anti-guru**: no hype, no time promises, no income promises.

**The spine of this skill: the board is CUMULATIVE and the user's work on it is SACRED.** New leads
from any prospecting round always land in the SAME board, in the **Novos** column, without duplicating
anyone and **without ever overwriting a card the user already moved, marked or annotated**. If you
ever have to choose between refreshing data and preserving what the user did, **preserve what the
user did** and report the difference.

Two files hold everything, and they never mix:
- `leads.json` — the FACTS about each lead (found by prospecting). Scripts may complete empty fields here.
- `estado.json` — the USER's work (column, marks, notes, next action). **Nothing but the panel writes here.**

This file is the orchestrator. Read a reference file only when you reach the step that needs it:
- `reference/instalacao-painel.md` — creating the folder, copying the assets, starting/stopping the panel, every failure mode. Read at Step 2 and whenever the panel misbehaves.
- `reference/modelo-dados.md` — the exact fields, the dedup key, the merge rules, what each script does. Read whenever you write leads into the board.
- `reference/operacao.md` — the funnel report, moving a lead by chat, importing an outside spreadsheet, cleaning up. Read at Step 4.

## Non-negotiable rules
1. **Never write to `estado.json` yourself.** Only the panel writes the user's work. If the user asks
   you to move a lead by chat, follow `reference/operacao.md` §mover — you edit it through the
   documented path and you say plainly that you touched it.
2. **Never overwrite a filled field with an empty one.** Merge only completes holes. `importar.mjs`
   already enforces this — do not hand-edit `leads.json` to "fix" a lead unless the user asked.
3. **Never duplicate a lead.** Dedup is CNPJ > telefone/WhatsApp > empresa+cidade, and a business is
   the same business if ANY of those match. Always import through `importar.mjs`, never by appending
   JSON by hand.
4. **Never invent a lead field.** This skill organizes what prospecting found. Empty stays empty; if
   something is missing, it goes in `pendencias` in plain words, never as a guessed phone or name.
5. **Zero-config, but honest about Node.** The panel needs Node (it comes with Claude Code on most
   installs). If Node is missing, say so in one line and fall back to the no-server mode — never
   pretend the state is being saved to the project when it is not.
6. **Anti-guru tone.** No time estimates, no "seu funil vai explodir". R$ for money. Reports the user
   reads in the editor are PLAIN TEXT: no emoji, no `**negrito**`, no `|` tables.
7. **LGPD stays visible.** The board holds contact data of real businesses. When the user marks
   "não perturbe", that lead is **out of every future prospecting round** — say it out loud once,
   when it first happens.
8. **Always close with the "Próximo movimento" block** — what the user can do now (abrir o painel,
   trazer mais leads com `/prospector`, montar a proposta de um QUENTE com `/gerar-proposta`). Never
   end the turn with only a question or only an error.

## Step 0 — Read the situation before doing anything
Glob for `.claude/leads/crm/leads.json` (the board) and `.claude/leads/*.csv` (old prospecting files).
Four possible situations — name the one you're in, in one line, and go:
- **Board exists + user wants to see it** → Step 3 (open it). Note: `/prospector` sets the board up
  and drops its leads in on its own, so it's normal to find it already populated — never rebuild it.
- **Board exists + new leads arriving** → Step 3 of the caller: import, then report what changed.
- **No board, but there ARE old CSVs** → Step 1, and offer to bring the old lists in.
- **Nothing at all** → Step 1 with an empty board, and point at `/prospector` to fill it.

## Step 1 — Confirm the scope in one short turn (only if it's genuinely unclear)
If the user's message already says what they want ("abre o painel", "joga esses leads lá"), **ask
nothing**. Otherwise use ONE `AskUserQuestion` with at most 2 questions: (a) start from zero or bring
in the CSVs you found (list them by name); (b) nothing else unless it changes what you'd do.
Fallback with no `AskUserQuestion`: same questions in one plain PT-BR paragraph.

## Step 2 — Install the board in the project (once)
Per `reference/instalacao-painel.md`:
1. Create `.claude/leads/crm/`.
2. Copy the 5 assets from this skill's `assets/` folder into it: `painel.html`, `servidor.mjs`,
   `importar.mjs`, `abrir-painel.bat`, `abrir-painel.command`. Resolve the skill folder by trying, in
   order, `~/.claude/skills/crm-leads/assets/`, then `.claude/skills/crm-leads/assets/` — never
   re-type the files from memory, always COPY them.
3. Create `leads.json` as `{"versao":1,"leads":[]}` if it doesn't exist. Do NOT create `estado.json` —
   the panel creates it on the first change.
4. If there were old CSVs, import each one (`node importar.mjs <caminho.csv>`) and report the totals.

## Step 3 — Bring leads in, then open the board
**Bringing leads in** (this is what `/prospector` hands over to):
1. Write the new leads to `.claude/leads/crm/entrada-<lote>.json` using the schema in
   `reference/modelo-dados.md` (`lote` = `<nicho>-<regiao>`, `nota_calor` a NUMBER, `tier` the word).
2. Run `node importar.mjs entrada-<lote>.json` from inside `.claude/leads/crm/`.
3. Report the script's real numbers in plain PT-BR: how many entered, how many were already there,
   how many holes got filled. **Never inflate the count.**

**Opening the board:** run the panel in the background per `reference/instalacao-painel.md` §abrir and
give the user the address (`http://127.0.0.1:7788/`). Tell them in one line that the janela do terminal
has to stay open, and that everything they do in the board is saved into the project.

## Step 4 — Answer questions about the funnel without opening anything
Per `reference/operacao.md`: read `leads.json` + `estado.json` and answer in **plain text** — how many
per stage, which QUENTES are still untouched, who has a next action set, who's marked não perturbe.
This is what makes the board useful from the chat too. No emoji, no table pipes.

## Step 5 — Close the loop with prospecting
Before a new prospecting round, `node importar.mjs --skip` prints who is already in the board (with
stage and marks). Hand that list to `/prospector` so it doesn't bring back someone the user already
contacted, discarded, or marked não perturbe. Say this out loud the first time — it's the reason the
board and the prospecting are worth having together.

## Modo degradado (say it, never fake it)
- **No Node** → the board still opens with two clicks on `painel.html`, reading `dados.js`; the user's
  work then lives only in that browser and Firefox won't keep it at all. Say this in plain words and
  offer the Node path.
- **Port busy** → the server walks to the next port on its own; just report the address it printed.
- **User cleared browser data in no-server mode** → the work is gone; the leads themselves are not
  (they're in `leads.json`). Say exactly that, without dressing it up.
