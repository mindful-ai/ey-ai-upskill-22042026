from urllib.parse import urlencode

query = {"q": "What are the symptoms of high blood pressure?"}
url = f"http://localhost:8000/ask?{urlencode(query)}"

print(url)