"""
Validator Agent (rule-based)
"""

# def run(state: dict) -> bool:
#     print("\n🔍 Validation Check")

#     required = ["po", "finance_ok", "compliance_ok"]

#     for r in required:
#         if state.get(r) is None:
#             print(f"❌ Missing: {r}")
#             return False

#     print("✅ Validation Passed")
#     return True

def run(state: dict) -> bool:
    po = state.get("po", {})

    if not po.get("total_amount"):
        return False

    if not po.get("vendor_name"):
        return False

    return True