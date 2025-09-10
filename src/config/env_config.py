# ⚠️ Versione con chiavi hardcoded per uso locale/test
# In produzione, usa dotenv e file .env per sicurezza

def get_api_key(service_name):
    """
    Restituisce la chiave API per il servizio richiesto.
    """
    keys = {
        "finnhub": "d2tel0pr01qr5a729tmgd2tel0pr01qr5a729tn0",
        "alpha_vantage": "SVMPIB4UHU0OCO1H",
        "openai": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  # se usi modelli esterni
        "fred": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"          # se usi dati macro da FRED
    }

    key = keys.get(service_name.lower())
    if not key:
        raise ValueError(f"❌ Chiave API per '{service_name}' non trovata.")
    return key