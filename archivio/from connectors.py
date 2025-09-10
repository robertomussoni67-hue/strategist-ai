from connectors.alpha_vantage import get_free_cash_flow_ttm

# Lista di ticker che vuoi analizzare
tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "META"]

# Stampa intestazione tabella
print(f"{'Ticker':<8} | {'Free Cash Flow TTM (USD)':>25}")
print("-" * 36)

for ticker in tickers:
    fcf = get_free_cash_flow_ttm(ticker)
    if fcf is None:
        print(f"{ticker:<8} | {'N/D':>25}")
    else:
        print(f"{ticker:<8} | {fcf:>25,.2f}")