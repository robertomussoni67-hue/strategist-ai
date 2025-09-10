# Importa i moduli necessari.
import os
import sys

# Aggiunge la cartella 'modules' al percorso di ricerca dei moduli.
# Questo permette di importare i sub-agenti e i moduli ausiliari.
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from strategist_main import run_analysis

def main():
    """
    Funzione principale per eseguire l'agente di analisi finanziaria.
    """
    print("Benvenuto nell'Agente AI per l'analisi del portafoglio.")
    print("Questo agente ti guiderà attraverso l'analisi di un portafoglio ETF e azionario.")
    print("Puoi avviare l'analisi in qualsiasi momento scrivendo 'start'.")
    print("Scrivi 'exit' per uscire.")

    while True:
        user_input = input("\n> ").strip().lower()

        if user_input == 'start':
            print("Avvio dell'analisi...")
            try:
                run_analysis()
            except Exception as e:
                print(f"Errore durante l'esecuzione dell'analisi: {e}")

        elif user_input == 'exit':
            print("Uscita dall'agente.")
            break

        else:
            print("Comando non riconosciuto. Digita 'start' per iniziare o 'exit' per uscire.")

if __name__ == "__main__":
    main()