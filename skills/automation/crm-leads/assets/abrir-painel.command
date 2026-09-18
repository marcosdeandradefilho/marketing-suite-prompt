#!/bin/sh
# Painel de leads — Mac e Linux.
# No Mac: dois cliques neste arquivo. Se o Mac reclamar, rode uma vez:
#   chmod +x abrir-painel.command
cd "$(dirname "$0")" || exit 1

if ! command -v node >/dev/null 2>&1; then
  echo ""
  echo "  Não encontrei o Node nesta máquina."
  echo "  O Node vem junto com o Claude Code na maioria das instalações."
  echo "  Baixe em https://nodejs.org (versão LTS) e rode este atalho de novo."
  echo ""
  echo "  Enquanto isso dá pra abrir o painel.html com dois cliques,"
  echo "  mas aí o que você mexer fica guardado só no navegador."
  echo ""
  exit 1
fi

node "$(dirname "$0")/servidor.mjs" "$1"
echo ""
echo "  O painel foi encerrado."
