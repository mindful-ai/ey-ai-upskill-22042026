"""
Utility helper functions
"""

import re


def extract_amount(text: str) -> int:
    """
    Extract numeric amount from text
    Example: "400000 INR" → 400000
    """
    numbers = re.findall(r"\d+", text)
    return int(numbers[0]) if numbers else 0


def extract_vendor(text: str) -> str:
    """
    Simple vendor extraction (demo purpose)
    """
    if "VendorA" in text:
        return "VendorA"
    if "VendorB" in text:
        return "VendorB"
    return "UnknownVendor"