import sqlite3
from datetime import datetime

DB_NAME = "brain.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS summaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL,
        source_type TEXT NOT NULL,
        tldr TEXT NOT NULL,
        key_ideas TEXT NOT NULL,
        why_it_matters TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def save_summary(url, source_type, tldr, key_ideas, why_it_matters):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO summaries (
        url, source_type, tldr, key_ideas, why_it_matters, created_at
    ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        url,
        source_type,
        tldr,
        key_ideas,
        why_it_matters,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()