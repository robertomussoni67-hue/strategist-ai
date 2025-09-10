# src/modules/philosophy_engine.py
from .philosophy_config import PHILOSOPHIES

def derive_regime_key(macro_outlook: dict) -> str:
    g = "up" if macro_outlook.get("gdp_trend") in ("positive", "up") else "down"
    i = "up" if macro_outlook.get("inflation_trend") == "up" else "down"
    return f"growth_{g}_infl_{i}"

def clamp(x, lo, hi): 
    return max(lo, min(hi, x))

def normalize(weights: dict) -> dict:
    s = sum(weights.values())
    return {k: v / s for k, v in weights.items()} if s > 0 else weights

def compute_allocation(macro_outlook: dict, sentiment: dict, preferences: dict) -> dict:
    phil_key = preferences.get("philosophy", "all_seasons")
    cfg = PHILOSOPHIES[phil_key]
    weights = cfg["base"].copy()

    # 1) Tilt per regime
    key = derive_regime_key(macro_outlook)
    for k, v in cfg.get("tilts", {}).get(key, {}).items():
        weights[k] = weights.get(k, 0) + v

    # 2) Modifica con sentiment
    ms = sentiment.get("market_sentiment", "neutral")
    conf = float(sentiment.get("confidence", 0) or 0)
    if ms == "negative":
        shift = 0.05 + min(conf, 0.15)  # più sfiducia => più cash
        weights["cash"] = weights.get("cash", 0) + shift
        if "equity" in weights:
            weights["equity"] = max(0.0, weights["equity"] - shift)
    elif ms == "positive":
        shift = 0.03 + min(conf, 0.10)
        if "cash" in weights:
            take = min(weights["cash"], shift)
            weights["cash"] -= take
            weights["equity"] = weights.get("equity", 0) + take

    # 3) Vincoli
    c = cfg.get("constraints", {})
    if "equity" in weights:
        weights["equity"] = clamp(weights["equity"], c.get("equity_min", 0), c.get("equity_max", 1))
    if "commodities" in weights:
        weights["commodities"] = clamp(weights["commodities"], 0, c.get("commodities_max", 1))
    if "gold" in weights:
        weights["gold"] = clamp(weights["gold"], 0, c.get("gold_max", 1))

    # bond_total_min: garantisce un cuscinetto obbligazionario
    bond_keys = [k for k in weights if k.startswith("gov_bonds") or k == "bond_agg"]
    bond_total = sum(weights[k] for k in bond_keys)
    if c.get("bond_total_min") and bond_total < c["bond_total_min"]:
        deficit = c["bond_total_min"] - bond_total
        # sposta da equity verso bond_mid se esiste, altrimenti bond_agg
        donor = "equity" if "equity" in weights else "cash"
        target = "gov_bonds_mid" if "gov_bonds_mid" in weights else ("bond_agg" if "bond_agg" in weights else None)
        if target and donor in weights and weights[donor] > deficit:
            weights[donor] -= deficit
            weights[target] = weights.get(target, 0) + deficit

    # 4) Normalizza
    weights = normalize(weights)

    # 5) Costruisci filtri dinamici per selezione strumenti
    filters = {
        "etf": {
            "max_ter": preferences.get("etf", {}).get("max_ter", 0.30),
            "domicile_whitelist": preferences.get("etf", {}).get("domicile_whitelist", []),
            "replication": preferences.get("etf", {}).get("replication", [])
        },
        "etc": {
            "prefer_physical": preferences.get("etc", {}).get("prefer_physical", True),
            "issuer_whitelist": preferences.get("etc", {}).get("issuer_whitelist", [])
        },
        "stocks": preferences.get("stocks", {}),
        "region_bias": preferences.get("region_bias", []),
        "equity_style": preferences.get("equity_style", [])
    }
    return {"weights": weights, "filters": filters, "philosophy": phil_key, "regime_key": key}