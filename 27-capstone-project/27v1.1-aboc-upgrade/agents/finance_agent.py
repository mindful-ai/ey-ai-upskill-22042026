"""
Finance Agent (LLM + rule grounding)
"""

from config.settings import get_llm
from config.prompts import FINANCE_PROMPT
from tools.utils import extract_amount
from config.constants import APPROVAL_THRESHOLD


# def run(po: str) -> bool:

#     llm = get_llm()

#     amount = extract_amount(po)

#     prompt = f"""
#     {FINANCE_PROMPT}

#     PO:
#     {po}

#     RULE:
#     Budget must be below {APPROVAL_THRESHOLD} INR
#       Example: 10000 should be accepted
#       Example: 100000 should be rejected

#     Amount detected: {amount}

#     Return ONLY:
#     PASS or FAIL
#     """
 
#     response = llm.invoke(prompt).content.upper()

#     print("\n💰 Finance Decision:", response)

#     return "PASS" in response

'''
LLM is deciding something it shouldn’t

Budget validation is:

- deterministic
- rule-based
- critical

👉 LLM should NOT decide this

We use LLMs for reasoning, but critical business decisions remain deterministic.
'''

"""
Finance Agent (Deterministic + Optional LLM explanation)
"""

from config.constants import APPROVAL_THRESHOLD, MAX_ALLOWED_AMOUNT
from tools.utils import extract_amount


def run(po: str) -> bool:
    print(f"\n💰 Running Finance Agent with PO: {po}")
    amount = extract_amount(po)
    
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