# mecanismo.md — why this saves tokens (honest), scoping, runtime behavior

## The honest economics (say the mechanism, never a number)
Verified against Claude Code docs + Anthropic engineering guidance (2026-06). What's TRUE and
defensible — and what is NOT.

**TRUE — say this:**
- `/compact` is **not free**. It fires a real summarization call whose INPUT is your entire
  conversation — you pay to re-read the whole history to produce the summary. Near a full window
  that's a big re-read.
- `/clear` costs **~0** — it just resets the window, no summarization call.
- A summary is **lossy**: it drops exact file paths, the precise decision and why, the dead-ends you
  already ruled out. A written `context.md` keeps those EXACTLY. So `/clear` + a handoff is both
  cheaper than `/compact` AND higher-fidelity.
- Anthropic's own guidance calls clearing between tasks "the single most effective lever" for context.
- Reading the local `context.md` / transcript costs **ZERO API tokens** — they're local files.

**NOT TRUE / do NOT say:**
- ❌ "economiza 95%", "evita 80% dos compacts", "recupera 100-400k tokens/dia" — **no measured source
  exists** for any of these. Don't put a number on it.
- ❌ "`/clear` reseta seu limite do PRO" — FALSE. Neither `/clear` nor `/compact` resets the account
  usage limit (the 5-hour / weekly cap). What clearing does is stop you from **re-paying for stale
  context every single turn** — that's the real, honest win. Frame it exactly that way.
- ❌ exact auto-compact trigger % as fact — it's ~80-83% of the window by community estimate; label it
  "perto do limite", not a hard number.

So the pitch, honestly: *"em vez de pagar pra resumir (e perder detalhe), tu salva o que importa num
arquivo, dá /clear de graça, e a próxima sessão recarrega o detalhe exato. Não é mágica nem reseta teu
limite — é parar de reprocessar contexto velho a cada mensagem."*

## Per-project scoping (no cross-contamination)
- The checkpoint lives in `<project>/.claude/context.md` — one per project, at the project root.
- The SessionStart hook is installed once at user scope but reads the hook's **stdin `cwd`** (the
  project you actually opened) and only prints THAT project's `context.md`. Open a different project
  with no checkpoint → the hook prints nothing. So one install is safe across all your projects.
- The `cwd` on hook stdin is the documented, reliable project signal. The script does not reverse-decode
  the `~/.claude/projects/<slug>` folder name (that encoding isn't a stable contract) — it uses `cwd`.

## Per-branch awareness (worktrees / parallel branches)
- A single working tree's `.claude/` is shared across git branches, so two branches can fight over one
  `context.md`. The checkpoint stamps the branch it was saved on (`gitBranch` from the transcript JSONL,
  or `git rev-parse --abbrev-ref HEAD`).
- On save: if the current branch differs from the stamped one, don't blind-merge — flag it and ask, or
  namespace the file as `.claude/context.<branch>.md` for that branch.
- On reload: the SessionStart script prints whatever `context.md` exists; if the user works heavily in
  parallel branches, recommend git **worktrees** (separate dirs → separate `.claude/`) — that's the real
  isolation mechanism. For a typical layperson on one branch, none of this matters; keep it invisible
  unless a branch mismatch actually shows up.

## What the hooks do at runtime (so you can explain it plainly)
- **SessionStart** (on open / `/clear` / resume / after compact): script reads its stdin JSON → takes
  `cwd` → if `cwd/.claude/context.md` exists, prints a one-line marker + the file. Claude Code injects
  that stdout as context. Cost: one local file read, 0 API tokens, a few KB of context (the lean file).
- **PreCompact** (just before `/compact` or auto-compact): script reads stdin → `cwd` + `transcript_path`
  → copies `context.md` to `.claude/handoffs/context-<ts>.md` and appends a line to `.claude/handoffs/log.md`
  noting the timestamp + transcript path. Runs `async` so it never delays the user. It's a safety net:
  if an auto-compact fires before the user ran `/handoff`, their last checkpoint is still versioned and
  the raw transcript is pointed to.

## Recurrence (why it's worth keeping, not one-and-done)
- Every work session ends → `/handoff` updates the checkpoint with the latest state (a DELTA, not a
  reprint). Re-running surfaces "o que mudou", merging onto the prior file. A project that runs for days
  accumulates a living, bounded checkpoint — that's the subscription-justifying loop.
- It pairs with the daily rhythm: work → `/handoff` → `/clear` → next day reload. And when the context
  window fills up → `/handoff` → `/clear` → back to a fresh session.

## Failure modes to handle gracefully
- No git → omit the branch line, everything else works.
- `.claude/` not present → create it (it's the standard project config dir).
- Two projects open in two terminals → each hook fires with its own `cwd`; no collision.
- User deletes the skill folder → hooks break (command path 404). Document that uninstalling the skill
  means running `/handoff off` first (or removing the hook entries) so settings.json doesn't point at a
  missing script.
