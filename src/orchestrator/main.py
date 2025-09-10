import json, asyncio
from pathlib import Path

# Carica registro agenti
def load_registry(path="config/agents_registry.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Mappa agenti attivi
def get_active_agents(registry):
    return [name for name, meta in registry.items() if meta["status"] == "active"]

# Import dinamico dei moduli
def import_agent(name):
    try:
        return __import__(f"agents.{name}", fromlist=["run"]).run
    except Exception as e:
        print(f"[ERRORE] Impossibile importare agente '{name}': {e}")
        return None

# Esecuzione orchestrata
def run_full_cycle(tags=None):
    registry = load_registry()
    active = get_active_agents(registry)
    results = {}
    for name in active:
        agent_run = import_agent(name)
        if agent_run:
            try:
                results[name] = asyncio.run(agent_run())
            except Exception as e:
                results[name] = {"error": str(e)}
    results["tags"] = tags or []
    results["summary"] = f"{len(active)} sub-agenti attivi eseguiti"
    return results

# Test locale
if __name__ == "__main__":
    print(json.dumps(run_full_cycle(), indent=2, ensure_ascii=False))