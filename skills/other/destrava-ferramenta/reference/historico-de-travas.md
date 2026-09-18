# historico-de-travas.md — the trava log (recurrence across re-runs)

This is what makes the skill worth re-running instead of being a one-shot chatbot answer: it
remembers past travas and recognizes patterns. A trava that keeps coming back is usually a
**layer-2 architectural cause wearing a fresh layer-1 error each time** — catching that is the
high-value move.

## Where it lives
`.claude/travas/` inside the user's project. Two kinds of file:
- **The log:** `.claude/travas/log.md` — one appended row per trava (the index).
- **The retomada plans:** `.claude/travas/AAAA-MM-DD-<slug>.md` — the full diagnosis + paths for a
  given trava, written on demand (Step 5).

Create the folder if it doesn't exist. If you can't write (read-only FS, permissions), don't
fail the run — just say you couldn't save and continue.

## Start of run — SCAN first (Step 0.5)
Before diagnosing, `Glob .claude/travas/*.md` and Read `log.md` if present. Match the current
symptom against past rows by: same error string, same file/module, OR same layer. If you find a
match, surface it up front, calm and specific:

> *"isso parece a mesma trava de [data]: na época era [camada N], e o que destravou foi
> [caminho]. Pode ser de novo — deixa eu confirmar antes de assumir."*

Then CONFIRM against the current state (don't assume it's identical). If it recurs across 2+ runs
with different surface errors, escalate the diagnosis a layer: treat it as layer-2 (architectural)
even if today's symptom looks like a fresh layer-1 bug.

If the folder is empty or absent → it's a first run, just continue silently (no "nenhuma trava
encontrada" noise).

## End of run — APPEND the record (Step 5)
After you deliver the paths, append ONE plain line per trava to `.claude/travas/log.md`. PLAIN TEXT —
NO pipe table (the user reads this raw). One bullet line, labeled fields separated by periods, with the
literal error string kept greppable:

```
Travas registradas (mais recente embaixo):

- 2026-06-07. sintoma: "X is not a function" no checkout. camada: 1 (API alucinada). caminho: conferir doc real do método. funcionou: a confirmar.
```

- **funcionou?** starts as "(a confirmar)". On a later run that touches the same trava, update the
  prior row to "sim"/"não/voltou" based on what the person tells you. That closing-the-loop is the
  recurrence signal — don't skip it.
- Keep the symptom short and greppable (the literal error string is ideal).
- The full diagnosis goes in the dated retomada file; the log row just points to the pattern.

## Retomada plan file (optional, on request or when the trava is big)
`.claude/travas/AAAA-MM-DD-<slug>.md`, written in the report structure from
`caminhos-de-saida.md`: read-back → 3-layer diagnosis → the 2-3 paths with acceptance → the
recommended first move → "tá resolvido de verdade quando...". This is what the person reopens
when they come back to the project, so it must stand alone in plain PT-BR.

## Privacy / scope
Only record what's needed to recognize a pattern (date, symptom, layer, path). Don't dump code,
secrets, or full diffs into the log. It's a memory of *travas*, not a copy of the project.
