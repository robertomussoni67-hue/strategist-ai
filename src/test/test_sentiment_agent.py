import sys
import os
import asyncio

# 🔧 Aggiunge la root del progetto Strategist al percorso
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from agents.sentiment_agent import run

async def test_run():
    result = await run()
    print("🧠 Risultato dell'agente sentiment:")
    print(f"Sentiment di mercato: {result.get('market_sentiment')}")
    print(f"Confidenza: {result.get('confidence')}")
    print("Dettagli:")
    for k, v in result.get("details", {}).items():
        print(f" - {k}: {v}")

if __name__ == "__main__":
    asyncio.run(test_run())