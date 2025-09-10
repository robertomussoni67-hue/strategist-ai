import sys, os, json, logging
from pathlib import Path

# === SETUP PATH ===
project_root = Path(__file__).resolve().parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

# === SETUP LOGGING ===
LOG_FORMAT = "%(levelname)s | %(asctime)s | %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
log = logging.getLogger(__name__)

# === IMPORT AGENTI ===
from agents.macro_agent import run as run_macro
from agents.sentiment_agent import run as run_sentiment
from agents.stocks_agent import run as run_stocks
from agents.etf_agent import run as run_etf
from agents.commodities_agent import run as run_commodities

# === IMPORT MODULI ===
from src.modules.user_profile import UserProfile
from src.modules.philosophy_engine import compute_allocation
from src.modules.allocation_mapper import map_allocation_to_plan
from src.modules.memory_store import init_db, save_episode, load_last_episodes
from src.modules.memory_policy import adjust_strategy_based_on_memory
from src.modules.export import save_json
from src.modules.export_csv import save_stocks_csv, save_etf_csv
from src.modules.advisor_agent import explain_plan
from src.modules.backtest_engine import backtest_plan
from src.modules.risk_analyzer import analyze_portfolio_risk

# === VALIDAZIONE BASE ===
def _ok(v):
    return v is not None and v != "" and not (isinstance(v, list) and len(v) == 0)

def validate_output(agent_name, data):
    if not isinstance(data, dict):
        return False, [f"{agent_name}: output non è un dict"]

    required_fields = {
        "macro_agent": ["regime", "outlook_3_6m"],
        "sentiment_agent": ["market_sentiment", "confidence"],
        "stocks_agent": ["stocks"],
        "etf_agent": ["etf"],
        "commodities_agent": ["commodities"]
    }

    errors = []
    for field in required_fields.get(agent_name, []):
        if not _ok(data.get(field)):
            errors.append(f"{agent_name}: campo mancante o vuoto '{field}'")

    return len(errors) == 0, errors

# === ESECUZIONE ORCHESTRATA ===
def run_all():
    log.info("🚀 Avvio Strategist...")

    macro = run_macro()
    sentiment = run_sentiment()

    regime = macro.get("regime", "neutral")
    mood = sentiment.get("market_sentiment", "neutral")

    log.info(f"📊 Regime macro: {regime} | Sentiment: {mood}")

    stocks = run_stocks()
    etf = run_etf()
    commodities = run_commodities()

    # Validazione
    agents_data = {
        "macro_agent": macro,
        "sentiment_agent": sentiment,
        "stocks_agent": stocks,
        "etf_agent": etf,
        "commodities_agent": commodities
    }

    validation_report = {}
    for name, data in agents_data.items():
        ok, errors = validate_output(name, data)
        validation_report[name] = {"valid": ok, "errors": errors}

    result = {
        "macro": macro,
        "sentiment": sentiment,
        "stocks": stocks.get("stocks", []),
        "etf": etf.get("etf", []),
        "commodities": commodities.get("commodities", []),
        "validation": validation_report,
        "summary": f"{sum(1 for v in validation_report.values() if v['valid'])} agenti validati su {len(validation_report)}"
    }

    log.info("✅ Strategist completato.")
    return result

# === MAIN ===
if __name__ == "__main__":
    # 1) Profilo utente
    user = UserProfile(name="Roberto", age=45, risk_level="moderate", horizon_years=10)
    prefs = user.get_preferences()
    log.info(f"[Profilo] {user.describe()}")

    # 2) Esegui agenti
    final = run_all()

    # 3) Memoria
    init_db()
    episodes = load_last_episodes()
    warnings = adjust_strategy_based_on_memory(episodes)
    for w in warnings:
        log.warning(w)

    try:
        save_episode(
            regime=final["macro"]["regime"],
            sentiment=final["sentiment"]["market_sentiment"],
            tickers=[s.get("ticker", "") for s in final.get("stocks", [])],
            etfs=[e.get("ticker", "") for e in final.get("etf", [])]
        )
    except Exception as e:
        log.warning(f"Memoria: salvataggio episodio non riuscito: {e}")

    # 4) Allocazione operativa
    try:
        alloc_bundle = compute_allocation(
            macro_outlook=final["macro"].get("outlook_3_6m", {}),
            sentiment=final["sentiment"],
            preferences=prefs
        )

        picks = {
            "stocks": final.get("stocks", []),
            "etf": final.get("etf", []),
            "etc": final.get("commodities", [])
        }

        plan = map_allocation_to_plan(
            weights=alloc_bundle["weights"],
            picks=picks,
            filters=alloc_bundle["filters"]
        )

        final["allocation"] = alloc_bundle["weights"]
        final["allocation_philosophy"] = alloc_bundle["philosophy"]
        final["allocation_regime_key"] = alloc_bundle["regime_key"]
        final["plan"] = plan
    except Exception as e:
        log.warning(f"Allocazione: errore nel calcolo → {e}")

    # 5) Spiegazione in linguaggio umano
    try:
        advisor_text = explain_plan(
            plan=final["plan"],
            regime=final["macro"]["regime"],
            sentiment=final["sentiment"]["market_sentiment"],
            profile=user
        )
        print("\n" + advisor_text + "\n")
    except Exception as e:
        log.warning(f"Advisor: errore nella spiegazione → {e}")

    # 6) Backtest storico
    try:
        backtest = backtest_plan(final["plan"])
        final["backtest"] = backtest
        print("\n📊 Backtest storico:")
        print(json.dumps(backtest, indent=2, ensure_ascii=False))
    except Exception as e:
        log.warning(f"Backtest: errore → {e}")

    # 7) Risk report
    try:
        risk_report = analyze_portfolio_risk(final["plan"], benchmark="SPY", years=5)
        final["risk"] = risk_report
        print("\n🧠 Risk report:")
        print(json.dumps(risk_report, indent=2, ensure_ascii=False))
    except Exception as e:
        log.warning(f"Risk Analyzer: errore → {e}")

    # 8) Stampa JSON finale
    print(json.dumps(final, indent=2, ensure_ascii=False))

    # 9) Export
    saved_path = save_json(final)
    if saved_path:
        log.info(f"📁 Report esportato in: {saved_path}")
    else:
        log.warning("⚠️ Esportazione fallita.")

    save_stocks_csv(final.get("stocks", []))
    save_etf_csv(final.get("etf", []))