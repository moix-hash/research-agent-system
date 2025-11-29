import asyncio
import uvicorn
from fastapi import FastAPI
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.routes import app as fastapi_app
from src.observability.logging import get_logger
from config.settings import settings

logger = get_logger(__name__)

class ResearchAgentSystem:
    def __init__(self):
        self.app = fastapi_app
        self.logger = logger
        
    async def start(self):
        self.logger.info("Starting Research Agent System")
        
        try:
            config = uvicorn.Config(
                app=self.app,
                host="0.0.0.0",
                port=8000,
                log_level="info"
            )
            server = uvicorn.Server(config)
            
            await server.serve()
            
        except Exception as e:
            self.logger.error(f"Failed to start system: {str(e)}")
            raise
    
    async def stop(self):
        self.logger.info("Stopping Research Agent System")

async def main():
    system = ResearchAgentSystem()
    
    try:
        await system.start()
    except KeyboardInterrupt:
        await system.stop()
    except Exception as e:
        logger.error(f"System error: {str(e)}")
        await system.stop()

if __name__ == "__main__":
    asyncio.run(main())