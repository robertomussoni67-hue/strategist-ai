import os
import ast

def list_all_py_files(directory):
    py_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files

def safe_read(file_path):
    """Legge un file in modo sicuro, ignorando errori di codifica"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, "r", encoding="latin-1") as f:
                return f.read()
        except Exception:
            return ""  # Se non riesce, restituisce stringa vuota

def find_imported_files(py_files):
    imported = set()
    for file in py_files:
        content = safe_read(file)
        if not content:
            continue
        try:
            tree = ast.parse(content, filename=file)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported.add(alias.name.split('.')[0] + ".py")
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imported.add(node.module.split('.')[0] + ".py")
        except SyntaxError:
            pass
    return imported

def analyze_function_lengths(py_files):
    long_functions = []
    for file in py_files:
        content = safe_read(file)
        if not content:
            continue
        try:
            tree = ast.parse(content, filename=file)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    length = len(node.body)
                    if length > 20:
                        long_functions.append((file, node.name, length))
        except SyntaxError:
            pass
    return long_functions

# 📌 Percorso del tuo progetto Strategist
project_path = "C:/Users/sonia/OneDrive/Desktop/Strategist"

all_files = list_all_py_files(project_path)
imported_files = find_imported_files(all_files)
unused_files = [f for f in all_files if os.path.basename(f) not in imported_files]
long_funcs = analyze_function_lengths(all_files)

print("📁 Tutti i file Python trovati:")
for f in all_files:
    print("-", f)

print("\n🚫 File mai importati da altri file:")
for f in unused_files:
    print("-", f)

print("\n📏 Funzioni troppo lunghe (>20 righe):")
for f, name, length in long_funcs:
    print(f"- {name} ({length} righe) in {f}")