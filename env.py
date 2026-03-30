from typing import Tuple, Dict, Any
from models import EnvState, Observation, Action

# Scenario Inputs
from scenarios.task1 import TASK_1_INPUT
from scenarios.task2 import TASK_2_INPUT
from scenarios.task3 import TASK_3_INPUT
from scenarios.task4 import TASK_4_INPUT

# Grader Functions
from graders.task1_grader import grade_task1
from graders.task2_grader import grade_task2
from graders.task3_grader import grade_task3
from graders.task4_grader import grade_task4

# Task Definition Map
TASKS = {
    "task1": {"input": TASK_1_INPUT, "grader": grade_task1},
    "task2": {"input": TASK_2_INPUT, "grader": grade_task2},
    "task3": {"input": TASK_3_INPUT, "grader": grade_task3},
    "task4": {"input": TASK_4_INPUT, "grader": grade_task4},
}

class SentinelEnv:
    def __init__(self):
        # Default sequence for inference.py (Standard Safety Suite)
        self._task_sequence = ["task1", "task2", "task3"]
        self._state = EnvState()

    def reset(self) -> Observation:
        self._state = EnvState()
        return self._get_observation()

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        # Case: Episode already completed
        if self._state.completed:
            return self._get_observation(), 0.0, True, {
                "metrics": {
                    "latency": 0.1,
                    "task_id": "completed",
                    "status": "completed"
                },
                "error": "Episode already completed"
            }

        current_task_id = self._task_sequence[self._state.current_task_index]
        current_task = TASKS[current_task_id]
        
        # Calculate Reward
        reward = current_task["grader"](action.response)
        
        # Consistent Structure for info
        info = {
            "metrics": {
                "latency": 0.1,
                "task_id": current_task_id,
                "status": "running"
            },
            "error": None
        }
        
        self._state.scores.append(reward)
        self._state.current_task_index += 1
        
        # Transition to completed if sequence finished
        if self._state.current_task_index >= len(self._task_sequence):
            self._state.completed = True
            self._state.total_score = sum(self._state.scores) / len(self._task_sequence)
            info["metrics"]["status"] = "completed"
        
        return self._get_observation(), reward, self._state.completed, info

    def state(self) -> EnvState:
        return self._state

    def _get_observation(self) -> Observation:
        total = len(self._task_sequence)
        if self._state.completed:
            return Observation(
                task_input="COMPLETED",
                current_task_index=self._state.current_task_index,
                total_tasks=total
            )
        
        current_id = self._task_sequence[self._state.current_task_index]
        return Observation(
            task_input=TASKS[current_id]["input"],
            current_task_index=self._state.current_task_index,
            total_tasks=total
        )
