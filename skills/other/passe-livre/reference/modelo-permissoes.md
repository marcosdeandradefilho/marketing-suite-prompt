# modelo-permissoes.md — how Claude Code decides (the model you're configuring)

Everything here is confirmed against the OFFICIAL Claude Code docs (consulted 2026-07):
- https://code.claude.com/docs/en/permissions
- https://code.claude.com/docs/en/settings
- https://code.claude.com/docs/en/permission-modes

Read this so your dry-run explanation and your merge are correct. Don't parrot it at the user — it's
your model; the user gets the plain-text [VERDE]/[AMARELO]/[VERMELHO] summary.

## The three lists + evaluation order
`permissions` holds `allow`, `ask`, `deny` (and `defaultMode`, `additionalDirectories`).
- `allow` → runs with no prompt.
- `ask` → always prompts, even if an allow rule also matches.
- `deny` → blocked, never even attempted.

Evaluation order is **deny → ask → allow**. The FIRST match in that order wins; rule specificity does
NOT change the order. So a `deny` beats any `allow` (even a narrower one), and an `ask` beats an
`allow`. This holds ACROSS scopes too: a deny in user settings blocks an allow in project settings and
vice-versa. **This is why the user's own deny must always win over our allow** (SKILL rule 2).

A bare tool name in `deny` (e.g. `"Bash"`) removes the tool from Claude's context entirely. A scoped
deny (e.g. `"Bash(rm *)"`) leaves the tool but blocks matching calls. We only ever use scoped rules.

## What is already free (no rule needed)
- Read-only tools never prompt: **Read, Grep, Glob, WebSearch**.
- A built-in set of read-only Bash commands never prompt in any mode: `ls, cat, echo, pwd, head, tail,
  grep, find, wc, which, diff, stat, du, cd`, and read-only `git` (status, diff, log). Not configurable.
So the prompts the user actually hits are: **non-read-only Bash/PowerShell commands** and **file
edits/writes**. That's exactly what the preset targets.

## defaultMode (the modes)
Set in `permissions.defaultMode`:
- `default` (aka `manual`) — prompts on first use of each tool. The stock behavior.
- `acceptEdits` — auto-approves file edits/creates + common filesystem commands (`mkdir, touch, mv, cp`)
  in the working dir / additionalDirectories. **Does NOT auto-approve `rm`** — delete still prompts,
  which is what we want. This is the preset's mode: it kills the edit-file prompts.
- `plan` — read-only exploration, no edits.
- `auto` — research preview, auto-approves with a background safety classifier; gated by tier, not
  always available. We don't rely on it.
- `dontAsk` — auto-denies anything not explicitly allowed.
- `bypassPermissions` — skips ALL prompts (the `--dangerously-skip-permissions` mode). NEVER set this.
  Even it still circuit-breaks `rm -rf /` and `rm -rf ~`.

acceptEdits still PROMPTS for writes to protected paths (`.git`, `.claude`, `.vscode`, `.idea`, etc.),
so the skill applying `~/.claude/settings.json` itself may prompt once — that's fine and correct
(changing permissions is the one important action worth a prompt).

## Rule syntax you must get right
- **Bash / PowerShell:** `Bash(npm run *)`. `*` matches any run of chars incl. spaces, at any position.
  A space before `*` enforces a word boundary: `Bash(ls *)` matches `ls -la` but NOT `lsof`; `Bash(ls*)`
  matches both. `:*` at the end == ` *`. PowerShell uses the same shape; aliases are canonicalized
  (`Get-ChildItem` also matches `gci`, `ls`, `dir`); matching is case-insensitive.
- **Compound commands are split.** Claude Code parses shell operators (`&&`, `||`, `;`, `|`, `|&`, `&`,
  newline) and requires EACH subcommand to match. So `Bash(git *)` does NOT green-light
  `git status && rm -rf x` — the `rm` half is judged on its own (and hits our `ask`/deny). This is a
  safety feature, not a bug.
- **Wrappers stripped before matching:** `timeout, time, nice, nohup, stdbuf`, and bare `xargs`. But
  `npx`, `docker exec`, `devbox run`, `mise exec` are NOT stripped — that's why `npx`/`dlx` go to `ask`
  (allowing `Bash(npx *)` would green-light any package it runs).
- **Read/Edit paths follow gitignore semantics.** Anchors: `//abs` (filesystem root), `~/home`,
  `/rel-to-settings-file`, `name` or `./name` (relative to CWD). A bare filename matches at any depth:
  `Read(.env)` == `Read(**/.env)`. On Windows, paths normalize to POSIX (`C:\` → `/c/`).
- **WebFetch:** `WebFetch(domain:github.com)` (exact host), `WebFetch(domain:*.github.com)` (subdomains,
  not the apex). Case-insensitive.
- **MCP:** `mcp__<server>` or `mcp__<server>__*` (allow needs a literal server segment).

## The two gotchas that shape the preset
1. **Arg-restricting Bash rules are fragile — don't trust them.** A rule like `Bash(curl github.com *)`
   is bypassable via `-X`, `https`, redirects, `URL=... && curl $URL`, or double spaces. The official
   guidance: DON'T try to allow a network tool for "just one domain" — block/ask the network command
   (curl/wget) and use `WebFetch(domain:...)` for trusted domains. That's why curl/wget are in `ask`
   and the doc domains are in WebFetch `allow`.
2. **Global-scope path anchoring.** In USER settings (`~/.claude/settings.json`), a `/path` rule
   resolves relative to `~/.claude/`, NOT the project. So the preset never uses single-slash project
   paths — it uses bare/`**` patterns (CWD-relative, match in every project: `Read(**/.env)`) and
   `~/` / `//` for home/absolute. Keep it that way when widening the catalog.

## Settings precedence (where to write)
Highest → lowest: managed (enterprise, can't be overridden) → CLI args → `.claude/settings.local.json`
→ `.claude/settings.json` (project, shared) → `~/.claude/settings.json` (user, global). The skill's
default is the user/global file so it applies in every project. Deny from ANY scope still wins.
Managed settings, if present, can force prompts we can't override — note that if you see them.

## Hooks are an option, not used here
A `PreToolUse` hook can return allow/deny/ask per call, but it can't override a deny/ask rule and it
needs shell scripting (breaks zero-config for a layperson). The preset stays pure rules + mode. If a
future "Máximo" preset wants open Bash with a script backstop, that's where a hook would live.
