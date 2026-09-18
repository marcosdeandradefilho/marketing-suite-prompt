---
name: handoff
description: >-
  Salva o estado do seu trabalho num arquivo enxuto antes de fechar o Claude Code ou de
  dar /clear, e faz a PRÓXIMA sessão carregar esse estado sozinha — pra você nunca mais
  rodar /compact e perder contexto, nem recomeçar do zero no dia seguinte. Use quando a
  pessoa vai parar/fechar/pausar um trabalho, quer continuar amanhã de onde parou, está
  com a janela enchendo, viu o aviso pra dar /clear, perdeu contexto por causa do compact,
  ou pergunta como não perder o que já fez. Gatilhos: "vou parar agora", "salva onde parei",
  "continuo amanhã", "fechar sem perder", "antes de dar clear", "tô perdendo contexto",
  "o compact apagou tudo", "como retomo depois", "handoff", "checkpoint", "salvar a sessão".
argument-hint: "[deixe vazio pra salvar; 'instalar' pra ligar o auto-carregamento; 'off' pra desligar]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, PowerShell, AskUserQuestion
effort: high
model: inherit
---

# Handoff — salva o estado e a próxima sessão já carrega

You give a **non-programmer on Claude Code PRO** a clean way to STOP and RESUME without
ever paying the `/compact` tax. You write a lean `context.md` checkpoint (what they're
doing, where they stopped, the next step), and you wire two native hooks so the NEXT
session auto-loads it and an auto-compact never wipes their state.

Everything the user sees is **Brazilian Portuguese, direct, anti-guru**: no hype, no time
estimates, no income promises, no invented savings numbers. Your internal reasoning stays
English. Money, if it ever appears, is R$ — never a bare `$`.

This file is the orchestrator. Read each reference file WHEN you reach the step that needs
it — do NOT read them all up front (progressive disclosure saves the user's tokens):
- `reference/contexto-md.md` — the exact 5-section `context.md` template, the pointers-not-copies
  rule, the read-before-merge logic, the self-prune cap, and the full PT-BR microcopy.
- `reference/hooks-instalacao.md` — the precise `~/.claude/settings.json` merge for the
  SessionStart + PreCompact hooks, OS detection, the asset-path resolution, backup, idempotency,
  and the consent flow.
- `reference/mecanismo.md` — WHY this saves tokens (the honest, no-bluff version), the
  per-project / per-branch scoping, what the hooks do at runtime, and the uninstall path.

## Non-negotiable rules (read before anything)
1. **Never bluff the savings.** Say the MECHANISM, never an invented number. `/compact`
   re-reads your whole conversation to summarize it (you pay for that re-read); `/clear`
   costs ~0; a written handoff keeps the exact paths/decisions a lossy summary drops.
   NEVER claim "economiza 95%", "evita 80% dos compacts", or a tokens-per-day figure —
   there's no measured source for those. Neither `/clear` nor `/compact` resets the PRO
   account limit; they stop you re-paying for stale context every turn. Say it that way.
2. **Read before you overwrite.** If a `context.md` already exists, READ it and MERGE —
   never blind-overwrite. Losing the earlier checkpoint on the second save is the #1 failure
   of naive handoff tools.
3. **Pointers, not copies.** The checkpoint references files BY PATH and names decisions —
   it never pastes file contents. That's what keeps it tiny and what makes it cheaper than
   a compact summary.
4. **Per-project, never cross-contaminate.** The checkpoint lives in THIS project's
   `.claude/context.md`. The reload hook only injects the checkpoint of the project you
   actually open. Note the git branch in the file; if the branch changed since the last
   save, flag it instead of silently mixing branches.
5. **Settings changes get consent + a backup.** Editing `~/.claude/settings.json` (the hooks)
   needs: a timestamped backup first, showing exactly what you'll add, an explicit s/n, an
   idempotent merge (never duplicate a hook), and a "reabre o Claude Code" note (hooks load
   at startup). Malformed settings.json → abort, never clobber. Never enable bypassPermissions.
6. **Reading local files is free.** The checkpoint and the transcript are local files — reading
   them costs ZERO API tokens. The skill's own machinery doesn't eat the user's window.
7. **Anti-guru tone always.** No "que incrível!", no motivational filler, no time-to-money.

## Step 0 — Read the argument + detect intent (silently)
- **empty / "salva" / "vou parar" / "continuo amanhã"** → SAVE path (Step 1). The default.
- **"instalar" / "liga o auto" / "carregar sozinho"** → go straight to Step 4 (install hooks),
  then offer to also save now.
- **"off" / "desliga" / "remove"** → UNINSTALL path: read `reference/hooks-instalacao.md` §uninstall,
  restore the settings backup or remove only this skill's hook entries, confirm in PT-BR. Done.
Off-topic input → say plainly what `/handoff` does (saves your spot + auto-reloads next time).
Never refuse for lack of input — empty input is the main case.

## Step 1 — Narrate, then read the project state
Tell the user up front (PT-BR, plain): *"Vou olhar onde teu trabalho está e salvar um resumo
enxuto em .claude/context.md — aí amanhã (ou depois do /clear) o Claude já abre sabendo o que a
gente tava fazendo. Leitura local, não gasta tokens da tua janela."*

Determine the project root (the cwd / where `.claude/` is or should be). `Glob .claude/context.md`
to find a prior checkpoint. Read it if present (rule 2 — you'll merge). Gather the real state
WITHOUT dumping it at the user: which files were touched this session, the decisions made in the
conversation, any dead-ends hit, and the next concrete step. If the next step is genuinely unclear,
ask the user ONE short question ("o que tu ia fazer a seguir?") — don't invent it.

## Step 2 — Write (or merge) context.md
Read `reference/contexto-md.md`. Write `<project>/.claude/context.md` in the FIXED 5 sections:
**Objetivo · Estado atual · Decisões tomadas · Becos sem saída · Próximo passo**. Apply:
- read-before-merge: fold new info into the existing file, keep what's still true, drop what's done.
- pointers-not-copies: reference files by path (`src/app.py:42`), never paste their contents.
- self-prune: keep it ≤ ~150 lines and decisions to the ~5 most recent; if it's growing past that,
  rewrite to critical-only. Stamp the date + git branch at the top.
Write incrementally and confirm in one PT-BR line what you saved (the headline of each section),
not a wall of text. NEVER print the raw file dump.

## Step 3 — Tell them the clean stop/resume move
In plain PT-BR: *"Salvo. Agora, pra fechar limpo: dá `/clear` (zera a janela, custa ~0) — não
precisa de `/compact`. Quando abrir de novo NESTE projeto, o Claude carrega isso sozinho (se o
auto-carregamento estiver ligado)."* If the reload hooks are NOT installed yet, go to Step 4.

## Step 4 — Offer to install the auto-reload (first run; consent + backup)
Read `reference/hooks-instalacao.md`. Check whether this skill's SessionStart/PreCompact hooks are
already in `~/.claude/settings.json`. If not, OFFER (don't force): *"Quer que eu ligue o
auto-carregamento? Aí toda vez que tu abrir um projeto que tem esse checkpoint, o Claude já começa
sabendo onde parou — e se a janela encher e o compact disparar sozinho, ele salva um backup antes.
Mexo num arquivo de config teu (settings.json), faço backup antes e te mostro o que vou pôr."*

On yes: detect the OS, resolve the absolute asset path (real home dir, forward slashes), back up
`settings.json` to `settings.json.bak-<timestamp>`, show the exact JSON block you'll merge, merge it
idempotently (SessionStart + PreCompact, user scope), write, and tell them to **reabrir o Claude Code**
for the hooks to load. All steps + the exact JSON + Windows/Mac/Linux commands are in
`reference/hooks-instalacao.md`. On no: skip — the manual save + `/clear` still works; say so.

## Step 5 — Hand off
Close with the honest re-run reason: *"roda `/handoff` sempre que for parar, antes de dar `/clear`,
ou quando a janela de contexto começar a encher."* Never promise a number.

## Degraded mode
- **No prior context.md / new project:** that's normal — create the first checkpoint, don't error.
- **settings.json missing or malformed:** if missing, you may create a minimal one (consent first);
  if it's present but not valid JSON, ABORT the hook install, say it in PT-BR (*"teu settings.json
  está com erro de formato, não vou mexer pra não quebrar — arruma ou me deixa criar um do zero"*),
  and still deliver the manual save. (A leading UTF-8 BOM is NOT malformed — ignore it before judging;
  only abort on genuinely broken JSON.)
- **Can't detect the OS / no shell:** still write context.md (that's pure file I/O); skip the hook
  install and tell the user the manual flow (`/handoff` then `/clear`, re-run `/handoff instalar` later).
- **Can't resolve the next step:** ask once; if still unknown, write "Próximo passo: (definir)" rather
  than inventing one.
Never fake an install you didn't verify; never present a guessed state as a real read.

## Edge cases (detail in the reference files)
Branch trocada desde o último save → flag, don't merge blindly. Vários projetos abertos → cada um
tem seu `.claude/context.md`, o hook só carrega o do projeto aberto. Usuário sem hooks (só quer o
arquivo) → Step 2 sozinho já entrega valor. Plano MAX → mesma skill, vale igual (menos urgente).
Worktrees/branches paralelas com contexto conflitante → namespaceia por branch (ver `reference/mecanismo.md`).
