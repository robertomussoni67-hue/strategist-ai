# src/modules/allocation_mapper.py

def apply_etf_filters(etfs, etf_filters, region_bias):
    def ok(e):
        if etf_filters.get("max_ter") is not None and e.get("ter") is not None and e["ter"] > etf_filters["max_ter"]:
            return False
        if etf_filters.get("domicile_whitelist"):
            if e.get("domicile") not in etf_filters["domicile_whitelist"]:
                return False
        if etf_filters.get("replication"):
            if e.get("replication") not in etf_filters["replication"]:
                return False
        # bias regione: preferisci, ma non escludere
        return True
    filtered = [e for e in etfs if ok(e)]
    # prova a promuovere ETF globali se presenti
    filtered.sort(key=lambda x: ("world" not in x["name"].lower() and "all-world" not in x["name"].lower(),
                                 x.get("ter", 1.0)))
    return filtered

def apply_etc_filters(etcs, etc_filters):
    def ok(e):
        name = e.get("name", "").lower()
        if etc_filters.get("prefer_physical", True):
            if "physical" in (e.get("replication", "") or "").lower():
                return True
        return True
    return [e for e in etcs if ok(e)]

def map_allocation_to_plan(weights, picks, filters):
    """
    weights: dict asset class -> weight
    picks: { 'stocks': [...], 'etf': [...], 'etc': [...] }
    filters: da philosophy_engine
    """
    plan = []

    # ETF filtrati
    etf_list = apply_etf_filters(picks.get("etf", []), filters["etf"], filters.get("region_bias", []))
    etc_list = apply_etc_filters(picks.get("etc", []), filters["etc"])
    stocks_list = picks.get("stocks", [])

    # Equity: 70% ETF core, 30% azioni selezionate (se presenti)
    eq_w = weights.get("equity", 0)
    if eq_w > 0:
        core = None
        for e in etf_list:
            if any(k in e["name"].lower() for k in ["all-world", "msci world", "acwi", "global"]):
                core = e; break
        core = core or (etf_list[0] if etf_list else None)
        if core:
            plan.append({"ticker": core["ticker"], "name": core["name"], "type": "ETF", "weight": round(eq_w * 0.7, 4)})
        if stocks_list:
            per_stock = round((eq_w * 0.3) / len(stocks_list), 4)
            for s in stocks_list:
                plan.append({"ticker": s["ticker"], "name": s.get("name", s["ticker"]), "type": "STOCK", "weight": per_stock})

    # Oro
    if weights.get("gold", 0) > 0 and etc_list:
        gold = next((x for x in etc_list if "gold" in x.get("name", "").lower()), None)
        if gold:
            plan.append({"ticker": gold["ticker"], "name": gold["name"], "type": "ETC", "weight": round(weights["gold"], 4)})

    # Commodities broad
    if weights.get("commodities", 0) > 0 and etc_list:
        broad = next((x for x in etc_list if any(k in x.get("name", "").lower() for k in ["broad", "commodity", "cmdty"])), None)
        if broad:
            plan.append({"ticker": broad["ticker"], "name": broad["name"], "type": "ETC", "weight": round(weights["commodities"], 4)})

    # Bond: prova a mappare su ETF obbligazionari se esistono in picks['etf']
    for k, label in [("gov_bonds_long", "long"), ("gov_bonds_mid", "mid"), ("bond_agg", "agg")]:
        w = weights.get(k, 0)
        if w > 0 and etf_list:
            candidate = None
            for e in etf_list:
                nm = e["name"].lower()
                if k == "gov_bonds_long" and any(t in nm for t in ["treasury 20+", "gov long", "long duration"]):
                    candidate = e; break
                if k == "gov_bonds_mid" and any(t in nm for t in ["7-10", "intermediate", "gov mid"]):
                    candidate = e; break
                if k == "bond_agg" and any(t in nm for t in ["aggregate", "global bond", "bond agg"]):
                    candidate = e; break
            candidate = candidate or etf_list[0]
            plan.append({"ticker": candidate["ticker"], "name": candidate["name"], "type": "ETF", "weight": round(w, 4)})

    # Cash: non mappato su strumento per default
    return plan