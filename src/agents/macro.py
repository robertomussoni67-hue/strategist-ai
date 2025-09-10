import logging
import datetime
import yfinance as yf
import pandas as pd
import numpy as np

log = logging.getLogger(__name__)

def to_float(value):
    """Converte qualsiasi tipo compatibile in float, evitando warning e errori."""
    try:
        # Se è una Series, prendi il primo elemento valido
        if isinstance(value, pd.Series):
            value = value.dropna()
            if value.empty:
                return None
            return float(value.iloc[0])
        # Se è una lista o array, prendi il primo elemento
        if isinstance(value, (np.ndarray, list)):
            if pd.isna(value[0]):
                return None
            return float(value[0])
        # Se è già scalare
        if pd.isna(value):
            return None
        return float(value)
    except Exception as e:
        log.warning(f"[Macro] Errore in to_float(): {e}")
        return None

def run_macro_analysis():
    """
    Analisi macro basata sulla SMA a 200 giorni dell'S&P 500 (SPY).
    Ritorna uno tra: 'growth' | 'defensive' | 'neutral'
    """
    log.info("[Macro] Avvio analisi macroeconomica (SMA 200 su SPY)")

    ticker = "SPY"
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365)

    try:
        data = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            progress=False,
            auto_adjust=False
        )

        if data is None or data.empty or "Close" not in data.columns:
            log.warning("[Macro] Dati SPY non disponibili/incompleti. Regime 'neutral'.")
            return "neutral"

        data["SMA_200"] = data["Close"].rolling(window=200, min_periods=200).mean()

        latest_close = to_float(data["Close"].iloc[-1])
        latest_sma = to_float(data["SMA_200"].iloc[-1])

        if latest_close is None or latest_sma is None:
            regime = "neutral"
        else:
            regime = "growth" if latest_close > latest_sma else "defensive"

        try:
            sma_str = "NaN" if latest_sma is None else f"{latest_sma:.2f}"
            log.info(f"[Macro] SPY Close: {latest_close:.2f} | SMA200: {sma_str} | Regime: {regime.upper()}")
        except Exception:
            log.info(f"[Macro] Regime: {regime.upper()}")

        return regime

    except Exception:
        log.error("[Macro] Errore durante il download/analisi dati. Regime 'neutral'.", exc_info=True)
        return "neutral"

async def run():
    regime = run_macro_analysis()
    return {
        "regime": regime,
        "source": "SPY",
        "method": "SMA_200",
        "timestamp": str(datetime.date.today())
    }