import os
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path

# --- CONFIGURATION ---
APP_FILE = "uiPoC1.py" 
PORT = 8501


def get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def is_server_ready(url: str, timeout: int = 20) -> bool:
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return True
        except Exception:
            time.sleep(0.5)
    return False


def find_browser_app_mode() -> str | None:
    possible_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None


def main():
    base_dir = get_base_dir()
    os.chdir(base_dir)

    # Pointe directement vers le python du venv
    venv_python = base_dir / "dist" / "venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        import ctypes

        ctypes.windll.user32.MessageBoxW(
            0,
            f"Dossier 'venv' introuvable dans :\n{base_dir}\n\nAssurez-vous que le .exe est à la racine du projet.",
            "Erreur",
            0x10,
        )
        sys.exit(1)

    url = f"http://localhost:{PORT}"
    creation_flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0

    # Lancement unique de Streamlit en arrière-plan
    streamlit_cmd = [
        str(venv_python),
        "-m",
        "streamlit",
        "run",
        APP_FILE,
        f"--server.port={PORT}",
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
    ]

    server_process = subprocess.Popen(
        streamlit_cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=creation_flags,
    )

    try:
        if not is_server_ready(url):
            raise RuntimeError("Le serveur n'a pas démarré.")

        browser_path = find_browser_app_mode()
        if browser_path:
            profile_dir = base_dir / ".app_profile"
            app_cmd = [
                browser_path,
                f"--app={url}",
                f"--user-data-dir={profile_dir}",
                "--window-size=1280,850",
            ]
            # Bloque l'exécution tant que la fenêtre de l'app reste ouverte
            subprocess.run(app_cmd)
        else:
            webbrowser.open(url)
            server_process.wait()

    finally:
        # Fermeture propre du serveur dès qu'on ferme l'application
        server_process.terminate()
        try:
            server_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            server_process.kill()


if __name__ == "__main__":
    main()