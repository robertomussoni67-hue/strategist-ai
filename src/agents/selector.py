import datetime
from agents.guru_strategy import guru_strategy, guru_filters

def selector(regime, goal, fiscal_profile):
    """
    Seleziona ETF e titoli azionari coerenti con regime macro, obiettivo e fiscalità.
    """
    allowed_domiciles = ["Irlanda", "Lussemburgo"]
    max_ter = 0.6

    # Attiva strategia dei guru
    gurus = guru_strategy(regime, goal)
    criteria = guru_filters(gurus)
    print("Strategia attiva:", gurus)
    print("Criteri di selezione:", criteria)

    etf_db = [
        {
            "name": "Vanguard FTSE All-World High Dividend Yield",
            "ticker": "VHYL",
            "domicile": "Irlanda",
            "ter": 0.29,
            "distribution": "trimestrale",
            "strategy": "dividendo globale",
            "regime_match": ["defensive", "neutral"],
            "goal_match": ["rendita", "protezione"]
        },
        {
            "name": "iShares MSCI World UCITS ETF",
            "ticker": "SWDA",
            "domicile": "Irlanda",
            "ter": 0.20,
            "distribution": "accumulazione",
            "strategy": "growth globale",
            "regime_match": ["growth"],
            "goal_match": ["accumulo", "crescita"]
        },
        {
            "name": "SPDR S&P Global Dividend Aristocrats",
            "ticker": "GBDV",
            "domicile": "Lussemburgo",
            "ter": 0.45,
            "distribution": "trimestrale",
            "strategy": "dividendi aristocratici",
            "regime_match": ["defensive", "neutral"],
            "goal_match": ["rendita", "protezione"]
        }
    ]

    stock_db = [
        {
            "name": "Johnson & Johnson",
            "ticker": "JNJ",
            "dividend": "trimestrale",
            "sector": "Healthcare",
            "price": 58,
            "regime_match": ["defensive", "neutral"],
            "goal_match": ["rendita", "protezione"]
        },
        {
            "name": "Nvidia",
            "ticker": "NVDA",
            "dividend": "accumulazione",
            "sector": "Tech",
            "price": 59,
            "regime_match": ["growth"],
            "goal_match": ["accumulo", "crescita"]
        },
        {
            "name": "Coca-Cola",
            "ticker": "KO",
            "dividend": "trimestrale",
            "sector": "Consumer Staples",
            "price": 55,
            "regime_match": ["defensive"],
            "goal_match": ["rendita", "protezione"]
        }
    ]

    selected_etf = [
        etf for etf in etf_db
        if etf["domicile"] in allowed_domiciles
        and etf["ter"] <= max_ter
        and regime in etf["regime_match"]
        and goal in etf["goal_match"]
    ]

    selected_stocks = [
        stock for stock in stock_db
        if regime in stock["regime_match"]
        and goal in stock["goal_match"]
        and stock["price"] <= 60
    ]

    return {
        "timestamp": str(datetime.date.today()),
        "regime": regime,
        "goal": goal,
        "fiscal_profile": fiscal_profile,
        "strategy": gurus,
        "etf": selected_etf,
        "stocks": selected_stocks
    }
📁 2. etf_filter.py
python
import datetime

def validate_etf(etf):
    dividend_history = {
        "VHYL": [0.45, 0.47, 0.44, 0.46],
        "SWDA": [],
        "GBDV": [0.38, 0.39, 0.40, 0.41]
    }

    holdings_quality = {
        "VHYL": ["Nestlé", "J&J", "PepsiCo"],
        "SWDA": ["Apple", "Microsoft", "Amazon"],
        "GBDV": ["Coca-Cola", "McDonald's", "3M"]
    }

    healthy_companies = {"Nestlé", "J&J", "PepsiCo", "Coca-Cola", "McDonald's", "3M"}

    ticker = etf["ticker"]
    dividends = dividend_history.get(ticker, [])
    holdings = holdings_quality.get(ticker, [])

    has_dividends = len(dividends) >= 4 and all(d > 0 for d in dividends)
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
    return [validate_etf(etf) for etf in etf_list]
📁 3. guru_strategy.py
python
def guru_strategy(regime, goal):
    strategy_map = {
        ("growth", "accumulo"): ["Buffett", "Wood"],
        ("growth", "speculazione"): ["Soros", "Wood"],
        ("growth", "crescita"): ["Buffett", "Munger"],
        ("defensive", "protezione"): ["Dalio", "Graham", "Klarman"],
        ("defensive", "rendita"): ["Buffett", "Munger", "Graham"],
        ("neutral", "rendita"): ["Buffett", "Munger"],
        ("neutral", "accumulo"): ["Buffett", "Dalio"],
        ("neutral", "protezione"): ["Dalio", "Klarman"]
    }
    return strategy_map.get((regime, goal), ["Dalio"])

def guru_filters(guru_list):
    filters = []
    for guru in guru_list:
        if guru == "Buffett":
            filters.append({"type": "value", "roe_min": 10, "moat": True})
        elif guru == "Graham":
            filters.append({"type": "deep_value", "pe_max": 15, "pb_max": 1})
        elif guru == "Dalio":
            filters.append({"type": "diversified", "asset_mix": ["stocks", "bonds", "gold"]})
        elif guru == "Soros":
            filters.append({"type": "macro", "theme": "event-driven"})
        elif guru == "Klarman":
            filters.append({"type": "contrarian", "sector_ignored": ["tech"], "volatility_max": 0.3})
        elif guru == "Munger":
            filters.append({"type": "quality", "moat": True, "debt_max": 0.5})
        elif guru == "Wood":
            filters.append({"type": "innovation", "sector": "tech", "growth_min": 15})
    return filters
    