"""
Run demo scenarios
"""

from graph.workflow import build_workflow
from tools.database_tool import init_db
from demo.scenarios import SCENARIOS


def run_demo():
    print("\n🚀 RUNNING DEMO SCENARIOS\n")

    init_db()
    app = build_workflow()

    for scenario in SCENARIOS:
        print("\n" + "#" * 60)
        print("SCENARIO:", scenario)

        result = app.invoke({
            "user_input": scenario
        })

        print("\nRESULT:")
        for k, v in result.items():
            print(f"{k}: {v}")


if __name__ == "__main__":
    run_demo()