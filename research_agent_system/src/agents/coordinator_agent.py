import asyncio
from typing import Dict, Any, List
from src.models.schemas import AgentType, AgentMessage, TaskStatus
from src.agents.base_agent import BaseAgent
from src.observability.tracing import tracer
from src.memory.session_manager import SessionManager

class CoordinatorAgent(BaseAgent):
    def __init__(self, research_agent, writing_agent, analysis_agent):
        super().__init__(AgentType.COORDINATOR, "System Coordinator")
        self.research_agent = research_agent
        self.writing_agent = writing_agent
        self.analysis_agent = analysis_agent
        self.session_manager = SessionManager()
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
        
    async def process_message(self, message: AgentMessage) -> Dict[str, Any]:
        with tracer.start_as_current_span("coordinator_agent.process_message") as span:
            if message.message_type == "new_task":
                return await self.coordinate_task(message.content)
            elif message.message_type == "task_update":
                return await self.handle_task_update(message.content)
            else:
                return {"status": "error", "reason": "unknown_message_type"}
    
    async def execute_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.coordinate_task(task_data)
    
    async def coordinate_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        with tracer.start_as_current_span("coordinator_agent.coordinate_task") as span:
            task_id = task_data.get("task_id", f"task_{len(self.active_tasks)}")
            topic = task_data.get("topic", "")
            content_type = task_data.get("content_type", "article")
            
            self.logger.info(f"Coordinating new task", task_id=task_id, topic=topic)
            
            session = await self.session_manager.create_session(task_id)
            self.active_tasks[task_id] = {
                "status": TaskStatus.IN_PROGRESS,
                "current_step": "research",
                "session": session
            }
            
            span.set_attribute("task.id", task_id)
            span.set_attribute("task.topic", topic)
            
            try:
                # Step 1: Research
                research_result = await self.research_agent.execute_task({
                    "task_id": task_id,
                    "topic": topic,
                    "depth": "comprehensive"
                })
                
                if research_result.get("status") != "completed":
                    raise Exception("Research phase failed")
                
                # Step 2: Writing
                writing_result = await self.writing_agent.execute_task({
                    "research_content": research_result["result"]["content"],
                    "content_type": content_type,
                    "tone": task_data.get("tone", "professional")
                })
                
                if writing_result.get("status") != "completed":
                    raise Exception("Writing phase failed")
                
                # Step 3: Analysis
                analysis_result = await self.analysis_agent.execute_task({
                    "content": writing_result["content"],
                    "analysis_type": "quality"
                })
                
                final_result = {
                    "task_id": task_id,
                    "status": TaskStatus.COMPLETED,
                    "research": research_result["result"],
                    "content": writing_result["content"],
                    "analysis": analysis_result["analysis_report"],
                    "timeline": {
                        "research_completed": True,
                        "writing_completed": True,
                        "analysis_completed": True
                    }
                }
                
                self.active_tasks[task_id]["status"] = TaskStatus.COMPLETED
                await session.update_state("completed", final_result)
                
                span.set_attribute("task.completed", True)
                return final_result
                
            except Exception as e:
                self.logger.error(f"Task coordination failed: {str(e)}")
                self.active_tasks[task_id]["status"] = TaskStatus.FAILED
                await session.update_state("failed", {"error": str(e)})
                
                return {
                    "task_id": task_id,
                    "status": TaskStatus.FAILED,
                    "error": str(e)
                }
    
    async def handle_task_update(self, update_data: Dict[str, Any]) -> Dict[str, Any]:
        task_id = update_data.get("task_id")
        if task_id in self.active_tasks:
            self.active_tasks[task_id].update(update_data)
            return {"status": "updated", "task_id": task_id}
        return {"status": "error", "reason": "task_not_found"}
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        completed_tasks = sum(1 for task in self.active_tasks.values() if task.get("status") == TaskStatus.COMPLETED)
        failed_tasks = sum(1 for task in self.active_tasks.values() if task.get("status") == TaskStatus.FAILED)
        
        return {
            "total_tasks": len(self.active_tasks),
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "success_rate": completed_tasks / max(len(self.active_tasks), 1),
            "active_sessions": len(self.session_manager.sessions)
        }