import requests
import json

def quick_test():
    url = "http://localhost:8001/api/v1/auth/register"
    user_data = {
        "email": "testuser@edms.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(url, json=user_data, timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            print("✅ ¡Registro exitoso!")
            print(f"User: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

quick_test()