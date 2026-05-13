# mcp_server.py

from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import requests
import json

app = FastAPI()

f = open(r"E:\Lenovo Ideapad 330\company-material\ai-upskill-2\key-vault\openai\ne-openai-api-key.txt")
apikey = f.read()
f.close()

client = OpenAI(api_key=apikey)

weather_api_key = "87772df6c012e938a4ec01e30f429d59"

# -----------------------------
# TOOL IMPLEMENTATION
# -----------------------------
def get_weather(city: str):
    api_key = "YOUR_OPENWEATHER_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"]
    }

# -----------------------------
# TOOL REGISTRY (MCP STYLE)
# -----------------------------
TOOLS = {
    "get_weather": get_weather
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# -----------------------------
# REQUEST MODEL
# -----------------------------
class Query(BaseModel):
    user_input: str

# -----------------------------
# MCP ENDPOINT
# -----------------------------
@app.post("/chat")
def chat(query: Query):
    print(f"Received query: {query.user_input}")
    messages = [
        {"role": "user", "content": query.user_input}
    ]

    # Step 1: Ask LLM
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=TOOL_SCHEMAS,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # Step 2: Tool call handling
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        # Execute tool
        result = TOOLS[function_name](**arguments)

        # Append tool response
        messages.append(message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })

        # Step 3: Final LLM response
        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        return {
            "response": final_response.choices[0].message.content,
            "tool_used": function_name,
            "tool_result": result
        }

    # No tool used
    return {
        "response": message.content,
        "tool_used": None
    }