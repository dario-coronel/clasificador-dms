import requests
import json

def single_test():
    url = "http://localhost:8000/api/v1/auth/register"
    user_data = {
        "email": "test@test.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpass123"
    }
    
    print("🧪 Single test for registration...")
    response = requests.post(url, json=user_data, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    single_test()