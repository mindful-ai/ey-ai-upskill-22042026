"""
Database Tool using LangChain @tool
"""

import sqlite3
from langchain.tools import tool

DB_PATH = "memory/po_memory.db"


def init_db():
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


@tool
def save_po_tool(po: str) -> str:
    """
    Save a purchase order to the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO po_history (po) VALUES (?)", (po,))
    conn.commit()
    conn.close()

    return "PO saved successfully"


@tool
def fetch_po_history_tool(_: str) -> str:
    """
    Retrieve recent purchase orders from the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT po FROM po_history ORDER BY id DESC LIMIT 5")
    rows = cursor.fetchall()
    conn.close()

    return str([r[0] for r in rows])