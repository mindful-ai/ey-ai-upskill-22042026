'''
Demonstration of building a LangGraph agent that interacts with a SQLite database 
using multiple tools.

✅ LangGraph workflow
✅ Multi-tool orchestration
✅ Retry + validation loop
✅ Dependency injection (correct design)
✅ Deterministic execution

- Purushotham

'''

from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.graph import StateGraph, END

import sqlite3
import json
from typing import TypedDict

# ============================================================
# STATE (DATA ONLY — NO LLM HERE)
# ============================================================

class AgentState(TypedDict):
    input: str
    plan: dict
    result: str
    status: str

# ============================================================
# DATABASE SETUP
# ============================================================

def setup_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT,
        authenticated INTEGER
    )
    """)

    conn.commit()
    conn.close()


def seed_data():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    users = [
        ("ML001", "Raj", 1),
        ("ML002", "Ram", 0),
        ("ML003", "Sham", 1)
    ]

    cursor.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", users)

    conn.commit()
    conn.close()

# ============================================================
# TOOLS (ALL STRUCTURED + DOCSTRINGS)
# ============================================================

@tool
def add_user(name: str, user_id: str) -> str:
    """Add a new user to the database"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (user_id, name, 1))
        conn.commit()
        return f"SUCCESS: Added {name}"
    except Exception as e:
        return f"ERROR: {str(e)}"
    finally:
        conn.close()


@tool
def list_users() -> str:
    """Return all users"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    return json.dumps(rows)


@tool
def get_user_by_id(user_id: str) -> str:
    """Fetch a user by ID"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return json.dumps(row)


@tool
def update_user_auth(user_id: str, authenticated: int) -> str:
    """Update authentication status (0 or 1)"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET authenticated=? WHERE id=?",
        (authenticated, user_id)
    )
    conn.commit()
    conn.close()
    return "SUCCESS: Updated"


@tool
def delete_user(user_id: str) -> str:
    """Delete a user"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    return "SUCCESS: Deleted"


@tool
def count_users() -> str:
    """Count total users"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return str(count)


@tool
def search_user_by_name(name: str) -> str:
    """Search users by partial name"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name LIKE ?", (f"%{name}%",))
    rows = cursor.fetchall()
    conn.close()
    return json.dumps(rows)

# TOOL REGISTRY
TOOLS = {
    "add_user": add_user,
    "list_users": list_users,
    "get_user_by_id": get_user_by_id,
    "update_user_auth": update_user_auth,
    "delete_user": delete_user,
    "count_users": count_users,
    "search_user_by_name": search_user_by_name,
}

# ============================================================
# LLM
# ============================================================

def get_llm(api_key):
    return ChatOpenAI(
        model="llama-3.1-8b-instant",
        openai_api_key=api_key,
        openai_api_base="https://api.groq.com/openai/v1",
        temperature=0
    )

# ============================================================
# NODES (WITH LLM INJECTION)
# ============================================================

def create_planner_node(llm):
    def planner_node(state: AgentState):
        prompt = f"""
You are a planner.

Available actions:
- add_user(name, user_id)
- list_users()
- get_user_by_id(user_id)
- update_user_auth(user_id, authenticated)
- delete_user(user_id)
- count_users()
- search_user_by_name(name)

Return ONLY JSON:
{{
  "action": "...",
  "args": {{...}}
}}

User input: {state['input']}
"""
        response = llm.invoke(prompt)

        try:
            plan = json.loads(response.content)
        except:
            plan = {"action": "list_users", "args": {}}

        return {**state, "plan": plan}

    return planner_node


def executor_node(state: AgentState):
    plan = state["plan"]
    action = plan.get("action")
    args = plan.get("args", {})

    if action in TOOLS:
        result = TOOLS[action].invoke(args)
    else:
        result = "ERROR: Unknown action"

    return {**state, "result": result}


def create_validator_node(llm):
    def validator_node(state: AgentState):
        prompt = f"""
Validate result.

User request: {state['input']}
Result: {state['result']}

Answer ONLY:
VALID or INVALID
"""
        response = llm.invoke(prompt)
        return {**state, "status": response.content.strip()}

    return validator_node

# ============================================================
# ROUTER
# ============================================================

def route(state: AgentState):
    if state["status"] == "VALID":
        return END
    return "planner"

# ============================================================
# GRAPH BUILDER
# ============================================================

def build_graph(llm):
    graph = StateGraph(AgentState)

    graph.add_node("planner", create_planner_node(llm))
    graph.add_node("executor", executor_node)
    graph.add_node("validator", create_validator_node(llm))

    graph.set_entry_point("planner")

    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "validator")

    graph.add_conditional_edges("validator", route)

    return graph.compile()

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    setup_db()
    seed_data()

    with open(r"E:\Lenovo Ideapad 330\company-material\ai-upskill\key-vault\groq\groq-api-key.txt") as f:
        api_key = f.read().strip()

    llm = get_llm(api_key)

    app = build_graph(llm)

    # TEST CASES
    inputs = [
        "Add user Alice with id ML200",
        "List all users",
        "Find user ML001",
        "Update ML002 authentication to 1",
        "Count users",
        "Search users named Raj",
        "Delete user ML003"
    ]

    for query in inputs:
        print("\n============================")
        print("USER:", query)

        state = {
            "input": query,
            "plan": {},
            "result": "",
            "status": ""
        }

        result = app.invoke(state)

        print("FINAL RESULT:", result["result"])

