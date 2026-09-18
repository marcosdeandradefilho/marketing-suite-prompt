# diagnostico-3-camadas.md — the 3-layer diagnosis + Claude Code failure catalog

Contents:
1. The 3-layer model (priority order)
2. Symptom → layer quick map
3. Claude Code failure catalog (symptom → cause → recovery, with the real command)
4. Git work-recovery (when files/edits got eaten)

---

## 1. The 3-layer model — diagnose in PRIORITY order
Order the diagnosis like an SRE incident: **stop the bleeding → restore service → root cause**
(sre.google/sre-book/managing-incidents). This is a PRIORITY call (what unblocks the person now),
NOT a SEVERITY call (the technically nastiest bug). Conflating the two is the #1 triage failure
(plane.so/blog/bug-triage-process-how-to-run-it-and-what-to-prioritize). It's OK to state impact
("é isso que te trava") before the exact root cause is known, so you never stall
(emmer.dev/blog/an-effective-incident-runbook-template).

**Camada 1 — erro técnico óbvio (o que está sangrando agora).**
Signals: a literal stack trace / error the person can paste; `"X is not a function"` or an unknown
flag (often a **hallucinated API/lib** — the model invented a method and presented it as real,
because it's trained on a snapshot and can't verify the library —
31daysofvibecoding.com/2026/01/14/when-ai-hallucinates); `"Prompt is too long"` (context
exhausted); a cryptic mid-turn API error. **Move:** read the ACTUAL error literally first (the
highest-ROI step a non-programmer skips), then map symptom → recovery from the catalog below.
Verify a suspected hallucinated method actually doesn't exist before blaming it.

**Camada 2 — decisão arquitetural anterior (por que continua travando).**
Signals: the plan doesn't fit the scope; a giant unrelated diff across files (the model edited
without reading surrounding context); a circular dependency; AI-bloated code (a God Class / Long
Method — `"funciona"` is NOT proof of clean); a speculative abstraction with no current caller.
**Move:** classify each stuck piece as **essential vs accidental complexity** — Brooks, "No Silver
Bullet" (en.wikipedia.org/wiki/No_Silver_Bullet). Only *accidental* complexity is eligible to cut;
the essential problem stays. Then go to `recuperacao-de-escopo.md`.

**Camada 3 — escopo/contexto grande demais (a causa de fundo).**
Signals: the context window blew up; a single sub-deliverable is huge; the model "lost the plot" /
repeats the same failing command; auto-compact thrashing
(code.claude.com/docs/en/how-claude-code-works). **Move:** re-cut to a thin vertical slice /
walking skeleton (`recuperacao-de-escopo.md`).

A trava that **recurs** with different surface errors is usually layer-2 masquerading as layer-1 —
check `historico-de-travas.md` and escalate the layer.

---

## 2. Symptom → layer quick map
| What the person says / you see | Likely layer |
|---|---|
| A specific error/stack trace, "X is not a function", unknown flag | 1 |
| "Prompt is too long" / it won't continue | 1 (context) → fix is layer-3 hygiene |
| Files disappeared / a bad edit wiped work | 1 (recover) → §4 |
| Claude made a huge diff touching unrelated files | 2 |
| "virou uma bagunça", circular deps, code nobody understands | 2 |
| "the Claude keeps doing the same wrong thing / lost the plot" | 3 |
| "non sei nem por onde começar", empty project | 3 (thin slice) |

---

## 3. Claude Code failure catalog (symptom → cause → recovery)
Use the REAL command. Tell the person what each does in one plain PT-BR line; never dump raw tool
names without explanation.

**a) "Prompt is too long" — context window full.**
Cause: conversation + files + MCP servers + CLAUDE.md filled the window. Auto-compact normally
prevents this; it only surfaces if auto-compact was disabled.
Recovery: `/context` shows what's eating the window → `/clear` to start fresh, or `/compact` to
summarize earlier turns (steerable: `/compact foca no bug do login`). Disable unused MCP servers;
move persistent rules into CLAUDE.md instead of relying on chat history.
(code.claude.com/docs/en/errors · /context-window)

**b) /compact vs /clear — they are DIFFERENT (people confuse them).**
`/compact` SUMMARIZES the conversation and preloads the summary as new context (you can steer it).
`/clear` WIPES history entirely. Heuristic: `/compact` when one phase is done but the context
still matters; `/clear` when switching to unrelated work.
(code.claude.com/docs/en/context-window)

**c) Auto-compaction stops with a "thrashing" error.**
Cause: a single file or tool output is so large that context refills right after each summary;
Claude Code stops auto-compacting instead of looping forever.
Recovery: find the huge file/output and get it OUT of the main window — `/clear`, or read it via a
subagent/forked context. (Mechanic confirmed at code.claude.com/docs/en/how-claude-code-works; the
exact step-by-step recovery wording is not pinned here — present the approach, don't fake precise
steps.)

**d) Claude made a bad/over-broad edit, or a giant unrelated diff.**
Cause: the model edited the immediate file without reading enough surrounding context.
Recovery: hit **Esc** to hard-stop the running tool. Open `/rewind` (or **Esc twice on an EMPTY
prompt**) and choose: restore code+conversation, conversation only, or code only. Prevent
recurrence with **Plan Mode** (read-only, approve before execute).
**GOTCHA:** Esc-twice only opens rewind if the prompt is EMPTY; with text typed it just clears the
text. (code.claude.com/docs/en/checkpointing)

**e) Stuck mid-turn API error ("400 ... tool use concurrency", "unexpected tool_use_id", "thinking blocks cannot be modified").**
Cause: the tool/thinking history no longer matches what the API expects. On Opus 4.7/4.8, CLI
versions before **v2.1.156** can trigger this during normal tool use, and `/rewind` alone won't
clear it.
Recovery: on Opus 4.7/4.8, run **`claude update` FIRST**, THEN `/rewind` (or Esc twice) to a
checkpoint before the corrupted turn. The version pin is load-bearing.
(code.claude.com/docs/en/errors)

**f) Claude is stuck in a loop repeating the SAME failing command.**
Cause: it attempts, fails, re-evaluates, and re-attempts the same flawed approach — sometimes not
noticing the command errored (claude-code issues #19699, #11034 — community-reported).
Recovery: interrupt with **Esc** (or Ctrl+C). Break the task into smaller atomic steps with
clearer instructions, OR `/rewind` to a clean checkpoint before the loop began.

**g) "X is not a function" / unknown flag — hallucinated API/library.**
Cause: the model invented a non-existent method/option and presented it as documented fact (it
can't verify the lib from its training snapshot). Self-repair is weak — it tends to say "I can't
fix this."
Recovery: point it at the REAL docs and explicitly instruct the fix (don't expect self-repair).
Verify the method/flag exists in the actual library version before re-running. (You can WebSearch
the library's docs to confirm — optional.)
(31daysofvibecoding.com/2026/01/14/when-ai-hallucinates)

**h) Model "lost the plot" — low-quality answers, ignoring instructions, anchored to a wrong earlier attempt.**
Cause: correcting in-thread keeps the wrong attempt in context, which anchors later answers. Or
CLAUDE.md never loaded, or the window is full.
Recovery: don't argue with the model — `/rewind` (Esc twice) to BEFORE the bad turn, then rephrase
with more specifics. Cheap checks first: `/context` (window full?) and `/memory` (did CLAUDE.md
load?). (code.claude.com/docs/en/errors)

**i) Constant permission prompts (prompt fatigue).**
Cause: `acceptEdits` auto-approves Edit/Write, but Reads and Bash still follow allow/ask/deny
rules and the allowlist is too thin.
Recovery: `/permissions` shows active rules (fastest way to see why a tool prompted). Add the
most-prompted Bash commands to allow with `:*` (e.g. `Bash(npm install:*)`) and set defaultMode to
acceptEdits. (Don't promise zero prompts — a known toggle bug exists.)
(code.claude.com/docs/en/permissions)

**j) "Rate limit reached" / locked out.**
Cause: Pro & Max limits are **SHARED across Claude web + Claude Code**, with a 5-hour rolling
window AND a separate weekly cap — so Claude web usage silently eats the Code budget.
Recovery: if genuinely exhausted, wait for reset, enable usage credits via Console, or upgrade.
**Folk remedy (community, not official):** a STUCK limiter showing "limit reached" under ~50%
usage sometimes clears with `claude logout` → delete cached credentials → `claude login`. Label it
as a community fix, not an Anthropic-documented one.
(support.claude.com/en/articles/11145838)

---

## 4. Git work-recovery — when files/edits got eaten
`/rewind` only tracks **direct edits via Claude's file-editing tools**. It does NOT track files
deleted/moved by bash commands (`rm`/`mv`/`cp`), manual external edits, or other sessions — and
there is **no redo stack**, so a wrong rewind can be permanently unrecoverable
(code.claude.com/docs/en/checkpointing). When work is gone, **git** is the real safety net.

**FIRST: stop editing / committing / running `git gc` until recovery is done** (it can prune the
dangling commits you need).

Suggest these to the PERSON to run (you don't run them — they're potentially state-changing):
- Find the lost state: `git reflog` and `git log --all --oneline`.
- Recover one file from a commit: `git checkout <sha> -- caminho/do/arquivo`.
- Recover the whole state: `git switch -c recuperado <sha>` (new branch, non-destructive).
- Modified-but-still-at-HEAD: `git restore <caminho>`.
- Staged but never committed (after a `reset`): `git fsck --lost-found` surfaces dangling blobs
  into `.git/lost-found`; inspect with `git show <hash>`.

**Known Claude bug to warn about:** it sometimes runs a DESTRUCTIVE `git reset --hard` instead of a
safe `git checkout`/`git restore` for a rollback (claude-code issues #17190; #34327 did it on
startup, twice, destroying uncommitted work). Prevention: commit before letting it loose; never
ask "undo my changes" loosely; consider a deny-rule / PreToolUse hook guarding `git reset --hard`.
(github.com/anthropics/claude-code/issues/17190)
