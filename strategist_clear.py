import os

def esplora_cartella(percorso):
    print(f"\n📂 Contenuto di: {percorso}")
    if not os.path.exists(percorso):
        print("❌ Cartella non trovata")
        return
    for root, dirs, files in os.walk(percorso):
        livello = root.replace(percorso, "").count(os.sep)
        indent = " " * 4 * livello
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 4 * (livello + 1)
        for f in files:
            print(f"{subindent}{f}")

if __name__ == "__main__":
    base_path = os.getcwd()
    print(f"🔍 Analisi progetto in: {base_path}")
    esplora_cartella(os.path.join(base_path, "modules"))
    esplora_cartella(os.path.join(base_path, "data_sources"))