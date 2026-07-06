import requests


url = "http://127.0.0.1:8000/evaluate"

payload = {
    "question": "What is RAG?"
}

response = requests.post(
    url,
    json=payload,
    timeout=30,
)

print("Status Code:", response.status_code)
print("Response:")
print(response.json())