import sys
import os
import asyncio

# 🔧 Aggiunge la root del progetto Strategist al percorso
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from agents.etf_agent import run

async def test_run():
    result = await run()
    print("📊 Risultato dell'agente ETF:")
    etfs = result.get("etf", [])
    if not etfs:
        print("⚠️ Nessun ETF selezionato.")
    for etf in etfs:
        print(f" - {etf['ticker']}: {etf['name']} | TER: {etf['ter']} | AUM: {etf['aum_eur_m']}M | {etf['distribution']}")

if __name__ == "__main__":
    asyncio.run(test_run())