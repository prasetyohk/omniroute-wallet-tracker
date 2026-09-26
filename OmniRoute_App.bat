@echo off
title OmniRoute Desktop App
set "PY_EXE=python"
if exist "%~dp0.venv\Scripts\python.exe" set "PY_EXE=%~dp0.venv\Scripts\python.exe"
"%PY_EXE%" launch_omniroute.py
exit /b 0
