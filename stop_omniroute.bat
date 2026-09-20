@echo off
title Hentikan OmniRoute Server
color 0A

echo ================================================================
echo               MENGHENTIKAN SERVER OMNIROUTE
echo ================================================================
echo.

set FOUND=0
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr /r ":5000 .*LISTENING"') do (
    echo [*] Menghentikan proses server PID %%a pada port 5000...
    taskkill /F /PID %%a >nul 2>&1
    set FOUND=1
)

if %FOUND%==1 (
    echo.
    echo [OK] Server OmniRoute berhasil dihentikan.
) else (
    echo [*] Tidak ada server OmniRoute yang sedang aktif pada port 5000.
)

echo.
timeout /t 2 >nul
exit /b 0
