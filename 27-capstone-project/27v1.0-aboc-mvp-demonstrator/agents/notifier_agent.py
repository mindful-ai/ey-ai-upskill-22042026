"""
Notifier Agent
Final communication + memory storage
"""

from tools.email_tool import send_email
from memory.long_term import store_po


def run(state: dict) -> str:
    print("\n📢 Notifier")

    po = state.get("po")

    # Store in memory
    if po:
        store_po(po)

    if state.get("approved"):
        message = "PO Approved and processed successfully."
    else:
        message = "PO Rejected."

    send_email(message)

    return message