import yfinance as yf
import pandas as pd

def fetch_prices(ticker: str, period: str = "2y", interval: str = "1d") -> pd.DataFrame:
    tk = yf.Ticker(ticker)
    df = tk.history(period=period, interval=interval, auto_adjust=True)
    if df.empty:
        raise ValueError(f"Nessun dato prezzo per {ticker}")
    return df

def fetch_market_prices(market: str = "^GSPC", period: str = "2y", interval: str = "1d") -> pd.DataFrame:
    df = yf.download(market, period=period, interval=interval, auto_adjust=True, progress=False)
    if df.empty:
        raise ValueError(f"Nessun dato indice per {market}")
    return df

def fetch_shares_outstanding(ticker: str) -> int | None:
    info = yf.Ticker(ticker).fast_info
    return getattr(info, "shares", None)