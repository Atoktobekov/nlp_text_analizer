# backend/app/model_setup.py
import importlib
import subprocess
import sys

def ensure_spacy_model(model_name="en_core_web_sm"):
    try:
        importlib.import_module(model_name)
        return True
    except Exception:
        # try to download
        subprocess.run([sys.executable, "-m", "spacy", "download", model_name], check=True)
        return True

if __name__ == "__main__":
    ensure_spacy_model()
