"""
Infrastructure - System Support Services

VERSION: 3.1.0 - Consistent Naming Convention
All infrastructure modules follow *_service.py pattern.

Provides core system infrastructure for logging, monitoring, error handling,
context management, and agent registry.
"""

from .error_service import ErrorTracker, resilient_task, RetryConfig, human_escalation_handler
from .logging_service import StructuredLogger, setup_structured_logger, AgentLogger, set_trace_id, get_trace_id
from .monitoring_service import PerformanceMonitor, AgentMetrics, PerformanceTimer
from .context_service import ContextManager
from .registry_service import AgentRegistry

__all__ = [
    # Error Handling (error_service.py)
    "ErrorTracker",
    "resilient_task",
    "RetryConfig",
    "human_escalation_handler",
    # Logging (logging_service.py)
    "StructuredLogger",
    "setup_structured_logger",
    "AgentLogger",
    "set_trace_id",
    "get_trace_id",
    # Monitoring (monitoring_service.py)
    "PerformanceMonitor",
    "AgentMetrics",
    "PerformanceTimer",
    # Context & Registry
    "ContextManager",      # context_service.py
    "AgentRegistry",       # registry_service.py
]
