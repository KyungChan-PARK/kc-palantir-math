"""
Performance Monitor for Multi-Agent System
VERSION: 2.0.0 - Integrated from v5.0 + Korean plan improvements

Tracks agent execution metrics:
- Execution time (avg, median, p95)
- Success rate
- Token consumption (if available)
- API call count

Based on:
- scalable.pdf: Performance monitoring for multi-agent systems
- OpenTelemetry metrics patterns
"""

import time
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from statistics import mean, median
from datetime import datetime


@dataclass
class AgentMetrics:
    """Performance metrics for a single agent"""
    agent_name: str
    execution_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    total_duration_ms: float = 0.0
    token_consumption: int = 0
    api_call_count: int = 0
    duration_history: List[float] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage"""
        total = self.success_count + self.failure_count
        return (self.success_count / total * 100) if total > 0 else 0.0

    @property
    def avg_duration_ms(self) -> float:
        """Calculate average execution duration"""
        return (self.total_duration_ms / self.execution_count) if self.execution_count > 0 else 0.0

    @property
    def median_duration_ms(self) -> float:
        """Calculate median execution duration"""
        return median(self.duration_history) if self.duration_history else 0.0

    @property
    def p95_duration_ms(self) -> float:
        """Calculate 95th percentile execution duration"""
        if not self.duration_history:
            return 0.0
        sorted_durations = sorted(self.duration_history)
        idx = int(len(sorted_durations) * 0.95)
        return sorted_durations[min(idx, len(sorted_durations) - 1)]

    @property
    def p99_duration_ms(self) -> float:
        """Calculate 99th percentile execution duration"""
        if not self.duration_history:
            return 0.0
        sorted_durations = sorted(self.duration_history)
        idx = int(len(sorted_durations) * 0.99)
        return sorted_durations[min(idx, len(sorted_durations) - 1)]

    def to_dict(self) -> Dict:
        """Convert metrics to dictionary for serialization"""
        return {
            "agent_name": self.agent_name,
            "execution_count": self.execution_count,
            "success_rate": f"{self.success_rate:.1f}%",
            "avg_duration_ms": f"{self.avg_duration_ms:.0f}",
            "median_duration_ms": f"{self.median_duration_ms:.0f}",
            "p95_duration_ms": f"{self.p95_duration_ms:.0f}",
            "p99_duration_ms": f"{self.p99_duration_ms:.0f}",
            "total_duration_ms": f"{self.total_duration_ms:.0f}",
            "token_consumption": self.token_consumption,
            "api_call_count": self.api_call_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count
        }


class PerformanceMonitor:
    """
    Monitors and aggregates performance metrics for all agents.
    Tracks execution time, success rate, token usage, API calls, etc.
    """

    def __init__(self):
        """Initialize performance monitor"""
        self.metrics: Dict[str, AgentMetrics] = {}
        self.session_start = time.time()

    def record_execution(
        self,
        agent_name: str,
        duration_ms: float,
        success: bool,
        token_count: int = 0,
        api_calls: int = 0
    ):
        """
        Record metrics for a single agent execution.

        Args:
            agent_name: Name of the agent
            duration_ms: Execution duration in milliseconds
            success: Whether execution succeeded
            token_count: Number of tokens consumed (optional)
            api_calls: Number of API calls made (optional)
        """
        if agent_name not in self.metrics:
            self.metrics[agent_name] = AgentMetrics(agent_name=agent_name)

        metrics = self.metrics[agent_name]
        metrics.execution_count += 1
        metrics.total_duration_ms += duration_ms
        metrics.duration_history.append(duration_ms)

        if success:
            metrics.success_count += 1
        else:
            metrics.failure_count += 1

        metrics.token_consumption += token_count
        metrics.api_call_count += api_calls

    def get_metrics(self, agent_name: str) -> Optional[AgentMetrics]:
        """
        Get metrics for specific agent.

        Args:
            agent_name: Name of agent

        Returns:
            AgentMetrics instance or None if agent not found
        """
        return self.metrics.get(agent_name)

    def get_all_metrics(self) -> Dict[str, AgentMetrics]:
        """
        Get metrics for all agents.

        Returns:
            Dictionary mapping agent names to their metrics
        """
        return self.metrics

    def print_summary(self):
        """Print a summary table of performance metrics for all agents."""
        print("\n" + "=" * 110)
        print("Performance Monitoring Summary")
        print("=" * 110)

        session_duration = time.time() - self.session_start
        print(f"Session duration: {session_duration:.0f}s\n")

        # Table header
        header = (
            f"{'Agent':<25} {'Exec':<6} {'Success':<10} "
            f"{'Avg(ms)':<9} {'Med(ms)':<9} {'P95(ms)':<9} "
            f"{'Tokens':<8} {'API':<5}"
        )
        print(header)
        print("-" * 110)

        # Metrics rows
        for agent_name in sorted(self.metrics.keys()):
            metrics = self.metrics[agent_name]
            row = (
                f"{agent_name:<25} "
                f"{metrics.execution_count:<6} "
                f"{metrics.success_rate:>6.1f}%   "
                f"{metrics.avg_duration_ms:>8.0f} "
                f"{metrics.median_duration_ms:>8.0f} "
                f"{metrics.p95_duration_ms:>8.0f} "
                f"{metrics.token_consumption:>8} "
                f"{metrics.api_call_count:>5}"
            )
            print(row)

        print("=" * 110 + "\n")

    def to_dict(self) -> Dict:
        """
        Export metrics as dictionary for serialization.

        Returns:
            Dictionary with session info and agent metrics
        """
        return {
            "session_start": datetime.fromtimestamp(self.session_start).isoformat(),
            "session_duration_s": time.time() - self.session_start,
            "agents": {
                name: metrics.to_dict()
                for name, metrics in self.metrics.items()
            }
        }

    def save_to_memory_keeper(self, memory_save_func: Callable):
        """
        Persist all metrics to memory-keeper storage.

        Args:
            memory_save_func: Function to call memory-keeper save
                             Signature: (key, value, category, priority)
        """
        state = {
            "session_start": datetime.fromtimestamp(self.session_start).isoformat(),
            "session_duration_s": time.time() - self.session_start,
            "agent_metrics": {
                name: metrics.to_dict()
                for name, metrics in self.metrics.items()
            },
            "timestamp": datetime.now().isoformat()
        }

        try:
            memory_save_func(
                key="performance-metrics",
                value=json.dumps(state, indent=2),
                category="agent-performance",
                priority="high"
            )
        except Exception as e:
            import logging
            logging.error(f"Failed to save performance metrics: {e}")

    def detect_performance_regression(
        self,
        agent_name: str,
        baseline_avg_ms: float,
        threshold_percent: float = 20.0
    ) -> bool:
        """
        Check if average duration exceeds baseline by more than threshold%.

        Args:
            agent_name: Name of agent to check
            baseline_avg_ms: Baseline average duration
            threshold_percent: Threshold percentage for regression (default 20%)

        Returns:
            True if regression detected, False otherwise
        """
        metrics = self.get_metrics(agent_name)

        # Not enough data to determine regression
        if not metrics or metrics.execution_count < 5:
            return False

        # Check if average exceeds baseline + threshold
        threshold_ms = baseline_avg_ms * (1 + threshold_percent / 100)
        return metrics.avg_duration_ms > threshold_ms

    def get_slowest_agents(self, limit: int = 5) -> List[tuple]:
        """
        Get top N slowest agents by average duration.

        Args:
            limit: Number of agents to return

        Returns:
            List of (agent_name, avg_duration_ms) tuples
        """
        agents = [
            (name, metrics.avg_duration_ms)
            for name, metrics in self.metrics.items()
            if metrics.execution_count > 0
        ]
        agents.sort(key=lambda x: x[1], reverse=True)
        return agents[:limit]

    def get_most_reliable_agents(self, limit: int = 5) -> List[tuple]:
        """
        Get top N most reliable agents by success rate.

        Args:
            limit: Number of agents to return

        Returns:
            List of (agent_name, success_rate) tuples
        """
        agents = [
            (name, metrics.success_rate)
            for name, metrics in self.metrics.items()
            if metrics.execution_count > 0
        ]
        agents.sort(key=lambda x: x[1], reverse=True)
        return agents[:limit]

    def reset_metrics(self, agent_name: Optional[str] = None):
        """
        Reset metrics for specific agent or all agents.

        Args:
            agent_name: Name of agent to reset (None = reset all)
        """
        if agent_name:
            if agent_name in self.metrics:
                del self.metrics[agent_name]
        else:
            self.metrics.clear()
            self.session_start = time.time()


class PerformanceTimer:
    """Context manager for timing agent operations"""

    def __init__(self, monitor: PerformanceMonitor, agent_name: str):
        """
        Initialize performance timer.

        Args:
            monitor: PerformanceMonitor instance
            agent_name: Name of agent being timed
        """
        self.monitor = monitor
        self.agent_name = agent_name
        self.start_time = None
        self.success = False

    def __enter__(self):
        """Start timer"""
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop timer and record metrics"""
        duration_ms = (time.time() - self.start_time) * 1000
        success = exc_type is None
        self.monitor.record_execution(
            agent_name=self.agent_name,
            duration_ms=duration_ms,
            success=success
        )
        return False  # Don't suppress exceptions

    def mark_success(self):
        """Explicitly mark operation as successful"""
        self.success = True
