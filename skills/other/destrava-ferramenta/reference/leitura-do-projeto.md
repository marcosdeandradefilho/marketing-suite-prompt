# leitura-do-projeto.md — read the real state before diagnosing (Step 1)

The differentiator over a generic chatbot is that you LOOK at the actual project. Do this BEFORE
asking the emotional question, and narrate it in plain PT-BR (*"Deixa eu olhar o que mudou no teu
projeto antes de te perguntar nada..."*). Everything here is READ-ONLY. You never run a command
that edits or deletes.

## The read-state sweep (each line has a fallback — never stall on one)

| What you want | Command (read-only) | If it fails / is empty |
|---|---|---|
| What's uncommitted | `git status` | Not a git repo → go to "No git repo" below |
| The actual change | `git diff` and `git diff --staged` | Empty diff → nothing uncommitted; the trava is in committed code or in runtime, not in a pending edit |
| Recent history / a "last good" point | `git log --oneline -10` | No commits yet → there's no fallback commit; note it (a revert path won't exist) |
| Where the action/mess is | Glob the repo, newest-first (e.g. `**/*.{js,ts,py,...}`), Read the 2-3 most-recently-touched files | Huge repo → only read the files the diff/error point at, not everything |
| The error itself | Ask them to paste the FULL error/stack trace; Grep the repo for the error string or recent `console.error`/`throw`/`raise` | No error text → it's not a layer-1 crash; lean to layer 2/3 (mess / lost-the-plot) |
| Stray context bloat | Note CLAUDE.md size, number of files open, MCP servers — candidates for "Prompt is too long" | — |

**Reading the actual error message first is the highest-ROI move a non-programmer skips.** "X is
not a function" or an unknown flag often means a hallucinated API (layer 1). A giant diff touching
unrelated files is a layer-2 signal. "Prompt is too long" is layer 3. (Symptom → layer mapping is
in `diagnostico-3-camadas.md`.)

Use **Glob / Grep / Read** for files (cross-platform — works the same on Windows and Mac). Use
**Bash only for the read-only git commands above.** Do not shell out to `ls`/`find`/`cat` — the
native tools are safer and OS-independent.

## Degraded mode (mandatory branches — define the fallback move for each)

### No git repo (`git status` errors with "not a git repository")
- Skip every git step. Don't treat this as a failure — many beginners haven't run `git init`.
- Fall back to: file modification times (Glob newest-first) + the error they paste + their
  description. Diagnose from those.
- Only suggest `git init` if they want checkpoints/undo going forward — frame it plainly:
  *"sem git, não dá pra voltar no tempo se algo quebrar; se quiser essa rede de segurança, dá pra
  ativar com `git init` — mas não é obrigatório pra gente destravar agora."* Don't lecture.

### Empty or near-empty project (no real code yet)
- Skip diff/bisect/log analysis — there's nothing to bisect.
- Go straight to the emotional read + a **walking-skeleton path** (`recuperacao-de-escopo.md`):
  the trava here is usually "não sei nem por onde começar," not a bug. Help them define one thin
  end-to-end slice.

### A command or tool is down / output is unreadable
- Retry once. If still down, SAY it plainly: *"não consegui rodar [X] agora — pode ser limite do
  plano ou indisponibilidade."* Continue with whatever signal exists (pasted error, mtimes, their
  words). NEVER stall waiting, and NEVER fill the gap by guessing what the code says.

### Web optional (WebSearch/WebFetch)
- This skill diagnoses fully from LOCAL state. Web is only used to verify a suspected hallucinated
  API/library or look up an exact error code. If web is down, still diagnose — just label any
  "does this method exist?" check as *"não consegui confirmar agora, trate como hipótese"* instead
  of asserting it.

## What NOT to read
Keep the read bounded to the trava. Don't open unrelated files, secrets, or `.env` to be
"thorough" — you're triaging a stuck project, not auditing it. If the input isn't about a stuck
project at all, you shouldn't be at Step 1 (see SKILL.md Step 0 scope guard).
