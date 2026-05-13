import requests

url = "http://127.0.0.1:8000/chat"

payload = {
    "user_input": "What is the weather in Bangalore?"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())