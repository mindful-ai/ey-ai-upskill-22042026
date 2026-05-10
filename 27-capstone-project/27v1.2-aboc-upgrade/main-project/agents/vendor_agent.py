"""
Vendor Agent
Enriches PO with vendor details from external API
"""

from tools.vendor_tool import fetch_vendor_details
from tools.utils import extract_vendor


# def run(state: dict) -> str:
#     print("\n🏢 Vendor Agent")

#     po = state.get("po", "")

#     vendor_name = extract_vendor(po)

#     print(f"Fetching details for: {vendor_name}")

#     vendor_data = fetch_vendor_details.invoke(vendor_name)

#     enriched_po = f"""
#     {po}

#     --- Vendor Details ---
#     {vendor_data}
#     """

#     return enriched_po.strip()


def run(state: dict):
    po = state.get("po")

    vendor_name = po["vendor_name"]

    vendor_data = fetch_vendor_details.invoke(vendor_name)

    # convert string → dict safely (for demo)
    import ast
    vendor_data = ast.literal_eval(vendor_data)

    po["vendor_details"] = vendor_data

    return po