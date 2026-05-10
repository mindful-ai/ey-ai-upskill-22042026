"""
Planner Agent (LLM-based)
"""

from config.settings import get_llm
from config.prompts import PLANNER_PROMPT


def run(user_input: str) -> str:
    llm = get_llm()

    prompt = f"""
    {PLANNER_PROMPT}

    USER REQUEST:
    {user_input}
    """

    response = llm.invoke(prompt)

    return response.content.strip()