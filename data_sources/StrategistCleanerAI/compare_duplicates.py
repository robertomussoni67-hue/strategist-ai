import os
import hashlib
from collections import defaultdict

def file_hash(path):
    """Calcola l'hash di un file per confrontarne il contenuto"""
    hasher = hashlib.md5()
    try:
        with open(path, "rb") as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except Exception as e:
        return None

def find_duplicates(directory):
    """Trova file con lo stesso nome e confronta il contenuto"""
    files_by_name = defaultdict(list)

    # Raggruppa per nome file
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                files_by_name[file].append(os.path.join(root, file))

    # Confronta i file con lo stesso nome
    for name, paths in files_by_name.items():
        if len(paths) > 1:
            print(f"\n🔍 File con nome '{name}' trovato in più posizioni:")
            hashes = {}
            for p in paths:
                h = file_hash(p)
                hashes.setdefault(h, []).append(p)

            for h, same_files in hashes.items():
                if h is None:
                    print("  ⚠️ Impossibile leggere uno dei file")
                elif len(same_files) > 1:
                    print("  ✅ Copie identiche:")
                    for sf in same_files:
                        print("     -", sf)
                else:
                    print("  ❗ Versione diversa:")
                    for sf in same_files:
                        print("     -", sf)

# 📌 Percorso del tuo progetto Strategist
project_path = "C:/Users/sonia/OneDrive/Desktop/Strategist"
find_duplicates(project_path)