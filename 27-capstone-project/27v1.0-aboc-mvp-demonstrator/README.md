# 🚀 Autonomous Business Operations Co-Pilot (ABOC) — Advanced Version

## 📌 Overview
ABOC is an end-to-end multi-agent AI system that simulates business workflows such as:
- Purchase Order (PO) creation
- Budget validation
- Compliance checking (RAG-based)
- Approval (human-in-the-loop)
- Notification
- Memory (short-term + long-term)

This project is designed for **teaching Agentic AI concepts** using:
- LangGraph (orchestration)
- Tool-based agents
- RAG (policies)
- Memory (SQLite)

---

## 🧠 System Architecture

User Input  
↓  
Planner Agent  
↓  
Procurement Agent  
↓  
Finance Agent  
↓  
Compliance Agent (RAG)  
↓  
Validator Agent  
↓  
Approval Agent (Human-in-loop)  
↓  
Notifier Agent  

---

## 👥 Agent Responsibilities

### Planner Agent
Breaks the user request into steps.

### Procurement Agent
Generates structured PO from input.

### Finance Agent
Validates budget constraints.

### Compliance Agent
Uses policy data (RAG) to validate rules.

### Validator Agent
Ensures completeness and correctness.

### Approval Agent
Allows human approval/rejection.

### Notifier Agent
Sends final output + stores memory.

---

## 🧰 Tools

- **Database Tool (SQLite)** → Stores PO history  
- **RAG Tool** → Retrieves policies  
- **Email Tool** → Simulated notifications  
- **Utils** → Parsing helpers  

---

## 🧠 Memory

- **Short-term** → Session summary  
- **Long-term** → SQLite PO storage  

---

## 📁 Project Structure

Refer to your directory structure:
- config/
- graph/
- agents/
- tools/
- memory/
- rag/
- data/
- demo/

---

## 🧪 Demo Scenarios

1. Valid request → Approved  
2. Invalid vendor → Rejected  
3. Budget exceeded → Rejected  
4. Policy change → Behavior changes  

---

## ▶️ How to Run

### 1. Setup environment

```bash
pip install -r requirements.txt
```

---

### 2. Ensure project structure is correct

Add `__init__.py` in all folders:
- agents/
- graph/
- tools/
- memory/
- rag/
- config/
- demo/

---

### 3. Run the app

```bash
python app.py
```

---

### 4. Run demo scenarios

```bash
python demo/run_demo.py
```

---

## ⚠️ Common Errors & Fixes

### ❌ ModuleNotFoundError
Fix:
- Add `__init__.py` in folders
- Run from project root

---

### ❌ Database not created
Fix:
- Ensure `init_db()` is called in app.py

---

## 🎯 Learning Outcomes

- Multi-agent system design  
- LangGraph orchestration  
- RAG integration  
- Memory systems  
- Human-in-the-loop workflows  

---

## 🚀 Future Enhancements

- LangChain tool-calling agents  
- Streamlit UI  
- FastAPI backend  
- LangSmith observability  
- Vector DB memory  

---

## 🧠 Key Insight

This project demonstrates:

> AI systems that don’t just respond — they **operate workflows like a business**.
