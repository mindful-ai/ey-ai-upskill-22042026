
from groq import Groq
from langchain.chat_models import ChatOpenAI

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool
import sqlite3
import re

@tool
def user_db_tool(query: str) -> str:
    """
    Interact with user database.
    """
    print(f"Tool activated. Received query: {query}")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query_lower = query.lower()

    try:
        # ----------------------------
        # LIST AUTH USERS
        # ----------------------------
        if "authenticated users" in query_lower:
            print("Listing authenticated users...")
            cursor.execute("SELECT id, name FROM users WHERE authenticated=1")
            rows = cursor.fetchall()
            return "\n".join([f"{r[0]} - {r[1]}" for r in rows]) or "No authenticated users found"

        # ----------------------------
        # ADD USER
        # ----------------------------
        elif "add" in query_lower:

            # ✅ FIXED REGEX
            name_match = re.search(r"name is (\w+)", query, re.IGNORECASE)
            id_match = re.search(r"id is (\w+)", query, re.IGNORECASE)
            print(f"Parsed name: {name_match.group(1) if name_match else 'None'}, Parsed ID: {id_match.group(1) if id_match else 'None'}")  

            if name_match and id_match:
                name = name_match.group(1)
                user_id = id_match.group(1)
                print(f"Adding user: {name}, ID: {user_id}")

                cursor.execute(
                    "INSERT INTO users (id, name, authenticated) VALUES (?, ?, ?)",
                    (user_id, name, 1)
                )
                conn.commit()

                return f"User {name} added with ID {user_id}"

            else:
                return "Could not parse user details. Use format: 'name is X, id is Y'"

        # ----------------------------
        # LIST ALL USERS
        # ----------------------------
        elif "list all users" in query_lower:
            cursor.execute("SELECT id, name, authenticated FROM users")
            rows = cursor.fetchall()
            print("Listing all users...")
            return "\n".join([str(r) for r in rows]) or "No users found"

        else:
            return "Unsupported query"

    except Exception as e:
        return f"Error: {str(e)}"

    finally:
        conn.close()

# ----------------------------------------------------------------------------


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

# ----------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------

f = open(r"E:\Lenovo Ideapad 330\company-material\ai-upskill\key-vault\groq\groq-api-key.txt")
groq_api_key = f.read()
f.close()

if __name__ == "__main__":

    print("Setting up database...")
    setup_db()
    seed_data()
    
    client = Groq(api_key=groq_api_key)
    tools = [user_db_tool]

    print("Creating LLM reference...")
    llm = ChatOpenAI(
        model="llama-3.1-8b-instant",
        openai_api_key=groq_api_key,
        openai_api_base="https://api.groq.com/openai/v1",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that manages users."),
        ("human", "{input}")
    ])

    print("Creating agent...")
    # agent = create_agent(
    #     model=llm,
    #     tools=tools
    # )

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True
        )

    agent_executor.invoke({
        "input": "Add user John age 30"
    })


    # print("[Invoking agent to list authenticated users]")
    # response = agent.invoke({
    #     "messages": [
    #         {"role": "user", "content": "List all authenticated users"}
    #     ]
    # })
    # print(response["messages"][-1].content)

    # print("[Invoking agent to add a new user]")
    # response = agent.invoke({
    #     "messages": [  
    #         {"role": "user", "content": "My name is Purushotham, id is ML005, add a new user"}
    #     ]
    # })
    # print(response["messages"][-1].content) 

    # print("[Invoking agent to list authenticated users]")
    # response = agent.invoke({
    #     "messages": [
    #         {"role": "user", "content": "List all authenticated users"}
    #     ]
    # })
    # print(response["messages"][-1].content)