"""
Simple RAG tool using text-based retrieval
"""

def load_policies():
    """Load policy text"""
    with open("data/policies.txt", "r") as f:
        return f.read()


def retrieve_relevant_policy(query: str) -> str:
    """
    Very simple retrieval:
    Returns entire policy text (can be improved later)
    """
    policies = load_policies()
    return policies