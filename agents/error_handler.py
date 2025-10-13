"""
Error Handler for Claude Agent SDK
VERSION: 2.0.0 - Integrated from v5.0 + Korean plan improvements

Provides resilient agent execution with:
- Automatic retry with exponential backoff
- Error tracking and statistics
- Human escalation after max retries
- Memory-keeper integration for error persistence

Based on:
- scalable.pdf: Resilience patterns for multi-agent systems
- Official Anthropic SDK error handling best practices
"""

import asyncio
import logging
import time
from functools import wraps
from typing import Callable, Any, Dict, Optional, List
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ErrorRecord:
    """Individual error occurrence"""
    agent_name: str
    task_id: str
    error_type: str
    error_message: str
    timestamp: str
    retry_count: int
    context_snapshot: Dict

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            "agent": self.agent_name,
            "task": self.task_id,
            "error_type": self.error_type,
            "message": self.error_message,
            "timestamp": self.timestamp,
            "retry_count": self.retry_count,
            "context": self.context_snapshot
        }


@dataclass
class RetryConfig:
    """Configuration for retry behavior"""
    max_retries: int = 3
    initial_delay: float = 1.0
    backoff_factor: float = 2.0
    max_delay: float = 60.0

    def get_delay(self, retry_count: int) -> float:
        """Calculate exponential backoff delay: base * 2^(n-1)"""
        delay = self.initial_delay * (self.backoff_factor ** (retry_count - 1))
        return min(delay, self.max_delay)


class ErrorTracker:
    """Tracks errors per agent-task combination with escalation logic"""

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.error_history: Dict[str, int] = {}  # key -> retry count
        self.error_logs: List[ErrorRecord] = []

    def get_error_key(self, agent_name: str, task_id: str) -> str:
        """Generate unique key for agent-task combination"""
        return f"{agent_name}:{task_id}"

    def record_error(
        self,
        agent_name: str,
        task_id: str,
        error: Exception,
        context: Dict
    ) -> int:
        """
        Record an error occurrence and return current retry count.

        Returns:
            Current retry count for this agent-task combination
        """
        key = self.get_error_key(agent_name, task_id)
        current_count = self.error_history.get(key, 0) + 1
        self.error_history[key] = current_count

        # Log error details
        record = ErrorRecord(
            agent_name=agent_name,
            task_id=task_id,
            error_type=type(error).__name__,
            error_message=str(error),
            timestamp=datetime.now().isoformat(),
            retry_count=current_count,
            context_snapshot=context
        )
        self.error_logs.append(record)

        logger.warning(
            f"Error recorded for {agent_name}/{task_id}: "
            f"{type(error).__name__} (attempt {current_count}/{self.max_retries})"
        )

        return current_count

    def should_escalate(self, agent_name: str, task_id: str) -> bool:
        """
        Check if error count exceeded max_retries.
        Returns True if human intervention is required.
        """
        key = self.get_error_key(agent_name, task_id)
        return self.error_history.get(key, 0) >= self.max_retries

    def reset_counter(self, agent_name: str, task_id: str):
        """Reset error counter after successful execution"""
        key = self.get_error_key(agent_name, task_id)
        if key in self.error_history:
            del self.error_history[key]
            logger.info(f"Error counter reset for {agent_name}/{task_id}")

    def get_error_logs(self, agent_name: Optional[str] = None) -> List[ErrorRecord]:
        """Retrieve error logs (optionally filtered by agent)"""
        if agent_name:
            return [log for log in self.error_logs if log.agent_name == agent_name]
        return self.error_logs

    def get_error_summary(self) -> Dict:
        """Get error statistics"""
        if not self.error_logs:
            return {"total_errors": 0}

        by_agent: Dict[str, int] = {}
        by_type: Dict[str, int] = {}

        for record in self.error_logs:
            by_agent[record.agent_name] = by_agent.get(record.agent_name, 0) + 1
            by_type[record.error_type] = by_type.get(record.error_type, 0) + 1

        return {
            "total_errors": len(self.error_logs),
            "by_agent": by_agent,
            "by_type": by_type
        }

    def save_to_memory_keeper(self, memory_save_func: Callable):
        """
        Persist error tracker state to memory-keeper.
        Stores last 100 errors for debugging.

        Args:
            memory_save_func: Function to call memory-keeper save
                             Signature: (key, value, category, priority)
        """
        import json

        state = {
            "error_history": self.error_history,
            "error_logs": [log.to_dict() for log in self.error_logs[-100:]],
            "timestamp": datetime.now().isoformat()
        }

        try:
            memory_save_func(
                key="error-tracker-state",
                value=json.dumps(state),
                category="errors",
                priority="high"
            )
            logger.info("Error tracker state saved to memory-keeper")
        except Exception as e:
            logger.error(f"Failed to save error tracker state: {e}")


class RetryPolicy:
    """Retry policy with exponential backoff and retryable error detection"""

    def __init__(self, base_delay: float = 1.0, max_delay: float = 60.0):
        self.base_delay = base_delay
        self.max_delay = max_delay

    def get_delay(self, retry_count: int) -> float:
        """Calculate exponential backoff delay: 2^(n-1) * base_delay"""
        delay = self.base_delay * (2 ** (retry_count - 1))
        return min(delay, self.max_delay)

    def should_retry(self, error: Exception) -> bool:
        """Determine if error is retryable based on type/message"""
        # Retryable exception types
        retryable_types = (
            ConnectionError,
            TimeoutError,
            asyncio.TimeoutError,
        )

        if isinstance(error, retryable_types):
            return True

        # Check error message for retryable patterns
        error_msg = str(error).lower()
        retryable_patterns = [
            "timeout",
            "connection",
            "rate limit",
            "service unavailable",
            "503",
            "429",
            "temporarily unavailable"
        ]

        return any(pattern in error_msg for pattern in retryable_patterns)


def resilient_task(config: Optional[RetryConfig] = None):
    """
    Decorator for resilient agent task execution with retry and backoff.

    Usage:
        @resilient_task(RetryConfig(max_retries=3, initial_delay=1.0))
        async def call_agent(prompt: str):
            # SDK Task call here
            pass

    Args:
        config: Retry configuration (uses defaults if None)

    Returns:
        Decorated async function with retry logic
    """
    if config is None:
        config = RetryConfig()

    retry_policy = RetryPolicy(config.initial_delay, config.max_delay)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            retries = 0

            while retries < config.max_retries:
                try:
                    result = await func(*args, **kwargs)

                    # Success - reset retry counter if tracking
                    if retries > 0:
                        logger.info(
                            f"{func.__name__} succeeded after {retries} retries"
                        )

                    return result

                except Exception as e:
                    retries += 1

                    # Check if retryable
                    if not retry_policy.should_retry(e):
                        logger.error(
                            f"{func.__name__} failed with non-retryable error: {e}",
                            exc_info=True
                        )
                        raise

                    # Check if max retries exceeded
                    if retries >= config.max_retries:
                        logger.error(
                            f"{func.__name__} failed after {retries} retries: {e}",
                            exc_info=True
                        )
                        raise

                    # Calculate backoff delay
                    delay = config.get_delay(retries)

                    logger.warning(
                        f"{func.__name__} failed (attempt {retries}/{config.max_retries}). "
                        f"Retrying in {delay:.1f}s... Error: {e}"
                    )

                    await asyncio.sleep(delay)

            raise Exception(
                f"{func.__name__} failed after {config.max_retries} retries"
            )

        return wrapper
    return decorator


def human_escalation_handler(
    agent_name: str,
    task_id: str,
    error_logs: List[ErrorRecord],
    context: Dict
):
    """
    Handle escalation to human operator when max_retries exceeded.
    Prints detailed alert for manual intervention.

    Future: Can integrate with Slack/email notification system.

    Args:
        agent_name: Name of failing agent
        task_id: Unique task identifier
        error_logs: List of error records for this task
        context: Additional context about the failure
    """
    import json

    print("\n" + "=" * 80)
    print("⚠️  HUMAN INTERVENTION REQUIRED")
    print("=" * 80)
    print(f"\nAgent: {agent_name}")
    print(f"Task: {task_id}")
    print(f"Failed attempts: {len(error_logs)}\n")
    print("Error history:")
    for i, log in enumerate(error_logs, 1):
        print(f"  {i}. [{log.timestamp}] {log.error_type}: {log.error_message}")
    print("\nContext snapshot:")
    print(json.dumps(context, indent=2))
    print("\n" + "=" * 80)
    print("Action Required: Review errors and manually resolve the issue.")
    print("Possible actions:")
    print("  1. Check agent configuration and permissions")
    print("  2. Verify MCP server connectivity")
    print("  3. Review agent prompt for logic errors")
    print("  4. Check for resource constraints (API rate limits, etc.)")
    print("=" * 80 + "\n")

    logger.critical(
        f"Human escalation triggered for {agent_name}/{task_id}",
        extra={"error_count": len(error_logs)}
    )
