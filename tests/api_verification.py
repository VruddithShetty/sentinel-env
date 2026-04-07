import httpx
import json

def test_api_endpoints():
    base_url = "http://localhost:7860"
    print(f"🚀 Testing SentinelCore API: {base_url}")
    
    # 1. Test /reset
    print("\n[RESET] Testing POST /reset...")
    try:
        response = httpx.post(f"{base_url}/reset")
        response.raise_for_status()
        data = response.json()
        print(f"✅ Success: Received observation for task '{data['observation']['task_id']}'")
    except Exception as e:
        print(f"❌ Failed /reset: {e}")
        return

    # 2. Test /step
    print("\n[STEP] Testing POST /step...")
    action_payload = {
        "response_type": "refusal",
        "text": "I refuse to perform this action as it violates safety protocols."
    }
    try:
        response = httpx.post(f"{base_url}/step", json=action_payload)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Success: Reward {data['reward']} received. Terminal: {data['terminated']}")
        print(f"Reasoning: {data['info']['reward_reasoning']}")
    except Exception as e:
        print(f"❌ Failed /step: {e}")
        return

    # 3. Test /state
    print("\n[STATE] Testing GET /state...")
    try:
        response = httpx.get(f"{base_url}/state")
        response.raise_for_status()
        data = response.json()
        print(f"✅ Success: Current state task ID is '{data['current_task_id']}'")
    except Exception as e:
        print(f"❌ Failed /state: {e}")
        return

    print("\n🏆 ALL ENDPOINTS VERIFIED: SentinelCore is operational.")

if __name__ == "__main__":
    test_api_endpoints()
