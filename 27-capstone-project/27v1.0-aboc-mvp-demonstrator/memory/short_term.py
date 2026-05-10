"""
Short-term memory (in-session)
"""

def update_history(state: dict) -> str:
    """
    Create a short summary of current transaction
    """
    return f"Last PO: {state.get('po')}, Approved: {state.get('approved')}"