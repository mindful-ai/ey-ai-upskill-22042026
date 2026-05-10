# 🧠 Agentic Database System (Planner → Executor → Validator)

## 📌 Overview
This system demonstrates a production-style agent architecture using:
- Structured tools
- Groq (via OpenAI-compatible API)
- LangChain orchestration concepts

The core pattern is:

Planner → Executor → Validator → Retry Loop

---

## 🏗️ Architecture Components

### 🧠 Planner
- Converts user input into a structured plan
- Outputs JSON:
  {
    "action": "...",
    "args": {...}
  }

**Responsibilities:**
- Intent detection
- Tool selection
- Argument extraction

---

### ⚙️ Executor
- Executes the selected tool
- Maps plan → function call

**Responsibilities:**
- Deterministic execution
- DB interaction
- Returning raw results

---

### 🔍 Validator
- Verifies correctness of execution
- Ensures output satisfies user intent

**Output:**
- VALID
- INVALID

---

### 🔁 Orchestrator Loop
- Runs Planner → Executor → Validator
- Retries on failure

---

## 🧰 Tools (Structured)

### ➕ add_user(name, user_id)
- Inserts new user

### 📋 list_users()
- Returns all users

### 🔍 get_user_by_id(user_id)
- Fetch single user

### ✏️ update_user_auth(user_id, authenticated)
- Update authentication flag

### ❌ delete_user(user_id)
- Delete user

### 📊 count_users()
- Count total users

### 🔎 search_user_by_name(name)
- Fuzzy search by name

---

## ✅ Key Concepts

### Structured Tools
- Typed arguments
- No parsing required
- Reliable execution

### Deterministic Execution
- No hidden LLM decisions during execution
- Full control over logic

### Separation of Concerns
- Planner = reasoning
- Executor = action
- Validator = correctness

---

## ⚠️ Limitations

- Planner may produce invalid JSON
- Validator depends on LLM correctness
- No memory (duplicate operations possible)

---


## 🧠 Key Insight

This system mimics real-world AI architectures:
- AutoGPT-style loops
- LangGraph workflows
- Enterprise agent pipelines

---

## 🎯 Final Takeaway

This is not just tool calling.

It is a:
👉 Controlled reasoning system  
👉 Observable execution pipeline  
👉 Production-ready agent design  
