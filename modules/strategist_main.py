import datetime
import pandas as pd
import math
import matplotlib.pyplot as plt
import os
import json

from data_sources.data_retriever import get_all_data
from modules.subagent_stocks import propose_portfolio

# ====================
# Funzione Principale
# ====================

def run_analysis(portfolio_data: dict, years_to_analyze: int = 5):
    """
    Analizza il portafoglio fornito e genera un'analisi.
    """
    
    # Questo modulo ora si basa interamente sul sub-agente
    # "propose_portfolio" che hai fornito.
    
    print("\n--- 🧠 Avvio Agente AI per Analisi Autonoma ---")
    
    try:
        # Chiama la funzione di selezione del portafoglio
        portfolio_proposal = propose_portfolio(
            filters={
                "min_etf_aum_million": 150,
                "etf_distribution": "any",
                "allowed_domiciles": ("IE", "LU"),
                "allowed_etf_currencies": ("EUR", "USD"),
                "max_etf_ter": 0.6,
                "require_european_dividend": True,
                "stock_price_min": 5.0,
                "stock_price_max": 200.0,
                "allowed_stock_currencies": ("EUR",),
                "min_dividend_yield_pct": 2.0,
                "total_picks": 7
            }
        )
        
        # Stampa i risultati in un formato leggibile
        print("\n--- ✅ Selezione Autonoma Completata ---")
        print(f"Segnali macro: {portfolio_proposal['macro']['comment']}")
        print(f"Temi favoriti: {', '.join(portfolio_proposal['macro']['favored_themes'])}")

        print("\n--- ETF Selezionati ---")
        if portfolio_proposal['etf']:
            for etf in portfolio_proposal['etf']:
                print(f" - {etf['name']} ({etf['ticker']})")
                print(f"   Motivo: {etf['reason']}")
        else:
            print("Nessun ETF selezionato con i filtri correnti.")

        print("\n--- Azioni Europee Selezionate ---")
        if portfolio_proposal['stocks']:
            for stock in portfolio_proposal['stocks']:
                print(f" - {stock['name']} ({stock['ticker']})")
                print(f"   Motivo: {stock['reason']}")
        else:
            print("Nessuna azione selezionata con i filtri correnti.")

    except Exception as e:
        print(f"❌ Errore durante l'esecuzione del modulo Strategist: {e}")
