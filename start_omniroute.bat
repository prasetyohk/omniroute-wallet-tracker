@echo off
title OmniRoute - Cross-Chain Swap & Bridge Target Tracker (Built by Prasetyo HK)
color 0A

echo ================================================================
echo           OMNIROUTE - CROSS-CHAIN TARGET WALLET TRACKER
echo             Relay.link ^| Li.Fi ^| Jumper ^| Across ^| LayerZero
echo                     Built by Prasetyo HK
echo      X: https://x.com/Prasetyo_HK  ^|  GitHub: prasetyohk
echo ================================================================
echo.

cd /d "%~dp0"

set "PY_EXE=python"
if exist "%~dp0.venv\Scripts\python.exe" (
    set "PY_EXE=%~dp0.venv\Scripts\python.exe"
) else (
    where python >nul 2>nul
    if %errorlevel% neq 0 (
        echo [ERROR] Python tidak ditemukan di sistem Anda!
        echo Pastikan Python sudah terinstall dan opsi "Add Python to PATH" dicentang.
        echo.
        pause
        exit /b 1
    )
)

echo [*] Membuka browser ke http://127.0.0.1:5000 ...
start http://127.0.0.1:5000

echo [*] Menjalankan server lokal OmniRoute di http://127.0.0.1:5000 ...
echo [*] Jangan tutup jendela terminal ini selama menggunakan website.
echo [*] Tekan Ctrl+C jika ingin menghentikan server.
echo.

"%PY_EXE%" app.py

if %errorlevel% neq 0 (
    echo.
    echo [!] Server terhenti atau terjadi error.
    pause
)
