import yfinance as yf
import pandas as pd
import json
from datetime import date
from modules.macro_module import execute_macro, get_latest_news

# Nota: per eseguire questo codice, è necessario installare le librerie yfinance, pandas e requests.
# Puoi farlo con il seguente comando da terminale:
# pip install yfinance pandas requests

def get_macro_data(ticker="^GSPC", period="1y", interval="1d"):
    """
    Scarica i dati storici di un indice di mercato come l'S&P 500.

    Args:
        ticker (str): Il ticker dell'asset. Default è "^GSPC" (S&P 500).
        period (str): L'intervallo di tempo (es. "1y", "5y", "max").
        interval (str): La frequenza dei dati (es. "1d", "1wk").

    Returns:
        pd.DataFrame: Un DataFrame con i dati storici (Close, Volume, ecc.).
    """
    try:
        data = yf.download(ticker, period=period, interval=interval)
        if data.empty:
            print(f"⚠️ Dati non disponibili per il ticker {ticker}. Restituisco un DataFrame vuoto.")
            return pd.DataFrame()
        print(f"✅ Dati macro storici per {ticker} recuperati con successo.")
        return data
    except Exception as e:
        print(f"❌ Errore durante il recupero dei dati per {ticker}: {e}")
        return pd.DataFrame()

def analyze_cpi():
    """
    Simula l'analisi dell'indice dei prezzi al consumo (CPI).
    
    Questa funzione è un segnaposto che in futuro potrebbe
    essere integrata con l'analisi macro più completa.
    """
    print("⏳ Simulazione di recupero dati CPI...")
    return "inflazione_stabile"

def get_latest_economic_news(num_articles=3):
    """
    Recupera le ultime notizie economiche utilizzando una funzione dedicata.
    """
    print("⏳ Recupero notizie economiche in corso...")
    # Ora usiamo una funzione reale dal modulo macro
    news = get_latest_news()
    return news[:num_articles]

def main():
    """
    Esegue un'analisi di prova del modulo macro.
    """
    print("--- Test del Modulo 'macro_analysis' ---")
    
    # 1. Test del recupero dati storici
    sp500_data = get_macro_data(ticker="^GSPC", period="6mo")
    if not sp500_data.empty:
        print("\nAnteprima dati S&P 500:")
        print(sp500_data.tail())

    # 2. Test dell'analisi CPI (simulato)
    cpi_signal = analyze_cpi()
    print(f"\nSegnale CPI simulato: {cpi_signal}")

    # 3. Test del recupero notizie
    news = get_latest_economic_news()
    print("\nUltime notizie economiche:")
    for article in news:
        print(f"- {article}")

    print("\n--- Test Completato ---")

if __name__ == "__main__":
    main()

