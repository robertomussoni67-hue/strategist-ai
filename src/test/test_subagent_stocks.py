import sys
import os

# 🔧 Aggiunge la root del progetto Strategist al percorso
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from subagent_stocks import propose_portfolio

results = propose_portfolio(macro_regime="growth", goal="accumulo")
print("✅ Titoli selezionati:")
for r in results:
    print(f"{r['ticker']} | {r['name']} | Settore: {r['sector']} | ROE: {r['roe']} | Payout: {r['payout']}")