import logging
import os
import sys

# Aggiunge manualmente la cartella 'modules' al percorso
current_dir = os.path.dirname(__file__)
modules_path = os.path.abspath(os.path.join(current_dir, "..", "..", "modules"))
if modules_path not in sys.path:
    sys.path.append(modules_path)

from subagent_stocks import propose_portfolio

log = logging.getLogger(__name__)

async def run():
    try:
        portfolio_proposal = propose_portfolio(
            filters={
                "min_etf_aum_million": 150,
                "etf_distribution": "any",
                "allowed_domiciles": ("IE", "LU"),
                "allowed_etf_currencies": ("EUR", "USD"),
                "max_etf_ter": 0.6,
                "require_european_dividend": True,
                "stock_price_min": 5.0,
                "stock_price_max": 200.0,
                "allowed_stock_currencies": ("EUR",),
                "min_dividend_yield_pct": 2.0,
                "total_picks": 7
            }
        )

        return {
            "macro": portfolio_proposal.get("macro", {}),
            "etf": portfolio_proposal.get("etf", []),
            "stocks": portfolio_proposal.get("stocks", [])
        }
    except Exception:
        log.error("Errore nell'agente stocks", exc_info=True)
        return {"error": "Stocks agent failed", "macro": {}, "etf": [], "stocks": []}