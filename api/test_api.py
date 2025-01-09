import requests
import os

def test_api():
    # Base URL - change this to match your server
    BASE_URL = "http://localhost:5000"
    
    print("Testing API endpoints...")
    
    # Test 1: Health Check
    print("\n1. Testing /api/healthcheck")
    try:
        response = requests.get(f"{BASE_URL}/api/healthcheck")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")

    # Test 2: File Upload
    print("\n2. Testing /api/analyze")
    # Use existing test file path
    test_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'test.csv')
    
    if not os.path.exists(test_file_path):
        print(f"Test file not found at {test_file_path}")
        return
    
    try:
        files = {'file': open(test_file_path, 'rb')}
        response = requests.post(f"{BASE_URL}/api/analyze", files=files)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_api()
