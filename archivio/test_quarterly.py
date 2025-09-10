import sys
import pandas as pd
from datetime import datetime, timedelta

# Importa l'agente principale
from modules.macro_module import execute_macro

if __name__ == "__main__":
    print("Avvio del test per la generazione del grafico di bilancio trimestrale.")
    # Esegui la funzione di test specificando il comando "test_quarterly"
    execute_macro("test_quarterly")

    print("\n✅ Test completato. Se tutto è andato a buon fine, dovresti trovare il grafico di bilancio trimestrale nella cartella 'report'.")
    print("Apri il file nel tuo browser per vedere il risultato interattivo.")