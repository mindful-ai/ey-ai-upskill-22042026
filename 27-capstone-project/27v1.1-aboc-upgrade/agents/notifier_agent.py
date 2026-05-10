"""
Notifier Agent (LLM + tools)
"""

from config.settings import get_llm
from config.prompts import NOTIFIER_PROMPT
from tools.email_tool import send_email_tool
from memory.long_term import store_po


def run(state: dict) -> str:
    llm = get_llm()

    po = state.get("po")

    if po:
        store_po(po)

    prompt = f"""
    {NOTIFIER_PROMPT}

    STATE:
    {state}

    Generate final user-friendly message.
    """

    message = llm.invoke(prompt).content.strip()

    send_email_tool.invoke(message)

    return message