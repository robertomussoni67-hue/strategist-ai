import logging
import os
import sys

# Aggiunge manualmente la cartella 'modules' al percorso
current_dir = os.path.dirname(__file__)
modules_path = os.path.abspath(os.path.join(current_dir, "..", "..", "modules"))
if modules_path not in sys.path:
    sys.path.append(modules_path)

from subagent_etf import select_etfs

log = logging.getLogger(__name__)

async def run():
    try:
        etf_selection = select_etfs(
            filters={
                "min_aum_million": 150,
                "distribution": "any",
                "allowed_domiciles": ("IE", "LU"),
                "allowed_currencies": ("EUR", "USD"),
                "max_ter": 0.6,
                "require_dividend": True,
                "total_picks": 5
            }
        )
        return {"etf": etf_selection}
    except Exception:
        log.error("Errore nell'agente ETF", exc_info=True)
        return {"error": "ETF agent failed", "etf": []}