import csv
import os
from datetime import datetime

def save_stocks_csv(stocks):
    if not stocks:
        return

    filename = f"reports\\stocks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    fieldnames = ["ticker", "name"]

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for stock in stocks:
                row = {key: stock.get(key, "") for key in fieldnames}
                writer.writerow(row)

        print(f"[CSV] Titoli salvati in: {filename}")
    except Exception as e:
        print(f"[CSV] Errore salvataggio titoli: {e}")

def save_etf_csv(etfs):
    if not etfs:
        return

    filename = f"reports\\etf_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    fieldnames = ["ticker", "name", "ter", "aum", "style"]

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for etf in etfs:
                row = {key: etf.get(key, "") for key in fieldnames}
                writer.writerow(row)

        print(f"[CSV] ETF salvati in: {filename}")
    except Exception as e:
        print(f"[CSV] Errore salvataggio ETF: {e}")