import yfinance as yf
from datetime import datetime, timedelta
import os
import json

# Percorso del file di cache
CACHE_FILE = "cache.json"
# Durata della cache in minuti
CACHE_DURATION_MINUTES = 30

def _get_cache():
    """Carica la cache dal file, se esiste."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def _save_cache(cache_data):
    """Salva la cache sul file."""
    with open(CACHE_FILE, "w") as f:
        json.dump(cache_data, f, indent=4)

def get_price_yahoo(ticker: str):
    """
    Restituisce il prezzo corrente di un asset da Yahoo Finance, usando una cache per limitare le chiamate API.
    """
    cache = _get_cache()
    now = datetime.now()
    cache_key = f"price_{ticker}"

    # Controlla se il prezzo è già in cache e se è ancora valido
    if cache_key in cache and (now - datetime.fromtimestamp(cache[cache_key]["timestamp"])) < timedelta(minutes=CACHE_DURATION_MINUTES):
        print(f"✅ Prezzo di {ticker} recuperato da cache.")
        return cache[cache_key]["data"]

    try:
        asset = yf.Ticker(ticker)
        price = asset.history(period="1d")["Close"].iloc[-1]
        
        # Aggiorna la cache
        cache[cache_key] = {"data": price, "timestamp": now.timestamp()}
        _save_cache(cache)
        
        return price
    except Exception as e:
        print(f"❌ Errore nel recupero dati da Yahoo Finance per {ticker}: {e}")
        return None

def get_historical_data_and_financials(ticker: str, years: int = 5):
    """
    Restituisce i dati storici, i ricavi e gli utili trimestrali di un titolo.
    """
    try:
        asset = yf.Ticker(ticker)
        
        # Dati storici
        start_date = datetime.now() - timedelta(days=years * 365)
        history = asset.history(start=start_date.strftime('%Y-%m-%d'))
        
        # Dati finanziari trimestrali
        quarterly_financials = asset.quarterly_financials
        quarterly_earnings = asset.quarterly_earnings
        
        # Estrai ricavi e utili
        revenues = quarterly_financials.loc['Total Revenue'].iloc[::-1] if 'Total Revenue' in quarterly_financials.index else None
        earnings = quarterly_earnings.iloc[0].iloc[::-1] if not quarterly_earnings.empty else None

        return {
            'history': history,
            'revenues': revenues,
            'earnings': earnings
        }
    except Exception as e:
        print(f"❌ Errore nel recupero dati storici per {ticker}: {e}")
        return None

if __name__ == "__main__":
    symbol = "AAPL"
    prezzo = get_price_yahoo(symbol)
    if prezzo:
        print(f"Prezzo {symbol}: {prezzo:.2f} USD")
    else:
        print("Dati non disponibili.")
    
    dati_storici = get_historical_data_and_financials(symbol)
    if dati_storici:
        print("\nDati storici recuperati.")
        print("Ricavi trimestrali:\n", dati_storici['revenues'])
        print("\nUtili trimestrali:\n", dati_storici['earnings'])