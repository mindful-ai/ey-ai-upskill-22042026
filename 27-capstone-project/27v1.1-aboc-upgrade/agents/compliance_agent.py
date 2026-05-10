"""
Compliance Agent (RAG + LLM)
"""

from config.settings import get_llm
from config.prompts import COMPLIANCE_PROMPT
from tools.rag_tool import retrieve_policy_tool
from tools.utils import extract_vendor


def run(po: str) -> bool:
    llm = get_llm()

    vendor = extract_vendor(po)

    # 🔥 RAG retrieval
    policies = retrieve_policy_tool.invoke(po)

    prompt = f"""
    {COMPLIANCE_PROMPT}

    PO:
    {po}

    Retrieved Policies:
    {policies}

    Vendor detected: {vendor}

    Return ONLY:
    PASS or FAIL with reason
    """

    response = llm.invoke(prompt).content.upper()

    print("\n📜 Compliance Decision:", response)

    return "PASS" in response