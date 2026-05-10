import re

def extract_amount(text: str):
    nums = re.findall(r"\d+", text)
    return int(nums[0]) if nums else 0


def extract_vendor(text: str):
    if "VendorA" in text:
        return "VendorA"
    if "VendorB" in text:
        return "VendorB"
    return "UnknownVendor"