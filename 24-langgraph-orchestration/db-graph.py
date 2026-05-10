from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.graph import StateGraph, END

import sqlite3
import json
from typing import TypedDict

# ============================================================
# STATE
# ============================================================

class AgentState(TypedDict):
    input: str
    plan: dict
    result: str
    status: str
    retries: int

MAX_RETRIES = 2

# ============================================================
# DATABASE
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
# TOOLS (ALL INCLUDED)
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
    """Fetch user by ID"""
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
    return "SUCCESS: Updated authentication"


@tool
def delete_user(user_id: str) -> str:
    """Delete a user from the database"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    return "SUCCESS: Deleted user"


@tool
def count_users() -> str:
    """Return total number of users"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return str(count)


@tool
def search_user_by_name(name: str) -> str:
    """Search users by name (partial match)"""
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
# SAFE JSON PARSER
# ============================================================

def safe_parse_json(text):
    try:
        return json.loads(text)
    except:
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            return json.loads(text[start:end])
        except:
            return None

# ============================================================
# NODES
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
        plan = safe_parse_json(response.content)

        if not plan or "action" not in plan:
            plan = {"action": "list_users", "args": {}}

        return {**state, "plan": plan}

    return planner_node


def executor_node(state: AgentState):
    action = state["plan"].get("action")
    args = state["plan"].get("args", {})

    if action in TOOLS:
        result = TOOLS[action].invoke(args)
    else:
        result = "ERROR: Unknown action"

    return {**state, "result": result}


def create_validator_node(llm):
    def validator_node(state: AgentState):

        prompt = f"""
Check if result satisfies request.

User: {state['input']}
Result: {state['result']}

Answer ONLY: VALID or INVALID
"""

        response = llm.invoke(prompt)
        status = response.content.strip()

        if status not in ["VALID", "INVALID"]:
            status = "VALID"

        return {**state, "status": status}

    return validator_node


def retry_node(state: AgentState):
    return {**state, "retries": state["retries"] + 1}

# ============================================================
# ROUTER
# ============================================================

def route(state: AgentState):

    if state["status"] == "VALID":
        return END

    if state["retries"] >= MAX_RETRIES:
        return END

    return "retry"

# ============================================================
# DEMO: GRAPH
# ============================================================

def build_graph(llm):
    
    graph = StateGraph(AgentState)

    graph.add_node("planner", create_planner_node(llm))
    graph.add_node("executor", executor_node)
    graph.add_node("validator", create_validator_node(llm))
    graph.add_node("retry", retry_node)

    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "validator")

    graph.add_conditional_edges("validator", route)
    graph.add_edge("retry", "planner")

    graph.set_entry_point("planner")

    return graph.compile()

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    setup_db()
    seed_data()

    with open(r"E:\Lenovo Ideapad 330\company-material\ai-upskill-3\key-vault\groq\groq-api-key.txt") as f:
        api_key = f.read().strip()

    llm = get_llm(api_key)
    graph = build_graph(llm)

    queries = [
        "Add user Alice with id ML200",
        "List all users",
        "Find user with id ML001", # Discuss here
        "Update ML002 authentication to 1",
        "Count users",
        "Search users named Raj",
        "Delete user ML003"
    ]

    for q in queries:
        print("\n==========================")
        print("USER:", q)

        state = {
            "input": q,
            "plan": {},
            "result": "",
            "status": "",
            "retries": 0
        }

        result = graph.invoke(state)

        print("FINAL RESULT:", result["result"])