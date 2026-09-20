@echo off
title Hentikan OmniRoute
color 0A

echo ================================================================
echo                   MENGHENTIKAN OMNIROUTE
echo ================================================================
echo.

:: 1. Tutup jendela aplikasi OmniRoute (Chrome, Edge, Brave) jika masih terbuka
echo [*] Menutup jendela aplikasi OmniRoute...
powershell -NoProfile -Command "Get-Process chrome, msedge, brave -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like '*OmniRoute*' } | ForEach-Object { $_.CloseMainWindow() }" >nul 2>&1

:: 2. Hentikan server backend pada port 5000
set FOUND=0
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr /r ":5000 .*LISTENING"') do (
    echo [*] Menghentikan proses server PID %%a...
    taskkill /F /PID %%a >nul 2>&1
    set FOUND=1
)

echo.
if %FOUND%==1 (
    echo [OK] Aplikasi dan server OmniRoute berhasil ditutup dengan bersih.
) else (
    echo [OK] Server OmniRoute sudah tidak aktif.
)

echo.
timeout /t 2 >nul
exit /b 0
