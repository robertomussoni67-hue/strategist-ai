# Importiamo il motore strategico che vogliamo testare.
# Assicurati che strategic_engine.py si trovi nella stessa directory.
import strategic_engine

def run_test():
    """
    Funzione per eseguire un test del motore strategico con dati di esempio.
    """
    print("--- Avvio del test per strategic_engine.py ---")
    
    # Dati di esempio per i ticker di borsa.
    # Puoi cambiare questi valori per testare diversi titoli.
    test_tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA']
    
    # Dati di esempio per l'importo totale del portafoglio (in dollari).
    # Puoi cambiare questo valore a tuo piacimento.
    portfolio_value = 100000

    print(f"\nAnalizzando un portafoglio con i seguenti titoli: {', '.join(test_tickers)}")
    print(f"Valore del portafoglio: ${portfolio_value}\n")

    try:
        # Chiamiamo la funzione principale del nostro motore strategico.
        strategic_engine.analyze_portfolio(test_tickers, portfolio_value)
        print("\n--- Test completato con successo. L'analisi è stata eseguita. ---")
    except Exception as e:
        print(f"\n!!! Errore durante l'esecuzione del test: {e} !!!")
        print("Il motore strategico non è riuscito a completare l'analisi.")

# Eseguiamo il test quando lo script viene eseguito direttamente.
if __name__ == "__main__":
    run_test()
