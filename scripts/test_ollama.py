import requests

url = "https://be24-194-214-160-117.ngrok-free.app/api/chat"  # Use your ngrok URL + /api/chat

headers = {
    "Content-Type": "application/json",
    "ngrok-skip-browser-warning": "true"  # You can keep this if needed
}

payload = {
    "model": "deepseek-r1:70b",
    "messages": [
        {
            "role": "user",
            "content": "Solve: 25 * 25"
        }
    ],
    "stream": False
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.text)
