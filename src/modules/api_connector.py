import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_price_history(ticker, years=5):
    end = datetime.today()
    start = end - timedelta(days=365 * years)
    try:
        df = yf.download(ticker, start=start, end=end)
        return df[["Adj Close"]].dropna()
    except Exception as e:
        return pd.DataFrame()

def get_latest_price(ticker):
    try:
        data = yf.Ticker(ticker).history(period="1d")
        return data["Close"].iloc[-1]
    except Exception:
        return None

def get_summary_info(ticker):
    try:
        info = yf.Ticker(ticker).info
        return {
            "name": info.get("longName", ""),
            "sector": info.get("sector", ""),
            "industry": info.get("industry", ""),
            "marketCap": info.get("marketCap", ""),
            "peRatio": info.get("trailingPE", ""),
            "dividendYield": info.get("dividendYield", ""),
            "beta": info.get("beta", "")
        }
    except Exception:
        return {}