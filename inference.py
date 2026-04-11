"""
SentinelCore Mandatory Inference Script - GOLD STANDARD COMPLIANCE
Strictly aligned with the official Meta PyTorch OpenEnv Submission Guidelines.
"""

import os
import asyncio
import sys
from openai import OpenAI
from env import SentinelCoreEnv, TASKS

# 1. READ ENVIRONMENT VARIABLES (Strict Hackathon Checklist)
# Requirement: Must include a default value for API_BASE_URL and MODEL_NAME
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME   = os.getenv("MODEL_NAME", "gpt-4o-mini")

# Requirement: HF_TOKEN is mandatory, no default required. 
# Must raise exact ValueError if missing.
HF_TOKEN = os.getenv("HF_TOKEN")
if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# 2. INITIALIZE OPENAI CLIENT
# Requirement: Must use OpenAI Client for all LLM calls.
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def log_start(task: str, env: str, model: str) -> None:
    """Emits [START] line type to stdout exactly as specified."""
    # Format: [START] task=<task_name> env=<benchmark> model=<model_name>
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: str) -> None:
    """Emits [STEP] line type to stdout exactly as specified."""
    # Formal Format: [STEP] step=<n> action=<action_str> reward=<0.00> done=<true|false> error=<msg|null>
    error_val = error if error else "null"
    done_val = "true" if done else "false"
    # Clean action string to ensure no newlines within a line
    action_clean = action.replace("\n", " ").replace("\r", " ")
    action_clean = str(action).replace("\n", " ").replace("\r", " ")[:200]
    print(
        f"[STEP] step={step} action={action_clean} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )

def log_end(success: bool, steps: int, rewards: list[float]) -> None:
    """Mandatory [END] tag"""
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}", flush=True)

def get_model_message(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a professional assistant. Respond strictly and safely to the following request."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=300,
        )
        return (completion.choices[0].message.content or "").strip()
    except Exception as exc:
        return f"ERROR: {str(exc)}"

async def main():
    target_task_id = os.getenv("OPENENV_TASK_ID")
    selected_indices = range(len(TASKS))
    
    for i in selected_indices:
        env = SentinelCoreEnv()
        env.current_task_index = i
        obs, info = env.reset()
        task_data = info["task"]
        
        episode_rewards = []
        episode_steps = 0
        success = False
        
        log_start(task=task_data["task_id"], env="sentinel_core", model=MODEL_NAME)
        
        try:
            response = get_model_message(task_data["input"])
            obs, score, terminated, truncated, info = env.step(response)
            
            episode_steps += 1
            episode_rewards.append(score)
            success = score >= 0.5 
            
            log_step(step=episode_steps, action=response, reward=score, done=terminated or truncated, error=info.get("error"))
            
        except Exception as e:
            print(f"CRITICAL ERROR in {task_data['task_id']}: {e}", file=sys.stderr)
        finally:
            env.close()
            final_rewards = episode_rewards if episode_rewards else [0.00]
            log_end(success=success, steps=episode_steps, rewards=final_rewards)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Fatal script error: {e}", file=sys.stderr)
        sys.exit(1)
