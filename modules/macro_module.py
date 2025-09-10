import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import os

# Importa i moduli di supporto
from modules.subagent_stocks import propose_portfolio, InvestorFilters

# =======================
# Funzioni di supporto
# =======================

def get_asset_name(ticker):
    """Restituisce il nome completo dell'asset da yfinance."""
    try:
        return yf.Ticker(ticker).info.get("longName", ticker)
    except Exception:
        return ticker

def plot_plotly_chart(df, ticker):
    """Crea e mostra un grafico interattivo con Plotly."""
    asset_name = get_asset_name(ticker)

    fig = go.Figure()

    # Aggiungi il grafico a candele (candlestick)
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['High'],
        close=df['Close'],
        name='Candele'
    ))

    fig.update_layout(
        title=f"Andamento {asset_name} ({ticker})",
        xaxis_rangeslider_visible=False
    )
    
    fig.show()

# =======================
# Funzione per l'analisi del trimestre
# =======================
def get_quarterly_data(ticker):
    """
    Recupera i dati trimestrali per entrate, spese e utile.
    """
    try:
        t = yf.Ticker(ticker)
        # Recupera i dati trimestrali di bilancio
        quarterly_financials = t.quarterly_financials

        if quarterly_financials.empty:
            print(f"⚠️ Dati finanziari trimestrali non disponibili per {ticker}.")
            return None

        # Prendi solo le colonne che ci interessano
        columns_of_interest = [
            'Total Revenue',
            'Operating Expenses',
            'Net Income'
        ]
        
        # Filtra e trasponi il dataframe per facilitare la lettura
        df = quarterly_financials.loc[columns_of_interest].T
        return df
        
    except Exception as e:
        print(f"❌ Errore nel recupero dati trimestrali per {ticker}: {e}")
        return None

# =======================
# Funzione principale del modulo
# =======================

def execute_macro(command, ticker=None):
    """
    Esegue il comando specificato per il modulo macro.
    """
    if command == "report":
        print("Funzione 'report' in sviluppo...")
    elif command == "analizza":
        print("Funzione 'analizza' in sviluppo...")
        # Ho rimosso la riga che causava l'errore 'analyze_stocks'
        # Dato che non esiste più.
        print("L'analisi del modulo macro è completata, ma la funzione 'analizza' non è ancora implementata.")

    elif command == "test_quarterly":
        if not ticker:
            print("⚠️ Specifica un ticker per il comando 'test_quarterly'.")
            return
        
        print(f"🔎 Recupero dati trimestrali per {ticker}...")
        df_quarterly = get_quarterly_data(ticker)

        if df_quarterly is not None:
            print("\n✅ Dati trimestrali recuperati con successo:")
            print(df_quarterly)
            print("\nReport del test completato. Ora puoi usare questi dati per un'analisi più approfondita.")
    else:
        print(f"⚠️ Comando '{command}' non riconosciuto dal modulo macro.")