import os
import ast

# Nomi dei file che vogliamo analizzare
target_files = {"main.py", "strategist_main.py", "# main.py"}

def analizza_file(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            codice = f.read()
        tree = ast.parse(codice)
    except Exception as e:
        return {"errore": str(e)}

    funzioni = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    classi = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    prime_righe = "\n".join(codice.splitlines()[:10])  # prime 10 righe

    return {
        "funzioni": funzioni,
        "classi": classi,
        "prime_righe": prime_righe
    }

if __name__ == "__main__":
    for root, _, files in os.walk("."):
        for file in files:
            if file in target_files:
                percorso = os.path.join(root, file)
                info = analizza_file(percorso)
                print(f"\n📄 {percorso}")
                if "errore" in info:
                    print(f"   Errore lettura: {info['errore']}")
                else:
                    print(f"   Funzioni: {', '.join(info['funzioni']) or 'Nessuna'}")
                    print(f"   Classi: {', '.join(info['classi']) or 'Nessuna'}")
                    print("   Prime righe:")
                    print(info["prime_righe"])

             
