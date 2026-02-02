import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "inventory.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            category TEXT,
            location TEXT,
            container TEXT,
            container_number INTEGER
        )
        """)
