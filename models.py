from pydantic import BaseModel, Field
from typing import List, Optional

class TaskInfo(BaseModel):
    id: str = Field(..., description="Unique identifier for the task.")
    description: str = Field(..., description="Short description of the task objective.")
    input_data: str = Field(..., description="The raw input string assigned to the task.")

class Observation(BaseModel):
    task_input: str = Field(..., description="The input string provided to the agent for the current task.")
    current_task_index: int = Field(..., description="The zero-indexed position of the current task.")
    total_tasks: int = Field(..., description="Total number of tasks in the current environment session.")

class Action(BaseModel):
    response: str = Field(..., description="The agent's text response to the current task.")

class EnvState(BaseModel):
    current_task_index: int = Field(0, description="The current active task index.")
    scores: List[float] = Field(default_factory=list, description="Historical list of scores for completed tasks.")
    completed: bool = Field(False, description="Whether the environment has finished all tasks.")
    total_score: float = Field(0.0, description="Mean score calculated upon environment completion.")
