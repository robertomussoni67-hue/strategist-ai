# forex_source.py
import os
import json
import requests

CACHE_FILE = "cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

def get_eur_usd():
    cache = load_cache()
    if "eur_usd" in cache:
        return cache["eur_usd"], True  # True = da cache
    try:
        resp = requests.get("https://open.er-api.com/v6/latest/EUR", timeout=5)
        if resp.status_code == 200:
            eur_usd = resp.json()["rates"]["USD"]
            cache["eur_usd"] = eur_usd
            save_cache(cache)
            return eur_usd, False
    except Exception as e:
        print(f"Errore forex_source: {e}")
    return None, False