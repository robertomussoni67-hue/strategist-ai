import requests
import pandas as pd
from datetime import datetime
import json
import os

# Inserisci qui la tua API key di Alpha Vantage.
# Puoi ottenerla creando un account gratuito su https://www.alphavantage.co/support/#api-key
ALPHA_VANTAGE_API_KEY = "SVMPIB4UHU0OCO1H"

def get_historical_data(ticker):
    """
    Recupera i dati storici giornalieri per un ticker da Alpha Vantage.
    """
    if ALPHA_VANTAGE_API_KEY == "YOUR_ALPHA_VANTAGE_API_KEY" or not ALPHA_VANTAGE_API_KEY:
        print("❌ Errore: la chiave API di Alpha Vantage non è stata configurata.")
        return None

    print(f"Tentativo di recupero dati storici da Alpha Vantage per {ticker}...")
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={ALPHA_VANTAGE_API_KEY}"
    
    try:
        r = requests.get(url)
        r.raise_for_status() # Solleva un'eccezione per i codici di stato di errore HTTP
        data = r.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Errore di connessione ad Alpha Vantage: {e}")
        return None
    except json.JSONDecodeError:
        print(f"❌ Errore nel decodificare la risposta JSON da Alpha Vantage. Controlla la tua API key.")
        return None

    if "Time Series (Daily)" not in data:
        if "Error Message" in data and "Invalid API key" in data["Error Message"]:
            print(f"❌ Errore API: la tua chiave Alpha Vantage non è valida.")
        else:
            print(f"❌ Errore nel recupero dati storici da Alpha Vantage per {ticker}.")
        return None
    
    df = pd.DataFrame(data['Time Series (Daily)']).T
    df.index = pd.to_datetime(df.index)
    df = df.rename(columns={
        '1. open': 'Open',
        '2. high': 'High',
        '3. low': 'Low',
        '4. close': 'Close',
        '5. volume': 'Volume'
    })
    df = df.astype({'Open': float, 'High': float, 'Low': float, 'Close': float, 'Volume': float})
    
    print(f"✅ Dati storici da Alpha Vantage per {ticker} recuperati con successo.")
    return df

def get_earnings_data(ticker):
    """
    Recupera i dati sugli utili trimestrali da Alpha Vantage.
    """
    if ALPHA_VANTAGE_API_KEY == "YOUR_ALPHA_VANTAGE_API_KEY" or not ALPHA_VANTAGE_API_KEY:
        print("❌ Errore: la chiave API di Alpha Vantage non è stata configurata.")
        return None

    print(f"Tentativo di recupero dati utili da Alpha Vantage per {ticker}...")
    url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}"

    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Errore di connessione ad Alpha Vantage: {e}")
        return None
    except json.JSONDecodeError:
        print(f"❌ Errore nel decodificare la risposta JSON da Alpha Vantage. Controlla la tua API key.")
        return None
    
    if "quarterlyEarnings" not in data:
        if "Error Message" in data and "Invalid API key" in data["Error Message"]:
            print(f"❌ Errore API: la tua chiave Alpha Vantage non è valida.")
        else:
            print(f"❌ Errore nel recupero dati utili da Alpha Vantage per {ticker}. Il ticker potrebbe non essere supportato.")
        return None

    df = pd.DataFrame(data['quarterlyEarnings'])
    df['reportedDate'] = pd.to_datetime(df['reportedDate'])
    df['reportedEPS'] = pd.to_numeric(df['reportedEPS'])
    
    df = df.sort_values(by='reportedDate', ascending=True)
    df.set_index('reportedDate', inplace=True)
    
    print(f"✅ Dati utili da Alpha Vantage per {ticker} recuperati con successo.")
    return df['reportedEPS']
