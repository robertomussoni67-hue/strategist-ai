import sys

# Mostrare i grafici a schermo? False = solo salvataggio PNG, nessun blocco
SHOW_PLOTS = False

import matplotlib
if not SHOW_PLOTS:
    # Backend non interattivo: evita finestre e blocchi
    matplotlib.use("Agg")

import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

# === Controllo argomenti ===
if len(sys.argv) < 2:
    print("Uso: python analisi_enel.py <TICKER1> <TICKER2> ...")
    sys.exit(1)

tickers = sys.argv[1:]  # es. ["ENEL.MI", "ENI.MI", "ISP.MI"]

summary_records = []

for ticker in tickers:
    print("\n" + "-" * 70)
    print(f"=== Analisi per {ticker} ===")

    # === Download dati ===
    # Nota: non impostiamo 'end' per prendere l'ultima barra disponibile
    data = yf.download(
        ticker,
        start="2023-01-01",
        auto_adjust=True,
        progress=False
    )

    if data.empty:
        print(f"[!] Nessun dato scaricato per {ticker}. Salto...")
        continue

    # === Calcolo RSI (14) ===
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=14, min_periods=14).mean()
    avg_loss = loss.rolling(window=14, min_periods=14).mean()
    rs = avg_gain / avg_loss
    data["RSI"] = 100 - (100 / (1 + rs))

    # === Calcolo MACD (12, 26, 9) ===
    ema12 = data["Close"].ewm(span=12, adjust=False).mean()
    ema26 = data["Close"].ewm(span=26, adjust=False).mean()
    data["MACD"] = ema12 - ema26
    data["Signal"] = data["MACD"].ewm(span=9, adjust=False).mean()

    # === Output ultimi dati ===
    print(data.tail())

    # === ALERT RSI ===
    last_idx = data["RSI"].last_valid_index()
    if last_idx is not None:
        last_rsi = float(data.at[last_idx, "RSI"])
        stato = "IPERCOMPRATO (>70)" if last_rsi > 70 else ("IPERVENDUTO (<30)" if last_rsi < 30 else "NEUTRA")
        last_close = float(data.at[last_idx, "Close"])
        print("\n" + "="*60)
        print(f"Ticker: {ticker} | Data: {last_idx.date()} | Close: {last_close:.3f} | RSI: {last_rsi:.2f} → {stato}")
        print("="*60 + "\n")

        summary_records.append({
            "Ticker": ticker,
            "Data": last_idx.date().isoformat(),
            "Close": round(last_close, 3),
            "RSI": round(last_rsi, 2),
            "Stato": stato
        })
    else:
        print("\n[!] RSI non disponibile: servono almeno 14 barre per il calcolo.\n")

    # === Grafico ===
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

    # Titolo principale del grafico
    fig.suptitle(f"Analisi tecnica: {ticker}", fontsize=16, fontweight="bold")

    # Prezzo
    ax1.plot(data.index, data["Close"], label="Close", color="blue")
    ax1.set_ylabel("Prezzo")
    ax1.legend()
    ax1.grid(True)

    # RSI
    ax2.plot(data.index, data["RSI"], label="RSI", color="purple")
    ax2.axhline(70, color="red", linestyle="--")   # ipercomprato
    ax2.axhline(30, color="green", linestyle="--") # ipervenduto
    ax2.set_ylabel("RSI")
    ax2.legend()
    ax2.grid(True)

    # MACD
    ax3.plot(data.index, data["MACD"], label="MACD", color="orange")
    ax3.plot(data.index, data["Signal"], label="Signal", color="black", linestyle="--")
    ax3.set_ylabel("MACD")
    ax3.legend()
    ax3.grid(True)

    # Lascia spazio per il titolo in alto
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Salvataggio PNG e gestione finestre
    out_png = f"analisi_{ticker}.png"
    plt.savefig(out_png, dpi=300)
    if SHOW_PLOTS:
        plt.show()   # blocca finché chiudi la finestra
    else:
        plt.close()  # nessuna finestra, nessun blocco

# === Riepilogo finale in tabella e CSV ===
if summary_records:
    df = pd.DataFrame(summary_records, columns=["Ticker", "Data", "Close", "RSI", "Stato"])

    # Ordina per RSI decrescente per avere prima i più tirati
    df = df.sort_values(by="RSI", ascending=False, ignore_index=True)

    print("\n=== Riepilogo finale RSI ===")
    print(df.to_string(index=False))

    # Salva anche su CSV per consultazione (apri con Excel)
    out_csv = "rsi_summary.csv"
    df.to_csv(out_csv, index=False, encoding="utf-8-sig")
    print(f"\nRiepilogo salvato in: {out_csv}\n")
else:
    print("\n[!] Nessun riepilogo da mostrare (nessun dato valido o RSI non disponibile).\n")