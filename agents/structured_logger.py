"""
Structured Logger for Multi-Agent System
VERSION: 2.0.0 - Integrated from v5.0 + Korean plan improvements

Provides JSON logging with:
- trace_id propagation for distributed tracing
- Structured LogEntry dataclass
- JSONL file output for log analysis
- Agent-aware logging context

Based on:
- scalable.pdf: Observability patterns for multi-agent systems
- OpenTelemetry-inspired trace propagation
"""

import json
import logging
import sys
from datetime import datetime
from typing import Optional, Dict, Any
from contextvars import ContextVar
from dataclasses import dataclass, asdict
from pathlib import Path

# Context variable for trace_id propagation across async boundaries
trace_id_var: ContextVar[Optional[str]] = ContextVar('trace_id', default=None)


@dataclass
class LogEntry:
    """Structured log entry schema for agent events"""
    timestamp: str
    trace_id: str
    event_type: str
    agent_name: Optional[str]
    level: str
    message: str
    duration_ms: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_json(self) -> str:
        """Convert to JSON string for JSONL output"""
        data = asdict(self)
        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}
        return json.dumps(data, ensure_ascii=False)


class JSONFormatter(logging.Formatter):
    """Formats log records as JSON with trace_id propagation"""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON string"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.name,
            "function": record.funcName,
            "line": record.lineno
        }

        # Add trace_id if available in context
        trace_id = trace_id_var.get()
        if trace_id:
            log_data["trace_id"] = trace_id

        # Add exception info if present
        if record.exc_info:
            log_data["exc_info"] = self.formatException(record.exc_info)

        # Add extra fields from LogRecord
        if hasattr(record, 'agent_name'):
            log_data["agent_name"] = record.agent_name
        if hasattr(record, 'duration_ms'):
            log_data["duration_ms"] = record.duration_ms
        if hasattr(record, 'event_type'):
            log_data["event_type"] = record.event_type
        if hasattr(record, 'metadata'):
            log_data["metadata"] = record.metadata

        return json.dumps(log_data, ensure_ascii=False)


def setup_structured_logger(
    name: str = "math_agents",
    level: int = logging.INFO,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Setup structured logger with JSON formatting.

    Args:
        name: Logger name
        level: Log level (default: INFO)
        log_file: Optional file path for JSONL output

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    logger.handlers = []

    # Console handler with JSON formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)

    # File handler if specified
    if log_file:
        # Create log directory if needed
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setFormatter(JSONFormatter())
        logger.addHandler(file_handler)

    logger.propagate = False
    return logger


class AgentLogger:
    """Context-aware logger for agent operations"""

    def __init__(self, logger: logging.Logger, agent_name: str):
        """
        Initialize agent logger with context.

        Args:
            logger: Base logger instance
            agent_name: Name of the agent for context
        """
        self.logger = logger
        self.agent_name = agent_name

    def _log(self, level: int, message: str, **kwargs):
        """Internal log method with agent context"""
        extra = {"agent_name": self.agent_name}
        extra.update(kwargs)
        self.logger.log(level, message, extra=extra)

    def info(self, message: str, **kwargs):
        """Log info level message"""
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs):
        """Log warning level message"""
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs):
        """Log error level message"""
        self._log(logging.ERROR, message, **kwargs)

    def debug(self, message: str, **kwargs):
        """Log debug level message"""
        self._log(logging.DEBUG, message, **kwargs)

    def agent_start(self, task_description: str, metadata: Optional[Dict] = None):
        """Log agent start event"""
        self._log(
            logging.INFO,
            f"Starting agent: {self.agent_name}",
            event_type="agent_start",
            metadata={"task": task_description, **(metadata or {})}
        )

    def agent_complete(
        self,
        duration_ms: float,
        success: bool,
        metadata: Optional[Dict] = None
    ):
        """Log agent completion event"""
        self._log(
            logging.INFO if success else logging.ERROR,
            f"Agent {'completed' if success else 'failed'}: {self.agent_name}",
            event_type="agent_complete",
            duration_ms=duration_ms,
            metadata={"success": success, **(metadata or {})}
        )

    def tool_call(
        self,
        tool_name: str,
        duration_ms: float,
        success: bool,
        metadata: Optional[Dict] = None
    ):
        """Log tool call event"""
        self._log(
            logging.INFO,
            f"Tool call: {tool_name}",
            event_type="tool_call",
            duration_ms=duration_ms,
            metadata={"tool": tool_name, "success": success, **(metadata or {})}
        )


class StructuredLogger:
    """
    Enhanced structured logger with JSONL file output.
    Provides agent-aware logging with trace_id support.
    """

    def __init__(
        self,
        log_dir: str = "/tmp/math-agent-logs",
        trace_id: Optional[str] = None
    ):
        """
        Initialize structured logger.

        Args:
            log_dir: Directory for JSONL log files
            trace_id: Optional trace ID (generates short UUID if None)
        """
        import uuid

        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.trace_id = trace_id or str(uuid.uuid4())[:8]
        self.log_file = self.log_dir / f"agent-{datetime.now().strftime('%Y%m%d')}.jsonl"

        # Set trace_id in context
        trace_id_var.set(self.trace_id)

    def _write_log(self, entry: LogEntry):
        """Write log entry to JSONL file"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(entry.to_json() + '\n')

    def agent_start(
        self,
        agent_name: str,
        task_description: str,
        metadata: Optional[Dict] = None
    ):
        """Log agent start event"""
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            trace_id=self.trace_id,
            event_type="agent_start",
            agent_name=agent_name,
            level="INFO",
            message=f"Starting agent: {agent_name}",
            metadata={"task": task_description, **(metadata or {})}
        )
        self._write_log(entry)
        print(f"[{entry.timestamp}] START {agent_name}: {task_description}")

    def agent_complete(
        self,
        agent_name: str,
        duration_ms: float,
        success: bool,
        metadata: Optional[Dict] = None
    ):
        """Log agent completion event"""
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            trace_id=self.trace_id,
            event_type="agent_complete",
            agent_name=agent_name,
            level="INFO" if success else "ERROR",
            message=f"Agent {'completed' if success else 'failed'}: {agent_name}",
            duration_ms=duration_ms,
            metadata={"success": success, **(metadata or {})}
        )
        self._write_log(entry)
        status_icon = "✅" if success else "❌"
        print(f"[{entry.timestamp}] {status_icon} {agent_name}: {duration_ms:.0f}ms")

    def tool_call(
        self,
        agent_name: str,
        tool_name: str,
        duration_ms: float,
        success: bool,
        metadata: Optional[Dict] = None
    ):
        """Log tool call event"""
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            trace_id=self.trace_id,
            event_type="tool_call",
            agent_name=agent_name,
            level="INFO",
            message=f"Tool call: {tool_name}",
            duration_ms=duration_ms,
            metadata={"tool": tool_name, "success": success, **(metadata or {})}
        )
        self._write_log(entry)

    def error(
        self,
        agent_name: str,
        error_type: str,
        error_message: str,
        metadata: Optional[Dict] = None
    ):
        """Log error event"""
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            trace_id=self.trace_id,
            event_type="error",
            agent_name=agent_name,
            level="ERROR",
            message=error_message,
            metadata={"error_type": error_type, **(metadata or {})}
        )
        self._write_log(entry)
        print(f"[{entry.timestamp}] ❌ ERROR ({agent_name}): {error_message}")

    def metric(
        self,
        metric_name: str,
        value: float,
        unit: str,
        metadata: Optional[Dict] = None
    ):
        """Log performance metric"""
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            trace_id=self.trace_id,
            event_type="metric",
            agent_name=None,
            level="INFO",
            message=f"Metric: {metric_name}",
            metadata={
                "metric_name": metric_name,
                "value": value,
                "unit": unit,
                **(metadata or {})
            }
        )
        self._write_log(entry)

    def system_event(
        self,
        event_name: str,
        message: str,
        metadata: Optional[Dict] = None
    ):
        """Log system-level event"""
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            trace_id=self.trace_id,
            event_type="system",
            agent_name=None,
            level="INFO",
            message=message,
            metadata={"event": event_name, **(metadata or {})}
        )
        self._write_log(entry)


def set_trace_id(trace_id: str):
    """Set trace_id for current async context"""
    trace_id_var.set(trace_id)


def get_trace_id() -> Optional[str]:
    """Get current trace_id from context"""
    return trace_id_var.get()


class AgentExecutionLogger:
    """Context manager for automatic agent execution logging"""

    def __init__(
        self,
        logger: StructuredLogger,
        agent_name: str,
        task_description: str
    ):
        """
        Initialize execution logger.

        Args:
            logger: StructuredLogger instance
            agent_name: Name of agent being executed
            task_description: Description of task
        """
        self.logger = logger
        self.agent_name = agent_name
        self.task_description = task_description
        self.start_time = None

    def __enter__(self):
        """Log agent start"""
        import time
        self.start_time = time.time()
        self.logger.agent_start(self.agent_name, self.task_description)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Log agent completion"""
        import time
        duration_ms = (time.time() - self.start_time) * 1000
        success = exc_type is None
        self.logger.agent_complete(self.agent_name, duration_ms, success)
        return False  # Don't suppress exceptions
