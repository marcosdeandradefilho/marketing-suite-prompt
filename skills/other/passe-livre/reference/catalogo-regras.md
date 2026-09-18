# catalogo-regras.md — the curated EQUILIBRADO catalog, explained

The rules themselves live in `assets/preset-equilibrado.json` (read that file verbatim — this file
explains the WHY so you can answer questions and widen/tighten safely). The design principle:

> Auto-approve ordinary dev work. Prompt on risky-but-legitimate (deploy/delete/publish). Hard-block
> the dangerous (root, disk wipe, secret reads). Nothing that "constrains arguments" of a shell command
> is trusted (see gotcha #1 in `modelo-permissoes.md`).

## [VERDE] allow — runs with no prompt
Chosen because each is normal, high-frequency, and reversible-in-practice dev work:
- **Package managers (install/run/test/build/list):** npm, pnpm, yarn, bun. Yes, `install`/`add` run
  postinstall scripts (arbitrary code) — but installing declared project deps is the baseline dev loop
  and blocking it defeats the purpose. Global installs and `publish` are carved out to `ask`.
- **Runtimes / build / test / lint:** node, python, pip install, tsc, eslint, prettier, jest, vitest,
  pytest, vite, next, nuxt, go build/test/run, cargo build/test/run, make. Running a dev server is just
  a long-running process — safe.
- **Git (local, non-destructive):** add, commit, checkout, switch, branch, merge, rebase, stash, fetch,
  pull, restore, tag, cherry-pick, init, remote, show, `config --get/--list`. History rewrites that stay
  local (rebase) are allowed; anything that hits the remote (push) or destroys work (`reset --hard`,
  `clean`) is in `ask`.
- **gh (read-only):** pr/issue/repo/run list+view. Write ops (release, pr create/merge) are in `ask`.
- **WebFetch of known docs:** github, npm, MDN, python docs, pypi, stackoverflow/stackexchange, the
  Claude docs, react.dev, nodejs.org, go.dev, crates.io. Any other domain still prompts.
- **PowerShell mirror** of the essentials for Windows users (npm/git/node/python + read-only cmdlets
  like Get-ChildItem/Get-Content/Test-Path/Select-String). Aliases (gci/ls/dir) are covered automatically.

## [AMARELO] ask — prompts every time
Legitimate but risky, irreversible, or outward-facing — the user should eyeball it:
- **Destructive-local:** `rm`, `rmdir`, `git reset --hard`, `git clean`. (`rm` is NOT auto-approved even
  by acceptEdits, so this reinforces the prompt.)
- **Reaches the network / third-party code:** `curl`, `wget` (fragile to allowlist — see gotcha #1),
  `npx`, `pnpm dlx`, `bunx`, `yarn dlx` (run arbitrary downloaded packages).
- **Publishing / global state:** `npm publish`, `npm install -g`, pnpm/yarn publish.
- **Deploy / cloud:** vercel, netlify, firebase, supabase, aws, gcloud, az, heroku, fly, railway,
  wrangler, `gh release`, `gh pr create/merge`.
- **Containers / remote / process / system-pkg:** docker, docker-compose, kubectl, ssh, scp, rsync,
  kill, pkill, brew, apt, apt-get, yum, dnf, pacman, chmod, chown.
- **PowerShell:** Remove-Item, git push, Invoke-WebRequest, Invoke-RestMethod, Start-Process,
  Stop-Process, Set-ExecutionPolicy.

## [VERMELHO] deny — never runs
- **Privilege escalation:** sudo, su, doas. A layperson should never have Claude run as root; if they
  truly need it, they run it themselves in a terminal.
- **Catastrophe:** `rm -rf /` and `~` variants, `mkfs`, `dd if=`/`dd of=/dev/`, `chmod -R 777 /*`.
  (Claude Code already circuit-breaks `rm -rf /` and `~`; these are belt-and-suspenders.)
- **Secret reads (tool-agnostic — also blocks cat/head/tail in Bash and Grep/Glob best-effort):**
  `**/.env`, `**/.env.*`, `**/secrets/**`, `**/secret/**`, `**/*.pem`, `**/*.key`, common private keys
  (`id_rsa`, `id_ed25519`, `id_dsa`), `**/.npmrc` + `~/.npmrc` (npm tokens), `~/.ssh`, `~/.aws`,
  `~/.gnupg`, `~/.kube/config`, `~/.docker/config.json`, `**/credentials`, `**/credentials.json`.
- **Secret writes / repo internals:** `Edit(**/.env)`, `Edit(**/.env.*)`, `Edit(**/.git/**)`.
- **PowerShell:** Format-Volume (the Read/Edit denies above already cover PS file reads/writes).

Note: `Read(**/*.key)` is deliberately conservative — it can catch a non-secret file named `*.key`.
If that bites a user, tell them how to remove that one deny; don't quietly drop it for a security skill.

## Widening / tightening (if the user asks)
- To auto-approve a command they use constantly that still prompts: add `Bash(<cmd> *)` to `allow`.
  Prefer a specific prefix over a broad one; never add `Bash(curl *)`/`Bash(npx *)`/`Bash(sudo *)` to
  allow (that's the whole point of the guardrail).
- To read a specific `.env` they own: remove exactly that path from `deny` (or add a narrower allow that
  the deny still overrides — deny wins, so they must actually remove the deny). Explain the tradeoff.
- To make it stricter: move an `ask` item to `deny`, or a broad `allow` to `ask`.
- Never point them at `bypassPermissions` / `--dangerously-skip-permissions`.

## Provenance
Tier assignment follows the official security guidance in
https://code.claude.com/docs/en/permissions (deny curl/wget + use WebFetch domains; read-only builtins;
deny>ask>allow) and https://code.claude.com/docs/en/permission-modes (what acceptEdits auto-approves).
