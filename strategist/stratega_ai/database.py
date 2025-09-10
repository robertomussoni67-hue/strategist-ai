import sqlite3
import pandas as pd

DB_FILE = "strategist.db"

def get_db_connection():
    """Crea e restituisce una connessione al database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Crea le tabelle del database se non esistono."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Tabella per il portafoglio
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS portafoglio (
                id INTEGER PRIMARY KEY,
                isin TEXT,
                simbolo TEXT,
                quantita REAL,
                prezzo_medio REAL,
                valore_mercato REAL,
                pl_non_realizzato REAL,
                valuta TEXT,
                data_ultimo_prezzo TEXT
            )
        """)

        # Tabella per l'analisi delle aziende (dcf, indici di rischio, ecc.)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analisi_aziende (
                id INTEGER PRIMARY KEY,
                nome TEXT UNIQUE,
                valore_intrinseco REAL,
                indice_rischio REAL,
                debt_equity REAL,
                current_ratio REAL,
                interest_coverage REAL
            )
        """)

        # Tabella per la cache dei dati (es. prezzi, news)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                chiave TEXT PRIMARY KEY,
                valore_json TEXT,
                timestamp REAL
            )
        """)
    print("✅ Tabelle del database create o verificate.")

def add_portfolio_from_csv(csv_path):
    """
    Legge un CSV e inserisce i dati nella tabella 'portafoglio'.
    """
    df = pd.read_csv(csv_path)
    df.columns = [col.lower().replace(' ', '_').replace('/', '_').replace('.', '_') for col in df.columns]

    with get_db_connection() as conn:
        df.to_sql('portafoglio', conn, if_exists='replace', index=False)
    print(f"✅ Dati del portafoglio da '{csv_path}' importati nel database.")

if __name__ == '__main__':
    create_tables()
    # Non decommentare ancora la riga qui sotto! La useremo tra poco.
    add_portfolio_from_csv('portafoglio_directa_esteso.csv')