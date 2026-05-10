"""
Validator Agent
Ensures all required fields are present
"""

def run(state: dict) -> bool:
    print("\n🔍 Validation Check")

    required_fields = ["po", "finance_ok", "compliance_ok"]

    for field in required_fields:
        if state.get(field) is None:
            print(f"❌ Missing field: {field}")
            return False

    print("✅ Validation passed")
    return True