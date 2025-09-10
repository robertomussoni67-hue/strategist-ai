import logging
import pandas as pd

# Configura il logger per il modulo
logger = logging.getLogger(__name__)

def run_etf_analysis(etfs_data, regime="neutral"):
    """
    Analizza e filtra una lista di ETF in base al regime di mercato e ad altri criteri.

    La funzione ora accetta e utilizza il DataFrame 'etfs_data' anziché una lista fissa.

    Args:
        etfs_data (pd.DataFrame): DataFrame con i dati degli ETF. Si presume che contenga
                                  le colonne 'ticker', 'nome', 'settore' e 'prezzo'.
        regime (str): Il regime di mercato corrente ("risk_on", "risk_off", "neutral").

    Returns:
        list: Una lista di ETF filtrati e selezionati, come una lista di dizionari.
    """
    if not isinstance(etfs_data, pd.DataFrame) or etfs_data.empty:
        logger.error("[ETF] Errore: Il DataFrame 'etfs_data' è vuoto o non valido.")
        return []

    logger.info(f"[ETF] Analisi ETF avviata con regime macro: {regime}")

    # Converti il DataFrame in una lista di dizionari per la logica di selezione.
    # Questo mantiene la compatibilità con il resto del tuo codice, se necessario.
    etf_universe = etfs_data.to_dict('records')

    selected_etfs = []

    # Implementa la logica di selezione in base al regime
    for etf in etf_universe:
        if regime == "risk_off":
            # Ipotizziamo che la colonna del settore si chiami 'settore'
            if etf.get("settore") in ["utilities", "broad"]:
                selected_etfs.append(etf)
        elif regime == "risk_on":
            if etf.get("settore") in ["technology", "broad"]:
                selected_etfs.append(etf)
        else: # regime "neutral" o non riconosciuto
            # Selezione bilanciata - seleziona tutti gli ETF per default
            selected_etfs.append(etf)

    logger.info(f"[ETF] Selezionati {len(selected_etfs)} ETF in base al regime '{regime}':")
    for etf in selected_etfs:
        logger.info(f" - Ticker: {etf.get('ticker')} | Settore: {etf.get('settore')}")
    
    logger.info("[ETF] Analisi completata ✅")
    
    return selected_etfs

# Esempio di utilizzo (solo per testare la funzione)
if __name__ == '__main__':
    # Simula un DataFrame che verrebbe passato da un connettore API
    sample_data = pd.DataFrame([
        {"ticker": "VTI", "nome": "Vanguard Total Stock Market", "tipo": "accumulo", "settore": "broad", "prezzo": 220},
        {"ticker": "QQQ", "nome": "Invesco NASDAQ 100", "tipo": "accumulo", "settore": "technology", "prezzo": 450},
        {"ticker": "XLU", "nome": "Utilities Select Sector SPDR", "tipo": "distribuzione", "settore": "utilities", "prezzo": 75},
        {"ticker": "SPY", "nome": "SPDR S&P 500", "tipo": "accumulo", "settore": "broad", "prezzo": 520},
    ])

    # Esegui l'analisi in un regime "risk_on"
    risultati_risk_on = run_etf_analysis(sample_data, regime="risk_on")
    print("\nRisultati per il regime 'risk_on':", risultati_risk_on)

    # Esegui l'analisi in un regime "risk_off"
    risultati_risk_off = run_etf_analysis(sample_data, regime="risk_off")
    print("\nRisultati per il regime 'risk_off':", risultati_risk_off)
