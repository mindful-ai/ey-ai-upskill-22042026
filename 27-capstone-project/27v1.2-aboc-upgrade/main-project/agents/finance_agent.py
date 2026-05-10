"""
Finance Agent (DICT-SAFE VERSION)
"""

from config.constants import APPROVAL_THRESHOLD, MAX_ALLOWED_AMOUNT


def run(po: dict) -> bool:
    """
    Finance decision based on structured PO data
    """

    # ✅ Extract directly from dict
    amount = po.get("total_amount", 0)

    print(f"\n💰 Finance Check: Amount = {amount}")

    # Hard fail
    if amount > MAX_ALLOWED_AMOUNT:
        print("❌ Exceeds maximum allowed limit")
        return False

    # Auto approve
    if amount <= APPROVAL_THRESHOLD:
        print("✅ Within auto-approval limit")
        return True

    # Needs manual approval
    print("⚠️ Requires manual approval")
    return False