"""
Shared state passed between all agents
"""

from typing import TypedDict, Optional


class State(TypedDict):
    # Input
    user_input: str

    # Planner output
    plan: Optional[str]

    # Procurement
    po: Optional[str]

    # Validation flags
    finance_ok: Optional[bool]
    compliance_ok: Optional[bool]
    validation_ok: Optional[bool]

    # Approval
    approved: Optional[bool]

    # Output
    notification: Optional[str]

    # Memory (for future use)
    history: Optional[str]