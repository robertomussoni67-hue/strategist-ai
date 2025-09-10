# strategist_main.py - Il cuore del motore Strategist
import logging
import time

# Importa i moduli per i sub-agenti
from modules.subagent_macro import run_macro_analysis
from modules.subagent_etf import run_etf_analysis, get_etf_universe
from modules.subagent_stocks import get_stock_universe, run_stock_analysis # <-- Nuova importazione

# Configura il logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

log = logging.getLogger(__name__)

def main():
    """
    Funzione principale che esegue il ciclo di analisi dello Strategist.
    """
    log.info("=== Avvio ciclo di analisi Strategist ===")
    
    # STEP 1: Analisi macroeconomica
    macro_regime = run_macro_analysis()
    
    # STEP 2: Analisi degli ETF
    try:
        etf_universe = get_etf_universe()
        if etf_universe:
            selected_etfs = run_etf_analysis(etf_universe, macro_regime)
            if selected_etfs is None:
                log.warning("L'analisi degli ETF ha restituito 'None'. Impostato su lista vuota.")
                selected_etfs = []
        else:
            selected_etfs = []
    except Exception as e:
        log.error(f"Errore durante l'analisi degli ETF: {e}")
        selected_etfs = []
        
    log.info("Analisi ETF completata.")

    # STEP 3: Analisi dei titoli
    try:
        stock_universe = get_stock_universe() # <-- Chiamata esplicita
        if stock_universe:
            selected_stocks = run_stock_analysis(stock_universe, macro_regime)
        else:
            selected_stocks = []
    except Exception as e:
        log.error(f"Errore durante l'analisi dei titoli: {e}")
        selected_stocks = []
        
    log.info("Analisi titoli completata.")
    
    # STEP 4: Reporting
    if selected_etfs:
        log.info("ETF selezionati:")
        for etf in selected_etfs:
            log.info(f" - {etf.get('ticker', 'N/A')} | {etf.get('name', 'N/A')}")
    else:
        log.info("Nessun ETF selezionato.")
        
    if selected_stocks:
        log.info("Titoli selezionati:")
        for stock in selected_stocks:
            log.info(f" - {stock.get('symbol', 'N/A')} | {stock.get('name', 'N/A')}")
    else:
        log.info("Nessun titolo selezionato.")
    
    log.info("=== Ciclo di analisi completato ===")

if __name__ == "__main__":
    main()
