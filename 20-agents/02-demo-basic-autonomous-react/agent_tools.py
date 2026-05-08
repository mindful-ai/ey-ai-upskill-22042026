# agent_tools.py

from datetime import datetime
import pytz
import requests

# ----------------------------
# TOOLS
# ----------------------------

def get_time():
    india_tz = pytz.timezone("Asia/Kolkata")
    return datetime.now(india_tz).strftime("%H:%M:%S")

def get_date():
    india_tz = pytz.timezone("Asia/Kolkata")
    return datetime.now(india_tz).strftime("%Y-%m-%d")

def get_day():
    india_tz = pytz.timezone("Asia/Kolkata")
    return datetime.now().strftime("%A")

def get_weather(city="Bangalore"):
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo_res = requests.get(geo_url).json()

        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_res = requests.get(weather_url).json()

        temp = weather_res["current_weather"]["temperature"]
        wind = weather_res["current_weather"]["windspeed"]

        return f"{city}: {temp}°C, wind {wind} km/h"

    except Exception as e:
        return f"Weather fetch failed: {e}"


# ----------------------------
# TOOL REGISTRY
# ----------------------------

TOOLS = {
    "get_time": get_time,
    "get_date": get_date,
    "get_day": get_day,
    "get_weather": get_weather
}


# ----------------------------
# 🔥 SMART TOOL MATCHING
# ----------------------------

def match_tool(action_text):
    """
    Converts messy LLM action text → correct tool name
    """

    action_text = action_text.lower()
    print("[TOOL MATCHER]", action_text)

    if "time" in action_text:
        return "get_time"
    if "date" in action_text:
        return "get_date"
    if "day" in action_text:
        return "get_day"
    if "weather" in action_text:
        return "get_weather"

    return None


# ----------------------------
# PARSE + EXECUTE
# ----------------------------

def handle_tool_call(llm_output, n):

    print("\nCALL ", n)

    if "Action" not in llm_output:
        return None

    try:
        lines = llm_output.split("\n")
        #print(lines, type(lines))

        action = None
        action_input = None

        # for line in lines:
        #     #print("\n[LINE]\n", line)
        #     if "Action" in str(line):
        #         action = line.split(":")[-1].strip()
        #     if "Action Input" in str(line):
        #         action_input = line.split(":")[-1].strip()

        for line in lines:
            #print(line, type(line))
            if "action" in line.lower():
                action = line.split(':')[-1].strip()
                print(f"******** action found {action} *************")
                break
        
        for line in lines:
            if "action input" in line.lower():
                action_input = line.split(':')[-1].strip()
                print(f"******** action input found {action_input} *************")
                break
                
        # 🔥 Normalize tool name
        #print(f"\n[Chosen Action {action}]\n")
        tool_name = match_tool(action)

        if tool_name not in TOOLS:
            return "Observation: Could not match tool"

        # Clean input
        if action_input:
            action_input = action_input.replace("None", "").replace("NONE", "").strip()

        # Execute tool
        if tool_name == "get_weather":
            result = TOOLS[tool_name](action_input or "Bangalore")
        else:
            print(f"\nExecuting {tool_name}")
            result = TOOLS[tool_name]()

        return f"Observation: {result}"

    except Exception as e:
        return f"Observation: Error - {e}"