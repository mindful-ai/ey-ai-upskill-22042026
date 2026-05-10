# 🚀 ABOC Upgrade Specifications — Vendor Integration + UI Enhancements

## 📌 Overview
This upgrade enhances the ABOC (Autonomous Business Operations Co-Pilot) system with:
- External Vendor Service (FastAPI)
- Vendor Agent integration
- MCP-style architecture demonstration
- Rich console output formatting

---

## 🧩 Architecture Overview

User Input  
↓  
Planner (LLM)  
↓  
Procurement (LLM)  
↓  
Vendor Agent (API Tool)  **
↓  
Finance (Rules)  
↓  
Compliance (RAG + LLM)  
↓  
Validator (Rules)  
↓  
Approval (Human-in-loop)  
↓  
Notifier (LLM)  
↓  
Rich Renderer (Presentation Layer) **

---

## 🌐 Phase 1 — Vendor Service (External System)

### Goal
Create a standalone FastAPI service to fetch vendor details.

### Components
- `main.py` → API endpoints
- `database.py` → Mock vendor DB
- `models.py` → Pydantic schema

### Endpoints
- `/vendor/{vendor_name}` → Get vendor details
- `/vendors` → List all vendors

### Run
```bash
uvicorn main:app --reload --port 8001
```

---

## 🔧 Phase 2 — Vendor Tool + Agent

### Tool
Create a LangChain `@tool`:
```python
@tool
def fetch_vendor_details(vendor_name: str) -> dict:
    # Calls FastAPI service
```

### Agent
- Calls tool
- Enriches PO with vendor details

---

## 🔗 Phase 3 — LangGraph Update

### Add node
```python
graph.add_node("vendor", vendor_node)
```

### Update flow
```python
graph.add_edge("procurement", "vendor")
graph.add_edge("vendor", "finance")
```

---

## 🧠 MCP Demonstration

### Concept
Agents interact with external systems via tools.

### Demo Narrative
- No hallucination
- Real-time API call
- Structured response

---

## 🎨 Phase 4 — Rich Console Output

### Library
Use Python `rich`

### Example
```python
from rich.console import Console
from rich.table import Table
```

### Purpose
- Better readability
- Professional demo experience

---

## ⚠️ Design Principles

### DO
- Keep tools separate from agents
- Use rules for critical decisions
- Use LLM for reasoning only

### DON'T
- Use LLM for finance decisions
- Over-create agents for formatting

---

## 🧪 Demo Scenarios

1. Valid vendor → enriched PO  
2. Invalid vendor → API 404  
3. High budget → finance rejection  

---

## 🚀 Learning Outcomes

- Multi-agent orchestration
- Tool-based architecture
- External system integration
- RAG + API hybrid design
- Clean separation of concerns

---

## 🔮 Future Enhancements

- LangSmith tracing
- Multi-agent negotiation
- Dashboard analytics
- Docker deployment
