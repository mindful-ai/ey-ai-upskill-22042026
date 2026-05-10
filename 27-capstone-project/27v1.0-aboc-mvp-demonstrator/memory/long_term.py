"""
Long-term memory wrapper around database
"""

from tools.database_tool import save_po, get_recent_pos


def store_po(po: str):
    save_po(po)


def retrieve_history():
    return get_recent_pos()