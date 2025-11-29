import asyncio
from typing import Dict, Any, Optional
import time
import uuid
from src.observability.logging import get_logger

logger = get_logger(__name__)

class Session:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = time.time()
        self.updated_at = time.time()
        self.state: Dict[str, Any] = {}
        self.history: list[Dict[str, Any]] = []
        self.context: Dict[str, Any] = {}
        self.logger = get_logger(f"session.{session_id}")
    
    async def update_state(self, key: str, value: Any):
        self.state[key] = value
        self.updated_at = time.time()
        self.history.append({
            "timestamp": time.time(),
            "action": "state_update",
            "key": key,
            "value": value
        })
        self.logger.debug(f"Session state updated", key=key)
    
    async def get_state(self, key: str) -> Any:
        return self.state.get(key)
    
    async def update_context(self, context_data: Dict[str, Any]):
        self.context.update(context_data)
        self.updated_at = time.time()
    
    async def get_context(self) -> Dict[str, Any]:
        return self.context.copy()
    
    async def add_to_history(self, event: str, data: Any = None):
        self.history.append({
            "timestamp": time.time(),
            "event": event,
            "data": data
        })
        self.updated_at = time.time()
    
    async def get_full_history(self) -> list[Dict[str, Any]]:
        return self.history.copy()
    
    async def get_session_info(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "state_keys": list(self.state.keys()),
            "context_keys": list(self.context.keys()),
            "history_entries": len(self.history),
            "duration_seconds": time.time() - self.created_at
        }

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        self.logger = get_logger(__name__)
    
    async def create_session(self, session_id: str = None) -> Session:
        if not session_id:
            session_id = str(uuid.uuid4())
            
        session = Session(session_id)
        self.sessions[session_id] = session
        self.logger.info(f"Created new session: {session_id}")
        return session
    
    async def get_session(self, session_id: str) -> Optional[Session]:
        return self.sessions.get(session_id)
    
    async def end_session(self, session_id: str):
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session_info = await session.get_session_info()
            del self.sessions[session_id]
            self.logger.info(f"Ended session: {session_id}", duration=session_info["duration_seconds"])
    
    async def cleanup_old_sessions(self, max_age_seconds: int = 3600):
        current_time = time.time()
        expired_sessions = [
            session_id for session_id, session in self.sessions.items()
            if current_time - session.updated_at > max_age_seconds
        ]
        
        for session_id in expired_sessions:
            await self.end_session(session_id)
        
        if expired_sessions:
            self.logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
    
    async def get_session_stats(self) -> Dict[str, Any]:
        current_time = time.time()
        active_sessions = []
        
        for session_id, session in self.sessions.items():
            session_info = await session.get_session_info()
            active_sessions.append(session_info)
        
        return {
            "total_sessions": len(self.sessions),
            "active_sessions": active_sessions,
            "oldest_session": min([s.created_at for s in self.sessions.values()]) if self.sessions else 0,
            "newest_session": max([s.created_at for s in self.sessions.values()]) if self.sessions else 0
        }