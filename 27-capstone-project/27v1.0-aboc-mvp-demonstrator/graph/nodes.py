"""
Node wrappers for LangGraph
Each node calls an agent and updates shared state
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


def planner_node(state):
    print("\n🧠 Planner Agent")
    state["plan"] = planner_agent.run(state["user_input"])
    print(state["plan"])
    return state


def procurement_node(state):
    print("\n🧾 Procurement Agent")
    state["po"] = procurement_agent.run(state["user_input"])
    print(state["po"])
    return state


def finance_node(state):
    state["finance_ok"] = finance_agent.run(state["po"])
    return state


def compliance_node(state):
    state["compliance_ok"] = compliance_agent.run(state["po"])
    return state


def validator_node(state):
    state["validation_ok"] = validator_agent.run(state)
    return state


def approval_node(state):
    state["approved"] = approval_agent.run(state)
    return state


def notifier_node(state):
    state["notification"] = notifier_agent.run(state)

    # Update short-term memory summary
    state["history"] = update_history(state)

    print("\n🧠 Session Summary:")
    print(state["history"])

    return state