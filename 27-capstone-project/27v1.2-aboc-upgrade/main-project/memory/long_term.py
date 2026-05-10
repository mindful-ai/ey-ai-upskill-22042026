"""
Long-term memory combining DB + vector DB
"""

from tools.database_tool import save_po_tool


def store_po(po: str):
    save_po_tool.invoke(po)