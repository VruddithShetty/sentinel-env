import requests

BASE_URL = "http://localhost:7860"

def run_tests():
    print("Testing Root (GET /)")
    res = requests.get(f"{BASE_URL}/")
    print("Status:", res.status_code, "Body:", res.json(), "\n")

    print("Testing Health Check (GET /health)")
    res = requests.get(f"{BASE_URL}/health")
    print("Status:", res.status_code, "Body:", res.json(), "\n")

    print("Testing Environment Reset (POST /reset)")
    res = requests.post(f"{BASE_URL}/reset")
    print("Status:", res.status_code, "Body:", res.json(), "\n")

    print("Testing Environment Step (POST /step)")
    # Using the exact Action schema for the body, which requires "response"
    action = {"response": "[BLOCK] Harmful command detected: DELETE_SYSTEM_FILES. Refusing to execute."}
    res = requests.post(f"{BASE_URL}/step", json=action)
    print("Status:", res.status_code, "Body:", res.json(), "\n")

    print("Testing Environment State (GET /state)")
    res = requests.get(f"{BASE_URL}/state")
    print("Status:", res.status_code, "Body:", res.json(), "\n")

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print("Error during tests:", e)
