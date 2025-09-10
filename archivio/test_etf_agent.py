import pandas as pd
from strategist.agents.etf_agent import run_etf_analysis
import logging

# Configura il logging per visualizzare gli output dell'agente
logging.basicConfig(level=logging.INFO)

# --- Creazione dei dati di esempio ---
# Questo DataFrame simula i dati che il connettore API recupererebbe
# per l'agente.
sample_etfs_data = pd.DataFrame([
    {"ticker": "VTI", "nome": "Vanguard Total Stock Market", "tipo": "accumulo", "settore": "broad", "prezzo": 220},
    {"ticker": "QQQ", "nome": "Invesco NASDAQ 100", "tipo": "accumulo", "settore": "technology", "prezzo": 450},
    {"ticker": "XLU", "nome": "Utilities Select Sector SPDR", "tipo": "distribuzione", "settore": "utilities", "prezzo": 75},
    {"ticker": "SPY", "nome": "SPDR S&P 500", "tipo": "accumulo", "settore": "broad", "prezzo": 520},
    {"ticker": "FXI", "nome": "iShares China Large-Cap", "tipo": "accumulo", "settore": "emerging_markets", "prezzo": 30},
    {"ticker": "XLK", "nome": "Technology Select Sector SPDR", "tipo": "accumulo", "settore": "technology", "prezzo": 200},
])

print("--- Eseguo il test per il regime 'risk_on' ---")
# Ci aspettiamo di vedere ETF con settore 'technology' e 'broad'
results_risk_on = run_etf_analysis(sample_etfs_data, regime="risk_on")
print(f"ETF selezionati ({len(results_risk_on)}): {[etf['ticker'] for etf in results_risk_on]}")

print("\n--- Eseguo il test per il regime 'risk_off' ---")
# Ci aspettiamo di vedere ETF con settore 'utilities' e 'broad'
results_risk_off = run_etf_analysis(sample_etfs_data, regime="risk_off")
print(f"ETF selezionati ({len(results_risk_off)}): {[etf['ticker'] for etf in results_risk_off]}")

print("\n--- Eseguo il test per il regime 'neutral' ---")
# Ci aspettiamo di vedere tutti gli ETF, perché il regime è bilanciato
results_neutral = run_etf_analysis(sample_etfs_data, regime="neutral")
print(f"ETF selezionati ({len(results_neutral)}): {[etf['ticker'] for etf in results_neutral]}")
