"""
macro_signals.py
Autore: Sonia
Data: 27 agosto 2025

Descrizione:
Modulo per analisi tecnica e macroeconomica su titoli ed ETF.
Include calcolo RSI, medie mobili, rilevamento segnali di regime
e generazione grafici/report con nome dell'asset analizzato.
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# =======================
# Funzioni di supporto
# =======================

def get_macro_data(ticker="^GSPC", period="6mo"):
    """Scarica i dati storici dal mercato."""
    data = yf.download(ticker, period=period, interval="1d")
    return data

def get_asset_name(ticker):
    """Restituisce il nome completo dell'asset (es. ETF, indice, azione)."""
    try:
        info = yf.Ticker(ticker).info
        return info.get("longName", ticker)
    except Exception:
        return ticker

def calculate_indicators(df):
    """Aggiunge RSI e medie mobili al DataFrame."""
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df

def detect_regime(df):
    """Rileva segnali di ipercomprato/ipervenduto in base all'RSI."""
    signals = []
    for idx in df.index:
        rsi_value = df.loc[idx, 'RSI']
        try:
            rsi_float = float(rsi_value)
            if rsi_float > 70:
                signals.append((idx, 'Ipercomprato'))
            elif rsi_float < 30:
                signals.append((idx, 'Ipervenduto'))
        except (TypeError, ValueError):
            continue
    return signals

def plot_chart(df, ticker, signals):
    """Mostra grafico prezzi + medie mobili + segnali RSI."""
    asset_name = get_asset_name(ticker)

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label='Chiusura', color='blue')
    plt.plot(df.index, df['SMA20'], label='SMA20', color='orange', linestyle='--')
    plt.plot(df.index, df['SMA50'], label='SMA50', color='magenta', linestyle='--')

    shown_labels = set()
    for date, sig in signals:
        color = 'red' if sig == 'Ipercomprato' else 'green'
        label = sig if sig not in shown_labels else None
        plt.scatter(date, df.loc[date]['Close'], color=color, marker='o', s=100, label=label)
        shown_labels.add(sig)

    plt.title(f"Andamento: {asset_name} ({ticker})")
    plt.xlabel("Data")
    plt.ylabel("Prezzo")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def generate_report(ticker="^GSPC"):
    """Genera un report semplice dei segnali più recenti."""
    asset_name = get_asset_name(ticker)
    data = get_macro_data(ticker)
    data = calculate_indicators(data)
    signals = detect_regime(data)

    latest = signals[-5:] if signals else []
    report_lines = [f"Ultimi segnali per {asset_name} ({ticker}):"]
    for date, sig in latest:
        report_lines.append(f"{date.date()} → {sig}")
    return "\n".join(report_lines)

# =======================
# Funzione principale
# =======================

def execute_macro(command, ticker="^GSPC"):
    if command == "start":
        data = get_macro_data(ticker)
        data = calculate_indicators(data)
        signals = detect_regime(data)
        plot_chart(data, ticker, signals)
    elif command == "report":
        print(generate_report(ticker))
    else:
        print(f"Comando '{command}' non riconosciuto.")

# =======================
# Avvio interattivo
# =======================

if __name__ == "__main__":
    print("📊 Strategist AI - Analisi tecnica e macroeconomica")
    ticker = input("Inserisci il ticker (es. MSFT, SPY, VTI, ^GSPC): ").strip().upper()
    command = input("Vuoi 'start' (grafico) o 'report' (testo)? ").strip().lower()
    execute_macro(command, ticker)