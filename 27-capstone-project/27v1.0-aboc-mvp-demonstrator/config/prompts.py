"""
Centralized prompts for all agents
"""

PLANNER_PROMPT = """
Break the user request into clear business steps.
"""

PROCUREMENT_PROMPT = """
Generate a structured purchase order with:
- item
- quantity
- vendor
- amount
"""

FINANCE_PROMPT = """
Check if the purchase is within budget limits.
"""

COMPLIANCE_PROMPT = """
Validate the request against company policies.
"""

VALIDATOR_PROMPT = """
Ensure all required fields exist and are valid.
"""

APPROVAL_PROMPT = """
Decide whether to approve or reject.
"""

NOTIFIER_PROMPT = """
Generate a user-friendly final message.
"""


"""
Global settings and optional LLM config
"""