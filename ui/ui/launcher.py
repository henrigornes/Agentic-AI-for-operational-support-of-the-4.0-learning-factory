import ctypes
import os
import shutil
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path

# --- CONFIGURATION ---
APP_FILE = "uiPoC1.py"
PORT = 8501


EXPLICIT_PYTHON_PATH = r"C:\Users\henri\AppData\Local\Python\pythoncore-3.15-64\python.exe"

def get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def find_real_python(base_dir: Path) -> Path | None:
    # 1. Chemin explicite configuré en haut du fichier
    if EXPLICIT_PYTHON_PATH:
        p = Path(EXPLICIT_PYTHON_PATH)
        if p.exists() and p.name.lower() == "python.exe":
            return p

    # 2. Si lancé via un vrai python.exe (non compilé)
    if not getattr(sys, "frozen", False):
        exe = Path(sys.executable)
        if exe.name.lower() == "python.exe":
            return exe

    # 3. Recherche d'un dossier venv / .venv en remontant vers la racine du projet
    for parent in [base_dir, *base_dir.parents]:
        for folder in ["venv", ".venv", "env"]:
            candidate = parent / folder / "Scripts" / "python.exe"
            if candidate.exists():
                return candidate

    # 4. Recherche du python.exe installé dans le PATH Windows
    which_py = shutil.which("python")
    if which_py:
        p = Path(which_py)
        # Vérifie que ce n'est pas le faux alias du Microsoft Store (WindowsApps)
        if p.exists() and "WindowsApps" not in str(p):
            return p

    return None


def wait_for_streamlit(url: str, timeout: int = 20) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=1) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(0.4)
    return False


def find_browser() -> str | None:
    paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None


def main():
    base_dir = get_base_dir()
    os.chdir(base_dir)

    python_exe = find_real_python(base_dir)

    # Garde-fou anti-boucle : refuse d'exécuter quoi que ce soit d'autre qu'un vrai python.exe
    if not python_exe or not python_exe.exists() or python_exe.name.lower() != "python.exe":
        ctypes.windll.user32.MessageBoxW(
            0,
            "Impossible de trouver un interpréteur python.exe valide.\nRenseignez EXPLICIT_PYTHON_PATH dans launcher.py.",
            "Erreur de lancement",
            0x10,
        )
        sys.exit(1)

    url = f"http://localhost:{PORT}"

    cmd = [
        str(python_exe),
        "-m",
        "streamlit",
        "run",
        APP_FILE,
        f"--server.port={PORT}",
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
    ]

    creation_flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    server = subprocess.Popen(
        cmd,
        cwd=str(base_dir),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=creation_flags,
    )

    try:
        if not wait_for_streamlit(url):
            raise RuntimeError("Délai dépassé : Streamlit n'a pas répondu.")

        browser = find_browser()
        if browser:
            profile_dir = base_dir / ".app_profile"
            subprocess.run([
                browser,
                f"--app={url}",
                f"--user-data-dir={profile_dir}",
                "--window-size=1280,850",
            ])
        else:
            webbrowser.open(url)
            server.wait()

    finally:
        server.terminate()
        try:
            server.wait(timeout=3)
        except subprocess.TimeoutExpired:
            server.kill()


if __name__ == "__main__":
    main()