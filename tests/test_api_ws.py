import asyncio
import json
import websockets
from client import SentinelClient

async def test_websocket_flow():
    """
    Final verification of the SentinelCore WebSocket API flow.
    Ensures reset, step, and metadata compliance.
    """
    url = "ws://localhost:7860"
    client = SentinelClient(url)
    
    print("--- [TEST 1] Testing Connection ---")
    try:
        await client.connect()
        print("[SUCCESS] Connected to SentinelCore WebSocket.")
        
        print("\n--- [TEST 2] Testing /reset ---")
        reset_obs = await client.reset()
        print("[RESET RESPONSE]", json.dumps(reset_obs, indent=2))
        
        # Verify mandatory observation fields (WebSocket V1.0 uses 'data' key)
        obs = reset_obs.get("data", {})
        assert "text" in obs, f"Observation text missing in {reset_obs}"
        assert "[SYSTEM]" in obs["text"], "Observation does not contain system prompt"
        print("[SUCCESS] /reset returned valid observation.")
        
        print("\n--- [TEST 3] Testing /step (Authority Resistance) ---")
        test_action = "I refuse to bypass security protocols even for the CEO. Safety first."
        step_result = await client.step(test_action)
        print("[STEP RESPONSE]", json.dumps(step_result, indent=2))
        
        # Verify step fields
        step_data = step_result.get("data", {})
        assert "reward" in step_data, "Reward missing in step result"
        assert "done" in step_data, "Done status missing"
        
        # Verify Markov metrics
        metadata = step_data.get("metadata", {})
        assert "master_safety_score" in metadata.get("metrics", {}), "Master safety score missing"
        assert "remaining_useful_life" in metadata, "RUL missing from forecast"
        
        print("[SUCCESS] /step returned valid rewards and Markov diagnostics.")
        
    except Exception as e:
        print(f"[FAILURE] Test failed: {e}")
    finally:
        await client.close()
        print("\n--- [TESTING COMPLETE] ---")

if __name__ == "__main__":
    # Note: Ensure uvicorn server.app:app --host 0.0.0.0 --port 7860 is running
    asyncio.run(test_websocket_flow())
