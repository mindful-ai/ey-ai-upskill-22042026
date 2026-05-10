"""
Finance Agent
Checks if budget is within threshold
"""

from config.constants import APPROVAL_THRESHOLD
from tools.utils import extract_amount


def run(po: str) -> bool:
    amount = extract_amount(po)

    print(f"\n💰 Finance Check: Amount = {amount}")

    if amount <= APPROVAL_THRESHOLD:
        print("✅ Within budget")
        return True

    print("❌ Exceeds budget")
    return False