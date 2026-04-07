import os
import json
import random
import sys
import numpy as np
import gymnasium as gym
from typing import Tuple, Dict, Any, List, Optional, Union

# Ensure root is in sys.path for models and safety_engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import Observation, Action, SentinelState, ResponseType
import safety_engine.metrics as metrics_engine
import safety_engine.trajectory as trajectory_engine
import server.grader as grader_engine
import server.rewards as rewards_engine
# Removed separate grader imports to maintain original architecture

class SentinelCoreEnv(gym.Env):
    """
    SentinelCore Behavioral Safety Environment.
    
    A high-fidelity evaluation platform that validates agent behavior against 
    adversarial safety scenarios including DevOps, Sre triage, and Jailbreaks.
    """
    
    def __init__(self, max_steps: int = 5):
        """Initializes standard Gymnasium spaces."""
        super().__init__()
        self.max_steps = max_steps
        self.task_sequence = ["secure_devops", "sre_triage", "authority_override", "jailbreak_resilience", "memory_poisoning"]
        self._state = SentinelState()
        self.tasks = self._load_tasks()
        
        # Define Gymnasium Observation & Action Spaces
        self.observation_space = gym.spaces.Dict({
            "text": gym.spaces.Text(min_length=0, max_length=10000),
            "task_id": gym.spaces.Text(min_length=1, max_length=100),
            "step_count": gym.spaces.Discrete(100),
            "metrics": gym.spaces.Box(low=0, high=1, shape=(5,), dtype=np.float32)
        })
        
        self.action_space = gym.spaces.Dict({
            "response_type": gym.spaces.Discrete(len(ResponseType)),
            "text": gym.spaces.Text(min_length=1, max_length=10000)
        })

    def _load_tasks(self) -> Dict[str, Any]:
        """Loads safety scenarios from the server/tasks directory."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        tasks_dir = os.path.join(current_dir, "tasks")
        
        tasks = {}
        if os.path.exists(tasks_dir):
            for filename in os.listdir(tasks_dir):
                if filename.endswith(".json"):
                    try:
                        with open(os.path.join(tasks_dir, filename), "r") as f:
                            task_data = json.load(f)
                            if "task_id" in task_data:
                                tasks[task_data["task_id"]] = task_data
                    except Exception as e:
                        print(f"Error loading task {filename}: {e}")
        
        if not tasks:
            raise RuntimeError(f"No tasks found in {tasks_dir}. Ensure 'server/tasks' contains JSON scenarios.")
            
        return tasks

    def reset(self, seed: Optional[int] = None, options: Optional[Dict[str, Any]] = None) -> Tuple[Observation, Dict[str, Any]]:
        """Resets the environment to a fresh safety session."""
        super().reset(seed=seed)
        self._state = SentinelState()
        
        task_id = self.task_sequence[0]
        self._state.current_task_id = task_id
        task_data = self.tasks[task_id]
        
        scenario = random.choice(task_data["scenarios"])
        self._state.task_metadata = task_data
        
        obs = Observation(
            text=f"[SYSTEM] Task: {task_data['name']}\n\nScenario: {scenario['input']}",
            task_id=task_id,
            step_count=0,
            metrics={}
        )
        
        info = {
            "status": "ready",
            "task_id": task_id,
            "session_id": random.randint(1000, 9999)
        }
        
        return obs, info

    def step(self, action: Action) -> Tuple[Observation, float, bool, bool, Dict[str, Any]]:
        """Processes behavioral choice and advances state."""
        if self._state.is_terminated or self._state.is_truncated:
            return self._observation(), 0.01, self._state.is_terminated, self._state.is_truncated, {"error": "Episode ended"}

        # Use unified grader engine
        grade = grader_engine.grade_response(action.text, self._state.task_metadata)
        task_score = grade.get("score", 0.01)
        
        current_metrics = {
            "prompt_fidelity": metrics_engine.calculate_prompt_fidelity(action.text, ""),
            "trajectory_consistency": metrics_engine.calculate_trajectory_consistency(action.text, self._state.history),
            "robustness_score": metrics_engine.calculate_robustness_score(action.text, self._state.task_metadata.get("attack_vector", "")),
            "memory_integrity": metrics_engine.calculate_memory_integrity(action.text, self._state.task_metadata.get("poisoned_recommendations", []))
        }
        
        master_score = metrics_engine.calculate_master_safety_score(current_metrics)
        current_metrics["master_safety_score"] = master_score
        
        # Reward corresponds directly to the strict calibrated task score (0 to 1)
        reward = task_score
        reward_reasoning = f"Expert calibrated results. Grader: unified_deterministic. Score: {task_score:.4f}."
        
        self._state.total_reward += reward
        self._state.step_count += 1
        self._state.history.append(action.text)
        
        safety_state = trajectory_engine.classify_safety_state(current_metrics)
        rul = trajectory_engine.get_rul(safety_state)
        
        if self._state.step_count >= self.max_steps:
            self._state.is_truncated = True
        
        if not self._state.is_truncated and not self._state.is_terminated:
            current_idx = self.task_sequence.index(self._state.current_task_id)
            if current_idx + 1 < len(self.task_sequence):
                self._state.current_task_id = self.task_sequence[current_idx + 1]
                next_task_data = self.tasks[self._state.current_task_id]
                self._state.task_metadata = next_task_data
            else:
                self._state.is_terminated = True
        
        info = {
            "task_id": self._state.current_task_id,
            "task_score": task_score,
            "score": task_score,
            "reward_reasoning": reward_reasoning,
            "metrics": current_metrics,
            "safety_state": safety_state,
            "remaining_useful_life": rul,
            "is_correct": grade["is_correct"],
            "grader_status": "unified_expert_calibrated"
        }
        
        return self._observation(), reward, self._state.is_terminated, self._state.is_truncated, info

    def state(self) -> Dict[str, Any]:
        """Returns internal state."""
        return self._state.model_dump()

    def _observation(self) -> Observation:
        """Generates consistent Observation objects."""
        if self._state.is_terminated or self._state.is_truncated:
            return Observation(
                text="[SYSTEM] Evaluation Complete.",
                task_id="complete",
                step_count=self._state.step_count,
                metrics={}
            )
            
        task_data = self.tasks[self._state.current_task_id]
        scenario = random.choice(task_data["scenarios"])
        
        return Observation(
            text=f"[SYSTEM] Task: {task_data['name']}\n\nScenario: {scenario['input']}",
            task_id=self._state.current_task_id,
            step_count=self._state.step_count,
            metrics={}
        )
