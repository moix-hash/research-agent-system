import asyncio
import subprocess
import tempfile
import os
from typing import Dict, Any
from src.observability.logging import get_logger

logger = get_logger(__name__)

class CodeExecutorTool:
    def __init__(self):
        self.logger = get_logger(__name__)
        
    async def execute_python_code(self, code: str, timeout: int = 30) -> Dict[str, Any]:
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            result = await asyncio.wait_for(
                self._run_subprocess(temp_file),
                timeout=timeout
            )
            
            os.unlink(temp_file)
            
            return {
                "success": True,
                "output": result,
                "error": None
            }
            
        except asyncio.TimeoutError:
            return {
                "success": False,
                "output": "",
                "error": "Execution timeout"
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e)
            }
        finally:
            if os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass
    
    async def _run_subprocess(self, file_path: str) -> str:
        process = await asyncio.create_subprocess_exec(
            'python', file_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            return stdout.decode()
        else:
            return stderr.decode()
    
    async def validate_syntax(self, code: str, language: str = "python") -> Dict[str, Any]:
        if language == "python":
            try:
                compile(code, '<string>', 'exec')
                return {"valid": True, "errors": []}
            except SyntaxError as e:
                return {
                    "valid": False,
                    "errors": [{
                        "line": e.lineno,
                        "message": e.msg,
                        "offset": e.offset
                    }]
                }
        else:
            return {"valid": True, "errors": [], "note": f"Syntax validation for {language} not implemented"}