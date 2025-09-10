import os
import ast

PROJECT_ROOT = "."  # cartella di Strategist

def analizza_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        try:
            tree = ast.parse(f.read(), filename=path)
        except SyntaxError:
            return None

    funzioni = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    classi = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    docstring = ast.get_docstring(tree)
    return {
        "funzioni": funzioni,
        "classi": classi,
        "docstring": docstring.strip() if docstring else None
    }

def trova_imports():
    imports = {}
    for root, _, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if line.startswith("import ") or line.startswith("from "):
                            imports.setdefault(file, []).append(line.strip())
    return imports

if __name__ == "__main__":
    imports = trova_imports()
    report = []

    for root, _, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                info = analizza_file(path)
                if info:
                    stato = "ATTIVO" if any(file in v for v in imports.values()) else "POTENZIALMENTE OBSOLETO"
                    if not info["funzioni"] and not info["classi"]:
                        stato = "INCOMPLETO/PLACEHOLDER"
                    report.append({
                        "file": path,
                        "stato": stato,
                        "funzioni": info["funzioni"],
                        "classi": info["classi"],
                        "docstring": info["docstring"]
                    })

    # Stampa report
    for r in report:
        print(f"\n📄 {r['file']}")
        print(f"   Stato: {r['stato']}")
        if r['docstring']:
            print(f"   Docstring: {r['docstring']}")
        print(f"   Funzioni: {', '.join(r['funzioni']) if r['funzioni'] else 'Nessuna'}")
        print(f"   Classi: {', '.join(r['classi']) if r['classi'] else 'Nessuna'}")