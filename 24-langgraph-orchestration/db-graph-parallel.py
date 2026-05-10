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
    parallel_results: dict

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
# TOOLS
# ============================================================

@tool
def add_user(name: str, user_id: str) -> str:
    """Add a new user"""
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
    """List all users"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    return json.dumps(rows)


@tool
def count_users() -> str:
    """Count users"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return str(count)


@tool
def search_user_by_name(name: str) -> str:
    """Search users by name"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name LIKE ?", (f"%{name}%",))
    rows = cursor.fetchall()
    conn.close()
    return json.dumps(rows)

TOOLS = {
    "add_user": add_user,
    "list_users": list_users,
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

        prompt = f"""
You are a planner.

If user asks for analytics, return:
{{"mode": "parallel"}}

Otherwise:
{{"mode": "single", "action": "...", "args": {{}}}}

User input: {state['input']}
"""

        response = llm.invoke(prompt)
        plan = safe_parse_json(response.content)

        if not plan:
            plan = {"mode": "single", "action": "list_users", "args": {}}

        return {"plan": plan}

    return planner_node


# -------- Single execution --------
def executor_single(state: AgentState):
    plan = state["plan"]
    action = plan.get("action")
    args = plan.get("args", {})

    if action in TOOLS:
        result = TOOLS[action].invoke(args)
    else:
        result = "ERROR: Unknown action"

    return {"result": result}


# -------- Parallel execution (SAFE) --------
def executor_parallel(state: AgentState):

    results = {
        "count": count_users.invoke({}),
        "list": list_users.invoke({}),
        "search": search_user_by_name.invoke({"name": "a"})
    }

    return {"parallel_results": results}


# -------- Aggregator --------
def aggregator_node(state: AgentState):
    combined = json.dumps(state.get("parallel_results", {}), indent=2)
    return {"result": combined}


# -------- Validator --------
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

        return {"status": status}

    return validator_node


def retry_node(state):
    return {"retries": state["retries"] + 1}


# ============================================================
# ROUTERS
# ============================================================

def route_after_planner(state: AgentState):
    if state["plan"].get("mode") == "parallel":
        return "executor_parallel"
    return "executor_single"


def route_after_validator(state: AgentState):
    if state["status"] == "VALID":
        return END
    if state["retries"] >= MAX_RETRIES:
        return END
    return "retry"


# ============================================================
# DEMOGRAPH
# ============================================================

def build_graph(llm):
    
    graph = StateGraph(AgentState)

    graph.add_node("planner", create_planner_node(llm))
    graph.add_node("executor_single", executor_single)
    graph.add_node("executor_parallel", executor_parallel)
    graph.add_node("aggregator", aggregator_node)
    graph.add_node("validator", create_validator_node(llm))
    graph.add_node("retry", retry_node)

    graph.set_entry_point("planner")
    graph.add_conditional_edges("planner", route_after_planner)

    graph.add_edge("executor_single", "validator")
    graph.add_edge("executor_parallel", "aggregator")
    graph.add_edge("aggregator", "validator")

    graph.add_conditional_edges("validator", route_after_validator)
    graph.add_edge("retry", "planner")

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
    app = build_graph(llm)

    queries = [
        "Add user Alice with id ML300",
        "List all users",
        "Show analytics of users"
    ]

    for q in queries:
        print("\n======================")
        print("USER:", q)

        state = {
            "input": q,
            "plan": {},
            "result": "",
            "status": "",
            "retries": 0,
            "parallel_results": {}
        }

        result = app.invoke(state)

        print("FINAL RESULT:")
        print(result["result"])