#!/usr/bin/env python3
"""
Research Agent System - Main Runner
A multi-agent AI system for automated research and content creation
"""

import uvicorn
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.api.routes import app
from src.observability.logging import get_logger

logger = get_logger(__name__)

def main():
    """Main entry point for the Research Agent System"""
    print(" Research Agent System Starting...")
    print("=" * 50)
    
    # Display system information
    print(" Server will be available at: http://localhost:8000")
    print(" Interactive API Documentation: http://localhost:8000/docs")
    print(" Health Check: http://localhost:8000/health")
    print(" System Metrics: http://localhost:8000/metrics")
    print(" System Status: http://localhost:8000/status")
    
    print("\n Available Endpoints:")
    print("  GET  /                 - System information")
    print("  POST /research         - Create research task")
    print("  GET  /tasks/{id}       - Get task status")
    print("  GET  /tasks            - List all tasks")
    print("  GET  /status           - System status")
    print("  GET  /health           - Health check")
    print("  GET  /metrics          - Prometheus metrics")
    print("  GET  /memory/stats     - Memory statistics")
    print("  GET  /sessions/stats   - Session statistics")
    
    print("\n Example Usage:")
    print('  curl -X POST "http://localhost:8000/research" \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d "{\\"topic\\": \\"AI in Healthcare\\", \\"content_type\\": \\"article\\"}"')
    
    print("\n Features:")
    print("   Multi-agent architecture")
    print("   Automated research and content generation")
    print("   Real-time task tracking")
    print("   Comprehensive observability")
    print("   Memory and session management")
    print("   RESTful API with full documentation")
    
    print("\n" + "=" * 50)
    print(" Starting server... (Press Ctrl+C to stop)")
    
    try:
        # Start the server - FIXED: Use the app directly instead of string
        uvicorn.run(
            app,  # Pass the app object directly
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n Server stopped by user")
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        print(f" Server failed to start: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":

    main()
