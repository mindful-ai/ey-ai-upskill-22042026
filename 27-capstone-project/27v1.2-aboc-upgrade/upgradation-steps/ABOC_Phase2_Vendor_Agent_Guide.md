# 🚀 ABOC Phase 2 — Vendor Tool + Agent Integration (Step-by-Step)

## 📌 Objective
Integrate the external Vendor Service into the ABOC system using:
- LangChain Tool
- Vendor Agent
- LangGraph workflow update

---

## 🧩 Step 1: Create Vendor Tool

📄 File: `tools/vendor_tool.py`

```python
import os
import requests
from langchain.tools import tool

BASE_URL = os.getenv("VENDOR_API_BASE_URL", "http://localhost:8001")

@tool
def fetch_vendor_details(vendor_name: str) -> str:
    """
    Fetch vendor details from external Vendor Service API.
    """
    try:
        response = requests.get(f"{BASE_URL}/vendor/{vendor_name}")
        if response.status_code == 200:
            return str(response.json())
        return f"Vendor {vendor_name} not found"
    except Exception as e:
        return f"Error fetching vendor: {str(e)}"
```

---

## 🧩 Step 2: Create Vendor Agent

📄 File: `agents/vendor_agent.py`

```python
from tools.vendor_tool import fetch_vendor_details
from tools.utils import extract_vendor

def run(state: dict) -> str:
    print("\n🏢 Vendor Agent")

    po = state.get("po", "")
    vendor_name = extract_vendor(po)

    print(f"Fetching details for: {vendor_name}")

    vendor_data = fetch_vendor_details.invoke(vendor_name)

    enriched_po = f"""
{po}

--- Vendor Details ---
{vendor_data}
"""

    return enriched_po.strip()
```

---

## 🧩 Step 3: Update Graph Nodes

📄 File: `graph/nodes.py`

### Add import:
```python
from agents import vendor_agent
```

### Add node:
```python
def vendor_node(state):
    print("\n🔹 VENDOR ENRICHMENT")
    state["po"] = vendor_agent.run(state)
    print(state["po"])
    return state
```

---

## 🧩 Step 4: Update Workflow

📄 File: `graph/workflow.py`

### Add node:
```python
graph.add_node("vendor", vendor_node)
```

### Update edges:
```python
graph.add_edge("procurement", "vendor")
graph.add_edge("vendor", "finance")
```

---

## 🧠 Updated Flow

Planner → Procurement → Vendor → Finance → Compliance → Validator → Approval → Notifier

---

## 🧪 Step 5: Run & Test

### Start Vendor Service:
```bash
uvicorn main:app --reload --port 8001
```

### Run ABOC:
```bash
python app.py
```

### Test Input:
```
Create a PO for 20 components from VendorA under 300000 INR
```

---

## ✅ Expected Output

- Vendor Agent runs
- API call made
- Vendor details appended to PO

---

## ⚠️ Common Issues

| Issue | Fix |
|------|-----|
| Connection error | Ensure API running |
| Vendor not found | Check case sensitivity |
| Empty response | Verify endpoint |

---

## 🎤 Demo Talking Points

- "This agent fetches data from a real system"
- "No hallucination — only verified data"
- "We are integrating AI with enterprise systems"

---

## 🚀 Next Phase

Phase 3:
- Rich console output
- Beautiful formatted tables
- Demo-ready UI experience
