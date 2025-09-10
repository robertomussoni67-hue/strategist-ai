 intelligence_macro.py
# Macro strategica per analisi documenti

import os
import datetime

def run_macro():
    print("🧠 Intelligence Macro Avviata")
    today = datetime.date.today()
    print(f"📅 Data: {today}")

    docs_path = os.path.join("..", "Docs")
    if os.path.exists(docs_path):
        files = os.listdir(docs_path)
        print(f"📂 File trovati: {files}")
    else:
        print("❌ Cartella Docs non trovata.")

if __name__ == "__main__":
    run_macro()