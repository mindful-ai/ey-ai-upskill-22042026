"""
Procurement Agent (LLM + structured output)
"""

from config.settings import get_llm
from config.prompts import PROCUREMENT_PROMPT
from tools.utils import extract_amount, extract_vendor


# def run(user_input: str) -> str:
#     llm = get_llm()

#     amount = extract_amount(user_input)
#     vendor = extract_vendor(user_input)

#     prompt = f"""
#     {PROCUREMENT_PROMPT}

#     USER INPUT:
#     {user_input}

#     Extracted:
#     amount: {amount}
#     vendor: {vendor}

#     Return a clean PO format.
#     """

#     response = llm.invoke(prompt)

#     return response.content.strip()


def run(user_input: str) -> dict:
    amount = extract_amount(user_input)
    vendor = extract_vendor(user_input)

    return {
        "po_number": "PO001",
        "date": "27 April 2026",
        "vendor_name": vendor,
        "items": [
            {
                "name": "Component",
                "quantity": 20,
                "unit_price": amount // 20,
                "total": amount
            }
        ],
        "total_amount": amount
    }