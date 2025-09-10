import pandas as pd
import matplotlib.pyplot as plt
from data_sources.data_retriever import get_all_data
from data_visualizer.plotter import plot_price_performance, plot_quarterly_financials

def analizza_portafoglio(percorso_csv):
    """
    Analizza un portafoglio titoli leggendo i dati da un file CSV.
    Recupera prezzi attuali e dati storici/finanziari da più piattaforme
    e genera report e grafici.
    """
    try:
        df = pd.read_csv(percorso_csv)
    except FileNotFoundError:
        print(f"❌ Errore: Il file '{percorso_csv}' non è stato trovato.")
        return None

    print("Prime righe del portafoglio:\n", df.head(), "\n")

    df = df.rename(columns={
        'Simbolo': 'Simbolo', 
        'Quantità': 'Quantità', 
        'Prezzo medio': 'Prezzo Medio'
    })

    df['Prezzo Attuale'] = None
    df['Valore'] = None

    for index, row in df.iterrows():
        simbolo = row['Simbolo']
        
        # Recupera tutti i dati usando la nuova funzione
        print(f"\nRecupero dati per {simbolo}...")
        data = get_all_data(simbolo, years=5)
        
        if data and 'price' in data and data['price'] is not None:
            df.at[index, 'Prezzo Attuale'] = data['price']
            print(f"✅ Aggiornato il prezzo per {simbolo}: {data['price']}")

            print(f"Generando grafico performance YTD per {simbolo}...")
            # Controlla se i dati storici sono disponibili prima di plottare
            if 'history' in data and not data['history'].empty:
                plot_price_performance(simbolo, data['history'])
            else:
                print(f"❌ Impossibile generare il grafico YTD: dati storici non disponibili per {simbolo}.")
            
            # Aggiungi un controllo per i dati di ricavi e utili prima di plottare
            if 'revenues' in data and 'earnings' in data:
                print(f"Generando grafico ricavi e utili per {simbolo}...")
                plot_quarterly_financials(
                    simbolo, 
                    data['revenues'], 
                    data['earnings']
                )
            else:
                print(f"❌ Impossibile generare il grafico finanziario: dati di ricavi/utili non disponibili per {simbolo}.")

        else:
            print(f"❌ Impossibile recuperare dati per {simbolo} da tutte le piattaforme. Saltando.")

    df.dropna(subset=['Prezzo Attuale'], inplace=True)
    df['Valore'] = df['Quantità'] * df['Prezzo Attuale']
    df['P/L non realizzato'] = (df['Prezzo Attuale'] - df['Prezzo Medio']) * df['Quantità']
    df['Rendimento %'] = (df['P/L non realizzato'] / (df['Prezzo Medio'] * df['Quantità'])) * 100

    valore_totale = df['Valore'].sum()
    pl_non_realizzato = df['P/L non realizzato'].sum()
    
    # Classifica i titoli per rendimento
    classifica_rendimento = df.sort_values(by='Rendimento %', ascending=False)
    
    # Prepara i risultati da restituire
    risultati = {
        'valore_totale': valore_totale,
        'pl_totale': pl_non_realizzato,
        'pl_medio': df['P/L non realizzato'].mean(),
        'miglior_titolo': classifica_rendimento.iloc[0]['Simbolo'] if not classifica_rendimento.empty else 'N/A',
        'miglior_pl': classifica_rendimento.iloc[0]['P/L non realizzato'] if not classifica_rendimento.empty else 'N/A',
        'peggior_titolo': classifica_rendimento.iloc[-1]['Simbolo'] if not classifica_rendimento.empty else 'N/A',
        'peggior_pl': classifica_rendimento.iloc[-1]['P/L non realizzato'] if not classifica_rendimento.empty else 'N/A',
        'percentuale_guadagno': (df['P/L non realizzato'] > 0).mean() * 100,
        'classifica_rendimento': {
            row['Simbolo']: {'rendimento': row['Rendimento %'], 'pl': row['P/L non realizzato']}
            for _, row in classifica_rendimento.iterrows()
        }
    }

    return risultati

if __name__ == "__main__":
    percorso_del_tuo_csv = "portafoglio_directa_esteso.csv"
    risultati = analizza_portafoglio(percorso_del_tuo_csv)
    if risultati:
        print("\n\n--- RISULTATI COMPLETI DELL'ANALISI ---")
        print(f"Valore Totale: {risultati['valore_totale']:,}")
        print(f"P/L Totale: {risultati['pl_totale']:,}")
