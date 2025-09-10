import yfinance as yf
import pandas as pd

def safe_download(ticker, period="1y", interval="1d"):
    """
    Scarica i dati storici per un ticker in modo sicuro, gestendo gli errori.
    Restituisce un DataFrame o None in caso di errore.
    """
    try:
        data = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)
        if data.empty:
            print(f"⚠️ Dati storici non disponibili per '{ticker}'.")
            return None
        return data
    except Exception as e:
        print(f"❌ Errore durante il download dei dati per '{ticker}': {e}")
        return None

def safe_get_info(ticker):
    """
    Recupera le informazioni di base per un ticker in modo sicuro.
    Restituisce un dizionario o None in caso di errore.
    """
    try:
        info = yf.Ticker(ticker).info
        if not info:
            print(f"⚠️ Informazioni non disponibili per '{ticker}'.")
            return None
        return info
    except Exception as e:
        print(f"❌ Errore durante il recupero info per '{ticker}': {e}")
        return None

def safe_get_quarterly_financials(ticker):
    """
    Recupera i dati finanziari trimestrali per un ticker in modo sicuro.
    Restituisce un DataFrame o None in caso di errore.
    """
    try:
        t = yf.Ticker(ticker)
        df = t.quarterly_financials
        if df.empty:
            print(f"⚠️ Dati finanziari trimestrali non disponibili per '{ticker}'.")
            return None
        return df
    except Exception as e:
        print(f"❌ Errore durante il recupero dati finanziari per '{ticker}': {e}")
        return None
