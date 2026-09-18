# hooks-instalacao.md — wiring SessionStart + PreCompact (consent + backup + idempotent)

> All facts here were verified against the official Claude Code hooks docs
> (code.claude.com/docs/en/hooks) in 2026-06. Do not invent fields.

## What gets installed and why
- **SessionStart hook** → when the user opens (or `/clear`s, resumes, or just got compacted) a
  project, it prints `<project>/.claude/context.md` to stdout. For SessionStart, **plain stdout is
  added to Claude's context** (one of the only events where that happens) — so the next session
  starts already knowing where they stopped. No JSON to build. If the project has no `context.md`,
  the script prints nothing (zero noise, no cross-contamination).
- **PreCompact hook** → right before a `/compact` (manual) or an auto-compact (window full), it copies
  the current `context.md` to `.claude/handoffs/context-<timestamp>.md` and records the transcript
  path, so nothing is silently lost to a lossy summary. Runs `async` (doesn't delay the user).

Both go in **user scope** (`~/.claude/settings.json`) so ONE install works in every project. The
scripts are project-agnostic — they read the project from the hook's stdin `cwd`.

## Step A — locate settings.json + the asset scripts (resolve absolute paths)
1. Find the config dir. Default `~/.claude` → Windows `C:\Users\<name>\.claude`, Mac/Linux
   `~/.claude`. If `$CLAUDE_CONFIG_DIR` is set, use that instead (rare; a layperson won't have it).
   - Windows home: PowerShell `$env:USERPROFILE`. Mac/Linux home: `$HOME`.
2. The skill's scripts live at `<config>/skills/handoff/assets/`. Build the script path and convert
   ALL backslashes to **forward slashes** (Windows Git Bash silently fails on backslash paths):
   - Windows: `C:/Users/<name>/.claude/skills/handoff/assets/session-start.ps1`
   - Mac/Linux: `/Users/<name>/.claude/skills/handoff/assets/session-start.sh`
3. Sanity-check the asset files exist (`Glob` them). If they're missing, the skill folder was copied
   without `assets/` — tell the user to re-copy the whole `handoff` folder; don't half-install.

## Step B — back up, show, consent
1. Read `~/.claude/settings.json`. If it doesn't exist, you'll create a minimal `{}` (consent first).
   If it exists but is NOT valid JSON → ABORT (rule: never clobber). Tell the user in PT-BR.
   - **A leading UTF-8 BOM is NOT "invalid JSON".** Windows tools often write `settings.json` with a
     BOM (`EF BB BF`) — a strict parser chokes on it, but the file is perfectly valid. Strip/ignore a
     leading BOM before judging validity, and preserve it (or re-save as UTF-8) on write. ABORT only
     when the actual JSON content is malformed, never just because a BOM is present.
2. Copy it to `settings.json.bak-<AAAAMMDD-HHMMSS>` (Bash `cp` / PowerShell `Copy-Item`). Never edit
   without a backup.
3. Show the user the exact block you'll ADD (the `hooks` entries below) and ask via AskUserQuestion:
   header *"Ligar auto-load"*, question *"Posso ligar o auto-carregamento? Faço backup do teu
   settings.json antes."* — options **Pode ligar** / **Agora não**.

## Step C — the exact JSON to merge (idempotent)
You are MERGING, not replacing. Preserve every existing key. Ensure `settings.json` has a top-level
`hooks` object; under it, APPEND to the `SessionStart` and `PreCompact` arrays (create them if absent).

**Idempotency:** before appending, scan the existing `SessionStart`/`PreCompact` hooks for a command
containing `skills/handoff/assets/session-start` (or `precompact-backup`). If found, it's already
installed — do NOT add a duplicate; just confirm it's on.

**Windows** (`command` values — note `-ExecutionPolicy Bypass` so a locked-down PC still runs it, and
the escaped quotes for paths that may contain spaces):
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear|compact",
        "hooks": [
          { "type": "command", "command": "powershell -NoProfile -ExecutionPolicy Bypass -File \"C:/Users/<NAME>/.claude/skills/handoff/assets/session-start.ps1\"" }
        ]
      }
    ],
    "PreCompact": [
      {
        "matcher": "auto|manual",
        "hooks": [
          { "type": "command", "command": "powershell -NoProfile -ExecutionPolicy Bypass -File \"C:/Users/<NAME>/.claude/skills/handoff/assets/precompact-backup.ps1\"", "async": true }
        ]
      }
    ]
  }
}
```

**Mac/Linux** (`command` values):
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear|compact",
        "hooks": [
          { "type": "command", "command": "bash \"/Users/<NAME>/.claude/skills/handoff/assets/session-start.sh\"" }
        ]
      }
    ],
    "PreCompact": [
      {
        "matcher": "auto|manual",
        "hooks": [
          { "type": "command", "command": "bash \"/Users/<NAME>/.claude/skills/handoff/assets/precompact-backup.sh\"", "async": true }
        ]
      }
    ]
  }
}
```
Replace `<NAME>` with the real resolved home path. Write the FULL merged JSON back with `Write`.

> Matcher note: `startup|clear|compact` deliberately SKIPS `resume` — a `--resume`/`--continue`
> restores the whole prior conversation already, so re-injecting `context.md` there would just spend
> context for nothing. We reload exactly when the window is fresh or just got summarized.

## Step D — verify + tell them to restart
1. Re-read the file; confirm it's valid JSON and your entries are present (this is the "I verified the
   install" step — never claim it worked without re-reading).
2. Tell the user (PT-BR): *"Pronto. **Fecha e abre o Claude Code de novo** pra valer (hooks carregam no
   boot). Da próxima vez que tu abrir esse projeto, ele já vem com o contexto."*
3. Optional: tell them they can confirm hooks loaded with `/hooks` and the whole pack with `/doctor`.

## Uninstall (`/handoff off`)
1. Read `~/.claude/settings.json`; back it up first (same as Step B).
2. Remove ONLY the `SessionStart`/`PreCompact` hook entries whose command references
   `skills/handoff/assets/` (leave every other hook and key intact). If that empties an array, you may
   drop the empty array.
3. Write back, re-read to confirm, tell the user it's off and that the `context.md` files stay (the
   skill just won't auto-load them anymore). Mention the timestamped backups if they want to revert.

## Windows gotchas (verified)
- On Windows, hook commands run under **Git Bash if installed, else PowerShell — never cmd.exe**.
  Invoking `powershell -NoProfile -ExecutionPolicy Bypass -File <forward/slash/path>` works under
  BOTH, so it's the portable choice regardless of which shell CC picks.
- **Backslash paths fail SILENTLY under Git Bash** (it eats the `\`). Always forward slashes.
- If the user's home path has spaces (`C:/Users/John Doe/...`), the quotes around the path matter —
  keep them (already in the template).
