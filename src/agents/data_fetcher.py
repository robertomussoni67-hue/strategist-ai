import requests
from config.env_config import get_api_key

ALPHA_VANTAGE_KEY = get_api_key("1H")
FINNHUB_KEY = get_api_key("d2tel0pr01qr5a729tmgd2tel0pr01qr5a729tn0")

# TITOLI AZIONARI

def get_stock_overview_alpha(ticker):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={ALPHA_VANTAGE_KEY}"
    response = requests.get(url)
    return response.json()

def get_price_alpha(ticker):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={ALPHA_VANTAGE_KEY}"
    response = requests.get(url)
    data = response.json()
    try:
        return float(data["Global Quote"]["05. price"])
    except:
        return None

def fetch_stock_data(ticker):
    overview = get_stock_overview_alpha(ticker)
    price = get_price_alpha(ticker)
    return {
        "ticker": ticker,
        "name": overview.get("Name"),
        "sector": overview.get("Sector"),
        "roe": overview.get("ReturnOnEquityTTM"),
        "payout_ratio": overview.get("DividendPayoutRatio"),
        "price": price
    }

# ETF

def get_etf_holdings_finnhub(ticker):
    url = f"https://finnhub.io/api/v1/etf/holdings?symbol={ticker}&token={FINNHUB_KEY}"
    response = requests.get(url)
    return response.json().get("holdings", [])

def get_dividends_finnhub(ticker):
    url = f"https://finnhub.io/api/v1/stock/dividend?symbol={ticker}&token={FINNHUB_KEY}"
    response = requests.get(url)
    return response.json()

def fetch_etf_data(ticker):
    holdings = get_etf_holdings_finnhub(ticker)
    dividends = get_dividends_finnhub(ticker)
    return {
        "ticker": ticker,
        "holdings": holdings,
        "dividends": dividends
    }