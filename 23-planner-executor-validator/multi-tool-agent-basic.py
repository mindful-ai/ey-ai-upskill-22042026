from langchain_openai import ChatOpenAI
from langchain.tools import tool
import sqlite3
import json

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
# TOOLS
# ============================================================

@tool
def add_user(name: str, user_id: str) -> str:
    """Add a new user"""
    print(f"[TOOL]Adding user: {name} with ID: {user_id}")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (user_id, name, 1))
    conn.commit()
    conn.close()
    return f"Added {name}"


@tool
def list_users() -> str:
    """List all users"""
    print("[TOOL] Listing all users")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    return json.dumps(rows)


@tool
def get_user_by_id(user_id: str) -> str:
    """Get user by ID"""
    print(f"[TOOL] Getting user by ID: {user_id}")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return json.dumps(row)


@tool
def update_user_auth(user_id: str, authenticated: int) -> str:
    """Update auth status"""
    print(f"[TOOL] Updating auth for user ID: {user_id} to {authenticated}")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET authenticated=? WHERE id=?",
        (authenticated, user_id)
    )
    conn.commit()
    conn.close()
    return "Updated"


@tool
def delete_user(user_id: str) -> str:
    """Delete user"""
    print(f"[TOOL] Deleting user ID: {user_id}")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    return "Deleted"


@tool
def count_users() -> str:
    """Count users"""
    print("[TOOL] Counting users")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return str(count)


@tool
def search_user_by_name(name: str) -> str:
    """Search user by name"""
    print(f"[TOOL] Searching users by name: {name}")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name LIKE ?", (f"%{name}%",))
    rows = cursor.fetchall()
    conn.close()
    return json.dumps(rows)


# ============================================================
# TOOL REGISTRY
# ============================================================

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
# PLANNER
# ============================================================

def planner(llm, user_input):
    prompt = f"""
Detect the tool action needed for the query along with args
Return ONLY JSON.

Format:
{{
  "action": "tool_name",
  "args": {{}}
}}

User request: {user_input}
"""

    response = llm.invoke(prompt)
    raw = response.content.strip()

    print("[RAW]", raw)   # 👈 important for debugging

    # 🔥 FIX 1: Handle empty response
    if not raw:
        return {"action": "list_users", "args": {}}

    # 🔥 FIX 2: Safe parsing
    try:
        return json.loads(raw)
    except:
        print("⚠️ Invalid JSON, using fallback")
        return {"action": "list_users", "args": {}}

# ============================================================
# EXECUTOR
# ============================================================

def executor(plan):
    try:
        plan_json = plan if isinstance(plan, dict) else json.loads(plan)
        action = plan_json.get("action")
        args = plan_json.get("args", {})
        print(f"[EXECUTOR] Action: {action}, Args: {args}")
        if action in TOOLS:
            print(f"[EXECUTOR] Executing {action} with args {args}")
            result = TOOLS[action].invoke(args)
            return result
        else:
            return f"Unknown action: {action}"
    except Exception as e:
        return f"Error executing plan: {str(e)}"


# ============================================================
# VALIDATOR
# ============================================================

def validator(llm, user_input, result):
    prompt = f"""
You are a validator agent that checks if the result from the executor answers the user's question.
User's question: {user_input}
Executor result: {result}   

Does the result answer the user's question? 
Return ONLY:
"VALID" if it does, otherwise return "INVALID".
"""
    return llm.invoke(prompt)


# ============================================================
# ORCHESTRATOR
# ============================================================

def run_agent(llm, user_input):
    print("\n\n----------- AGENT RUN ------------------")
    plan = planner(llm, user_input)
    print(f"[PLANNER] Plan: {plan}")
    result = executor(plan)
    print(f"[EXECUTOR] Result: {result}")
    validation = validator(llm, user_input, result)
    print(f"[VALIDATOR] Validation: {validation.content.strip()}")
    print("\n\n----------------------------------------")
    return validation


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    setup_db()
    seed_data()

    with open(r"E:\Lenovo Ideapad 330\company-material\ai-upskill-3\key-vault\groq\groq-api-key.txt") as f:
        api_key = f.read().strip()

    llm = get_llm(api_key)

    # DEMO CASES
    # print("1. Adding user named Alice with id ML200")
    # print(run_agent(llm, "Add user named Alice with id ML200"))
    # print("2. Finding user with name Raj")
    # print(run_agent(llm, "Find user with name Raj"))
    # print("3. How many users exist?")
    # print(run_agent(llm, "How many users exist?"))
    # print("4. Set authentication of ML002 to 1")
    # print(run_agent(llm, "Set authentication of ML002 to 1"))
    # print("5. Delete user ML003")
    # print(run_agent(llm, "Delete user ML003"))
    # print("6. List all users")
    # print(run_agent(llm, "List all users"))

    run_agent(llm, "Add user named Alice with id ML200")
    run_agent(llm, "List all users")