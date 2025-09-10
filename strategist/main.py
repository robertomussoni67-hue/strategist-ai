# main.py
import schedule
import time
from datetime import datetime

# Import dai moduli
from data_sources.forex_source import get_eur_usd
from data_sources.yahoo_source import get_prices
from data_sources.news_source import get_latest_news
from stratega_ai.main import avvia_ai  # resta com'era

def stratega():
    print(f"\n=== Aggiornamento: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    # Cambio EUR/USD
    eur_usd, from_cache = get_eur_usd()
    if eur_usd:
        print(f"EUR/USD{' (cache)' if from_cache else ''}: {eur_usd}")
    
    # Prezzi azioni/ETF
    prezzi = get_prices()
    for ticker, prezzo in prezzi.items():
        print(f"{ticker}: {prezzo}")
    
    # Notizie
    notizie = get_latest_news()
    for fonte, titoli in notizie.items():
        print(f"--- News da {fonte} ---")
        for titolo in titoli:
            print(f"- {titolo}")
    
    # Avvio AI
    avvia_ai()
    print("=== Fine ciclo ===\n")

if __name__ == "__main__":
    print("Avvio motore Stratega modularizzato...")
    stratega()
    schedule.every(10).minutes.do(stratega)
    while True:
        schedule.run_pending()
        time.sleep(1)