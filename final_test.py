import requests
import json

url = "http://localhost:8002/api/v1/auth/register"
data = {
    "email": "finaltest@edms.com",
    "username": "finaltest",
    "first_name": "Final",
    "last_name": "Test",
    "password": "password123"
}

print("🧪 Testing final registration...")
try:
    response = requests.post(url, json=data, timeout=5)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print("✅ SUCCESS! Registration working!")
        print(f"User: {response.json()}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Connection error: {e}")