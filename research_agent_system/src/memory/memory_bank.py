import asyncio
from typing import Dict, Any, List, Optional
import redis.asyncio as redis
import json
from src.observability.logging import get_logger
from config.settings import settings

logger = get_logger(__name__)

class MemoryBank:
    def __init__(self, redis_url: str = None):
        self.redis_url = redis_url or settings.redis_url
        self.redis_client = None
        self.logger = get_logger(__name__)
        self.fallback_storage: Dict[str, Any] = {}
        
    async def initialize(self):
        if not self.redis_client:
            try:
                self.redis_client = redis.from_url(
                    self.redis_url, 
                    encoding="utf-8", 
                    decode_responses=True
                )
                await self.redis_client.ping()
                self.logger.info("MemoryBank initialized with Redis")
            except Exception as e:
                self.logger.warning(f"Redis connection failed, using fallback storage: {str(e)}")
                self.redis_client = None
    
    async def store_memory(self, key: str, data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None):
        await self.initialize()
        
        memory_data = {
            "data": data,
            "metadata": metadata or {},
            "timestamp": asyncio.get_event_loop().time()
        }
        
        try:
            if self.redis_client:
                await self.redis_client.setex(
                    f"memory:{key}", 
                    3600,  # 1 hour TTL
                    json.dumps(memory_data)
                )
            else:
                self.fallback_storage[f"memory:{key}"] = memory_data
                
            self.logger.debug(f"Stored memory for key: {key}")
        except Exception as e:
            self.logger.error(f"Failed to store memory: {str(e)}")
    
    async def retrieve_memory(self, key: str) -> Optional[Dict[str, Any]]:
        await self.initialize()
        
        try:
            if self.redis_client:
                data = await self.redis_client.get(f"memory:{key}")
                if data:
                    return json.loads(data)
            else:
                return self.fallback_storage.get(f"memory:{key}")
                
        except Exception as e:
            self.logger.error(f"Failed to retrieve memory: {str(e)}")
        
        return None
    
    async def search_memories(self, pattern: str) -> List[Dict[str, Any]]:
        await self.initialize()
        
        try:
            if self.redis_client:
                keys = await self.redis_client.keys(f"memory:*{pattern}*")
                memories = []
                
                for key in keys:
                    data = await self.redis_client.get(key)
                    if data:
                        memories.append(json.loads(data))
                
                self.logger.debug(f"Found {len(memories)} memories for pattern: {pattern}")
                return memories
            else:
                memories = []
                for key, value in self.fallback_storage.items():
                    if pattern in key:
                        memories.append(value)
                return memories
                
        except Exception as e:
            self.logger.error(f"Failed to search memories: {str(e)}")
            return []
    
    async def clear_old_memories(self, older_than_seconds: int = 3600):
        await self.initialize()
        
        if self.redis_client:
            try:
                # Redis handles TTL automatically
                self.logger.info("Redis TTL handles memory cleanup automatically")
            except Exception as e:
                self.logger.error(f"Failed to clear old memories: {str(e)}")
        else:
            # For fallback storage, we'd need to implement manual cleanup
            current_time = asyncio.get_event_loop().time()
            keys_to_remove = [
                key for key, value in self.fallback_storage.items()
                if current_time - value.get('timestamp', 0) > older_than_seconds
            ]
            for key in keys_to_remove:
                del self.fallback_storage[key]
    
    async def get_memory_stats(self) -> Dict[str, Any]:
        await self.initialize()
        
        if self.redis_client:
            try:
                keys = await self.redis_client.keys("memory:*")
                return {
                    "total_memories": len(keys),
                    "storage_backend": "redis",
                    "status": "connected"
                }
            except Exception as e:
                return {
                    "total_memories": 0,
                    "storage_backend": "redis",
                    "status": "error",
                    "error": str(e)
                }
        else:
            return {
                "total_memories": len(self.fallback_storage),
                "storage_backend": "fallback",
                "status": "active"
            }