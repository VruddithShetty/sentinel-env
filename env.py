import gymnasium as gym
import os
import sys
import numpy as np
from typing import Tuple, Dict, Any, List, Optional

# IMPORTANT: Ensure the root directory is in sys.path
sys.path.append(os.getcwd())

# 1. IMPORT ALL TASKS + GRADERS (As requested)
from tasks.task1_devops import get_task as task1
from tasks.task2_sre import get_task as task2
from tasks.task3_authority import get_task as task3
from tasks.task4_jailbreak import get_task as task4
from tasks.task5_memory import get_task as task5

from graders.task1_grader import grade as grade1
from graders.task2_grader import grade as grade2
from graders.task3_grader import grade as grade3
from graders.task4_grader import grade as grade4
from graders.task5_grader import grade as grade5

from models import Observation, ResponseType

# 2. REGISTER TASKS
TASKS = [
    (task1, grade1),
    (task2, grade2),
    (task3, grade3),
    (task4, grade4),
    (task5, grade5),
]

class SentinelCoreEnv(gym.Env):
    """
    SentinelCore Behavioral Safety Environment.
    Fixed via Senior Backend Engineer Structural Pattern.
    """
    
    def __init__(self, render_mode: Optional[str] = None):
        super().__init__()
        self.current_task_index = 0
        
        # Define Gymnasium Observation & Action Spaces (Standard compliance)
        self.observation_space = gym.spaces.Dict({
            "text": gym.spaces.Text(min_length=0, max_length=10000),
            "task_id": gym.spaces.Text(min_length=1, max_length=100)
        })
        self.action_space = gym.spaces.Text(min_length=1, max_length=10000)

    def reset(self, seed=None, options=None):
        """RESET FUNCTION (As requested)"""
        super().reset(seed=seed)
        task_func = TASKS[self.current_task_index][0]
        task_data = task_func()
        
        # Return Observation Pydantic model for app.py compatibility
        obs = Observation(
            text=task_data["input"],
            task_id=task_data["task_id"]
        )
        return obs, {"status": "reset", "task": task_data}

    def step(self, action: Any):
        """STEP FUNCTION (As requested logic)"""
        # Handle both raw string (from inference.py) and Action object (from app.py)
        action_text = action.text if hasattr(action, "text") else str(action)
        
        task_func, grader = TASKS[self.current_task_index]
        task_data = task_func()
        
        # Execute grader
        score = grader(action_text)
        
        done = True
        
        info = {
            "metrics": {
                "task_id": task_data["task_id"],
                "status": "completed",
                "latency": 0.1,
                "score": score
            },
            "task_score": score,
            "score": score,
            "error": None
        }

        obs = Observation(
            text=task_data["input"],
            task_id=task_data["task_id"]
        )
        
        return obs, score, done, False, info

    def state(self) -> Dict[str, Any]:
        task_func = TASKS[self.current_task_index][0]
        return {"current_task": task_func(), "index": self.current_task_index}
