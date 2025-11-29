import google.generativeai as genai
from typing import Dict, Any
from src.models.schemas import AgentType, AgentMessage, ContentRequest
from src.agents.base_agent import BaseAgent
from src.observability.tracing import tracer
from src.tools.custom_tools import ContentOptimizerTool
from config.settings import settings

class WritingAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.WRITING, "Content Writer")
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro-latest')
        else:
            self.model = None
        self.content_optimizer = ContentOptimizerTool()
        
    async def process_message(self, message: AgentMessage) -> Dict[str, Any]:
        with tracer.start_as_current_span("writing_agent.process_message") as span:
            if message.message_type == "content_request":
                return await self.generate_content(message.content)
            else:
                return {"status": "error", "reason": "unknown_message_type"}
    
    async def execute_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.generate_content(task_data)
    
    async def generate_content(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        with tracer.start_as_current_span("writing_agent.generate_content") as span:
            research_content = content_data.get("research_content", "")
            content_type = content_data.get("content_type", "article")
            tone = content_data.get("tone", "professional")
            length = content_data.get("length", "medium")
            
            self.logger.info(f"Generating {content_type} content", tone=tone, length=length)
            
            if self.model:
                writing_prompt = f"""
                Based on the following research, create a {content_type} with {tone} tone and {length} length:
                
                RESEARCH:
                {research_content}
                
                Requirements:
                - Well-structured and engaging
                - Appropriate for {tone} tone
                - {length} length
                - Include key insights from research
                """
                
                try:
                    response = self.model.generate_content(writing_prompt)
                    draft_content = response.text
                except Exception as e:
                    self.logger.warning(f"Gemini API failed, using fallback: {str(e)}")
                    draft_content = self._generate_fallback_content(research_content, content_type, tone)
            else:
                draft_content = self._generate_fallback_content(research_content, content_type, tone)
            
            optimized_content = await self.content_optimizer.optimize_content(
                draft_content, 
                content_type, 
                tone
            )
            
            await self.memory_bank.store_memory(
                f"content_{content_type}",
                optimized_content,
                metadata={"content_type": content_type, "tone": tone, "length": length}
            )
            
            span.set_attribute("content.generated", True)
            span.set_attribute("content.type", content_type)
            
            return {
                "status": "completed",
                "content": optimized_content,
                "content_type": content_type,
                "agent": self.agent_type.value
            }
    
    def _generate_fallback_content(self, research_content: str, content_type: str, tone: str) -> str:
        return f"""
        # {content_type.title()} on Research Topic
        
        ## Executive Summary
        This {content_type} synthesizes key research findings in a {tone} tone.
        
        ## Main Content
        Based on comprehensive research analysis, this content presents the most significant 
        insights and recommendations for stakeholders.
        
        ## Key Insights from Research
        {research_content[:500]}...
        
        ## Conclusion
        The research demonstrates important implications that warrant further consideration 
        and strategic planning.
        """