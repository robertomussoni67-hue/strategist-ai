import sqlite3
from datetime import datetime

DB_PATH = "reports/strategist_memory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS episodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            regime TEXT,
            sentiment TEXT,
            tickers TEXT,
            etfs TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_episode(regime, sentiment, tickers, etfs):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO episodes (timestamp, regime, sentiment, tickers, etfs)
        VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        regime,
        sentiment,
        ",".join(tickers),
        ",".join(etfs)
    ))
    conn.commit()
    conn.close()

def load_last_episodes(n=5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM episodes ORDER BY timestamp DESC LIMIT ?", (n,))
    rows = c.fetchall()
    conn.close()
    return rows