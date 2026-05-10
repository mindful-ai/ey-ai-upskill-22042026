from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.graph import StateGraph, END

import sqlite3
import json
from typing import TypedDict, List


# ============================================================
# STATE (SHORT-TERM MEMORY)
# ============================================================

class AgentState(TypedDict):
    input: str
    plan: dict
    result: str
    status: str
    messages: List[dict]   # 🔥 short-term memory


# ============================================================
# DATABASE (LONG-TERM MEMORY)
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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        key TEXT PRIMARY KEY,
        value TEXT
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
# TOOLS
# ============================================================

@tool
def add_user(name: str, user_id: str) -> str:
    """Add user to database"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            (user_id, name, 1)
        )
        conn.commit()

        # 🔥 save long-term memory
        cursor.execute(
            "INSERT OR REPLACE INTO memory VALUES (?, ?)",
            ("last_user", f"{name}:{user_id}")
        )
        conn.commit()

        return f"User {name} added with ID {user_id}"

    except Exception as e:
        return f"ERROR: {str(e)}"

    finally:
        conn.close()


@tool
def list_users() -> str:
    """List all users"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, authenticated FROM users")
    rows = cursor.fetchall()
    conn.close()

    return "\n".join([str(r) for r in rows]) or "No users found"


@tool
def get_memory(key: str) -> str:
    """Retrieve memory"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT value FROM memory WHERE key=?", (key,))
    row = cursor.fetchone()
    conn.close()

    return row[0] if row else "No memory found"


TOOLS = {
    "add_user": add_user,
    "list_users": list_users,
    "get_memory": get_memory
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

def create_planner_node(llm):
    def planner_node(state: AgentState):

        messages = state["messages"]

        prompt = f"""
You are a planner.

Conversation history:
{messages}

Available actions:
- add_user(name, user_id)
- list_users()
- get_memory(key)

Examples:
"Add user Alice ML100" → add_user(name="Alice", user_id="ML100")
"List users" → list_users()
"Who was last user?" → get_memory(key="last_user")

Return ONLY JSON:
{{"action": "...", "args": {{}}}}

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

    # update short-term memory
    new_messages = state["messages"] + [
        {"role": "user", "content": state["input"]},
        {"role": "assistant", "content": result}
    ]

    # detect error
    if "ERROR" in result:
        return {
            "result": result,
            "status": "ERROR",
            "messages": new_messages
        }

    return {
        "result": result,
        "messages": new_messages
    }


def create_validator_node(llm):
    def validator_node(state: AgentState):

        if state.get("status") == "ERROR":
            return {"status": "ERROR"}

        prompt = f"""
Validate result.

User: {state['input']}
Result: {state['result']}

Answer ONLY: VALID or INVALID
"""

        response = llm.invoke(prompt)

        status = response.content.strip()
        if status not in ["VALID", "INVALID"]:
            status = "VALID"

        return {"status": status}

    return validator_node


# ============================================================
# ROUTER
# ============================================================

def route(state: AgentState):

    if state["status"] == "VALID":
        return END

    if state["status"] == "ERROR":
        return END

    return END


# ============================================================
# GRAPH
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

    state = {
        "input": "",
        "plan": {},
        "result": "",
        "status": "",
        "messages": []   # 🔥 short-term memory
    }

    queries = [
        "Add user Ravi with id ML600",
        "Now list users",
        "Was RAVI added successfully?",
        "Who was the last user added?"
    ]

    for q in queries:
        print("\n======================")
        print("USER:", q)

        state["input"] = q

        state = app.invoke(state)

        print("RESULT:", state["result"])