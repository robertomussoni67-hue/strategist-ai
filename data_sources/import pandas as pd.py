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
        return

    print("Prime righe del portafoglio:\n", df.head(), "\n")

    df = df.rename(columns={
        'Simbolo': 'Simbolo', 
        'Quantità': 'Quantità', 
        'Prezzo medio': 'Prezzo Medio'
    })

    df['Prezzo Attuale'] = None

    for index, row in df.iterrows():
        simbolo = row['Simbolo']
        
        print(f"\nRecupero dati per {simbolo}...")
        data = get_all_data(simbolo, years=5)
        
        if data:
            df.at[index, 'Prezzo Attuale'] = data['price']
            print(f"✅ Aggiornato il prezzo per {simbolo}: {data['price']}")

            print(f"Generando grafico performance YTD per {simbolo}...")
            plot_price_performance(simbolo, data['history'])
            
            print(f"Generando grafico ricavi e utili per {simbolo}...")
            plot_quarterly_financials(
                simbolo, 
                data['revenues'], 
                data['earnings']
            )
        else:
            print(f"❌ Impossibile recuperare dati per {simbolo} da tutte le piattaforme. Saltando.")

    df.dropna(subset=['Prezzo Attuale'], inplace=True)
    df['Valore'] = df['Quantità'] * df['Prezzo Attuale']
    df['P/L non realizzato'] = (df['Prezzo Attuale'] - df['Prezzo Medio']) * df['Quantità']
    df['Rendimento %'] = (df['P/L non realizzato'] / (df['Prezzo Medio'] * df['Quantità'])) * 100

    valore_totale = df['Valore'].sum()
    pl_non_realizzato = df['P/L non realizzato'].sum()
    rendimento_medio = df['Rendimento %'].mean()
    
    print("\n\n📑 RISULTATI ANALISI PORTAFOGLIO (aggiornati in tempo reale)")
    print(f"💰 Valore totale portafoglio: {valore_totale:,.2f}")
    print(f"📈 P/L totale non realizzato: {pl_non_realizzato:,.2f}")
    print(f"📊 Rendimento medio: {rendimento_medio:.2f} %")

    top = df.sort_values('Rendimento %', ascending=False).head(3)
    flop = df.sort_values('Rendimento %').head(3)
    
    print("\n🏆 Top 3 titoli:")
    print(top[['Simbolo', 'Rendimento %', 'Valore']])
    
    print("\n📉 Flop 3 titoli:")
    print(flop[['Simbolo', 'Rendimento %', 'Valore']])

if __name__ == "__main__":
    percorso_del_tuo_csv = "portafoglio_directa_esteso.csv"
    analizza_portafoglio(percorso_del_tuo_csv)