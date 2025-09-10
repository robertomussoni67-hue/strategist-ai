import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def backtest_plan(plan, start_years_ago=5):
    tickers_weights = [(p["ticker"], p["weight"]) for p in plan if p["type"] in ["STOCK", "ETF"]]
    if not tickers_weights:
        return {"error": "Nessun ticker valido nel piano."}

    end_date = datetime.today()
    start_date = end_date - timedelta(days=365 * start_years_ago)

    prices = {}
    for ticker, _ in tickers_weights:
        try:
            data = yf.download(ticker, start=start_date, end=end_date)["Adj Close"]
            prices[ticker] = data
        except Exception:
            continue

    df = pd.DataFrame(prices).dropna()
    if df.empty:
        return {"error": "Dati storici non disponibili."}

    # Calcolo rendimento giornaliero
    returns = df.pct_change().dropna()

    # Calcolo rendimento aggregato del portafoglio
    weights = np.array([w for _, w in tickers_weights])
    weights /= weights.sum()  # normalizza
    portfolio_returns = returns.dot(weights)

    # Metriche
    cumulative_return = (1 + portfolio_returns).prod() - 1
    cagr = (1 + cumulative_return) ** (1 / start_years_ago) - 1
    volatility = portfolio_returns.std() * np.sqrt(252)
    sharpe = cagr / volatility if volatility > 0 else 0
    max_drawdown = (df / df.cummax()).min().min() - 1

    return {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "cagr": round(cagr * 100, 2),
        "volatility": round(volatility * 100, 2),
        "sharpe_ratio": round(sharpe, 2),
        "max_drawdown": round(max_drawdown * 100, 2)
    }