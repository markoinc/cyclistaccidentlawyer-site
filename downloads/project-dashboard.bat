@echo off
title Project Dashboard - KuriosBrand
echo ========================================
echo   Sierra Dashboard - KuriosBrand
echo ========================================
echo.

:: Start tunnel in background (port 8888 -> dashboard server)
start /B ssh -i "%~dp0linux clawdbot.pem" -L 8888:localhost:8888 ec2-user@54.83.113.36 -N

:: Wait for tunnel
timeout /t 2 /nobreak >nul

:: Open dashboard in browser
start http://localhost:8888/dashboard.html

echo.
echo Dashboard open! Close this window to disconnect.
pause
