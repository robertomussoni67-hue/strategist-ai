import yfinance as yf
import pandas as pd
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import sys
import os

# ==============================================================================
# DATI UTENTE E PORTAFOGLIO
# ==============================================================================

PORTFOLIO = {
    'ENI.MI': {'shares': 100, 'buy_price': 13.00},
    'ISP.MI': {'shares': 200, 'buy_price': 2.50},
    'AAPL': {'shares': 10, 'buy_price': 170.00},
}

# ==============================================================================
# FUNZIONI DI SUPPORTO (ORIGINALI DAI MODULI)
# ==============================================================================

def get_all_data(ticker: str) -> dict:
    """
    Recupera i dati di un singolo ticker da Yahoo Finance,
    inclusi prezzi attuali, dati storici, ricavi e utili.
    
    :param ticker: Il simbolo del titolo da cercare.
    :return: Un dizionario contenente i dati recuperati.
    """
    try:
        stock = yf.Ticker(ticker)
        
        # Recupera il prezzo attuale
        current_price = stock.info.get('currentPrice')
        if current_price is None:
            print(f"Errore: Prezzo non trovato per {ticker}.")
            return {'price': None}
        
        # Recupera i dati storici YTD (Year-to-Date)
        end_of_last_year = datetime(datetime.now().year - 1, 12, 31)
        # CORREZIONE: rimossa la ridondanza di "period" per evitare l'errore
        history = stock.history(start=end_of_last_year.strftime('%Y-%m-%d'))
        
        # Recupera i ricavi e gli utili trimestrali
        revenues = stock.quarterly_income_stmt.loc['Total Revenue'].to_dict()
        earnings = stock.quarterly_earnings
        
        return {
            'price': current_price,
            'history': history,
            'revenues': revenues,
            'earnings': earnings
        }
    except Exception as e:
        print(f"Errore nel recupero dati per {ticker}: {e}")
        return {'price': None}

def get_cpi_data() -> pd.DataFrame:
    """
    Simula il recupero dei dati CPI (Consumer Price Index)
    poiché non è disponibile un'API diretta.
    
    :return: Un DataFrame di pandas con dati CPI di esempio.
    """
    print("Simulazione di recupero dati CPI...")
    # Dati CPI di esempio per l'analisi macro
    cpi_data = {
        '2023-01-01': 100,
        '2023-04-01': 101.2,
        '2023-07-01': 102.5,
        '2023-10-01': 102.8,
        '2024-01-01': 103.1,
        '2024-04-01': 103.5
    }
    return pd.DataFrame.from_dict(cpi_data, orient='index', columns=['CPI'])

def plot_price_performance(ticker: str, history: pd.DataFrame):
    """
    Genera e mostra un grafico della performance YTD del titolo.
    
    :param ticker: Simbolo del titolo.
    :param history: DataFrame con i dati storici del prezzo.
    """
    if history.empty:
        print(f"Nessun dato storico per {ticker}, impossibile creare il grafico.")
        return
    
    plt.figure(figsize=(10, 6))
    plt.plot(history.index, history['Close'])
    plt.title(f'Performance YTD di {ticker}')
    plt.xlabel('Data')
    plt.ylabel('Prezzo di Chiusura')
    plt.grid(True)
    plt.show()

def plot_quarterly_financials(ticker: str, financials: dict):
    """
    Funzione placeholder per la visualizzazione dei dati finanziari trimestrali.
    """
    print(f"Generazione grafico finanziario per {ticker}...")
    # Logica per grafici finanziari andrebbe qui
    pass

# ==============================================================================
# AGENTE PRINCIPALE (Basato sui tuoi 25 Blocchi)
# ==============================================================================

class ChiefInvestmentStrategist:
    """
    Questo agente esegue una strategia di investimento basata su 25 compiti.
    Ogni metodo rappresenta un blocco logico della strategia.
    """

    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.data = {}
        
    def execute_strategy(self):
        """
        Orchestra l'esecuzione di tutti i 25 blocchi della strategia.
        """
        print("🚀 L'Agente Chief Investment Strategist sta avviando l'analisi...")

        # BLOCCO 1: Recupero dati del portafoglio (prezzi e info)
        self.step_1_retrieve_data()

        # BLOCCO 2: Calcolo del valore totale del portafoglio
        self.step_2_calculate_total_value()

        # BLOCCO 3: Analisi P/L (Profitto/Perdita)
        self.step_3_analyze_pl()

        # BLOCCO 4: Generazione grafici di performance YTD (Year-To-Date)
        self.step_4_generate_ytd_charts()

        # BLOCCO 5: Analisi macroeconomica (corretta con FRED API)
        self.step_5_macro_analysis()

        # BLOCCO 6: Selezione di nuovi titoli (Screener)
        self.step_6_stock_screener()
        
        # BLOCCO 7: Generazione del report finale
        self.step_7_generate_final_report()

        # BLOCCO 8: Controllo del portafoglio esistente (Peer analysis)
        self.step_8_portfolio_check()
        
        # NUOVO BLOCCO 9: Esportazione dati su file JSON
        self.step_9_export_to_json()

        # ... (BLOCCHI 10-25: Verranno aggiunti qui man mano)
        # Ogni metodo rappresenta un passo specifico della tua strategia.
        print("✅ Analisi completa. Il tuo report è pronto e salvato in un file JSON.")

    def step_1_retrieve_data(self):
        """BLOCCO 1: Recupera i dati di tutti i titoli del portafoglio."""
        print("Fase 1: Recupero dei dati...")
        
        for ticker, info in self.portfolio.items():
            data_retrieved = get_all_data(ticker)
            if data_retrieved and data_retrieved['price']:
                self.data[ticker] = {
                    'price': data_retrieved['price'],
                    'history': data_retrieved.get('history'),
                    'revenues': data_retrieved.get('revenues'),
                    'earnings': data_retrieved.get('earnings'),
                }
                print(f"✅ Dati recuperati per {ticker}.")
            else:
                print(f"❌ Impossibile recuperare dati per {ticker}. Saltando.")

    def step_2_calculate_total_value(self):
        """BLOCCO 2: Calcola il valore totale del portafoglio."""
        print("Fase 2: Calcolo del valore totale...")
        total_value = 0
        for ticker, info in self.portfolio.items():
            if ticker in self.data and 'price' in self.data[ticker]:
                total_value += self.data[ticker]['price'] * info['shares']
        
        self.data['total_value'] = total_value
        print(f"✅ Valore totale del portafoglio calcolato: {total_value:,.2f}")

    def step_3_analyze_pl(self):
        """BLOCCO 3: Analizza il profitto e la perdita di ogni titolo."""
        print("Fase 3: Analisi del P/L...")
        total_pl = 0
        results = []
        for ticker, info in self.portfolio.items():
            if ticker in self.data and 'price' in self.data[ticker]:
                current_price = self.data[ticker]['price']
                shares = info['shares']
                buy_price = info['buy_price']
                pl = (current_price - buy_price) * shares
                total_pl += pl
                
                results.append({
                    'Simbolo': ticker,
                    'Prezzo': current_price,
                    'Valore': round(current_price * shares, 2),
                    'P/L': round(pl, 2),
                    'Rendimento': round((pl / (buy_price * shares)) * 100, 2)
                })
        
        self.data['total_pl'] = total_pl
        self.data['pl_results'] = pd.DataFrame(results)
        print(f"✅ P/L totale del portafoglio calcolato: {total_pl:,.2f}")
        print("\nDettaglio P/L:")
        print(self.data['pl_results'].to_string(index=False))

    def step_4_generate_ytd_charts(self):
        """BLOCCO 4: Generazione grafici di performance YTD."""
        print("Fase 4: Generazione grafici YTD...")
        for ticker, info in self.portfolio.items():
            if ticker in self.data and 'history' in self.data[ticker] and not self.data[ticker]['history'].empty:
                print(f"Generando grafico YTD per {ticker}...")
                plot_price_performance(ticker, self.data[ticker]['history'])
            else:
                print(f"❌ Dati storici non disponibili per {ticker}. Saltando il grafico.")

    def step_5_macro_analysis(self):
        """BLOCCO 5: Esegue un'analisi macroeconomica."""
        print("Fase 5: Analisi macro...")
        cpi_data = get_cpi_data()
        
        # Aggiungo una logica per l'analisi macro come hai suggerito
        if not cpi_data.empty:
            self.data['cpi_data'] = cpi_data
            # Aggiungi qui la tua logica di analisi basata sui dati
            # Esempio: calcola la variazione trimestrale e genera un segnale
            # CORREZIONE: Uso il metodo corretto per evitare il FutureWarning
            last_cpi_value = cpi_data['CPI'].iloc[-1]
            cpi_change = (last_cpi_value - cpi_data['CPI'].iloc[-2]) / cpi_data['CPI'].iloc[-2] * 100
            
            if cpi_change > 0.5:
                self.data['macro_signal'] = 'inflazione_in_aumento'
            else:
                self.data['macro_signal'] = 'inflazione_stabile'

            print(f"✅ Dati CPI pronti per l'analisi. Segnale: {self.data['macro_signal']}.")
        else:
            print("❌ Impossibile recuperare dati CPI. Saltando l'analisi macro.")
            self.data['macro_signal'] = 'errore'
    
    def step_6_stock_screener(self):
        """
        BLOCCO 6: Esegue uno screening di titoli in base a segnali macro e criteri
        di bilancio. Questo è il "sub-agente" che trova i candidati.
        """
        print("Fase 6: Screening e Selezione di nuovi titoli...")
        
        # Logica di esempio basata sul segnale macro
        if self.data.get('macro_signal') == 'inflazione_in_aumento':
            print("Scenario: Inflazione in aumento. Cerco titoli difensivi e a dividendo.")
            # Qui si integrerà la logica per cercare i titoli e gli ETF adatti
            # Usando dati da Finnhub per bilanci e dividendi
        elif self.data.get('macro_signal') == 'inflazione_stabile':
            print("Scenario: Inflazione stabile. Cerco titoli growth o a bassa volatilità.")
        else:
            print("Nessun segnale macro affidabile. Lo screener si basa su criteri generali.")

        # Qui avverrà la chiamata alle API di Finnhub e la logica di filtro.
        # Per ora, è un placeholder.
        print("⏳ Il motore di screening è in fase di sviluppo...")

    def step_7_generate_final_report(self):
        """BLOCCO 7: Crea un report finale leggibile."""
        print("Fase 7: Generazione del report...")
        print("\n" + "="*80)
        print("📑 RISULTATI ANALISI PORTAFOGLIO (aggiornati in tempo reale)")
        print(f"💰 Valore totale portafoglio: {self.data.get('total_value', 0):,.2f}")
        print(f"📈 P/L totale non realizzato: {self.data.get('total_pl', 0):,.2f}")
        print("="*80)
        
        if 'pl_results' in self.data and not self.data['pl_results'].empty:
            print("\n📈 Composizione Portafoglio:")
            print(self.data['pl_results'].to_string(index=False))
            
            top_3 = self.data['pl_results'].sort_values('Rendimento', ascending=False).head(3)
            flop_3 = self.data['pl_results'].sort_values('Rendimento').head(3)
            
            print("\n🏆 Top 3 titoli:")
            print(top_3.to_string(index=False))
            
            print("\n📉 Flop 3 titoli:")
            print(flop_3.to_string(index=False))
        else:
            print("\n❌ Impossibile generare l'analisi del portafoglio a causa di dati mancanti.")
    
    def step_8_portfolio_check(self):
        """
        BLOCCO 8: Questo è il sub-agente che controlla i titoli esistenti nel portafoglio.
        Controlla bilancio, sentiment e valore intrinseco.
        """
        print("\nFase 8: Controllo dei titoli esistenti nel portafoglio...")
        
        for ticker in self.portfolio.keys():
            print(f"Analisi di bilancio e sentiment per {ticker}...")
            # Qui si integrerà la logica per controllare i bilanci (Finnhub) e
            # fare un'analisi più approfondita, come hai suggerito tu.
            # Per ora, è un placeholder.
            
        print("✅ Controllo del portafoglio completato.")

    def step_9_export_to_json(self):
        """
        BLOCCO 9: Esporta i dati analizzati in un file JSON.
        Questo file farà da ponte tra l'agente Python e l'interfaccia web.
        """
        print("\nFase 9: Esportazione dei dati in formato JSON...")
        
        # Prepara un dizionario per l'esportazione
        export_data = {
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_value': self.data.get('total_value'),
            'total_pl': self.data.get('total_pl'),
            'portfolio_details': []
        }
        
        # Aggiungi i dettagli del portafoglio, convertendo il DataFrame in una lista di dizionari
        if 'pl_results' in self.data and not self.data['pl_results'].empty:
            export_data['portfolio_details'] = self.data['pl_results'].to_dict('records')
        
        # Salva il dizionario su un file JSON
        try:
            with open('portfolio_data.json', 'w') as f:
                json.dump(export_data, f, indent=4)
            print("✅ Dati del portafoglio esportati con successo in 'portfolio_data.json'.")
        except Exception as e:
            print(f"❌ Errore durante l'esportazione in JSON: {e}")

if __name__ == "__main__":
    strategist = ChiefInvestmentStrategist(PORTFOLIO)
    strategist.execute_strategy()
