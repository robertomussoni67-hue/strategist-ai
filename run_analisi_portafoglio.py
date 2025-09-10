import datetime
import yfinance as yf
from modules.macro_module import execute_macro, get_quarterly_data
from modules.strategist_main import run_analysis

# ====================
# Funzione Principale per l'Esecuzione
# ====================

def run_portfolio_agent():
    """
    Orchestra l'esecuzione dell'analisi del portafoglio.
    """
    
    # Dati di esempio per simulare un portafoglio
    portfolio_data = {
        'ENI.MI': {'shares': 100, 'buy_price': 13.00},
        'ISP.MI': {'shares': 200, 'buy_price': 2.50},
        'AAPL': {'shares': 10, 'buy_price': 170.00},
    }
    
    print("\n--- 📑 RISULTATI ANALISI PORTAFOGLIO ---")
    
    # Esegue l'analisi del portafoglio con l'agente Strategist
    run_analysis(portfolio_data)

    print("\n--- 🧠 Avvio Agente AI per Analisi Macro ---")
    # Esegue il modulo macro per il reporting, se necessario.
    # Nota: abbiamo rimosso il comando 'start' che non esiste.
    execute_macro("report")
    
    # === NUOVO TEST: Recupero dati trimestrali con la funzione affidabile ===
    print("\n--- 🧪 TEST AGGIUNTIVO: Recupero dati finanziari con yfinance ---")
    for ticker in portfolio_data:
        print(f"🔎 Tentativo di recupero dati trimestrali per {ticker}...")
        try:
            # Usa la funzione robusta dal modulo macro
            earnings_data = get_quarterly_data(ticker)
            if earnings_data is not None:
                print(f"✅ Dati trimestrali recuperati con successo per {ticker}:\n{earnings_data}")
            else:
                print(f"❌ Impossibile recuperare dati trimestrali per {ticker}.")
        except Exception as e:
            print(f"❌ Errore durante il recupero dei dati per {ticker}: {e}")

    print("\n--- Test completato. ---")

# Esegui l'intera analisi
run_portfolio_agent()