# precompact-backup.ps1 — Handoff (pack Fábrica de Ferramentas IA)
# Hook PreCompact (async): roda ANTES de um /compact ou auto-compact. Faz backup
# do .claude/context.md atual e anota o caminho do transcript, pra nada sumir num
# resumo com perda. Tudo local, NÃO gasta tokens de API. Zero dependência.
$ErrorActionPreference = 'SilentlyContinue'
try {
  $raw = [Console]::In.ReadToEnd()
  if (-not $raw) { exit 0 }
  $data = $raw | ConvertFrom-Json
  $cwd = $data.cwd
  if (-not $cwd) { exit 0 }
  $tp = $data.transcript_path
  $hd = "$cwd/.claude/handoffs"
  New-Item -ItemType Directory -Force -Path $hd | Out-Null
  $ts = Get-Date -Format 'yyyyMMdd-HHmmss'
  $ctx = "$cwd/.claude/context.md"
  if (Test-Path -LiteralPath $ctx) {
    Copy-Item -LiteralPath $ctx -Destination "$hd/context-$ts.md" -Force
  }
  Add-Content -LiteralPath "$hd/log.md" -Value "- $ts - compact disparado. transcript: $tp" -Encoding UTF8
} catch { exit 0 }
exit 0
