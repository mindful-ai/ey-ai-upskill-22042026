"""
Procurement Agent (LLM + structured output)
"""

from config.settings import get_llm
from config.prompts import PROCUREMENT_PROMPT
from tools.utils import extract_amount, extract_vendor


def run(user_input: str) -> str:
    llm = get_llm()

    amount = extract_amount(user_input)
    vendor = extract_vendor(user_input)

    prompt = f"""
    {PROCUREMENT_PROMPT}

    USER INPUT:
    {user_input}

    Extracted:
    amount: {amount}
    vendor: {vendor}

    Return a clean PO format.
    """

    response = llm.invoke(prompt)

    return response.content.strip()