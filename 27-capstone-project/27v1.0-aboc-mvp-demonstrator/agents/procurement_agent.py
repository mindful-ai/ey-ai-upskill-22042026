"""
Procurement Agent
Generates structured PO from user input
"""

from tools.utils import extract_amount, extract_vendor


def run(user_input: str) -> str:
    amount = extract_amount(user_input)
    vendor = extract_vendor(user_input)

    po = f"""
    PO DETAILS:
    Item: Sensors
    Quantity: 50
    Vendor: {vendor}
    Amount: {amount} INR
    """

    return po.strip()