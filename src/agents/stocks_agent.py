import logging

log = logging.getLogger(__name__)

def run():
    # === Titoli disponibili ===
    universe = [
        {"ticker": "AAPL", "name": "Apple Inc."},
        {"ticker": "MSFT", "name": "Microsoft Corp."},
        {"ticker": "GOOGL", "name": "Alphabet Inc."},
        {"ticker": "AMZN", "name": "Amazon.com Inc."},
        {"ticker": "TSLA", "name": "Tesla Inc."},
        {"ticker": "JNJ", "name": "Johnson & Johnson"},
        {"ticker": "NVDA", "name": "NVIDIA Corp."}
    ]

    # === Selezione in base al regime ===
    regime = "recession"  # Puoi passarlo come parametro in futuro

    if regime == "growth":
        selected = [t for t in universe if t["ticker"] in ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]]
    elif regime == "recession":
        selected = [t for t in universe if t["ticker"] in ["JNJ", "MSFT", "NVDA"]]
    else:
        selected = universe[:5]

    log.info(f"[Stocks] Universo definito con {len(universe)} titoli.")
    log.info(f"[Stocks] Analisi titoli per regime '{regime}'...")
    log.info(f"[Stocks] Selezionati {len(selected)} titoli.")

    return {"stocks": selected}