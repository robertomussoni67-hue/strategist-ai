import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# =======================
# Funzioni di supporto
# =======================

def get_macro_data(ticker="^GSPC", period="6mo"):
    """Scarica i dati storici dal mercato (es. S&P500 di default)."""
    data = yf.download(ticker, period=period, interval="1d")
    return data

def calculate_indicators(df):
    """Aggiunge RSI e medie mobili al DataFrame."""
    # Media mobile a 20 e 50 giorni
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    
    # Calcolo RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df

def detect_regime(df):
    """Rileva segnali di ipercomprato/ipervenduto in base all'RSI."""
    signals = []
    for idx, row in df.iterrows():
        if row['RSI'] > 70:
            signals.append((idx, 'Ipercomprato'))
        elif row['RSI'] < 30:
            signals.append((idx, 'Ipervenduto'))
    return signals

def plot_chart(df, ticker, signals):
    """Mostra grafico prezzi + medie mobili + segnali RSI."""
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label='Chiusura', color='blue')
    plt.plot(df.index, df['SMA20'], label='SMA20', color='orange', linestyle='--')
    plt.plot(df.index, df['SMA50'], label='SMA50', color='magenta', linestyle='--')

    for date, sig in signals:
        color = 'red' if sig == 'Ipercomprato' else 'green'
        plt.scatter(date, df.loc[date]['Close'], color=color, marker='o', s=100, label=sig)

    plt.title(f"Andamento {ticker}")
    plt.xlabel("Data")
    plt.ylabel("Prezzo")
    plt.legend()
    plt.grid(True)
    plt.show()

def generate_report(ticker="^GSPC"):
    """Genera un report semplice dei segnali più recenti."""
    data = get_macro_data(ticker)
    data = calculate_indicators(data)
    signals = detect_regime(data)

    latest = signals[-5:] if signals else []
    report_lines = [f"Ultimi segnali per {ticker}:"]
    for date, sig in latest:
        report_lines.append(f"{date.date()} → {sig}")
    return "\n".join(report_lines)

# =======================
# Funzione principale
# =======================

def execute_macro(command):
    if command == "start":
        ticker = "^GSPC"  # S&P 500 di default
        data = get_macro_data(ticker)
        data = calculate_indicators(data)
        signals = detect_regime(data)
        plot_chart(data, ticker, signals)
    elif command == "report":
        print(generate_report("^GSPC"))
    else:
        print(f"Comando '{command}' non riconosciuto.")

# =======================
# ESECUZIONE AUTOMATICA
# =======================

execute_macro("report")