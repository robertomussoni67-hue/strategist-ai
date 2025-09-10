import sys
import os
import asyncio

# 🔧 Aggiunge la root del progetto Strategist al percorso
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from agents.stocks_agent import run

async def test_run():
    result = await run()
    print("📊 Risultato dell'agente stocks:")
    print("Macro:", result.get("macro", {}))
    print("ETF selezionati:")
    for etf in result.get("etf", []):
        print(f" - {etf['ticker']}: {etf['name']} ({etf['reason']})")
    print("Titoli selezionati:")
    for stock in result.get("stocks", []):
        print(f" - {stock['ticker']}: {stock['name']}")

if __name__ == "__main__":
    asyncio.run(test_run())