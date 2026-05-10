"""
LangGraph node wrappers with clean logging
"""

from agents import (
    planner_agent,
    procurement_agent,
    finance_agent,
    compliance_agent,
    validator_agent,
    approval_agent,
    notifier_agent
)

from memory.short_term import update_history


def print_section(title):
    print("\n" + "=" * 50)
    print(f"🔹 {title}")
    print("=" * 50)


def planner_node(state):
    print_section("PLANNER")
    state["plan"] = planner_agent.run(state["user_input"])
    print(state["plan"])
    return state


def procurement_node(state):
    print_section("PROCUREMENT")
    state["po"] = procurement_agent.run(state["user_input"])
    print(state["po"])
    return state


def finance_node(state):
    print_section("FINANCE")
    state["finance_ok"] = finance_agent.run(state["po"])
    return state


def compliance_node(state):
    print_section("COMPLIANCE (RAG)")
    state["compliance_ok"] = compliance_agent.run(state["po"])
    return state


def validator_node(state):
    print_section("VALIDATOR")
    state["validation_ok"] = validator_agent.run(state)
    return state


def approval_node(state):
    print_section("APPROVAL")
    state["approved"] = approval_agent.run(state)
    return state


def notifier_node(state):
    print_section("NOTIFIER")

    state["notification"] = notifier_agent.run(state)

    state["history"] = update_history(state)

    print("\n🧠 Session Summary:")
    print(state["history"])

    return state