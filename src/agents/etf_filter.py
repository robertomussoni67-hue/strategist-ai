import datetime

def validate_etf(etf):
    """
    Valida un singolo ETF in base a criteri di distribuzione e qualità sottostante.
    """
    # Simulazione dati storici di distribuzione (in realtà da API o scraping)
    dividend_history = {
        "VHYL": [0.45, 0.47, 0.44, 0.46],  # trimestrali costanti
        "SWDA": [],  # ETF ad accumulazione
        "GBDV": [0.38, 0.39, 0.40, 0.41],
        "ARKK": []  # ETF growth, no distribuzione
    }

    # Simulazione qualità aziende sottostanti
    holdings_quality = {
        "VHYL": ["Nestlé", "J&J", "PepsiCo"],
        "SWDA": ["Apple", "Microsoft", "Amazon"],
        "GBDV": ["Coca-Cola", "McDonald's", "3M"],
        "ARKK": ["Roku", "Teladoc", "Zoom"]
    }

    # Simulazione aziende sane (in realtà da bilanci)
    healthy_companies = {"Nestlé", "J&J", "PepsiCo", "Coca-Cola", "McDonald's", "3M"}

    ticker = etf["ticker"]
    dividends = dividend_history.get(ticker, [])
    holdings = holdings_quality.get(ticker, [])

    # Verifica distribuzione costante
    has_dividends = len(dividends) >= 4 and all(d > 0 for d in dividends)

    # Verifica aziende sane
    healthy_holdings = [h for h in holdings if h in healthy_companies]
    quality_score = len(healthy_holdings) / max(len(holdings), 1)

    return {
        "ticker": ticker,
        "name": etf["name"],
        "distribution_ok": has_dividends,
        "quality_score": round(quality_score, 2),
        "strategy": etf["strategy"],
        "ter": etf["ter"],
        "domicile": etf["domicile"],
        "timestamp": str(datetime.date.today())
    }

def filter_etf_list(etf_list):
    """
    Applica la validazione a una lista di ETF.
    """
    return [validate_etf(etf) for etf in etf_list]