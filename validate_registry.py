import os
import json

CONFIG_PATH = r"C:\Users\sonia\OneDrive\Desktop\Strategist\config\agents_registry.json"
AGENTS_DIR = r"C:\Users\sonia\OneDrive\Desktop\Strategist\src\agents"

def load_registry(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_agent_files(directory):
    return [f.replace('.py', '') for f in os.listdir(directory) if f.endswith('.py')]

def validate(registry, files):
    active = [name for name, meta in registry.items() if meta['status'] == 'active']
    missing = [name for name in active if name not in files]
    unregistered = [f for f in files if f not in registry]
    inactive = [name for name, meta in registry.items() if meta['status'] != 'active' and name in files]

    print("\n📋 VALIDAZIONE REGISTRO AGENTI")
    print("-" * 40)
    print(f"✅ Moduli attivi trovati: {[a for a in active if a in files]}")
    print(f"❌ Moduli attivi mancanti: {missing}")
    print(f"⚠️  File non registrati: {unregistered}")
    print(f"🕓 Moduli presenti ma non attivi: {inactive}")
    print("-" * 40)

if __name__ == "__main__":
    try:
        registry = load_registry(CONFIG_PATH)
        files = get_agent_files(AGENTS_DIR)
        validate(registry, files)
    except Exception as e:
        print(f"Errore durante la validazione: {e}")