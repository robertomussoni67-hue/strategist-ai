import os
import requests
from dotenv import load_dotenv

# Carica variabili da .env (dove metteremo la API key)
load_dotenv()
AV_KEY = os.getenv("ALPHAVANTAGE_API_KEY", "")

BASE_URL = "https://www.alphavantage.co/query"

def get_free_cash_flow_ttm(ticker: str) -> float | None:
    """
    Recupera il Free Cash Flow TTM da Alpha Vantage
    FCF = Operating Cash Flow - Capital Expenditures
    Restituisce None se i dati non sono disponibili
    """
    if not AV_KEY:
        print("⚠️ Nessuna API key Alpha Vantage trovata in .env")
        return None

    params = {
        "function": "CASH_FLOW",
        "symbol": ticker,
        "apikey": AV_KEY
    }

    try:
        r = requests.get(BASE_URL, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()

        annual_reports = data.get("annualReports", [])
        if not annual_reports:
            return None

        # Prende il report più recente
        latest = annual_reports[0]
        ocf = float(latest.get("operatingCashflow", "0") or 0)
        capex = float(latest.get("capitalExpenditures", "0") or 0)
        fcf = ocf - capex

        return fcf if fcf != 0 else None

    except Exception as e:
        print(f"Errore nel recupero dati Alpha Vantage: {e}")
        return None