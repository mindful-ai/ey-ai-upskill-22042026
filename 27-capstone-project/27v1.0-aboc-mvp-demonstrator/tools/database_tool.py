"""
Database tool for storing Purchase Orders (POs)
"""

import sqlite3
import os

DB_PATH = "memory/po_memory.db"


def init_db():
    """Initialize database and table"""
    os.makedirs("memory", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS po_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            po TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_po(po: str):
    """Save PO to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO po_history (po) VALUES (?)", (po,))
    conn.commit()
    conn.close()


def get_recent_pos(limit: int = 5):
    """Fetch recent POs"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT po FROM po_history ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()

    conn.close()

    return [r[0] for r in rows]