"""
Approval Agent
Handles human-in-the-loop decision
"""

def run(state: dict) -> bool:
    print("\n👨‍💼 Approval Step")

    if not (state.get("finance_ok") and state.get("compliance_ok")):
        print("❌ Auto-rejected due to validation failure")
        return False

    user_input = input("Approve this PO? (y/n): ").strip().lower()

    if user_input == "y":
        print("✅ Approved by user")
        return True

    print("❌ Rejected by user")
    return False