@echo off
title Acelera PC - limpeza semanal
REM Clique 2x neste arquivo uma vez por semana. Ele pede admin sozinho e roda
REM so a limpeza LEVE e reversivel (temp, cache de apps, DNS, TRIM). Nao mexe em
REM registro, servico nem debloat - isso e so o modo Setup do acelera-pc.ps1.

net session >nul 2>&1
if %errorlevel% NEQ 0 (
    echo Pedindo permissao de administrador...
    powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0acelera-pc.ps1" Semanal
echo.
echo Pronto. Pode fechar esta janela.
pause
