import logging

log = logging.getLogger(__name__)

def run():
    # === ETF disponibili ===
    universe = [
        {"ticker": "VWCE.DE", "name": "Vanguard FTSE All-World", "ter": 0.22, "aum": 5000, "style": "global"},
        {"ticker": "IEUR", "name": "iShares Europe ETF", "ter": 0.20, "aum": 3000, "style": "europe"},
        {"ticker": "SPY", "name": "SPDR S&P 500 ETF", "ter": 0.09, "aum": 40000, "style": "us"},
        {"ticker": "AGGH", "name": "iShares Global Aggregate Bond", "ter": 0.10, "aum": 2500, "style": "bonds"},
        {"ticker": "GLD", "name": "SPDR Gold Shares", "ter": 0.40, "aum": 6000, "style": "gold"}
    ]

    # === Filtro base ===
    selected = [etf for etf in universe if etf["ter"] <= 0.25 and etf["aum"] >= 2000]

    log.info(f"[ETF] Universo ETF: {len(universe)} strumenti.")
    log.info(f"[ETF] Selezionati {len(selected)} ETF con TER ≤ 0.25 e AUM ≥ 2000M.")

    return {"etf": selected}