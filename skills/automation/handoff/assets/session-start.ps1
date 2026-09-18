# session-start.ps1 — Handoff (pack Fábrica de Ferramentas IA)
# Hook SessionStart: lê o JSON do stdin, acha o .claude/context.md do projeto
# atual (cwd) e imprime pra o Claude Code injetar como contexto. Ler arquivo
# local NÃO gasta tokens de API. Se não houver checkpoint, não imprime nada.
# Zero dependência: usa só PowerShell nativo (Windows 10/11).
$ErrorActionPreference = 'SilentlyContinue'
try {
  [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
  $raw = [Console]::In.ReadToEnd()
  if (-not $raw) { exit 0 }
  $data = $raw | ConvertFrom-Json
  $cwd = $data.cwd
  if (-not $cwd) { exit 0 }
  $ctx = "$cwd/.claude/context.md"
  if (-not (Test-Path -LiteralPath $ctx)) { exit 0 }
  $content = Get-Content -LiteralPath $ctx -Raw -Encoding UTF8
  if (-not $content) { exit 0 }
  Write-Output "[handoff] Recuperei o checkpoint da sessao anterior deste projeto (.claude/context.md). Diga ao usuario, em UMA linha curta em portugues, que o contexto da sessao anterior foi carregado, e continue a partir do 'Proximo passo'. Conteudo do checkpoint:"
  Write-Output ""
  Write-Output $content
} catch { exit 0 }
exit 0
