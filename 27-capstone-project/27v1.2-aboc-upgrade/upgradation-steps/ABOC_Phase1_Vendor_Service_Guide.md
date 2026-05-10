# 🚀 ABOC Phase 1 Upgrade — Vendor Service (Step-by-Step Guide)

## 📌 Objective
Build an external Vendor Service using FastAPI that will later be integrated with the ABOC system.

---

## 🧩 Step 1: Create Project Folder

Create a new folder outside your ABOC project:

```
vendor-service/
```

---

## 🧩 Step 2: Directory Structure

```
vendor-service/
│
├── main.py
├── database.py
├── models.py
├── requirements.txt
└── .env (optional)
```

---

## 🧩 Step 3: Install Dependencies

Inside `vendor-service/`:

```bash
pip install fastapi uvicorn
```

---

## 🧩 Step 4: Create `models.py`

```python
from pydantic import BaseModel

class Vendor(BaseModel):
    name: str
    address: str
    contact_person: str
    contact_number: str
    email: str
```

---

## 🧩 Step 5: Create `database.py`

```python
VENDOR_DB = {
    "VendorA": {
        "name": "VendorA",
        "address": "Bangalore, India",
        "contact_person": "Ravi Kumar",
        "contact_number": "9876543210",
        "email": "contact@vendora.com"
    },
    "VendorB": {
        "name": "VendorB",
        "address": "Mumbai, India",
        "contact_person": "Anita Sharma",
        "contact_number": "9123456780",
        "email": "info@vendorb.com"
    },
    "VendorC": {
        "name": "VendorC",
        "address": "Delhi, India",
        "contact_person": "Rahul Mehta",
        "contact_number": "9988776655",
        "email": "sales@vendorc.com"
    }
}
```

---

## 🧩 Step 6: Create `main.py`

```python
from fastapi import FastAPI, HTTPException
from models import Vendor
from database import VENDOR_DB

app = FastAPI(title="Vendor Service API")

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
```

---

## 🧩 Step 7: Run the Service

```bash
uvicorn main:app --reload --port 8001
```

---

## 🧩 Step 8: Test API

Open browser:

```
http://localhost:8001/vendor/VendorA
```

Expected output:

```json
{
  "name": "VendorA",
  "address": "Bangalore, India",
  "contact_person": "Ravi Kumar",
  "contact_number": "9876543210",
  "email": "contact@vendora.com"
}
```

---

## 🧩 Step 9: Test Edge Case

```
http://localhost:8001/vendor/UnknownVendor
```

Expected:

```
404 Vendor not found
```

---

## 🧠 What You Built

- External microservice
- REST API
- Mock database
- Foundation for tool-based agent interaction

---

## 🎤 Demo Talking Points

- "This is a separate system, not part of the AI."
- "Agent will call this API instead of hallucinating vendor data."
- "We now have real system integration."

---

## ✅ Checklist

- [ ] Service runs on port 8001
- [ ] VendorA API works
- [ ] Invalid vendor returns 404
- [ ] Code is clean and understandable

---

## 🚀 Next Phase

Phase 2:
- Create LangChain tool
- Create Vendor Agent
- Integrate into LangGraph
