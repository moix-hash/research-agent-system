import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.observability.metrics import metrics
from src.observability.logging import get_logger

logger = get_logger(__name__)

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Record metrics
        endpoint = request.url.path
        method = request.method
        status_code = response.status_code
        
        metrics.record_api_request(
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            duration=duration
        )
        
        # Log request
        logger.info(
            "API request completed",
            method=method,
            endpoint=endpoint,
            status_code=status_code,
            duration_ms=round(duration * 1000, 2),
            client_ip=request.client.host if request.client else "unknown"
        )
        
        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log incoming request
        logger.info(
            "Incoming request",
            method=request.method,
            endpoint=request.url.path,
            client_ip=request.client.host if request.client else "unknown",
            user_agent=request.headers.get("user-agent", "unknown")
        )
        
        response = await call_next(request)
        return response