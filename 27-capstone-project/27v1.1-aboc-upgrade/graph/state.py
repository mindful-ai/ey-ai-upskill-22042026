"""
Final shared state schema
"""

from typing import TypedDict, Optional


class State(TypedDict):
    # Input
    user_input: str

    # Planning
    plan: Optional[str]

    # Core data
    po: Optional[str]

    # Validation flags
    finance_ok: Optional[bool]
    compliance_ok: Optional[bool]
    validation_ok: Optional[bool]

    # Approval
    approved: Optional[bool]

    # Output
    notification: Optional[str]

    # Memory
    history: Optional[str]