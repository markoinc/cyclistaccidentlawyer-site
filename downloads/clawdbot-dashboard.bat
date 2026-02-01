@echo off
title Clawdbot Dashboard
echo ========================================
echo   Clawdbot Dashboard Tunnel
echo ========================================
echo.

:: Start tunnel in background
start /B ssh -i "%~dp0linux clawdbot.pem" -L 8080:localhost:18789 ec2-user@54.83.113.36 -N

:: Wait for tunnel to establish
timeout /t 2 /nobreak >nul

:: Open browser
start http://localhost:8080

echo Tunnel active. Close this window to disconnect.
echo.
pause
