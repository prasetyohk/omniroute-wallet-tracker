import os
import sys
import time
import socket
import subprocess
import urllib.request
from pathlib import Path

WORKSPACE_DIR = Path(__file__).resolve().parent
APP_URL = "http://127.0.0.1:5000"
PORT = 5000

def is_server_running(host="127.0.0.1", port=PORT, timeout=0.8):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (OSError, ConnectionRefusedError):
        return False

def find_browser():
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
    program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")

    candidates = [
        # Google Chrome
        Path(program_files_x86) / "Google" / "Chrome" / "Application" / "chrome.exe",
        Path(program_files) / "Google" / "Chrome" / "Application" / "chrome.exe",
        Path(local_app_data) / "Google" / "Chrome" / "Application" / "chrome.exe",
        # Brave Browser
        Path(program_files) / "BraveSoftware" / "Brave-Browser" / "Application" / "brave.exe",
        Path(program_files_x86) / "BraveSoftware" / "Brave-Browser" / "Application" / "brave.exe",
        # Microsoft Edge
        Path(program_files_x86) / "Microsoft" / "Edge" / "Application" / "msedge.exe",
        Path(program_files) / "Microsoft" / "Edge" / "Application" / "msedge.exe",
    ]

    for p in candidates:
        if p.is_file():
            return str(p)
    return None

def start_flask_server():
    if is_server_running():
        return

    # Use python executable with redirected logs so it never fails or crashes
    python_exe = sys.executable
    app_py = str(WORKSPACE_DIR / "app.py")
    log_file_path = WORKSPACE_DIR / "omniroute_server.log"
    log_file = open(log_file_path, "a", encoding="utf-8")

    creation_flags = 0
    if os.name == "nt":
        DETACHED_PROCESS = 0x00000008
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        CREATE_NO_WINDOW = 0x08000000
        creation_flags = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW

    subprocess.Popen(
        [python_exe, app_py],
        cwd=str(WORKSPACE_DIR),
        stdout=log_file,
        stderr=log_file,
        creationflags=creation_flags,
        close_fds=True
    )

    # Wait up to 10 seconds for server to be fully ready and responding
    for _ in range(30):
        time.sleep(0.3)
        if is_server_running():
            try:
                with urllib.request.urlopen(APP_URL, timeout=1) as resp:
                    if resp.status == 200:
                        break
            except Exception:
                pass

def launch_app_window():
    start_flask_server()

    browser_exe = find_browser()
    if browser_exe:
        # Launch in native App Mode: clean dedicated window, NO address bar, NO tabs, NO user-data-dir conflicts
        cmd = [
            browser_exe,
            f"--app={APP_URL}",
            "--window-size=1440,900",
            "--window-position=100,50"
        ]
        subprocess.Popen(cmd)
    else:
        # Fallback to default OS browser
        import webbrowser
        webbrowser.open(APP_URL)

if __name__ == "__main__":
    launch_app_window()
