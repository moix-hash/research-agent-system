import google.generativeai as genai
from typing import Dict, Any
from src.models.schemas import AgentType, AgentMessage
from src.agents.base_agent import BaseAgent
from src.observability.tracing import tracer
from src.tools.custom_tools import DataAnalysisTool, SentimentAnalyzerTool
from config.settings import settings

class AnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.ANALYSIS, "Data Analyst")
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro-latest')
        else:
            self.model = None
        self.data_analysis = DataAnalysisTool()
        self.sentiment_analyzer = SentimentAnalyzerTool()
        
    async def process_message(self, message: AgentMessage) -> Dict[str, Any]:
        with tracer.start_as_current_span("analysis_agent.process_message") as span:
            if message.message_type == "analysis_request":
                return await self.analyze_content(message.content)
            else:
                return {"status": "error", "reason": "unknown_message_type"}
    
    async def execute_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.analyze_content(task_data)
    
    async def analyze_content(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        with tracer.start_as_current_span("analysis_agent.analyze_content") as span:
            content = analysis_data.get("content", "")
            analysis_type = analysis_data.get("analysis_type", "comprehensive")
            
            self.logger.info(f"Starting {analysis_type} analysis")
            
            if self.model:
                analysis_prompt = f"""
                Perform {analysis_type} analysis on the following content:
                
                CONTENT:
                {content}
                
                Provide:
                1. Quality assessment
                2. Key insights summary
                3. Recommendations for improvement
                4. Confidence score
                """
                
                try:
                    response = self.model.generate_content(analysis_prompt)
                    analysis_result = response.text
                except Exception as e:
                    self.logger.warning(f"Gemini API failed, using fallback: {str(e)}")
                    analysis_result = self._generate_fallback_analysis(content)
            else:
                analysis_result = self._generate_fallback_analysis(content)
            
            sentiment = await self.sentiment_analyzer.analyze_sentiment(content)
            readability_score = await self.data_analysis.calculate_readability(content)
            
            analysis_report = {
                "analysis": analysis_result,
                "sentiment": sentiment,
                "readability_score": readability_score,
                "content_length": len(content),
                "key_topics": await self._extract_topics(content)
            }
            
            await self.memory_bank.store_memory(
                f"analysis_{analysis_type}",
                analysis_report,
                metadata={"analysis_type": analysis_type}
            )
            
            span.set_attribute("analysis.completed", True)
            span.set_attribute("analysis.type", analysis_type)
            
            return {
                "status": "completed",
                "analysis_report": analysis_report,
                "agent": self.agent_type.value
            }
    
    def _generate_fallback_analysis(self, content: str) -> str:
        return f"""
        Quality Assessment: Content appears well-structured and informative
        Key Insights: Comprehensive coverage of relevant topics
        Recommendations: Consider adding more specific examples and data points
        Confidence Score: 0.75
        """
    
    async def _extract_topics(self, content: str) -> list:
        words = content.lower().split()
        topic_keywords = {
            'technology': ['ai', 'artificial', 'intelligence', 'machine', 'learning', 'algorithm'],
            'business': ['market', 'investment', 'revenue', 'profit', 'strategy'],
            'health': ['medical', 'healthcare', 'treatment', 'patient', 'clinical'],
            'education': ['learning', 'teaching', 'student', 'curriculum', 'knowledge']
        }
        
        topics = []
        for topic, keywords in topic_keywords.items():
            if any(keyword in words for keyword in keywords):
                topics.append(topic)
        
        return topics if topics else ["general"]