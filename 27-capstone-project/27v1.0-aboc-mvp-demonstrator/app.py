"""
Main entry point to run ABOC system
"""

from graph.workflow import build_workflow
from tools.database_tool import init_db


def main():
    print("\n🚀 Starting ABOC System...\n")

    # Initialize database
    init_db()

    app = build_workflow()

    # User input (can be replaced with input())
    user_input = input("Enter your request: ")

    result = app.invoke({
        "user_input": user_input
    })

    print("\n===== FINAL RESULT =====\n")

    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()