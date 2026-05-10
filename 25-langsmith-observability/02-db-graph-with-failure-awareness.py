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
    suggestion: str


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
# TOOLS (SAFE)
# ============================================================

@tool
def add_user(name: str, user_id: str) -> str:
    """Add user safely (no duplicates)"""

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    existing = cursor.fetchone()

    if existing:
        conn.close()
        return f"ERROR: User with ID {user_id} already exists"

    cursor.execute(
        "INSERT INTO users VALUES (?, ?, ?)",
        (user_id, name, 1)
    )
    conn.commit()
    conn.close()

    return f"SUCCESS: Added {name}"


@tool
def list_users() -> str:
    """List all users"""
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

    if not row:
        return f"ERROR: User {user_id} not found"

    return json.dumps(row)


TOOLS = {
    "add_user": add_user,
    "list_users": list_users,
    "get_user_by_id": get_user_by_id,
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
# UTIL
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
# -- Changes made in prompt with exampples
def create_planner_node(llm):
    def planner_node(state: AgentState):

        prompt = f"""
You are a planner.

Available actions:
- add_user(name, user_id)
- list_users()
- get_user_by_id(user_id)

Examples:
"Add user Alice ML200" → add_user(name="Alice", user_id="ML200")
"Find user ML001" → get_user_by_id(user_id="ML001")

Return ONLY JSON:
{{"action": "...", "args": {{...}}}}

User input: {state['input']}
"""

        response = llm.invoke(prompt)
        plan = safe_parse_json(response.content)

        if not plan:
            plan = {"action": "list_users", "args": {}}

        return {"plan": plan}

    return planner_node


def executor_node(state: AgentState):
    action = state["plan"].get("action")
    args = state["plan"].get("args", {})

    if action in TOOLS:
        result = TOOLS[action].invoke(args)
    else:
        result = "ERROR: Unknown action"

    # 🔥 detect errors
    if "ERROR" in result:
        return {
            "result": result,
            "status": "ERROR"
        }

    return {"result": result}


def create_validator_node(llm):
    def validator_node(state: AgentState):

        # short-circuit errors
        if state.get("status") == "ERROR":
            return {"status": "ERROR"}

        prompt = f"""
Validate result.

User: {state['input']}
Result: {state['result']}

Answer ONLY:
VALID or INVALID
"""

        response = llm.invoke(prompt)
        status = response.content.strip()

        if status not in ["VALID", "INVALID"]:
            status = "VALID"

        return {"status": status}

    return validator_node


def create_suggester_node(llm):
    def suggester_node(state: AgentState):

        prompt = f"""
User request failed.

Request: {state['input']}
Error: {state['result']}

Suggest a helpful fix (short).

Example:
- Try a different user ID
"""

        response = llm.invoke(prompt)

        return {"suggestion": response.content}

    return suggester_node


# ============================================================
# ROUTER
# ============================================================

def route(state: AgentState):

    if state["status"] == "VALID":
        return END

    if state["status"] == "ERROR":
        return "suggester"

    return END


# ============================================================
# GRAPH
# ============================================================

def build_graph(llm):

    graph = StateGraph(AgentState)

    graph.add_node("planner", create_planner_node(llm))
    graph.add_node("executor", executor_node)
    graph.add_node("validator", create_validator_node(llm))
    graph.add_node("suggester", create_suggester_node(llm))

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

    queries = [
        "Add user Anil with id ML200",
        "Add user Anil with id ML200",  # duplicate
        "Find user ML001",
        "List all users"
    ]

    for q in queries:
        print("\n======================")
        print("USER:", q)

        state = {
            "input": q,
            "plan": {},
            "result": "",
            "status": "",
            "suggestion": ""
        }

        result = app.invoke(state)

        print("RESULT:", result.get("result"))

        if result.get("suggestion"):
            print("💡 SUGGESTION:", result["suggestion"])