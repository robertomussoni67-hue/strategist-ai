def guru_strategy(regime, goal):
    """
    Attiva strategie coerenti con il regime macro e l'obiettivo finanziario.
    Restituisce una lista di guru da applicare alla selezione.
    """
    strategy_map = {
        ("growth", "accumulo"): ["Buffett", "Wood"],
        ("growth", "speculazione"): ["Soros", "Wood"],
        ("growth", "crescita"): ["Buffett", "Munger"],
        ("defensive", "protezione"): ["Dalio", "Graham", "Klarman"],
        ("defensive", "rendita"): ["Buffett", "Munger", "Graham"],
        ("neutral", "rendita"): ["Buffett", "Munger"],
        ("neutral", "accumulo"): ["Buffett", "Dalio"],
        ("neutral", "protezione"): ["Dalio", "Klarman"],
    }

    return strategy_map.get((regime, goal), ["Dalio"])  # Default fallback

def guru_filters(guru_list):
    """
    Restituisce criteri di selezione associati ai guru.
    """
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