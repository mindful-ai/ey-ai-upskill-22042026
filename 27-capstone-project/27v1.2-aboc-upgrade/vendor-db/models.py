"""
Pydantic models for Vendor
"""

from pydantic import BaseModel


class Vendor(BaseModel):
    name: str
    address: str
    contact_person: str
    contact_number: str
    email: str