"""
Validator Agent (rule-based)
"""

def run(state: dict) -> bool:
    print("\n🔍 Validation Check")

    required = ["po", "finance_ok", "compliance_ok"]

    for r in required:
        if state.get(r) is None:
            print(f"❌ Missing: {r}")
            return False

    print("✅ Validation Passed")
    return True