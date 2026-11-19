import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def detecter_ollama():
    url_env = os.getenv("OLLAMA_BASE_URL")
    if url_env:
        return url_env
    try:
        test = requests.get("http://localhost:11434/api/tags", timeout=1)
        if test.status_code == 200:
            return "http://localhost:11434"
    except Exception:
        pass
    return "http://localhost:11434"

def call_ollama(prompt, model=None, base_url=None, json_mode=True):
    url = ""  #A revoir, à compléter éventuellement
    payload = {"model": model,"prompt": prompt,"stream": False}
    if json_mode:
        payload["format"] = "json"
    try:
        reponse = requests.post(url, json=payload, timeout=60)
        texte = reponse.json().get("response", "{}")
         
        if json_mode :
            return json.loads(texte)
        else:
            return texte

    except Exception as e:
        return {"erreur": f"Impossible de joindre Ollama : {e}"}           