import logging

log = logging.getLogger(__name__)

def run():
    # === DATI MACRO REALI (da fonte interna o file) ===
    inflation_yoy = 4.59
    policy_rate = 4.12
    gdp_growth = -0.08
    unemployment_rate = 9.11
    pmi_index = 46.4

    # === OUTLOOK 3–6 MESI ===
    outlook = {
        "inflation_trend": "stable" if 3 < inflation_yoy < 5 else "up" if inflation_yoy >= 5 else "down",
        "rates_trend": "down" if policy_rate > inflation_yoy else "up",
        "gdp_trend": "negative" if gdp_growth < 0 else "positive",
        "labor_trend": "loose" if unemployment_rate > 6 else "tight",
        "pmi_signal": "contraction" if pmi_index < 50 else "expansion"
    }

    # === DETERMINAZIONE REGIME ===
    if outlook["gdp_trend"] == "negative" and outlook["inflation_trend"] == "stable":
        regime = "recession"
    elif outlook["gdp_trend"] == "positive" and outlook["inflation_trend"] == "up":
        regime = "stagflation"
    elif outlook["gdp_trend"] == "positive" and outlook["inflation_trend"] == "down":
        regime = "growth"
    else:
        regime = "neutral"

    log.info(f"[Macro] Inflazione: {inflation_yoy}% | Tassi: {policy_rate}% | PIL: {gdp_growth}% | Disoccupazione: {unemployment_rate}% | PMI: {pmi_index}")
    log.info(f"[Macro] Regime determinato: {regime}")

    return {
        "inflation_yoy": inflation_yoy,
        "policy_rate": policy_rate,
        "gdp_growth": gdp_growth,
        "unemployment_rate": unemployment_rate,
        "pmi_index": pmi_index,
        "outlook_3_6m": outlook,
        "regime": regime
    }