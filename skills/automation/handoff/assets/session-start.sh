#!/usr/bin/env bash
# session-start.sh — Handoff (pack Fábrica de Ferramentas IA)
# Hook SessionStart: lê o JSON do stdin, acha o .claude/context.md do projeto
# atual (cwd) e imprime pra o Claude Code injetar como contexto. Ler arquivo
# local NÃO gasta tokens de API. Sem checkpoint, não imprime nada.
# Zero dependência: usa só cat/sed (sem jq).
raw="$(cat)"
[ -z "$raw" ] && exit 0
cwd="$(printf '%s' "$raw" | sed -n 's/.*"cwd"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
[ -z "$cwd" ] && exit 0
ctx="$cwd/.claude/context.md"
[ -f "$ctx" ] || exit 0
echo "[handoff] Recuperei o checkpoint da sessão anterior deste projeto (.claude/context.md). Diga ao usuário, em UMA linha curta em português, que o contexto da sessão anterior foi carregado, e continue a partir do 'Próximo passo'. Conteúdo do checkpoint:"
echo ""
cat "$ctx"
exit 0
