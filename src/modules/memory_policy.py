def adjust_strategy_based_on_memory(episodes):
    """
    Analizza gli ultimi episodi e suggerisce modifiche.
    Esempio: se TSLA è selezionata 5 volte di fila → segnalare sovrappeso.
    """
    tickers = [e[4].split(",") for e in episodes]
    flat = [t for sublist in tickers for t in sublist]
    freq = {t: flat.count(t) for t in set(flat)}

    warnings = []
    for ticker, count in freq.items():
        if count >= 4:
            warnings.append(f"⚠️ Titolo '{ticker}' selezionato {count} volte: possibile sovrappeso.")

    return warnings