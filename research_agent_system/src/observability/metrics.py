from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY
from typing import Dict, Any
import time
from src.observability.logging import get_logger

logger = get_logger(__name__)

class MetricsCollector:
    def __init__(self):
        # Agent metrics
        self.agent_requests = Counter(
            'agent_requests_total',
            'Total agent requests',
            ['agent_type', 'status']
        )
        
        self.request_duration = Histogram(
            'agent_request_duration_seconds',
            'Agent request duration',
            ['agent_type']
        )
        
        self.agent_errors = Counter(
            'agent_errors_total',
            'Total agent errors',
            ['agent_type', 'error_type']
        )
        
        # System metrics
        self.active_tasks = Gauge(
            'active_tasks_total',
            'Number of active tasks'
        )
        
        self.memory_usage = Gauge(
            'memory_entries_total',
            'Number of memory entries'
        )
        
        self.sessions_active = Gauge(
            'sessions_active_total',
            'Number of active sessions'
        )
        
        # Performance metrics
        self.response_time = Histogram(
            'api_response_time_seconds',
            'API response time',
            ['endpoint', 'method']
        )
        
        self.requests_total = Counter(
            'api_requests_total',
            'Total API requests',
            ['endpoint', 'method', 'status_code']
        )
    
    def record_agent_request(self, agent_type: str, status: str, duration: float):
        self.agent_requests.labels(agent_type=agent_type, status=status).inc()
        self.request_duration.labels(agent_type=agent_type).observe(duration)
    
    def record_agent_error(self, agent_type: str, error_type: str):
        self.agent_errors.labels(agent_type=agent_type, error_type=error_type).inc()
    
    def update_active_tasks(self, count: int):
        self.active_tasks.set(count)
    
    def update_memory_usage(self, count: int):
        self.memory_usage.set(count)
    
    def update_sessions_active(self, count: int):
        self.sessions_active.set(count)
    
    def record_api_request(self, endpoint: str, method: str, status_code: int, duration: float):
        self.requests_total.labels(endpoint=endpoint, method=method, status_code=status_code).inc()
        self.response_time.labels(endpoint=endpoint, method=method).observe(duration)
    
    def get_metrics(self) -> str:
        return generate_latest(REGISTRY).decode('utf-8')
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        return {
            "agent_requests": "Available via /metrics endpoint",
            "system_metrics": "Available via /metrics endpoint",
            "performance_metrics": "Available via /metrics endpoint"
        }

# Global metrics instance
metrics = MetricsCollector()