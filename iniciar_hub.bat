@echo off
setlocal EnableDelayedExpansion
title Antigravity Central Hub (MCP)
cd /d "%~dp0"

echo ======================================================
echo    INICIANDO ANTIGRAVITY CENTRAL HUB (MCP + TUNNEL)
echo ======================================================
echo.

:: 1. Inicia o Cloudflare Tunnel se ainda nao estiver rodando
tasklist /fi "imagename eq cloudflared.exe" | find /i "cloudflared.exe" >nul
if errorlevel 1 (
    echo [*] Iniciando tunel permanente Cloudflare...
    for /f "usebackq tokens=*" %%T in ("token.txt") do set "TOKEN_RAW=%%T"
    set "TOKEN_CLEAN=!TOKEN_RAW:cloudflared.exe service install =!"
    set "TOKEN_CLEAN=!TOKEN_CLEAN:cloudflared service install =!"
    set "TOKEN_CLEAN=!TOKEN_CLEAN: =!"
    start "" /b cloudflared.exe tunnel run --token !TOKEN_CLEAN!
) else (
    echo [OK] Tunel Cloudflare ja esta em execucao.
)

:: 2. Inicia o Servidor MCP na porta 8000
echo [*] Iniciando Servidor MCP Python...
echo [*] Link Oficial Gemini Spark: https://mcp.promptpulse.com.br/mcp
echo.
.\.venv\Scripts\python.exe run_server.py
pause
