"""
Approval Agent (Human-in-the-loop)
"""

def run(state: dict) -> bool:
    print("\n👨‍💼 Approval Step")

    if not (state.get("finance_ok") and state.get("compliance_ok")):
        print("❌ Auto-rejected")
        return False

    decision = input("Approve this PO? (y/n): ").strip().lower()

    return decision == "y"