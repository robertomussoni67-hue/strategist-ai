import sys
import os
import pandas as pd
import requests
from datetime import datetime

# 🔧 Aggiunge la cartella src al percorso
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.append(src_path)

from config.env_config import get_api_key

def get_cpi_data():
    """
    Recupera dati CPI reali da FRED. Se la chiave è assente o la rete fallisce,
    usa una simulazione interna.
    """
    try:
        fred_key = get_api_key("fred")
        url = f"https://api.stlouisfed.org/fred/series/observations"
        params = {
            "series_id": "CPIAUCSL",  # CPI All Urban Consumers, USA
            "api_key": fred_key,
            "file_type": "json",
            "observation_start": "2022-01-01"
        }

        response = requests.get(url, params=params)
        data = response.json()

        if "observations" not in data:
            raise ValueError("Dati CPI non disponibili da FRED.")

        # Estrai date e valori
        dates = []
        values = []
        for obs in data["observations"]:
            try:
                value = float(obs["value"])
                date = pd.to_datetime(obs["date"])
                dates.append(date)
                values.append(value)
            except:
                continue

        cpi_series = pd.Series(values, index=dates)
        return cpi_series

    except Exception as e:
        print(f"⚠️ Errore nel recupero CPI da FRED: {e}")
        print("🔁 Uso dati simulati per continuare l'analisi.")

        # Simulazione fallback
        cpi_values = [280.1, 281.3, 282.0, 283.5, 284.2, 285.0, 286.1, 287.4]
        dates = pd.date_range(end=datetime.today(), periods=len(cpi_values), freq='Q')
        return pd.Series(cpi_values, index=dates)