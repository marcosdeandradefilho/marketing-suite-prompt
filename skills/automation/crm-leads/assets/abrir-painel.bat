@echo off
chcp 65001 >nul
title Painel de leads
cd /d "%~dp0"

where node >nul 2>nul
if errorlevel 1 (
  echo.
  echo   Nao encontrei o Node nesta maquina.
  echo   O Node vem junto com o Claude Code na maioria das instalacoes.
  echo   Baixe em https://nodejs.org ^(versao LTS^) e rode este atalho de novo.
  echo.
  echo   Enquanto isso da pra abrir o painel.html com dois cliques,
  echo   mas ai o que voce mexer fica guardado so no navegador.
  echo.
  pause
  exit /b 1
)

node "%~dp0servidor.mjs" %1
echo.
echo   O painel foi encerrado.
pause
