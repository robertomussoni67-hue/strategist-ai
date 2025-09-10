import os
import sys

def main():
    """
    Questo script esamina la directory corrente e le sue sottodirectory
    per esportare il contenuto di tutti i file di progetto supportati.
    """
    
    # Elenco delle estensioni di file da includere nell'esportazione
    supported_extensions = ['.py', '.js', '.html', '.css', '.txt', '.md']
    
    # La directory in cui si trova lo script
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    print(f"Esportazione del contenuto dei file da: {project_root}")
    print("-" * 50)
    
    try:
        # Attraversa tutte le directory e i file a partire dalla directory radice
        for root, dirs, files in os.walk(project_root):
            for file in files:
                # Controlla se l'estensione del file è supportata
                if any(file.endswith(ext) for ext in supported_extensions):
                    file_path = os.path.join(root, file)
                    
                    # Salta lo script stesso
                    if file_path == os.path.abspath(__file__):
                        continue
                    
                    # Stampa il titolo del file e il percorso relativo
                    relative_path = os.path.relpath(file_path, project_root)
                    print(f"\n--- Inizio del file: {relative_path} ---")
                    
                    try:
                        # Legge e stampa il contenuto del file
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            print(content)
                    except UnicodeDecodeError:
                        # Se la decodifica fallisce, riprova con un'altra codifica
                        try:
                            with open(file_path, 'r', encoding='latin-1') as f:
                                content = f.read()
                                print(content)
                        except Exception as e:
                            print(f"Impossibile leggere il file {relative_path}. Errore: {e}", file=sys.stderr)
                    except Exception as e:
                        print(f"Impossibile leggere il file {relative_path}. Errore: {e}", file=sys.stderr)
                    
                    print(f"--- Fine del file: {relative_path} ---")
                    
    except Exception as e:
        print(f"Si è verificato un errore generale: {e}", file=sys.stderr)
    
    print("-" * 50)
    print("Esportazione completata.")

if __name__ == "__main__":
    main()
