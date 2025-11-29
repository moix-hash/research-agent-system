import pytest
import asyncio
from src.agents.research_agent import ResearchAgent
from src.agents.writing_agent import WritingAgent
from src.agents.analysis_agent import AnalysisAgent
from src.models.schemas import AgentType, AgentMessage

@pytest.mark.asyncio
async def test_research_agent_initialization():
    """Test research agent initialization"""
    agent = ResearchAgent()
    await agent.start()
    
    assert agent.agent_type == AgentType.RESEARCH
    assert agent.name == "Research Specialist"
    assert agent.is_running == True
    
    await agent.stop()
    assert agent.is_running == False

@pytest.mark.asyncio
async def test_research_agent_process_message():
    """Test research agent message processing"""
    agent = ResearchAgent()
    await agent.start()
    
    message = AgentMessage(
        sender=AgentType.COORDINATOR,
        receiver=AgentType.RESEARCH,
        content={"topic": "Test Topic", "depth": "basic"},
        message_type="research_request"
    )
    
    result = await agent.process_message(message)
    assert result["status"] in ["completed", "failed"]
    assert "result" in result or "error" in result
    
    await agent.stop()

@pytest.mark.asyncio
async def test_writing_agent_content_generation():
    """Test writing agent content generation"""
    agent = WritingAgent()
    await agent.start()
    
    test_content = {
        "research_content": "This is test research content about AI technology.",
        "content_type": "article",
        "tone": "professional"
    }
    
    result = await agent.generate_content(test_content)
    assert result["status"] in ["completed", "failed"]
    assert "content" in result or "error" in result
    
    await agent.stop()

@pytest.mark.asyncio
async def test_analysis_agent_content_analysis():
    """Test analysis agent content analysis"""
    agent = AnalysisAgent()
    await agent.start()
    
    test_content = {
        "content": "This is a test content for analysis. It contains multiple sentences to analyze for quality and sentiment.",
        "analysis_type": "quality"
    }
    
    result = await agent.analyze_content(test_content)
    assert result["status"] in ["completed", "failed"]
    assert "analysis_report" in result or "error" in result
    
    if "analysis_report" in result:
        report = result["analysis_report"]
        assert "sentiment" in report
        assert "readability_score" in report
        assert "content_length" in report
    
    await agent.stop()

@pytest.mark.asyncio
async def test_agent_message_passing():
    """Test agent-to-agent message passing"""
    research_agent = ResearchAgent()
    writing_agent = WritingAgent()
    
    await research_agent.start()
    await writing_agent.start()
    
    # Test message creation
    message = await research_agent.send_message(
        AgentType.WRITING,
        {"research_data": "test data"},
        "data_transfer"
    )
    
    assert message.sender == AgentType.RESEARCH
    assert message.receiver == AgentType.WRITING
    assert message.message_type == "data_transfer"
    
    await research_agent.stop()
    await writing_agent.stop()

@pytest.mark.asyncio
async def test_agent_memory_storage():
    """Test agent memory storage functionality"""
    agent = ResearchAgent()
    await agent.start()
    
    test_data = {"key": "value", "number": 42}
    test_key = "test_memory"
    
    # Store memory
    await agent.memory_bank.store_memory(test_key, test_data)
    
    # Retrieve memory
    retrieved = await agent.memory_bank.retrieve_memory(test_key)
    assert retrieved is not None
    assert retrieved["data"]["key"] == "value"
    assert retrieved["data"]["number"] == 42
    
    await agent.stop()