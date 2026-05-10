"""
Final entry point for ABOC system
"""

import sys
import os

# Fix import issues
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from graph.workflow import build_workflow
from tools.database_tool import init_db


def main():
    print("\n🚀 ABOC AGENTIC SYSTEM (ADVANCED VERSION)\n")

    # Initialize DB
    init_db()

    # Build workflow
    app = build_workflow()

    while True:
        user_input = input("\nEnter your request (or 'exit'): ")

        if user_input.lower() == "exit":
            break

        result = app.invoke({
            "user_input": user_input
        })

        print("\n" + "=" * 50)
        print("✅ FINAL RESULT")
        print("=" * 50)

        for key, value in result.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()