from pydantic import Field, BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from enum import Enum

class ResponseType(str, Enum):
    """Semantic labels for agent responses to improve LLM reasoning."""
    REFUSAL = "refusal"
    COMPLIANCE = "compliance"
    CLARIFICATION = "clarification"
    TECHNICAL_EXECUTION = "technical_execution"

class Action(BaseModel):
    """
    SentinelCore Action model.
    Encapsulates the agent's behavioral choice and response text.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    response_type: ResponseType = Field(
        default=ResponseType.TECHNICAL_EXECUTION,
        description="The semantic category of the agent's action"
    )
    text: str = Field(
        ..., 
        description="The actual response text or command from the agent"
    )

class Observation(BaseModel):
    """
    SentinelCore Observation model.
    Provides structured context and feedback to the AI agent.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    text: str = Field(
        ..., 
        description="The textual observation or prompt for the agent"
    )
    task_id: str = Field(
        ..., 
        description="The unique identifier for the current safety task"
    )
    step_count: int = Field(
        default=0, 
        description="Number of steps taken in the current episode"
    )
    metrics: Dict[str, float] = Field(
        default_factory=dict, 
        description="Safety metrics from the previous step"
    )

class SentinelState(BaseModel):
    """
    Internal environment state for SentinelCore.
    Tracks trajectory, rewards, and task progression.
    """
    current_task_id: str = "secure_devops"
    total_reward: float = 0.0
    history: List[str] = Field(default_factory=list)
    step_count: int = 0
    is_terminated: bool = False
    is_truncated: bool = False
    task_metadata: Dict[str, Any] = Field(default_factory=dict)
