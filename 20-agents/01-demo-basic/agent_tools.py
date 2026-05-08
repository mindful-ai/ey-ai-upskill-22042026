from datetime import datetime
# import pytz

# Tool: Get the current day
def get_current_day_india():
    # india_tz = pytz.timezone("Asia/Kolkata")
    return datetime.now().strftime("%A")

def agent_router(topic):
    """Route the topic to the appropriate tool or question."""

    # Rule based routing for known topics
    if "day today" in topic.lower() or "current day" in topic.lower() or "what day" in topic.lower():
        day = get_current_day_india()
        return f"The current day in India is {day}."
    
    # When no tool is needed 
    return None

if __name__ == "__main__":
    print("Current day in India:", get_current_day_india())
    print(agent_router("What is the day today in India?"))