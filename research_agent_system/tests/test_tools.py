import pytest
import asyncio
from src.tools.web_search import WebSearchTool
from src.tools.custom_tools import DataAnalysisTool, ContentOptimizerTool, SentimentAnalyzerTool
from src.tools.file_operations import FileOperationsTool
from src.tools.code_executor import CodeExecutorTool

@pytest.mark.asyncio
async def test_web_search_tool():
    """Test web search tool functionality"""
    search_tool = WebSearchTool()
    
    results = await search_tool.search_async("artificial intelligence", max_results=3)
    
    assert isinstance(results, list)
    assert len(results) <= 3
    
    for result in results:
        assert "title" in result
        assert "snippet" in result
        assert "url" in result
    
    await search_tool.close()

@pytest.mark.asyncio
async def test_data_analysis_tool():
    """Test data analysis tool functionality"""
    analysis_tool = DataAnalysisTool()
    
    test_content = [
        {"snippet": "This is a research paper about machine learning algorithms."},
        {"snippet": "Breaking news: AI company announces breakthrough."},
        {"snippet": "General information about technology trends."}
    ]
    
    analysis = await analysis_tool.analyze_content(test_content)
    
    assert "total_items" in analysis
    assert "total_word_count" in analysis
    assert "content_types" in analysis
    assert "quality_score" in analysis
    
    assert analysis["total_items"] == 3
    assert isinstance(analysis["content_types"], list)

@pytest.mark.asyncio
async def test_content_optimizer_tool():
    """Test content optimizer tool functionality"""
    optimizer = ContentOptimizerTool()
    
    test_content = "This is kinda gonna be a great article. Yeah, it's really good."
    
    optimized = await optimizer.optimize_content(
        test_content, 
        "article", 
        "professional"
    )
    
    assert isinstance(optimized, str)
    assert len(optimized) > 0
    # Check that informal language is replaced
    assert "kinda" not in optimized or "kind of" in optimized

@pytest.mark.asyncio
async def test_sentiment_analyzer_tool():
    """Test sentiment analyzer tool functionality"""
    analyzer = SentimentAnalyzerTool()
    
    # Test positive content
    positive_content = "This is a great and amazing product with excellent features."
    positive_result = await analyzer.analyze_sentiment(positive_content)
    
    assert positive_result["sentiment"] in ["positive", "neutral", "negative"]
    assert "score" in positive_result
    assert "positive_words" in positive_result
    assert "negative_words" in positive_result
    
    # Test negative content
    negative_content = "This is a bad product with poor quality and terrible performance."
    negative_result = await analyzer.analyze_sentiment(negative_content)
    
    assert negative_result["sentiment"] in ["positive", "neutral", "negative"]

@pytest.mark.asyncio
async def test_file_operations_tool():
    """Test file operations tool functionality"""
    file_tool = FileOperationsTool(base_path="./test_data")
    
    test_content = "This is test content for file operations."
    test_filename = "test_file.txt"
    
    # Test save
    save_result = await file_tool.save_content(test_filename, test_content)
    assert save_result["success"] == True
    assert "filepath" in save_result
    
    # Test load
    load_result = await file_tool.load_content(test_filename)
    assert load_result["success"] == True
    assert load_result["content"] == test_content
    
    # Test list files
    files = await file_tool.list_files()
    assert test_filename in files
    
    # Cleanup
    import os
    if os.path.exists("./test_data"):
        import shutil
        shutil.rmtree("./test_data")

@pytest.mark.asyncio
async def test_code_executor_tool():
    """Test code executor tool functionality"""
    executor = CodeExecutorTool()
    
    # Test valid Python code
    valid_code = "print('Hello, World!')\nresult = 2 + 2\nprint(f'2 + 2 = {result}')"
    
    result = await executor.execute_python_code(valid_code)
    assert result["success"] == True
    assert "Hello, World!" in result["output"]
    assert "2 + 2 = 4" in result["output"]
    
    # Test syntax validation
    validation_result = await executor.validate_syntax(valid_code)
    assert validation_result["valid"] == True
    assert validation_result["errors"] == []
    
    # Test invalid Python code
    invalid_code = "print('Hello, World!'\n# Missing closing parenthesis"
    
    validation_result = await executor.validate_syntax(invalid_code)
    assert validation_result["valid"] == False
    assert len(validation_result["errors"]) > 0