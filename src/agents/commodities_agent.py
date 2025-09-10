import logging

log = logging.getLogger(__name__)

def run():
    # === Commodities disponibili ===
    universe = [
        {"ticker": "GLD", "name": "SPDR Gold Shares"},
        {"ticker": "SLV", "name": "iShares Silver Trust"},
        {"ticker": "USO", "name": "United States Oil Fund"},
        {"ticker": "DBB", "name": "Invesco Base Metals"},
        {"ticker": "PALL", "name": "Aberdeen Palladium ETF"}
    ]

    # === Regime macro (può essere passato come parametro in futuro)
    regime = "recession"

    # === Selezione in base al regime ===
    if regime == "recession":
        selected = [c for c in universe if c["ticker"] in ["GLD", "SLV", "PALL"]]
    elif regime == "inflation":
        selected = [c for c in universe if c["ticker"] in ["GLD", "USO", "DBB"]]
    else:
        selected = universe[:3]

    log.info(f"[Commodities] Universo: {len(universe)} strumenti.")
    log.info(f"[Commodities] Selezionati {len(selected)} strumenti per regime '{regime}'.")

    return {"commodities": selected}