# yahoo_source.py
import yfinance as yf

def get_prices(tickers=["AAPL", "MSFT", "ENI.MI"]):
    """
    Restituisce un dizionario con i prezzi correnti per la lista di ticker.
    """
    try:
        dati = yf.download(tickers, period="1d", interval="1m")
        risultati = {}
        for ticker in tickers:
            last_price = dati["Close"][ticker].dropna().iloc[-1]
            risultati[ticker] = round(last_price, 2)
        return risultati
    except Exception as e:
        print(f"Errore yahoo_source: {e}")
        return {}

# Test veloce
if __name__ == "__main__":
    prezzi = get_prices()
    for simbolo, valore in prezzi.items():
        print(f"{simbolo}: {valore}")