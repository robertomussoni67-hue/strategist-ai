import pandas as pd
import matplotlib.pyplot as plt
import os

# Nome del file CSV con i dati di Enel
csv_file = "enel_data.csv"

def carica_dati(file_path):
    """Carica i dati da CSV e li restituisce come DataFrame."""
    if not os.path.exists(file_path):
        print(f"⚠️ Il file {file_path} non esiste nella cartella attuale.")
        return None
    try:
        df = pd.read_csv(file_path)
        print(f"✅ Dati caricati: {len(df)} righe trovate.")
        return df
    except Exception as e:
        print(f"❌ Errore nel caricamento: {e}")
        return None

def analizza_dati(df):
    """Esegue un'analisi di base sul DataFrame."""
    print("\n📊 Informazioni sui dati:")
    print(df.info())
    print("\n🔍 Prime 5 righe:")
    print(df.head())

    if 'Prezzo' in df.columns:
        print(f"\n💰 Prezzo medio: {df['Prezzo'].mean():.2f}")
        df['Prezzo'].plot(title="Andamento Prezzo ENEL", ylabel="€", xlabel="Tempo")
        plt.show()
    else:
        print("\n⚠️ Nessuna colonna 'Prezzo' trovata.")

if __name__ == "__main__":
    # Apertura interattiva: chiede all'utente il nome file se diverso dal predefinito
    file_da_usare = input(f"📂 Inserisci nome file CSV (Enter per '{csv_file}'): ").strip()
    if file_da_usare:
        csv_file = file_da_usare

    dati = carica_dati(csv_file)
    if dati is not None:
        analizza_dati(dati)