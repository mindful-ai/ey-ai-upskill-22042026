"""
Vendor Tool
Calls external Vendor FastAPI service
"""

import requests
from langchain.tools import tool

BASE_URL = "http://localhost:8001"


@tool
def fetch_vendor_details(vendor_name: str) -> str:
    """
    Fetch vendor details from external Vendor Service API.
    """

    try:
        response = requests.get(f"{BASE_URL}/vendor/{vendor_name}")

        if response.status_code == 200:
            data = response.json()
            return str(data)

        return f"Vendor {vendor_name} not found"

    except Exception as e:
        return f"Error fetching vendor: {str(e)}"