# merge-e-reversao.md — the exact merge algorithm, scopes, and revert

This is a SECURITY-adjacent write. Do it deterministically, back up first, verify after. No runtime
dependency (no node/jq/python) — you (the model) perform the merge from the two JSON files, and the
only shell you use is a byte-exact file copy for the backup.

## Scope resolution (which file)
- **GLOBAL (default):** the real home dir + `.claude/settings.json`.
  - Windows: `%USERPROFILE%\.claude\settings.json` (resolve via `$env:USERPROFILE`).
  - Mac/Linux: `$HOME/.claude/settings.json` (resolve via `echo $HOME`).
  - Never write a literal `~` into a path you pass to tools; expand it first.
- **PROJECT:** `<project root>/.claude/settings.json` (the dir with `.claude/`, i.e. the cwd root).
  Warn that project `allow` rules only take effect after the workspace-trust dialog; `deny`/`ask` apply
  regardless.
Create the `.claude/` dir if missing (the Write tool auto-creates parent dirs).

## The merge (step by step)
Inputs: `current` = parsed existing settings (or `{}` if the file doesn't exist);
`preset` = parsed `assets/preset-equilibrado.json`.

1. **Parse guard.** Strip a leading UTF-8 BOM if present, then parse `current` as JSON. If it does NOT
   parse (genuinely malformed, not just a BOM) → ABORT, do not write, tell the user in PT-BR. A BOM
   alone is fine.
2. **Ensure** `current.permissions` is an object (create `{}` if absent). Ensure `.allow`, `.ask`,
   `.deny` are arrays (default `[]`).
3. **deny (union first — it has precedence):**
   `newDeny = dedup(current.permissions.deny ++ preset.deny)` preserving order (existing first, then
   new ones not already present). Never remove a user's existing deny.
4. **ask:** `newAsk = dedup(current.permissions.ask ++ preset.ask)`, THEN remove any entry that is in
   `newDeny` (deny wins).
5. **allow:** `newAllow = dedup(current.permissions.allow ++ preset.allow)`, THEN remove any entry that
   is in `newDeny` OR in `newAsk` (deny and ask both beat allow). This is where **the user's existing
   deny/ask overrides our allow** — e.g. if they already `deny`/`ask` `Bash(npm run *)`, it will NOT
   end up in allow. Record these as "mantive tua regra" for the report.
6. **defaultMode:**
   - unset, `"default"`, or `"manual"` → set to `"acceptEdits"`.
   - already `"acceptEdits"` → leave.
   - `"plan"`, `"auto"`, `"dontAsk"` → LEAVE it (don't override the user's intent) and note it.
   - `"bypassPermissions"` → do NOT silently change; WARN (they're in the dangerous mode) and offer to
     switch to `acceptEdits` with explicit consent (SKILL rule 5).
7. **Preserve everything else.** Every other key in `current` (`hooks`, `env`, `model`, `statusLine`,
   `additionalDirectories`, `$schema`, anything) is copied through UNCHANGED. Only `permissions` (and
   its sub-arrays + defaultMode) is touched. Do NOT copy the preset's `_sobre` comment field into the
   output.
8. **Idempotency falls out of dedup:** running twice adds nothing new. If nothing changed, report
   "nada novo a liberar — já tava aplicado".

`dedup` = keep first occurrence, drop later exact-string duplicates. Rule strings are compared as exact
strings (that's how Claude Code stores them).

## Backup (before writing, always)
Only if the target file already exists. Real byte copy — NOT Read→Write (the Read tool adds line
numbers and can normalize bytes; copying its output would corrupt the backup):
- Windows (PowerShell): `Copy-Item "<path>" "<path>.bak-<STAMP>"`
- Mac/Linux (Bash): `cp "<path>" "<path>.bak-<STAMP>"`
`<STAMP>` = `AAAA-MM-DD-HHMMSS`. Tell the user the exact backup path.

## Write + read-back verify (mandatory)
Write the merged object with the Write tool: 2-space indent, UTF-8, no BOM, trailing newline, valid
JSON. Then Read it back and confirm ALL of:
- parses as valid JSON;
- `permissions.defaultMode` is present;
- `permissions.deny` contains `Read(**/.env)` AND `Bash(sudo *)`;
- `permissions.ask` contains `Bash(git push *)` and does NOT also list it in `allow`;
- `permissions.allow` does NOT contain `Bash(curl *)` (it must be ask);
- every top-level key that existed in `current` before is still present (hooks/env/etc.).
If any check fails → restore the backup (copy `.bak-<STAMP>` back over the file) and report the failure
honestly. Never leave a half-applied file.

## Reverter (undo)
Trigger: `/passe-livre reverter` / "desfazer" / "voltar".
1. `Glob` for `<path>.bak-*` next to the target settings file; pick the most recent by timestamp.
2. If found: copy it back over `settings.json` (`Copy-Item`/`cp`), confirm in PT-BR, tell them to reopen
   Claude Code. Leave the `.bak` in place (don't delete their safety net).
3. If no backup exists (e.g. they hand-edited since): don't guess — show them how to remove the
   `permissions` block manually, or offer to strip exactly the preset's rules back out (union-subtract:
   remove only rules that are in the preset AND weren't there before — but if you can't prove what was
   there before, say so and stop).

## What NOT to do
- Never write without a backup of an existing file.
- Never overwrite the whole settings.json — only merge `permissions`.
- Never set `bypassPermissions`.
- Never invent rules not in the preset (widening is user-driven, per `catalogo-regras.md`).
