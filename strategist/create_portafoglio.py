# create_portafoglio.py
import os

# Percorso dove creare il CSV
csv_path = r"C:\Users\sonia\OneDrive\Desktop\Strategist\portafoglio_directa_esteso.csv"

# Contenuto del CSV
content = """ISIN,Simbolo,Quantità,Prezzo medio,Valore di mercato,P/L non realizzato,Valuta,Data ultimo prezzo
IT0003128367,ENEL.MI,200,5.80,1220.00,40.00,EUR,2025-08-27
IT0003132476,ENI.MI,150,13.20,1995.00,-75.00,EUR,2025-08-27
IT0000072618,ISP.MI,500,2.10,1065.00,15.00,EUR,2025-08-27
US0378331005,AAPL,10,170.00,1850.00,150.00,USD,2025-08-26
"""

# Crea la cartella se non esiste
os.makedirs(os.path.dirname(csv_path), exist_ok=True)

# Scrive il file in UTF-8
with open(csv_path, "w", encoding="utf-8", newline="") as f:
    f.write(content)

print(f"✅ CSV creato: {csv_path}")