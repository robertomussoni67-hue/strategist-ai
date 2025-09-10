import sys
import os
import asyncio

# 🔧 Aggiunge la root del progetto Strategist al percorso
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from agents.macro_agent import run

async def test_run():
    result = await run()
    print("📊 Risultato dell'agente macro:")
    print(f"Regime: {result.get('regime')}")
    print(f"Inflazione YoY: {result.get('inflation_yoy')}%")
    print(f"Tasso di policy: {result.get('policy_rate')}%")
    print(f"Crescita PIL: {result.get('gdp_growth')}%")
    print(f"Disoccupazione: {result.get('unemployment_rate')}%")
    print(f"PMI: {result.get('pmi_index')}")
    print("Outlook 3-6 mesi:")
    for k, v in result.get("outlook_3_6m", {}).items():
        print(f" - {k}: {v}")

if __name__ == "__main__":
    asyncio.run(test_run())