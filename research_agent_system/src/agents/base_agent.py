import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from src.models.schemas import AgentType, AgentMessage
from src.memory.memory_bank import MemoryBank
from src.observability.logging import get_logger
from src.observability.tracing import tracer

logger = get_logger(__name__)

class BaseAgent(ABC):
    def __init__(self, agent_type: AgentType, name: str):
        self.agent_type = agent_type
        self.name = name
        self.memory_bank = MemoryBank()
        self.logger = get_logger(f"agent.{name}")
        self.is_running = False
        
    @abstractmethod
    async def process_message(self, message: AgentMessage) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def execute_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    async def send_message(self, receiver: AgentType, content: Dict[str, Any], message_type: str):
        message = AgentMessage(
            sender=self.agent_type,
            receiver=receiver,
            content=content,
            message_type=message_type
        )
        self.logger.info(f"Sending message to {receiver}", message_type=message_type)
        return message
    
    async def start(self):
        self.is_running = True
        self.logger.info(f"Agent {self.name} started")
    
    async def stop(self):
        self.is_running = False
        self.logger.info(f"Agent {self.name} stopped")