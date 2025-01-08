import requests
import os

def test_healthcheck():
    response = requests.get('http://localhost:5000/api/healthcheck')
    print(f"Healthcheck status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_analyze():
    # Path to your test CSV file
    test_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'test.csv')
    
    if not os.path.exists(test_file_path):
        print(f"Test file not found at {test_file_path}")
        return
    
    files = {'file': open(test_file_path, 'rb')}
    response = requests.post('http://localhost:5000/api/analyze', files=files)
    print(f"Analyze status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == '__main__':
    print("Testing API endpoints...")
    test_healthcheck()
    test_analyze()
