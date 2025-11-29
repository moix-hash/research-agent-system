import asyncio
from typing import Dict, Any, List
import re
import math
from src.observability.logging import get_logger

logger = get_logger(__name__)

class DataAnalysisTool:
    def __init__(self):
        self.logger = get_logger(__name__)
        
    async def analyze_content(self, content: List[Dict[str, Any]]) -> Dict[str, Any]:
        await asyncio.sleep(0.1)
        
        total_items = len(content)
        word_count = sum(len(str(item.get('snippet', '')).split()) for item in content)
        
        analysis = {
            "total_items": total_items,
            "total_word_count": word_count,
            "average_words_per_item": word_count / max(total_items, 1),
            "content_types": self._identify_content_types(content),
            "quality_score": min(word_count / 100, 1.0)
        }
        
        return analysis
    
    def _identify_content_types(self, content: List[Dict[str, Any]]) -> List[str]:
        types = []
        for item in content:
            snippet = str(item.get('snippet', '')).lower()
            if any(word in snippet for word in ['research', 'study', 'data']):
                types.append('research')
            elif any(word in snippet for word in ['news', 'update', 'recent']):
                types.append('news')
            else:
                types.append('general')
        return list(set(types))
    
    async def calculate_readability(self, text: str) -> float:
        words = text.split()
        if not words:
            return 0.0
            
        sentences = re.split(r'[.!?]+', text)
        words_per_sentence = len(words) / max(len(sentences), 1)
        
        complex_words = [word for word in words if len(word) > 6]
        complexity_ratio = len(complex_words) / max(len(words), 1)
        
        readability = max(0, min(1, 1 - complexity_ratio + (30 / words_per_sentence) / 100))
        return round(readability, 2)

class ContentOptimizerTool:
    def __init__(self):
        self.logger = get_logger(__name__)
        
    async def optimize_content(self, content: str, content_type: str, tone: str) -> str:
        optimization_rules = self._get_optimization_rules(content_type, tone)
        
        optimized = content
        
        for rule in optimization_rules:
            optimized = await self._apply_optimization_rule(optimized, rule)
        
        self.logger.info(f"Optimized {content_type} content with {tone} tone")
        return optimized
    
    def _get_optimization_rules(self, content_type: str, tone: str) -> List[str]:
        rules = []
        
        if content_type == "article":
            rules.extend(["structure_paragraphs", "add_headings"])
        elif content_type == "report":
            rules.extend(["formal_language", "add_bullet_points"])
        
        if tone == "professional":
            rules.append("professional_tone")
        elif tone == "casual":
            rules.append("casual_tone")
            
        return rules
    
    async def _apply_optimization_rule(self, content: str, rule: str) -> str:
        await asyncio.sleep(0.05)
        
        if rule == "structure_paragraphs":
            paragraphs = content.split('\n\n')
            return '\n\n'.join([p.strip() for p in paragraphs if p.strip()])
        elif rule == "professional_tone":
            content = content.replace(" kinda ", " kind of ")
            content = content.replace(" gonna ", " going to ")
            content = content.replace(" yeah ", " yes ")
            return content
        
        return content

class SentimentAnalyzerTool:
    def __init__(self):
        self.positive_words = {"good", "excellent", "great", "amazing", "positive", "successful", "beneficial", "effective"}
        self.negative_words = {"bad", "poor", "terrible", "negative", "failed", "problem", "issue", "challenge"}
        
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        words = text.lower().split()
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        total_relevant = positive_count + negative_count
        
        if total_relevant == 0:
            sentiment = "neutral"
            score = 0.5
        else:
            score = positive_count / total_relevant
            if score > 0.6:
                sentiment = "positive"
            elif score < 0.4:
                sentiment = "negative"
            else:
                sentiment = "neutral"
        
        return {
            "sentiment": sentiment,
            "score": round(score, 2),
            "positive_words": positive_count,
            "negative_words": negative_count,
            "total_words_analyzed": len(words)
        }