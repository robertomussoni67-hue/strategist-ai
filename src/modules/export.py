import json
import os
from datetime import datetime
import logging

log = logging.getLogger(__name__)

def save_json(data, folder="reports", prefix="strategist_report"):
    """
    Salva i dati in formato JSON nella cartella specificata.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.json"
    path = os.path.join(folder, filename)

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        log.info(f"[Export] Report salvato in: {path}")
        return path
    except Exception as e:
        log.error(f"[Export] Errore nel salvataggio: {e}")
        return None