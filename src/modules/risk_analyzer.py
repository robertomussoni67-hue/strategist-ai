import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from src.modules.api_connector import (
    get_price_history,
    get_summary_info
)

TRADING_DAYS = 252

def _normalize_weights(weights: np.ndarray) -> np.ndarray:
    w = np.array(weights, dtype=float)
    if w.sum() == 0:
        return np.zeros_like(w)
    return w / w.sum()

def _daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna()

def compute_max_drawdown(series: pd.Series) -> float:
    # series: equity curve (non returns), e.g., cumulative portfolio value
    running_max = series.cummax()
    drawdown = (series / running_max) - 1.0
    return float(drawdown.min()) if len(drawdown) else 0.0

def compute_portfolio_series(returns_df: pd.DataFrame, weights: np.ndarray) -> pd.Series:
    # weights aligned with columns order
    port_ret = returns_df.dot(weights)
    equity = (1 + port_ret).cumprod()
    return equity

def compute_beta(asset_returns: pd.Series, benchmark_returns: pd.Series) -> float:
    # Align index
    df = pd.concat([asset_returns, benchmark_returns], axis=1).dropna()
    if df.shape[0] < 2:
        return np.nan
    cov = np.cov(df.iloc[:, 0], df.iloc[:, 1])[0, 1]
    var = np.var(df.iloc[:, 1])
    return float(cov / var) if var > 0 else np.nan

def _collect_prices(tickers: list[str], years: int) -> pd.DataFrame:
    price_cols = {}
    for t in tickers:
        hist = get_price_history(t, years=years)
        if not hist.empty:
            price_cols[t] = hist["Adj Close"]
    if not price_cols:
        return pd.DataFrame()
    df = pd.DataFrame(price_cols).dropna()
    return df

def _sector_breakdown(tickers: list[str]) -> dict:
    sectors = {}
    details = {}
    for t in tickers:
        info = get_summary_info(t) or {}
        sector = info.get("sector", "Unknown") or "Unknown"
        sectors[sector] = sectors.get(sector, 0) + 1
        details[t] = {
            "name": info.get("name", ""),
            "sector": sector,
            "industry": info.get("industry", "")
        }
    total = sum(sectors.values()) or 1
    sectors_pct = {k: round(v / total, 4) for k, v in sectors.items()}
    top_sectors = sorted(sectors_pct.items(), key=lambda x: x[1], reverse=True)[:5]
    return {
        "by_count": sectors,
        "by_weight_pct_estimate": sectors_pct,
        "top_sectors": top_sectors,
        "details": details
    }

def analyze_portfolio_risk(plan: list[dict], benchmark: str = "SPY", years: int = 5) -> dict:
    # Considera solo strumenti con prezzo (STOCK/ETF)
    picks = [p for p in plan if p.get("type") in {"STOCK", "ETF"}]
    if not picks:
        return {"error": "Nessun elemento valido nel piano per l'analisi del rischio."}

    tickers = [p["ticker"] for p in picks]
    weights = _normalize_weights([p.get("weight", 0.0) for p in picks])

    # Prezzi storici
    prices = _collect_prices(tickers, years=years)
    if prices.empty:
        return {"error": "Dati storici non disponibili per i tickers del piano."}

    returns = _daily_returns(prices)
    if returns.empty:
        return {"error": "Rendimenti insufficienti per il calcolo."}

    # Serie portafoglio ed equity
    port_equity = compute_portfolio_series(returns, weights)
    port_returns = returns.dot(weights)

    # Metriche rischio-rendimento
    ann_vol = float(port_returns.std() * np.sqrt(TRADING_DAYS))
    ann_ret_geom = float((1 + port_returns.mean())**TRADING_DAYS - 1)  # approssimazione geometrica
    sharpe = float(ann_ret_geom / ann_vol) if ann_vol > 0 else np.nan
    max_dd = compute_max_drawdown(port_equity)

    # Beta vs benchmark
    bench_prices = get_price_history(benchmark, years=years)
    if not bench_prices.empty:
        bench_rets = _daily_returns(bench_prices)["Adj Close"]
        beta = compute_beta(port_returns, bench_rets)
    else:
        beta = np.nan

    # Concentrazione (Herfindahl-Hirschman Index)
    hhi = float(np.sum(np.square(weights)))
    top_positions = sorted(
        [{"ticker": t, "weight": float(w)} for t, w in zip(tickers, weights)],
        key=lambda x: x["weight"],
        reverse=True
    )[:5]

    # Concentrazione settoriale (best-effort, solo per chi espone sector)
    sector_info = _sector_breakdown(tickers)

    # Output
    return {
        "universe_size": len(tickers),
        "period_years": years,
        "benchmark": benchmark,
        "metrics": {
            "annual_return_pct": round(ann_ret_geom * 100, 2),
            "annual_volatility_pct": round(ann_vol * 100, 2),
            "sharpe_ratio": round(sharpe, 2) if not np.isnan(sharpe) else None,
            "max_drawdown_pct": round(max_dd * 100, 2),
            "beta_vs_benchmark": round(beta, 2) if not np.isnan(beta) else None,
            "concentration_hhi": round(hhi, 4)
        },
        "top_positions": top_positions,
        "sectors": sector_info
    }