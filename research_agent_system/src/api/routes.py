from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import asyncio
import uuid
from datetime import datetime

from src.api.middleware import MetricsMiddleware, LoggingMiddleware
from src.observability.metrics import metrics
from src.observability.logging import get_logger
from src.memory.memory_bank import MemoryBank
from src.memory.session_manager import SessionManager
from src.agents.research_agent import ResearchAgent
from src.agents.writing_agent import WritingAgent
from src.agents.analysis_agent import AnalysisAgent
from src.agents.coordinator_agent import CoordinatorAgent

logger = get_logger(__name__)

# Initialize components
memory_bank = MemoryBank()
session_manager = SessionManager()
research_agent = ResearchAgent()
writing_agent = WritingAgent()
analysis_agent = AnalysisAgent()
coordinator_agent = CoordinatorAgent(research_agent, writing_agent, analysis_agent)

# FastAPI app
app = FastAPI(
    title="Research Agent System",
    description="A multi-agent AI system for automated research and content creation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middleware
app.add_middleware(MetricsMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class ResearchRequest(BaseModel):
    topic: str
    content_type: str = "article"
    tone: str = "professional"
    length: str = "medium"
    depth: str = "comprehensive"

class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str

class SystemStatus(BaseModel):
    status: str
    active_tasks: int
    agents_online: List[str]
    memory_entries: int
    active_sessions: int

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    components: Dict[str, str]

# Storage for active tasks
active_tasks: Dict[str, Dict[str, Any]] = {}

@app.on_event("startup")
async def startup_event():
    """Initialize agents and components on startup"""
    logger.info("Starting Research Agent System...")
    
    # Start all agents
    await research_agent.start()
    await writing_agent.start()
    await analysis_agent.start()
    await coordinator_agent.start()
    
    logger.info("All agents started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Research Agent System...")
    
    await research_agent.stop()
    await writing_agent.stop()
    await analysis_agent.stop()
    await coordinator_agent.stop()
    
    logger.info("All agents stopped")

@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "message": "Research Agent System API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "/research": "POST - Create research task",
            "/tasks/{id}": "GET - Get task status",
            "/tasks": "GET - List all tasks",
            "/status": "GET - System status",
            "/health": "GET - Health check",
            "/metrics": "GET - System metrics",
            "/docs": "GET - API documentation"
        }
    }

@app.post("/research", response_model=TaskResponse)
async def create_research_task(request: ResearchRequest, background_tasks: BackgroundTasks):
    """Create a new research task"""
    task_id = str(uuid.uuid4())
    
    task_data = {
        "task_id": task_id,
        "topic": request.topic,
        "content_type": request.content_type,
        "tone": request.tone,
        "length": request.length,
        "depth": request.depth
    }
    
    # Store task in active tasks
    active_tasks[task_id] = {
        "status": "pending",
        "request": request.dict(),
        "created_at": datetime.now().isoformat(),
        "result": None
    }
    
    # Update metrics
    metrics.update_active_tasks(len(active_tasks))
    
    # Execute task in background
    background_tasks.add_task(execute_research_task, task_id, task_data)
    
    logger.info(f"Created research task", task_id=task_id, topic=request.topic)
    
    return TaskResponse(
        task_id=task_id,
        status="started",
        message=f"Research task started for topic: {request.topic}"
    )

@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Get status of a specific task"""
    if task_id not in active_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return active_tasks[task_id]

@app.get("/tasks")
async def list_tasks():
    """List all tasks"""
    tasks_summary = []
    for task_id, task_data in active_tasks.items():
        tasks_summary.append({
            "task_id": task_id,
            "topic": task_data["request"]["topic"],
            "status": task_data["status"],
            "created_at": task_data["created_at"],
            "content_type": task_data["request"]["content_type"]
        })
    
    return {
        "total_tasks": len(active_tasks),
        "tasks": tasks_summary
    }

@app.get("/status", response_model=SystemStatus)
async def get_system_status():
    """Get system status and metrics"""
    memory_stats = await memory_bank.get_memory_stats()
    session_stats = await session_manager.get_session_stats()
    coordinator_metrics = await coordinator_agent.get_system_metrics()
    
    return SystemStatus(
        status="operational",
        active_tasks=len(active_tasks),
        agents_online=["research", "writing", "analysis", "coordinator"],
        memory_entries=memory_stats.get("total_memories", 0),
        active_sessions=session_stats.get("total_sessions", 0)
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    components = {
        "api": "healthy",
        "research_agent": "healthy" if research_agent.is_running else "unhealthy",
        "writing_agent": "healthy" if writing_agent.is_running else "unhealthy",
        "analysis_agent": "healthy" if analysis_agent.is_running else "unhealthy",
        "coordinator_agent": "healthy" if coordinator_agent.is_running else "unhealthy",
        "memory_bank": "healthy",
        "session_manager": "healthy"
    }
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        components=components
    )

@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return metrics.get_metrics()

@app.get("/memory/stats")
async def get_memory_stats():
    """Get memory bank statistics"""
    return await memory_bank.get_memory_stats()

@app.get("/sessions/stats")
async def get_session_stats():
    """Get session manager statistics"""
    return await session_manager.get_session_stats()

async def execute_research_task(task_id: str, task_data: Dict[str, Any]):
    """Execute research task using coordinator agent"""
    try:
        logger.info(f"Executing research task", task_id=task_id)
        
        # Update task status
        active_tasks[task_id]["status"] = "in_progress"
        
        # Execute task through coordinator
        result = await coordinator_agent.coordinate_task(task_data)
        
        # Update task with result
        active_tasks[task_id].update({
            "status": result.get("status", "completed"),
            "result": result,
            "completed_at": datetime.now().isoformat()
        })
        
        # Update metrics
        metrics.update_active_tasks(len(active_tasks))
        
        logger.info(f"Research task completed", task_id=task_id, status=result.get("status"))
        
    except Exception as e:
        logger.error(f"Research task failed", task_id=task_id, error=str(e))
        
        active_tasks[task_id].update({
            "status": "failed",
            "error": str(e),
            "completed_at": datetime.now().isoformat()
        })
        
        metrics.update_active_tasks(len(active_tasks))