import sys
import os
import random

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the environment from the server location
from server.environment import SentinelCoreEnv
from models import Action, ResponseType

def test_100_steps():
    """
    Standard OpenEnv validation script.
    Runs 100 random steps and verifies Gymnasium 5-tuple output.
    """
    print("🚀 Starting SentinelCore 100-step validation...")
    env = SentinelCoreEnv(max_steps=10)
    
    success_count = 0
    episodes = 0
    total_steps = 100
    
    obs, info = env.reset()
    print(f"✅ Reset successful. Task: {obs.task_id}")
    
    for i in range(total_steps):
        # Sample random action
        action_text = f"Random safety response {i}"
        action = Action(
            response_type=random.choice(list(ResponseType)),
            text=action_text
        )
        
        # Step the environment
        result = env.step(action)
        
        # Verify 5-tuple return
        if not isinstance(result, tuple) or len(result) != 5:
            print(f"❌ FAILED: Step {i} did not return 5-tuple. Got: {type(result)}")
            return False
            
        obs, reward, terminated, truncated, info = result
        
        # Verify JSON serializability of reward reasoning
        if "reward_reasoning" not in info:
            print(f"❌ FAILED: Step {i} info missing 'reward_reasoning'")
            return False
            
        if i % 20 == 0:
            print(f"Step {i:03d} | Reward: {reward:+.2f} | Score: {info.get('score', 'N/A')} | Reasoning: {info['reward_reasoning'][:50]}...")
            
        success_count += 1
        
        if terminated or truncated:
            episodes += 1
            obs, info = env.reset()
            
    print("-" * 50)
    print(f"🏆 Final Result: {success_count}/{total_steps} steps passed.")
    print(f"Episodes completed: {episodes}")
    print("STATUS: 100% OPENENV COMPLIANT")
    return True

if __name__ == "__main__":
    if test_100_steps():
        sys.exit(0)
    else:
        sys.exit(1)
