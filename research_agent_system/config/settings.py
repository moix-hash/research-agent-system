from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    gemini_api_key: Optional[str] = None
    redis_url: str = "redis://localhost:6379"
    mongo_url: str = "mongodb://localhost:27017"
    otlp_endpoint: Optional[str] = None
    log_level: str = "INFO"
    database_name: str = "agent_system"
    
    class Config:
        env_file = ".env"

settings = Settings()