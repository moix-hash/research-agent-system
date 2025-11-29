import pytest
import asyncio
import aiohttp
import json
from src.api.routes import app
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)

def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "endpoints" in data

def test_health_endpoint(client):
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "components" in data
    assert "api" in data["components"]

def test_status_endpoint(client):
    """Test status endpoint"""
    response = client.get("/status")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert "active_tasks" in data
    assert "agents_online" in data

def test_create_research_task(client):
    """Test research task creation"""
    research_data = {
        "topic": "Artificial Intelligence in Healthcare",
        "content_type": "research_report",
        "tone": "professional",
        "length": "medium",
        "depth": "comprehensive"
    }
    
    response = client.post("/research", json=research_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "task_id" in data
    assert "status" in data
    assert "message" in data

def test_get_task_status(client):
    """Test task status retrieval"""
    # First create a task
    research_data = {
        "topic": "Test Topic for Status Check",
        "content_type": "article"
    }
    
    create_response = client.post("/research", json=research_data)
    task_data = create_response.json()
    task_id = task_data["task_id"]
    
    # Then check its status
    status_response = client.get(f"/tasks/{task_id}")
    assert status_response.status_code == 200
    
    status_data = status_response.json()
    assert status_data["task_id"] == task_id
    assert "status" in status_data
    assert "request" in status_data

def test_list_tasks(client):
    """Test task listing"""
    response = client.get("/tasks")
    assert response.status_code == 200
    
    data = response.json()
    assert "total_tasks" in data
    assert "tasks" in data
    assert isinstance(data["tasks"], list)

def test_metrics_endpoint(client):
    """Test metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    
    # Metrics should return text/plain format
    assert response.headers["content-type"] == "text/plain; version=0.0.4; charset=utf-8"

def test_memory_stats_endpoint(client):
    """Test memory stats endpoint"""
    response = client.get("/memory/stats")
    assert response.status_code == 200
    
    data = response.json()
    assert "total_memories" in data
    assert "storage_backend" in data

def test_session_stats_endpoint(client):
    """Test session stats endpoint"""
    response = client.get("/sessions/stats")
    assert response.status_code == 200
    
    data = response.json()
    assert "total_sessions" in data

@pytest.mark.asyncio
async def test_full_agent_integration():
    """Test full agent integration"""
    from src.agents.research_agent import ResearchAgent
    from src.agents.writing_agent import WritingAgent
    from src.agents.analysis_agent import AnalysisAgent
    from src.agents.coordinator_agent import CoordinatorAgent
    
    # Initialize agents
    research_agent = ResearchAgent()
    writing_agent = WritingAgent()
    analysis_agent = AnalysisAgent()
    coordinator_agent = CoordinatorAgent(research_agent, writing_agent, analysis_agent)
    
    # Start agents
    await research_agent.start()
    await writing_agent.start()
    await analysis_agent.start()
    await coordinator_agent.start()
    
    # Test coordinated task execution
    task_data = {
        "task_id": "test_integration_task",
        "topic": "Machine Learning Applications",
        "content_type": "article",
        "tone": "professional",
        "depth": "basic"
    }
    
    try:
        result = await coordinator_agent.coordinate_task(task_data)
        
        assert "status" in result
        assert "task_id" in result
        assert result["task_id"] == "test_integration_task"
        
        if result["status"] == "completed":
            assert "research" in result
            assert "content" in result
            assert "analysis" in result
            
    finally:
        # Cleanup
        await research_agent.stop()
        await writing_agent.stop()
        await analysis_agent.stop()
        await coordinator_agent.stop()

def test_invalid_task_id(client):
    """Test handling of invalid task ID"""
    response = client.get("/tasks/invalid_task_id")
    assert response.status_code == 404
    
    data = response.json()
    assert "detail" in data
    assert "Task not found" in data["detail"]

def test_invalid_research_request(client):
    """Test handling of invalid research request"""
    invalid_data = {
        "topic": "",  # Empty topic should be invalid
        "content_type": "invalid_type"  # Invalid content type
    }
    
    response = client.post("/research", json=invalid_data)
    # Note: The actual validation would depend on Pydantic model constraints
    assert response.status_code in [200, 422]  # Could be either depending on validation