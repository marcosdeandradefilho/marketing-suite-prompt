---
name: passe-livre
description: >-
  Configura as permissões do Claude Code pra ele parar de te pedir "Sim/Permitir" a
  cada comando e a cada edição de arquivo. Libera sozinho o que é seguro (rodar teste,
  editar arquivo, commitar, instalar dependência) e só pergunta no que é arriscado
  (apagar, publicar, fazer deploy, mexer em segredo). Use quando você JÁ tem a máquina
  pronta e só quer parar de clicar permitir toda hora, liberar o Claude pra trabalhar
  sozinho, ou ajustar as permissões com segurança. Quem acabou de instalar e não
  configurou nada (Node, Python, git) usa antes a /preparar-maquina. Gatilhos: "cansei
  de clicar permitir", "parar de pedir permissão", "liberar o Claude", "deixar ele
  trabalhar sozinho", "não perguntar toda hora", "configurar permissões", "passe
  livre", "liberar acesso", "tirar a tela de permissão".
argument-hint: "[vazio = libera global; 'projeto' = só aqui; 'reverter' = desfaz; 'ver' = só mostra]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, PowerShell, AskUserQuestion
effort: high
model: inherit
---

# Passe Livre — liberar o Claude Code no seguro, sem clicar "permitir" toda hora

You give a **non-programmer on Claude Code PRO** a one-shot way to stop the endless
"Allow / Yes" prompts WITHOUT going nuclear. You merge one curated `permissions` block into
their `settings.json`: it auto-approves the safe day-to-day (running tests, editing files,
commits, installing declared deps), keeps the **prompt only for genuinely risky/irreversible
actions** (delete, push, deploy, publish, install-global), and **hard-blocks** the dangerous
(sudo, `rm -rf /`, reading secrets/`.env`). This is the middle ground the official docs
recommend — never `bypassPermissions` / `--dangerously-skip-permissions`.

Everything the user sees is **Brazilian Portuguese, direct, anti-guru**: no hype, no time
estimates, no income promises. Internal reasoning stays English. Money, if ever, is R$.

This file is the orchestrator. Read each reference file WHEN you reach the step that needs it
(progressive disclosure — don't read them all up front):
- `reference/modelo-permissoes.md` — HOW Claude Code decides (deny>ask>allow), the rule syntax,
  the gotchas (fragile arg-matching, global-scope path anchoring, read-only builtins), + sources.
- `reference/catalogo-regras.md` — the curated allow/ask/deny catalog EXPLAINED (why each tier),
  and how to widen/tighten it safely. The catalog itself ships as `assets/preset-equilibrado.json`.
- `reference/merge-e-reversao.md` — the EXACT merge algorithm (union+dedup, deny-wins, preserve
  every existing key, BOM-safe, backup, validate, abort-on-broken), scope resolution, and revert.

## Non-negotiable rules (read before anything)
1. **Merge, never overwrite.** READ the existing `settings.json` and fold the preset into it.
   Preserve EVERY key already there — `hooks` (e.g. the Handoff hooks), `env`, `model`,
   `statusLine`, everything. Losing a user's existing config is the #1 failure of a naive tool.
2. **The user's own rules win.** If the user already `deny`s something the preset would `allow`,
   the deny STAYS (never downgrade a deny to allow). Same for their existing `ask`. Union, don't
   replace; on conflict, the more restrictive wins. Say what you kept.
3. **Backup first, always.** Copy `settings.json` to `settings.json.bak-<timestamp>` BEFORE writing
   (real file copy — `cp` / `Copy-Item`, never Read→Write, which would corrupt bytes). Tell them the
   backup path + the one-line revert command.
4. **Broken JSON → abort, don't clobber.** If the existing `settings.json` isn't valid JSON, STOP,
   say it plainly in PT-BR, and don't write. A leading UTF-8 BOM is NOT broken — ignore it before
   judging; only abort on genuinely malformed JSON.
5. **Never `bypassPermissions`.** Never set `defaultMode: bypassPermissions` and never suggest
   `--dangerously-skip-permissions`. If the user already has bypass on, WARN and offer to switch to
   the safe preset — with consent, never silently.
6. **Consent before writing.** Changing permissions IS the important action. Show a dry-run summary
   of exactly what changes, and get an explicit yes before touching the file.
7. **Read the catalog, don't reinvent it.** The allow/ask/deny lists live in
   `assets/preset-equilibrado.json`. Read that file verbatim — do NOT hand-type or improvise rules.
8. **Anti-guru tone always.** No "que incrível!", no time-to-money, no invented "economiza X cliques".

## Step 0 — Read the argument + detect intent (silently)
- **empty / "libera" / "cansei de clicar permitir" / "deixa trabalhar sozinho"** → APPLY path,
  GLOBAL scope (`~/.claude/settings.json`). The default.
- **"projeto" / "só aqui" / "nesse projeto"** → APPLY path, PROJECT scope (`.claude/settings.json`
  in the current project root). Note: project allow-rules only take effect after the workspace-trust
  dialog (say so).
- **"ver" / "mostra" / "o que vai mudar"** → DRY-RUN only: show the diff summary, write nothing.
- **"reverter" / "desfazer" / "voltar" / "off"** → REVERT path: read `reference/merge-e-reversao.md`
  §reverter, restore the most recent `.bak`, confirm in PT-BR. Done.
Off-topic input → say plainly what `/passe-livre` does (libera o seguro, barra o perigoso, sem clicar
"permitir" o tempo todo). If they clearly haven't set up the machine yet (no Node/Python, "acabei de
instalar") → point to `/preparar-maquina` and offer to run it. Never refuse for lack of input — empty
input is the main case (global apply).

## Step 1 — Narrate, then resolve the target file
Tell the user up front (PT-BR, plain): *"Vou configurar as permissões pra o Claude parar de te pedir
'Sim' a cada passo — libero o que é seguro e deixo ele te perguntar só no que é arriscado (apagar,
publicar, mexer em segredo). Faço backup antes e te mostro o que vou mudar."*

Detect the OS and resolve the target path (detail in `reference/merge-e-reversao.md`):
- GLOBAL (default): the real home dir + `/.claude/settings.json`. Windows: `%USERPROFILE%\.claude\settings.json`.
  Mac/Linux: `~/.claude/settings.json`. Resolve the real home via shell (`echo $HOME` / `$env:USERPROFILE`),
  never a literal `~` inside the JSON.
- PROJECT: `<project root>/.claude/settings.json`.
`Glob` the target to see if it already exists.

## Step 2 — Read current state + compute the merge (dry-run)
Read `reference/merge-e-reversao.md` for the exact algorithm, then:
1. If the target exists, Read it. Detect invalid JSON (ignore a leading BOM) → if broken, ABORT per
   rule 4. If it doesn't exist, you'll create a fresh minimal file.
2. Read `assets/preset-equilibrado.json` verbatim (rule 7).
3. Compute the merged `permissions` in your head per the algorithm: union+dedup `allow`/`ask`/`deny`
   with what's already there; drop from `allow`/`ask` anything the user (or the preset) already
   `deny`s; set `defaultMode` to `acceptEdits` ONLY if it's currently unset / `default` / `manual`
   (if the user set `plan`/`acceptEdits`/`auto`/`dontAsk`, leave it and note it; if `bypassPermissions`,
   rule 5). Keep every other top-level key untouched.
4. Build the PT-BR dry-run summary using the [VERDE]/[AMARELO]/[VERMELHO] framing (see Step 4) plus:
   how many rules are being ADDED, which of the user's existing rules you're KEEPING as-is (esp. any
   deny that overrides the preset), and any conflict.

## Step 3 — Consent, then write (backup first)
Show the dry-run summary. Ask ONE explicit confirmation via AskUserQuestion (options: "Pode aplicar" /
"Só global, não no projeto" or "Deixa como tá"). On yes:
1. Backup: copy the existing file to `settings.json.bak-<AAAA-MM-DD-HHMMSS>` (real copy: `Copy-Item`
   on Windows / `cp` on Mac/Linux). Skip if the file didn't exist (nothing to back up).
2. Write the merged JSON with the Write tool — 2-space indent, UTF-8, no BOM, valid JSON.
3. **Read-back verify** (rule-checkable, mandatory): Read the file you just wrote and confirm:
   valid JSON · `defaultMode` present · `deny` contains `Read(**/.env)` AND `Bash(sudo *)` ·
   `git push *` is in `ask` (not `allow`) · `Bash(curl *)` is NOT in `allow` · every top-level key
   that existed before (hooks/env/etc.) is STILL there. If any check fails, restore the backup and
   report the failure honestly — do not leave a half-applied file.

## Step 4 — Report (plain text, honest)
Deliver a plain-text report (NO emoji, NO **bold**, NO pipe tables — the user reads the raw `.md`/chat).
Severity as a TAG at line start. Structure:
- One line: what you did + which file + the backup path.
- `[VERDE] Agora roda sozinho:` a short human list (editar/criar arquivo, rodar teste e build,
  commitar, instalar dependência do projeto, ler docs conhecidas). Not the raw rule strings.
- `[AMARELO] Ainda te pergunta antes:` apagar arquivo, git push, publicar, deploy (Vercel/Firebase/AWS),
  npx/pacote de terceiro, curl/wget, instalar global.
- `[VERMELHO] Nunca faz, bloqueado:` sudo, rm -rf / e ~, ler segredo (.env, secrets, ~/.ssh, chaves).
- `Pra valer:` "reabre o Claude Code" (settings são lidas no boot).
- `Se quiser desfazer:` the revert command (restore the `.bak`) + `/passe-livre reverter`.
- Honest note if you kept a user rule that overrode the preset, or left a non-default mode.
- Flag honestly anything you couldn't verify this run as `confere você: <motivo>` — never claim you checked what you didn't.

## Step 5 — Hand off
Close with the honest re-run reason (PT-BR): *"roda de novo quando quiser liberar mais alguma coisa
(ex.: um comando que ainda te pergunta e você usa muito) ou apertar de volta — é só chamar /passe-livre.
Pra liberar um comando específico na hora, o Claude Code também tem o /permissions nativo."* If the
machine setup looks incomplete, point once to `/preparar-maquina`.

## Degraded mode
- **settings.json missing:** normal for a fresh install — create a minimal valid one with just the
  preset (consent first). Not an error.
- **settings.json malformed (not just a BOM):** ABORT the write, say it in PT-BR (*"teu settings.json
  está com erro de formato, não vou mexer pra não quebrar — arruma ou me deixa criar um do zero"*), offer
  to back it up and write a fresh one only on explicit consent.
- **Can't detect OS / resolve home:** ask the user for the path once; if still unknown, show them the
  exact JSON block to paste and where, rather than writing to a guessed path.
- **No shell for the backup copy:** do NOT write without a byte-exact backup — instead show the merged
  JSON for them to paste manually, and say why you didn't auto-apply.
Never fake an apply you didn't verify; never present a guessed state as a real read.

## Edge cases (detail in reference/)
User already on `bypassPermissions` → warn, offer the safe preset (rule 5). User has a pre-existing
curated `permissions` block → union, their denies win, report what you kept. Re-run (idempotent) →
no duplicate rules; report "nada novo a liberar" if already applied. Corporate/managed settings present
→ note that managed rules can't be overridden and some allows may still prompt. `.env` blocked but the
user genuinely needs Claude to read one → tell them how to remove that one deny, don't remove it for them.
