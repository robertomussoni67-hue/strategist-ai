import sys
import os

# Aggiunge la cartella src al percorso
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if src_path not in sys.path:
    sys.path.append(src_path)

from config.env_config import get_api_key

def test_keys():
    print("🔍 Verifica chiavi API:")
    try:
        print("✅ Finnhub:", get_api_key("finnhub"))
    except Exception as e:
        print("❌ Finnhub non trovata:", e)

    try:
        print("✅ Alpha Vantage:", get_api_key("alpha_vantage"))
    except Exception as e:
        print("❌ Alpha Vantage non trovata:", e)

    try:
        print("✅ FRED:", get_api_key("fred"))
    except Exception as e:
        print("❌ FRED non trovata:", e)

    try:
        print("✅ OpenAI:", get_api_key("openai"))
    except Exception as e:
        print("❌ OpenAI non trovata:", e)

if __name__ == "__main__":
    test_keys()