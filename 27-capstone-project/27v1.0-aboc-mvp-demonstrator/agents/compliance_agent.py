"""
Compliance Agent
Uses RAG to validate policies
"""

from tools.rag_tool import retrieve_relevant_policy
from tools.utils import extract_vendor
from config.constants import APPROVED_VENDORS


def run(po: str) -> bool:
    policies = retrieve_relevant_policy(po)
    vendor = extract_vendor(po)

    print("\n📜 Compliance Check")
    print("Policies:", policies)

    if vendor not in APPROVED_VENDORS:
        print(f"❌ Vendor {vendor} not approved")
        return False

    print("✅ Compliance passed")
    return True