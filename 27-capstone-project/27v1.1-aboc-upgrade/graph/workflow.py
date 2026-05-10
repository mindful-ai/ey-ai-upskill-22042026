"""
Final LangGraph workflow
"""

from langgraph.graph import StateGraph
from graph.state import State
from graph.nodes import (
    planner_node,
    procurement_node,
    finance_node,
    compliance_node,
    validator_node,
    approval_node,
    notifier_node
)


def build_workflow():
    graph = StateGraph(State)

    # Nodes
    graph.add_node("planner", planner_node)
    graph.add_node("procurement", procurement_node)
    graph.add_node("finance", finance_node)
    graph.add_node("compliance", compliance_node)
    graph.add_node("validator", validator_node)
    graph.add_node("approval", approval_node)
    graph.add_node("notifier", notifier_node)

    # Entry point
    graph.set_entry_point("planner")

    # Flow
    graph.add_edge("planner", "procurement")
    graph.add_edge("procurement", "finance")
    graph.add_edge("finance", "compliance")
    graph.add_edge("compliance", "validator")
    graph.add_edge("validator", "approval")
    graph.add_edge("approval", "notifier")

    return graph.compile()