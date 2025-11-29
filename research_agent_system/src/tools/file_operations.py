import aiofiles
import asyncio
import os
import json
from typing import Dict, Any, List
from src.observability.logging import get_logger

logger = get_logger(__name__)

class FileOperationsTool:
    def __init__(self, base_path: str = "./data"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
        self.logger = get_logger(__name__)
        
    async def save_content(self, filename: str, content: str, subdirectory: str = "") -> Dict[str, Any]:
        try:
            directory = os.path.join(self.base_path, subdirectory)
            os.makedirs(directory, exist_ok=True)
            
            filepath = os.path.join(directory, filename)
            
            async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
                await f.write(content)
            
            self.logger.info(f"Content saved to {filepath}")
            return {
                "success": True,
                "filepath": filepath,
                "size": len(content)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to save content: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def load_content(self, filename: str, subdirectory: str = "") -> Dict[str, Any]:
        try:
            filepath = os.path.join(self.base_path, subdirectory, filename)
            
            async with aiofiles.open(filepath, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            return {
                "success": True,
                "content": content,
                "size": len(content)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to load content: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def save_json(self, filename: str, data: Dict[str, Any], subdirectory: str = "") -> Dict[str, Any]:
        try:
            directory = os.path.join(self.base_path, subdirectory)
            os.makedirs(directory, exist_ok=True)
            
            filepath = os.path.join(directory, filename)
            
            async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(data, indent=2))
            
            self.logger.info(f"JSON data saved to {filepath}")
            return {
                "success": True,
                "filepath": filepath,
                "size": len(json.dumps(data))
            }
            
        except Exception as e:
            self.logger.error(f"Failed to save JSON: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def load_json(self, filename: str, subdirectory: str = "") -> Dict[str, Any]:
        try:
            filepath = os.path.join(self.base_path, subdirectory, filename)
            
            async with aiofiles.open(filepath, 'r', encoding='utf-8') as f:
                content = await f.read()
                data = json.loads(content)
            
            return {
                "success": True,
                "data": data
            }
            
        except Exception as e:
            self.logger.error(f"Failed to load JSON: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def list_files(self, subdirectory: str = "") -> List[str]:
        try:
            directory = os.path.join(self.base_path, subdirectory)
            if not os.path.exists(directory):
                return []
            
            files = []
            for filename in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, filename)):
                    files.append(filename)
            
            return files
            
        except Exception as e:
            self.logger.error(f"Failed to list files: {str(e)}")
            return []