import sys
import os
import json
import pandas as pd
from datetime import datetime

# 🔧 Aggiunge la root del progetto Strategist al percorso
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

# ✅ Ora gli import funzionano
from data_sources.data_retriever import get_all_data
from data_sources.macro_data_retriever import get_cpi_data
from data_visualizer.plotter import plot_price_performance, plot_quarterly_financials
from agents.guru_strategy import guru_strategy, guru_filters
from agents.data_fetcher import fetch_stock_data, fetch_etf_data

# Moduli strategici e dati reali
from agents.guru_strategy import guru_strategy, guru_filters
from agents.data_fetcher import fetch_stock_data, fetch_etf_data


# ==============================
# DATI UTENTE E PORTAFOGLIO
# ==============================
PORTFOLIO = {
    'ENI.MI': {'shares': 100, 'buy_price': 13.00},
    'ISP.MI': {'shares': 200, 'buy_price': 2.50},
    'AAPL': {'shares': 10, 'buy_price': 170.00},
}


class ChiefInvestmentStrategist:
    """
    Agente principale che orchestra i blocchi della strategia (steps).
    """

    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.data = {}

    def execute_strategy(self):
        """
        Esegue in sequenza i blocchi principali della strategia.
        Aggiungi qui gli step futuri (12..25) quando pronti.
        """
        print("🚀 L'Agente Chief Investment Strategist sta avviando l'analisi...")

        # Blocchi 1-5: dati, valore, P/L, grafici, macro
        self.step_1_retrieve_data()
        self.step_2_calculate_total_value()
        self.step_3_analyze_pl()
        self.step_4_generate_ytd_charts()
        self.step_5_macro_analysis()

        # Blocchi 6: screener azioni con dati reali + strategie guru
        self.step_6_stock_screener()

        # Blocchi 7-9: report e export
        self.step_7_generate_final_report()
        self.step_8_portfolio_check()
        self.step_9_export_to_json()

        # Blocchi 10-11: screener ETF e asset allocation
        self.step_10_etf_screener()
        self.step_11_asset_allocation()

        print("✅ Analisi completa. Il tuo report è pronto e salvato in un file JSON.")

    # ==============================
    # STEP 1-5: DATI E MACRO
    # ==============================

    def step_1_retrieve_data(self):
        """BLOCCO 1: Recupera i dati di tutti i titoli del portafoglio."""
        print("Fase 1: Recupero dei dati...")

        for ticker, info in self.portfolio.items():
            data_retrieved = get_all_data(ticker)
            if data_retrieved and data_retrieved.get('price') is not None:
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
        self.data['pl_results'] = pd.DataFrame(results) if results else pd.DataFrame()
        print(f"✅ P/L totale del portafoglio calcolato: {total_pl:,.2f}")
        print("\nDettaglio P/L:")
        if not self.data['pl_results'].empty:
            print(self.data['pl_results'].to_string(index=False))
        else:
            print("Nessun dato disponibile.")

    def step_4_generate_ytd_charts(self):
        """BLOCCO 4: Generazione grafici di performance YTD."""
        print("Fase 4: Generazione grafici YTD...")
        for ticker, info in self.portfolio.items():
            if ticker in self.data and 'history' in self.data[ticker]:
                hist = self.data[ticker]['history']
                if hist is not None and not hist.empty:
                    print(f"Generando grafico YTD per {ticker}...")
                    plot_price_performance(ticker, hist)
                else:
                    print(f"❌ Dati storici non disponibili per {ticker}. Saltando il grafico.")
            else:
                print(f"❌ Dati storici non disponibili per {ticker}. Saltando il grafico.")

    def step_5_macro_analysis(self):
        """BLOCCO 5: Esegue un'analisi macroeconomica."""
        print("Fase 5: Analisi macro...")
        cpi_data = get_cpi_data()

        if cpi_data is not None and not cpi_data.empty:
            self.data['cpi_data'] = cpi_data
            last_cpi_value = cpi_data.iloc[-1]
            prev_cpi_value = cpi_data.iloc[-2] if len(cpi_data) > 1 else last_cpi_value
            cpi_change = ((last_cpi_value - prev_cpi_value) / prev_cpi_value) * 100 if prev_cpi_value != 0 else 0

            if cpi_change > 0.5:
                self.data['macro_signal'] = 'inflazione_in_aumento'
            else:
                self.data['macro_signal'] = 'inflazione_stabile'

            print(f"✅ Dati CPI pronti per l'analisi. Segnale: {self.data['macro_signal']}.")
        else:
            print("❌ Impossibile recuperare dati CPI. Saltando l'analisi macro.")
            self.data['macro_signal'] = 'errore'

    # ==============================
    # STEP 6: SCREENER AZIONI
    # ==============================

    def step_6_stock_screener(self):
        """
        BLOCCO 6: Screening titoli in base a segnale macro e strategie guru.
        Usa dati reali (Alpha Vantage tramite data_fetcher).
        """
        print("Fase 6: Screening e Selezione di nuovi titoli...")

        macro_signal = self.data.get('macro_signal', 'errore')
        regime = "defensive" if macro_signal == "inflazione_in_aumento" else "growth"
        goal = "rendita" if regime == "defensive" else "accumulo"

        print(f"📊 Regime macro rilevato: {regime.upper()} | Obiettivo: {goal.upper()}")

        gurus = guru_strategy(regime, goal)
        filters = guru_filters(gurus)
        print(f"🧠 Strategie attivate: {', '.join(gurus)}")
        print(f"🔍 Criteri di selezione: {filters}")

        # Lista di esempio da espandere (USA + difensivi)
        candidate_tickers = ["JNJ", "KO", "NVDA", "AAPL", "MSFT", "PEP", "UNH", "PG"]

        selected_stocks = []

        for ticker in candidate_tickers:
            try:
                stock = fetch_stock_data(ticker)
                if not stock or stock.get("price") is None:
                    print(f"⚠️ Dati incompleti per {ticker}.")
                    continue

                roe = float(stock.get("roe", 0) or 0)
                payout = float(stock.get("payout_ratio", 0) or 0)
                sector = (stock.get("sector") or "").lower()

                # Applica filtri guru (value, quality, innovation)
                for f in filters:
                    if f["type"] == "value" and roe >= f.get("roe_min", 10):
                        selected_stocks.append(stock)
                        break
                    elif f["type"] == "quality" and roe >= 15 and payout < 0.6:
                        selected_stocks.append(stock)
                        break
                    elif f["type"] == "innovation" and sector == f.get("sector", "").lower():
                        selected_stocks.append(stock)
                        break

            except Exception as e:
                print(f"❌ Errore nel recupero dati per {ticker}: {e}")

        self.data["screener_results"] = selected_stocks

        if selected_stocks:
            print(f"✅ Titoli selezionati: {[s['ticker'] for s in selected_stocks]}")
        else:
            print("❌ Nessun titolo ha superato i criteri di screening.")

    # ==============================
    # STEP 7-9: REPORT ED EXPORT
    # ==============================

    def step_7_generate_final_report(self):
        """BLOCCO 7: Crea un report finale leggibile a console."""
        print("Fase 7: Generazione del report...")
        print("\n" + "=" * 80)
        print("📑 RISULTATI ANALISI PORTAFOGLIO (aggiornati in tempo reale)")
        print(f"💰 Valore totale portafoglio: {self.data.get('total_value', 0):,.2f}")
        print(f"📈 P/L totale non realizzato: {self.data.get('total_pl', 0):,.2f}")
        print("=" * 80)

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
        BLOCCO 8: Controllo dei titoli esistenti nel portafoglio.
        (Placeholder per analisi bilancio, sentiment, fair value)
        """
        print("\nFase 8: Controllo dei titoli esistenti nel portafoglio...")
        for ticker in self.portfolio.keys():
            print(f"Analisi di bilancio e sentiment per {ticker}...")
            # TODO: Integrare analisi avanzate (es. margini, leva, sentiment news)
        print("✅ Controllo del portafoglio completato.")

    def step_9_export_to_json(self):
        """
        BLOCCO 9: Esporta i dati analizzati in un file JSON.
        """
        print("\nFase 9: Esportazione dei dati in formato JSON...")

        export_data = {
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_value': self.data.get('total_value'),
            'total_pl': self.data.get('total_pl'),
            'macro_signal': self.data.get('macro_signal'),
            'screener_results': self.data.get('screener_results', []),
            'etf_screener_results': self.data.get('etf_screener_results', []),
            'asset_allocation': self.data.get('asset_allocation', {}),
            'portfolio_details': []
        }

        if 'pl_results' in self.data and not self.data['pl_results'].empty:
            export_data['portfolio_details'] = self.data['pl_results'].to_dict('records')

        try:
            with open('portfolio_data.json', 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=4, ensure_ascii=False)
            print("✅ Dati del portafoglio esportati con successo in 'portfolio_data.json'.")
        except Exception as e:
            print(f"❌ Errore durante l'esportazione in JSON: {e}")

    # ==============================
    # STEP 10: SCREENER ETF
    # ==============================

    def step_10_etf_screener(self):
        """
        BLOCCO 10: Screening ETF in base a regime macro, distribuzione e qualità.
        Usa holdings e dividendi da Finnhub tramite data_fetcher.
        """
        print("Fase 10: Screening ETF...")

        macro_signal = self.data.get('macro_signal', 'errore')
        regime = "defensive" if macro_signal == "inflazione_in_aumento" else "growth"
        goal = "rendita" if regime == "defensive" else "accumulo"

        print(f"📊 Regime macro rilevato: {regime.upper()} | Obiettivo: {goal.upper()}")

        # Lista base (estendibile a ETC/UCITS europei se disponibili su Finnhub)
        candidate_etfs = ["SPY", "VYM", "HDV", "SCHD", "DGRO"]

        selected_etfs = []

        for ticker in candidate_etfs:
            try:
                etf = fetch_etf_data(ticker)
                holdings = etf.get("holdings", []) or []
                dividends = etf.get("dividends", []) or []

                # Distribuzione: almeno 4 dividendi positivi (ultimo ~12 mesi)
                recent_dividends = [d for d in dividends if isinstance(d, dict) and d.get("amount", 0) > 0]
                has_distribution = len(recent_dividends) >= 4

                # Qualità holdings: proxy semplice con lista di blue chips
                healthy_companies = {"JNJ", "KO", "PEP", "PG", "MSFT", "AAPL", "UNH", "COST"}
                healthy_count = sum(1 for h in holdings if (h.get("symbol") or h.get("isin") or "") in healthy_companies)
                quality_score = healthy_count / max(len(holdings), 1)

                if has_distribution and quality_score >= 0.6:
                    selected_etfs.append({
                        "ticker": ticker,
                        "distribution_ok": has_distribution,
                        "quality_score": round(quality_score, 2),
                        "holdings_count": len(holdings)
                    })

            except Exception as e:
                print(f"❌ Errore nel recupero dati ETF {ticker}: {e}")

        self.data["etf_screener_results"] = selected_etfs

        if selected_etfs:
            print(f"✅ ETF selezionati: {[etf['ticker'] for etf in selected_etfs]}")
        else:
            print("❌ Nessun ETF ha superato i criteri di screening.")

    # ==============================
    # STEP 11: ASSET ALLOCATION
    # ==============================

    def step_11_asset_allocation(self):
        """
        BLOCCO 11: Costruisce una ripartizione strategica del portafoglio.
        """
        print("Fase 11: Asset Allocation...")

        macro_signal = self.data.get('macro_signal', 'errore')
        regime = "defensive" if macro_signal == "inflazione_in_aumento" else "growth"
        goal = "rendita" if regime == "defensive" else "accumulo"

        print(f"📊 Regime macro: {regime.upper()} | Obiettivo: {goal.upper()}")

        if regime == "growth" and goal == "accumulo":
            allocation = {
                "azioni": 60,
                "etf_growth": 25,
                "obbligazioni": 10,
                "liquidità": 5
            }
        elif regime == "defensive" and goal == "rendita":
            allocation = {
                "azioni_dividendo": 30,
                "etf_dividendo": 40,
                "obbligazioni": 20,
                "liquidità": 10
            }
        elif regime == "neutral":
            allocation = {
                "azioni": 40,
                "etf_misti": 30,
                "obbligazioni": 20,
                "liquidità": 10
            }
        else:
            allocation = {
                "azioni": 35,
                "etf": 35,
                "obbligazioni": 20,
                "liquidità": 10
            }

        self.data["asset_allocation"] = allocation
        print("✅ Allocazione strategica completata:")
        for k, v in allocation.items():
            print(f" - {k}: {v}%")



if __name__ == "__main__":
    strategist = ChiefInvestmentStrategist(PORTFOLIO)
    strategist.execute_strategy()