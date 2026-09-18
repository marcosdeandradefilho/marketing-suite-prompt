#!/usr/bin/env bash
# precompact-backup.sh — Handoff (pack Fábrica de Ferramentas IA)
# Hook PreCompact (async): roda ANTES de um /compact ou auto-compact. Faz backup
# do .claude/context.md atual e anota o caminho do transcript, pra nada sumir num
# resumo com perda. Tudo local, NÃO gasta tokens de API. Zero dependência (sem jq).
raw="$(cat)"
[ -z "$raw" ] && exit 0
cwd="$(printf '%s' "$raw" | sed -n 's/.*"cwd"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
[ -z "$cwd" ] && exit 0
tp="$(printf '%s' "$raw" | sed -n 's/.*"transcript_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
hd="$cwd/.claude/handoffs"
mkdir -p "$hd"
ts="$(date +%Y%m%d-%H%M%S)"
[ -f "$cwd/.claude/context.md" ] && cp "$cwd/.claude/context.md" "$hd/context-$ts.md"
echo "- $ts - compact disparado. transcript: $tp" >> "$hd/log.md"
exit 0
