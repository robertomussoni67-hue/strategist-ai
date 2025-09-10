from connectors.alpha_vantage import get_free_cash_flow_ttm

ticker = "AAPL"  # oppure un altro titolo che ti serve
fcf = get_free_cash_flow_ttm(ticker)

if fcf is None:
    print(f"[ATTENZIONE] Nessun dato disponibile per {ticker}.")
else:
    print(f"Free Cash Flow TTM per {ticker}: {fcf:,.2f} USD")