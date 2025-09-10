import yfinance as yf
import requests
import pandas as pd
from datetime import datetime, timedelta
import json # Importa il modulo JSON per gestire l'errore specifico

# Importa i gestori specifici per ogni API
from data_sources.alpha_vantage_retriever import get_historical_data as get_alpha_vantage_history
from data_sources.alpha_vantage_retriever import get_earnings_data as get_alpha_vantage_earnings

# Inserisci qui la tua API key di Finnhub.
FINNHUB_API_KEY = "d2qtsphr01qluccq1v30d2qtsphr01qluccq1v3g"

def get_all_data(ticker, years=1):
    """
    Recupera i dati di un titolo da diverse fonti.
    Prova prima con Yahoo Finance e Finnhub, poi con Alpha Vantage come fallback.
    """
    data = {}
    
    # --- Recupero dati da Yahoo Finance ---
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=years * 365)
        stock_info = yf.Ticker(ticker)
        data['price'] = stock_info.info.get('regularMarketPrice', None)
        history_df = stock_info.history(start=start_date, end=end_date)
        if not history_df.empty:
            data['history'] = history_df
            print(f"✅ Dati storici di Yahoo Finance per {ticker} recuperati.")
        else:
            data['history'] = pd.DataFrame()
            print(f"❌ Nessun dato storico di Yahoo Finance trovato per {ticker}.")

    except Exception as e:
        print(f"❌ Errore durante il recupero dei dati di Yahoo Finance per {ticker}: {e}")
        data['price'] = None
        data['history'] = pd.DataFrame()

    # --- Tentativo di recupero dati finanziari da Finnhub ---
    print(f"\nTentativo di recupero dati finanziari da Finnhub per {ticker}...")
    try:
        # Questo controllo evita di chiamare l'API se la chiave non è impostata
        if FINNHUB_API_KEY and FINNHUB_API_KEY != "YOUR_FINNHUB_API_KEY":
            
            # Recupero ricavi trimestrali
            url_revenues = f"https://finnhub.io/api/v1/stock/revenue?symbol={ticker}&freq=quarterly&token={FINNHUB_API_KEY}"
            try:
                revenues_data = requests.get(url_revenues).json()
                if revenues_data and 'revenue' in revenues_data:
                    revenues = pd.DataFrame(revenues_data['revenue'])
                    revenues['period'] = pd.to_datetime(revenues['period'])
                    revenues.set_index('period', inplace=True)
                    data['revenues'] = revenues['value']
                    print(f"✅ Ricavi trimestrali da Finnhub per {ticker} recuperati.")
            except json.JSONDecodeError:
                print(f"❌ La risposta di Finnhub per i ricavi di {ticker} non è un JSON valido. Potrebbe essere un problema di limite di richieste.")

            # Recupero utili trimestrali
            url_earnings = f"https://finnhub.io/api/v1/stock/earnings?symbol={ticker}&freq=quarterly&token={FINNHUB_API_KEY}"
            try:
                earnings_data = requests.get(url_earnings).json()
                if earnings_data:
                    earnings = pd.DataFrame(earnings_data)
                    earnings['period'] = pd.to_datetime(earnings['period'])
                    earnings.set_index('period', inplace=True)
                    data['earnings'] = earnings['epsActual']
                    print(f"✅ Utili trimestrali da Finnhub per {ticker} recuperati.")
            except json.JSONDecodeError:
                print(f"❌ La risposta di Finnhub per gli utili di {ticker} non è un JSON valido. Potrebbe essere un problema di limite di richieste.")

        else:
            print("❌ La chiave API di Finnhub non è configurata. Saltando il recupero da Finnhub.")

    except Exception as e:
        print(f"❌ Errore durante il recupero dei dati di Finnhub per {ticker}: {e}")
    
    # --- Fallback su Alpha Vantage se i dati finanziari mancano ---
    if 'revenues' not in data or 'earnings' not in data:
        print(f"\nI dati di Finnhub non sono completi. Tentativo di fallback su Alpha Vantage...")
        
        # Recupero utili da Alpha Vantage
        earnings = get_alpha_vantage_earnings(ticker)
        if earnings is not None:
            data['earnings'] = earnings
            print(f"✅ Utili da Alpha Vantage per {ticker} recuperati come fallback.")
        
        # Nota: Alpha Vantage non fornisce i ricavi in modo separato e gratuito,
        # quindi ci concentriamo sugli utili.
    
    return data

