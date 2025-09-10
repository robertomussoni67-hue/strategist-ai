# strategist.py
# Versione base — inizializzazione

import datetime

def main():
    ora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Strategist avviato alle: {ora}")
    # Qui in futuro aggiungeremo:
    # - Raccolta dati da API
    # - Generazione grafici
    # - Salvataggio su cloud

if __name__ == "__main__":
    main()