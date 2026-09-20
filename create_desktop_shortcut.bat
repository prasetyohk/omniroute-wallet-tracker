@echo off
title Buat Shortcut Desktop OmniRoute
cd /d "%~dp0"

powershell -ExecutionPolicy Bypass -File "%~dp0create_desktop_shortcut.ps1"

echo.
pause
