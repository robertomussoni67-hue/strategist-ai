import pandas as pd
from datetime import datetime, timedelta

# Importa il tuo sub-agente per la visualizzazione
from data_visualizer.plotter import plot_price_performance

def run_test():
    """
    Funzione di test per verificare il corretto funzionamento del plotter.
    """
    print("Avvio del test per il generatore di grafici...")
    
    # Crea dati storici di esempio
    today = datetime.now()
    dates = pd.date_range(end=today, periods=90, freq='D')
    prices = [100 + i*0.5 + (i**2)*0.01 + i%10 for i in range(90)]
    sample_data = pd.DataFrame({'Close': prices}, index=dates)

    # Chiamata alla funzione del plotter
    print("Chiamata alla funzione 'plot_price_performance'...")
    output_path = plot_price_performance("AAPL", sample_data)
    
    if output_path:
        print(f"✅ Test completato. Grafico salvato in: {output_path}")
        print("Apri il file nel tuo browser per vedere il risultato interattivo.")
    else:
        print("❌ Test fallito. Verificare che i file siano nei percorsi corretti.")

# Esegui il test
if __name__ == "__main__":
    run_test()
