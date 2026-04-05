import json
import os
import random
from typing import Tuple, Dict, Any, List
from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import EnvironmentMetadata
from models import Observation, Action, SentinelState
import safety_engine.metrics as metrics_engine
import safety_engine.trajectory as trajectory_engine
from server.grader import grade_response
from server.rewards import calculate_reward

class SentinelCoreEnv(Environment[Action, Observation, SentinelState]):
    """
    SentinelCore Behavioral Safety Environment.
    Compliant with OpenEnv Hackathon Round 1 specifications.
    """
    def __init__(self):
        super().__init__()
        self._state = SentinelState()
        self.tasks = self._load_tasks()
        
    @property
    def state(self) -> SentinelState:
        """Returns the current environment state."""
        return self._state
        
    @state.setter
    def state(self, value: SentinelState):
        self._state = value
        
    def _load_tasks(self) -> Dict[str, Any]:
        """Loads all task scenarios from the server/tasks directory."""
        # Use absolute path relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        tasks_dir = os.path.join(current_dir, "tasks")
        
        if not os.path.exists(tasks_dir):
            # Fallback for different execution contexts
            tasks_dir = os.path.join(os.getcwd(), "server", "tasks")
            
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
            raise RuntimeError(f"No tasks loaded from {tasks_dir}")
            
        return tasks

    def reset(self) -> Observation:
        """Initializes the safety session and loads the first task."""
        self.state = SentinelState()
        # Initial task: secure_devops
        task_id = self.state.current_task_id
        task_data = self.tasks[task_id]
        scenario = random.choice(task_data["scenarios"])
        
        self.state.task_metadata = task_data
        
        return Observation(
            text=f"[SYSTEM] Task: {task_data['name']}\n\nScenario: {scenario['input']}",
            metadata={
                "task_id": task_id,
                "scenario_id": scenario["id"],
                "step": self.state.step_count
            }
        )

    def step(self, action: Action) -> Observation:
        """Processes the agent response and transitions safety state."""
        if self.state.is_terminated:
            return Observation(text="[TERMINATED] Session complete.", metadata={"done": True})

        # 1. Deterministic Grading
        grade = grade_response(action.text, self.state.task_metadata)
        
        # 2. Safety Metric Computation
        current_metrics = {
            "prompt_fidelity": metrics_engine.calculate_prompt_fidelity(action.text, ""),
            "trajectory_consistency": metrics_engine.calculate_trajectory_consistency(action.text, self.state.history),
            "robustness_score": metrics_engine.calculate_robustness_score(action.text, self.state.task_metadata.get("attack_vector", "")),
            "memory_integrity": metrics_engine.calculate_memory_integrity(action.text, self.state.task_metadata.get("poisoned_recommendations", []))
        }
        
        # Calculate Master Safety Score
        master_score = metrics_engine.calculate_master_safety_score(current_metrics)
        current_metrics["master_safety_score"] = master_score
        
        # 3. Transition Markov Model
        safety_state = trajectory_engine.classify_safety_state(current_metrics)
        rul = trajectory_engine.get_rul(safety_state)
        v_prob = trajectory_engine.violation_probability(safety_state)
        
        # 4. Reward Shaping
        reward = calculate_reward(grade, current_metrics)
        self.state.total_reward += reward
        self.state.step_count += 1
        self.state.history.append(action.text)
        
        # 5. Check Terminal Condition
        # In this hackathon, we cycle through tasks or end after a fixed number of steps
        task_sequence = ["secure_devops", "sre_triage", "authority_override", "jailbreak_resilience", "memory_poisoning"]
        current_idx = task_sequence.index(self.state.current_task_id)
        
        if self.state.step_count >= len(task_sequence):
            self.state.is_terminated = True
        else:
            self.state.current_task_id = task_sequence[current_idx + 1]
            
        # Get next task info for observation
        next_task_id = self.state.current_task_id
        next_task_data = self.tasks[next_task_id]
        next_scenario = random.choice(next_task_data["scenarios"])
        self.state.task_metadata = next_task_data
        
        # Rule 10: Returns Observation
        obs_text = f"[SYSTEM] Task: {next_task_data['name']}\n\nScenario: {next_scenario['input']}"
        if self.state.is_terminated:
            obs_text = "[SYSTEM] Evaluation session complete. Aggregate score calculated."

        return Observation(
            text=obs_text,
            metadata={
                "reward": reward,
                "done": self.state.is_terminated,
                "metrics": current_metrics,
                "safety_state": safety_state,
                "remaining_useful_life": rul,
                "violation_probability": v_prob,
                "next_task_id": next_task_id
            }
        )

    def get_metadata(self) -> EnvironmentMetadata:
        """Returns OpenEnv compliant metadata."""
        return EnvironmentMetadata(
            name="SentinelCore",
            description="Safety evaluation platform for agentic AI.",
            tasks=self.tasks
        )
