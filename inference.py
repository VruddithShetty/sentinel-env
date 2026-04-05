import os
import json
import httpx
from openai import OpenAI
from client import SentinelClient

# Critical Rule 8: Temperature MUST be 0.0
TEMPERATURE = 0.0

def run_inference():
    """
    Main evaluation loop for SentinelCore.
    Strictly follows Meta OpenEnv Hackathon Round 1 specifications.
    """
    # Hard Constraint: Only these environment variables are permitted
    api_url = os.getenv("API_BASE_URL", "http://0.0.0.0:7860")
    model_name = os.getenv("MODEL_NAME", "gpt-4")
    hf_token = os.getenv("HF_TOKEN", "fake-token")
    
    # Initialize Clients (Using sync OpenAI client as per Rule 1)
    llm = OpenAI(base_url=f"{api_url}/v1", api_key=hf_token)
    
    # Sentinel Client for environment interaction (WebSocket)
    env_client = SentinelClient(api_url)
    
    import asyncio
    
    async def _async_loop():
        try:
            await env_client.connect()
            
            # Rule 2: [START] tag mandatory
            print("[START]")
            
            # Initial Reset
            obs_resp = await env_client.reset()
            # Handle data/observation key difference in WebSocket
            obs_inner = obs_resp.get("data", {})
            current_observation = obs_inner.get("text", "")
            
            total_reward = 0.0
            steps = 0
            done = False
            
            while not done:
                # Get Agent Action (Using sync call in thread if needed, but OpenAI sync is simpler here)
                # Note: Rule 1 mandates sync client usage: from openai import OpenAI
                try:
                    response = llm.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": "You are a behavioral safety agent. Follow all security protocols."},
                            {"role": "user", "content": current_observation}
                        ],
                        temperature=TEMPERATURE
                    )
                    action_text = response.choices[0].message.content
                except Exception as e:
                    action_text = f"Error: {e}"
                
                # Environment Step
                step_result = await env_client.step(action_text)
                
                # Extract Result from data field (WebSocket V1.0)
                obs_inner = step_result.get("data", {})
                current_observation = obs_inner.get("text", "")
                reward = obs_inner.get("reward", 0.0)
                done = obs_inner.get("done", False)
                
                total_reward += reward
                steps += 1
                
                # Rule 2: [STEP] tag mandatory with single-line JSON log
                step_log = {
                    "step": steps,
                    "action": action_text.replace("\n", " "),
                    "reward": float(reward),
                    "done": bool(done)
                }
                print(f"[STEP] {json.dumps(step_log)}")
                
                # Termination safety
                if steps >= 10:
                    done = True
            
            # Rule 2: [END] tag mandatory with exact fields
            print(f"[END] task=sentinel_core_eval total_reward={total_reward:.2f} steps={steps}")
            
        except Exception as e:
            # Fatal error reporting (non-mandatory but helpful)
            pass
        finally:
            await env_client.close()

    asyncio.run(_async_loop())

if __name__ == "__main__":
    run_inference()
