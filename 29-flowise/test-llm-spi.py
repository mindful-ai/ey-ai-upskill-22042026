import requests

API_URL = "https://cloud.flowiseai.com/api/v1/prediction/fa3f3931-9645-4f9c-b3d4-461b6b25d9be"

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()
    
output = query({
    "question": "Give me 5 facts about AI in bullet points",
})

print(output["text"])