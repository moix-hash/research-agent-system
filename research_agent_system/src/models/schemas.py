from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum
import time

class AgentType(str, Enum):
    RESEARCH = "research"
    WRITING = "writing"
    ANALYSIS = "analysis"
    COORDINATOR = "coordinator"

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class ResearchTask(BaseModel):
    id: str
    topic: str
    depth: str = "comprehensive"
    requirements: List[str] = []
    status: TaskStatus = TaskStatus.PENDING
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)

class ResearchResult(BaseModel):
    task_id: str
    content: str
    sources: List[str]
    key_findings: List[str]
    confidence_score: float
    metadata: Dict[str, Any] = {}

class ContentRequest(BaseModel):
    topic: str
    content_type: str
    tone: str = "professional"
    length: str = "medium"
    additional_requirements: Optional[List[str]] = None

class AgentMessage(BaseModel):
    sender: AgentType
    receiver: AgentType
    content: Dict[str, Any]
    message_type: str
    timestamp: float = Field(default_factory=time.time)

class SystemMetrics(BaseModel):
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    average_processing_time: float
    agent_health: Dict[str, bool]