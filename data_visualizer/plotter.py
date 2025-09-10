import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import os

def check_and_create_dir(dir_name):
    """
    Verifica se la cartella esiste, altrimenti la crea.
    """
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print(f"Cartella '{dir_name}' creata con successo.")
    else:
        print(f"La cartella '{dir_name}' esiste già.")

def plot_price_performance(ticker: str, history_df: pd.DataFrame):
    """
    Genera un grafico interattivo della performance del prezzo del titolo da inizio anno.
    Il grafico viene salvato come file HTML.
    """
    if history_df is None or history_df.empty:
        print(f"Non ci sono dati storici disponibili per {ticker} per creare il grafico.")
        return None

    start_of_year = datetime(datetime.now().year, 1, 1)
    ytd_history = history_df[history_df.index >= start_of_year.strftime('%Y-%m-%d')]

    if ytd_history.empty:
        print(f"Non ci sono dati da inizio anno per {ticker} per creare il grafico.")
        return None

    fig = go.Figure(data=go.Scatter(x=ytd_history.index, y=ytd_history['Close'], mode='lines', name='Prezzo di chiusura'))
    
    fig.update_layout(
        title=f"Andamento del Prezzo di {ticker} da Inizio Anno",
        xaxis_title="Data",
        yaxis_title="Prezzo (USD)",
        xaxis_rangeslider_visible=True
    )
    
    check_and_create_dir('report')
    
    output_path = f'report/{ticker}_ytd_performance.html'
    fig.write_html(output_path)
    print(f"✅ Grafico interattivo per {ticker} salvato in '{output_path}'.")
    return output_path

def plot_quarterly_financials(ticker: str, revenues: pd.Series, earnings: pd.Series):
    """
    Genera un grafico interattivo a barre dei ricavi e utili trimestrali.
    Il grafico viene salvato come file HTML.
    """
    if revenues is None and earnings is None:
        print(f"Nessun dato finanziario trimestrale disponibile per {ticker}.")
        return None
        
    fig = go.Figure()
    
    if revenues is not None and not revenues.empty:
        fig.add_trace(go.Bar(
            x=[q.strftime('%Y-%m-%d') for q in revenues.index],
            y=revenues.values,
            name='Ricavi (Total Revenue)'
        ))

    if earnings is not None and not earnings.empty:
        fig.add_trace(go.Bar(
            x=[q.strftime('%Y-%m-%d') for q in earnings.index],
            y=earnings.values,
            name='Utili (Earnings)'
        ))

    fig.update_layout(
        title=f"Ricavi e Utili Trimestrali di {ticker}",
        xaxis_title="Trimestre",
        yaxis_title="Valore",
        barmode='group'
    )
    
    check_and_create_dir('report')
    
    output_path = f'report/{ticker}_quarterly_financials.html'
    fig.write_html(output_path)
    print(f"✅ Grafico finanziario per {ticker} salvato in '{output_path}'.")
    return output_path
