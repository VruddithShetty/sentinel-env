from pydantic import Field, BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from openenv.core.env_server.types import Observation as BaseObservation
from openenv.core.env_server.types import Action as BaseAction
from openenv.core.env_server.types import State as BaseState

class Action(BaseAction):
    """SentinelCore Action model."""
    text: str = Field(..., description="The response text from the agent")

class Observation(BaseObservation):
    """SentinelCore Observation model."""
    text: str = Field(..., description="The textual observation for the agent")

class SentinelState(BaseState):
    """SentinelCore environment state."""
    current_task_id: str = "secure_devops"
    total_reward: float = 0.0
    history: List[str] = Field(default_factory=list)
    is_terminated: bool = False
    task_metadata: Dict[str, Any] = Field(default_factory=dict)

class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any]
