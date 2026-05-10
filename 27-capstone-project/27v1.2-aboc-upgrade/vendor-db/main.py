"""
Vendor Service API
"""

from fastapi import FastAPI, HTTPException
from models import Vendor
from database import VENDOR_DB

app = FastAPI(title="Vendor Service")


@app.get("/")
def health():
    return {"message": "Vendor API is running"}


@app.get("/vendor/{vendor_name}", response_model=Vendor)
def get_vendor(vendor_name: str):
    vendor = VENDOR_DB.get(vendor_name)

    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    return vendor


@app.get("/vendors")
def list_vendors():
    return list(VENDOR_DB.values())