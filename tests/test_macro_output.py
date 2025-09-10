import sys
import os
import asyncio

# Aggiunge manualmente la cartella 'src' al percorso
current_dir = os.path.dirname(__file__)
src_path = os.path.abspath(os.path.join(current_dir, "..", "src"))
if src_path not in sys.path:
    sys.path.append(src_path)

from agents import macro  # Importa l'agente macro correttamente

def validate_macro_output(data):
    required_keys = {"regime", "source", "method", "timestamp"}
    forbidden_keys = {"etf", "stocks"}

    # Verifica che tutte le chiavi richieste siano presenti
    missing = required_keys - data.keys()
    if missing:
        raise AssertionError(f"Mancano chiavi obbligatorie: {missing}")

    # Verifica che non ci siano chiavi non previste
    unexpected = forbidden_keys & data.keys()
    if unexpected:
        raise AssertionError(f"Chiavi non valide presenti: {unexpected}")

    # Verifica che il regime sia uno tra quelli attesi
    if data["regime"] not in {"growth", "defensive", "neutral"}:
        raise AssertionError(f"Regime non valido: {data['regime']}")

    print("✅ Output macro valido:", data)

async def main():
    result = await macro.run()
    validate_macro_output(result)

if __name__ == "__main__":
    asyncio.run(main())