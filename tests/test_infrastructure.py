"""
Unit Tests for Infrastructure Modules
VERSION: 1.0.0

Tests all 4 infrastructure modules:
- error_handler.py
- structured_logger.py
- performance_monitor.py
- context_manager.py
"""

import pytest
import asyncio
import json
import time
import tempfile
from pathlib import Path

# Import infrastructure modules
from agents.error_handler import (
    ErrorTracker,
    RetryConfig,
    resilient_task,
    human_escalation_handler
)
from agents.structured_logger import (
    StructuredLogger,
    setup_structured_logger,
    JSONFormatter,
    set_trace_id,
    get_trace_id,
    AgentLogger,
    LogEntry
)
from agents.performance_monitor import (
    PerformanceMonitor,
    AgentMetrics,
    PerformanceTimer
)
from agents.context_manager import (
    ContextManager,
    ContextCategory
)


# ============================================================================
# ERROR HANDLER TESTS
# ============================================================================

def test_error_tracker_record_error():
    """Test error recording and counting"""
    tracker = ErrorTracker(max_retries=3)

    # Record 3 errors for same agent-task
    for i in range(3):
        count = tracker.record_error(
            agent_name="test-agent",
            task_id="task-1",
            error=Exception("Test error"),
            context={"attempt": i + 1}
        )
        assert count == i + 1

    # Check if should escalate
    assert tracker.should_escalate("test-agent", "task-1") is True
    assert len(tracker.error_logs) == 3


def test_error_tracker_reset():
    """Test error counter reset after success"""
    tracker = ErrorTracker(max_retries=3)

    # Record error
    tracker.record_error(
        agent_name="test-agent",
        task_id="task-1",
        error=Exception("Error"),
        context={}
    )

    # Reset counter
    tracker.reset_counter("test-agent", "task-1")

    # Should not escalate now
    assert tracker.should_escalate("test-agent", "task-1") is False


def test_error_tracker_summary():
    """Test error summary generation"""
    tracker = ErrorTracker()

    # Record errors from different agents
    tracker.record_error("agent1", "task1", Exception("E1"), {})
    tracker.record_error("agent1", "task2", Exception("E2"), {})
    tracker.record_error("agent2", "task1", TimeoutError("E3"), {})

    summary = tracker.get_error_summary()

    assert summary["total_errors"] == 3
    assert summary["by_agent"]["agent1"] == 2
    assert summary["by_agent"]["agent2"] == 1
    assert summary["by_type"]["Exception"] == 2
    assert summary["by_type"]["TimeoutError"] == 1


@pytest.mark.asyncio
async def test_resilient_task_success():
    """Test resilient task decorator - success case"""
    call_count = [0]

    @resilient_task(RetryConfig(max_retries=3, initial_delay=0.1))
    async def test_func():
        call_count[0] += 1
        return "success"

    result = await test_func()

    assert result == "success"
    assert call_count[0] == 1


@pytest.mark.asyncio
async def test_resilient_task_retry_then_success():
    """Test resilient task decorator - retry then succeed"""
    call_count = [0]

    @resilient_task(RetryConfig(max_retries=3, initial_delay=0.1))
    async def test_func():
        call_count[0] += 1
        if call_count[0] < 3:
            raise Exception("timeout error")
        return "success"

    result = await test_func()

    assert result == "success"
    assert call_count[0] == 3


@pytest.mark.asyncio
async def test_resilient_task_max_retries():
    """Test resilient task decorator - exhaust retries"""
    call_count = [0]

    @resilient_task(RetryConfig(max_retries=3, initial_delay=0.1))
    async def test_func():
        call_count[0] += 1
        raise Exception("timeout error")

    with pytest.raises(Exception):
        await test_func()

    assert call_count[0] == 3


def test_retry_config_delay_calculation():
    """Test exponential backoff delay calculation"""
    config = RetryConfig(initial_delay=1.0, backoff_factor=2.0, max_delay=10.0)

    assert config.get_delay(1) == 1.0  # 2^0 * 1 = 1
    assert config.get_delay(2) == 2.0  # 2^1 * 1 = 2
    assert config.get_delay(3) == 4.0  # 2^2 * 1 = 4
    assert config.get_delay(4) == 8.0  # 2^3 * 1 = 8
    assert config.get_delay(5) == 10.0  # capped at max_delay


# ============================================================================
# STRUCTURED LOGGER TESTS
# ============================================================================

def test_log_entry_serialization():
    """Test LogEntry to JSON serialization"""
    entry = LogEntry(
        timestamp="2025-10-13T12:00:00",
        trace_id="abc123",
        event_type="test",
        agent_name="test-agent",
        level="INFO",
        message="Test message",
        duration_ms=100.0,
        metadata={"key": "value"}
    )

    json_str = entry.to_json()
    data = json.loads(json_str)

    assert data["timestamp"] == "2025-10-13T12:00:00"
    assert data["trace_id"] == "abc123"
    assert data["message"] == "Test message"
    assert data["duration_ms"] == 100.0


def test_trace_id_propagation():
    """Test trace_id context variable propagation"""
    trace_id = "test-trace-456"
    set_trace_id(trace_id)

    assert get_trace_id() == trace_id


def test_json_formatter():
    """Test JSON log formatter"""
    import logging

    formatter = JSONFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=42,
        msg="Test log message",
        args=(),
        exc_info=None
    )

    # Set trace_id
    set_trace_id("test-123")

    output = formatter.format(record)
    data = json.loads(output)

    assert "timestamp" in data
    assert data["level"] == "INFO"
    assert data["message"] == "Test log message"
    assert data["trace_id"] == "test-123"


def test_structured_logger_file_output():
    """Test structured logger JSONL file output"""
    with tempfile.TemporaryDirectory() as tmpdir:
        logger = StructuredLogger(log_dir=tmpdir, trace_id="test-trace")

        logger.agent_start("test-agent", "Test task", {"key": "value"})
        logger.agent_complete("test-agent", 100.0, True, {"result": "ok"})

        # Check log file exists
        log_files = list(Path(tmpdir).glob("*.jsonl"))
        assert len(log_files) == 1

        # Read and verify log entries
        with open(log_files[0], 'r') as f:
            lines = f.readlines()
            assert len(lines) == 2

            # Parse first entry (agent_start)
            entry1 = json.loads(lines[0])
            assert entry1["event_type"] == "agent_start"
            assert entry1["agent_name"] == "test-agent"

            # Parse second entry (agent_complete)
            entry2 = json.loads(lines[1])
            assert entry2["event_type"] == "agent_complete"
            assert entry2["duration_ms"] == 100.0


def test_agent_logger():
    """Test AgentLogger context-aware logging"""
    import logging

    logger = logging.getLogger("test_logger")
    agent_logger = AgentLogger(logger, "test-agent")

    # Should not raise errors
    agent_logger.info("Info message")
    agent_logger.warning("Warning message")
    agent_logger.error("Error message")


# ============================================================================
# PERFORMANCE MONITOR TESTS
# ============================================================================

def test_agent_metrics_properties():
    """Test AgentMetrics calculated properties"""
    metrics = AgentMetrics(agent_name="test-agent")

    # Record executions
    metrics.execution_count = 10
    metrics.success_count = 8
    metrics.failure_count = 2
    metrics.total_duration_ms = 1000.0
    metrics.duration_history = [50, 100, 150, 200, 250]

    assert metrics.success_rate == 80.0
    assert metrics.avg_duration_ms == 100.0
    assert metrics.median_duration_ms == 150.0
    assert metrics.p95_duration_ms == 250.0


def test_performance_monitor_record_execution():
    """Test recording agent execution metrics"""
    monitor = PerformanceMonitor()

    # Record successful executions
    monitor.record_execution("agent1", 100.0, True, token_count=50, api_calls=2)
    monitor.record_execution("agent1", 150.0, True, token_count=75, api_calls=3)
    monitor.record_execution("agent1", 200.0, False, token_count=25, api_calls=1)

    metrics = monitor.get_metrics("agent1")

    assert metrics.execution_count == 3
    assert metrics.success_count == 2
    assert metrics.failure_count == 1
    assert metrics.token_consumption == 150
    assert metrics.api_call_count == 6
    assert metrics.success_rate == pytest.approx(66.67, rel=0.1)


def test_performance_monitor_to_dict():
    """Test performance monitor dictionary export"""
    monitor = PerformanceMonitor()

    monitor.record_execution("agent1", 100.0, True)
    monitor.record_execution("agent2", 200.0, True)

    data = monitor.to_dict()

    assert "session_duration_s" in data
    assert "agents" in data
    assert "agent1" in data["agents"]
    assert "agent2" in data["agents"]


def test_performance_monitor_regression_detection():
    """Test performance regression detection"""
    monitor = PerformanceMonitor()

    # Record 10 executions with avg ~100ms
    for _ in range(10):
        monitor.record_execution("agent1", 100.0, True)

    # No regression with 20% threshold
    assert monitor.detect_performance_regression("agent1", 100.0, 20.0) is False

    # Add slow executions to increase average
    for _ in range(10):
        monitor.record_execution("agent1", 200.0, True)

    # Should detect regression now (avg ~150ms > 120ms threshold)
    assert monitor.detect_performance_regression("agent1", 100.0, 20.0) is True


def test_performance_timer_context_manager():
    """Test PerformanceTimer context manager"""
    monitor = PerformanceMonitor()

    with PerformanceTimer(monitor, "agent1"):
        time.sleep(0.1)

    metrics = monitor.get_metrics("agent1")
    assert metrics.execution_count == 1
    assert metrics.duration_history[0] >= 100.0  # At least 100ms


# ============================================================================
# CONTEXT MANAGER TESTS
# ============================================================================

def test_context_manager_save_get():
    """Test context manager save and retrieve"""
    calls = []

    def mock_memory_tool(tool_name, **kwargs):
        calls.append((tool_name, kwargs))
        return {"items": []}

    manager = ContextManager(mock_memory_tool)

    # Save session state
    manager.save_session_state({"phase": "test", "tasks": ["task1"]})

    # Verify call was made
    assert len(calls) == 1
    assert calls[0][0] == 'mcp__memory-keeper__context_save'
    assert calls[0][1]["category"] == "session-state"
    assert calls[0][1]["priority"] == "high"


def test_context_manager_invalid_category():
    """Test that invalid category raises ValueError"""
    def mock_memory_tool(tool_name, **kwargs):
        return {"items": []}

    manager = ContextManager(mock_memory_tool)

    with pytest.raises(ValueError, match="Invalid category"):
        manager.save(
            key="test",
            value="data",
            category="invalid-category"
        )


def test_context_manager_category_definitions():
    """Test that all category definitions are valid"""
    assert "session-state" in ContextManager.CATEGORIES
    assert "errors" in ContextManager.CATEGORIES
    assert "decisions" in ContextManager.CATEGORIES

    # Check indefinite retention categories
    decisions_cat = ContextManager.CATEGORIES["decisions"]
    assert decisions_cat.retention_days == -1
    assert decisions_cat.max_items == -1


def test_context_manager_save_decision():
    """Test saving architectural decision"""
    calls = []

    def mock_memory_tool(tool_name, **kwargs):
        calls.append((tool_name, kwargs))
        return {"items": []}

    manager = ContextManager(mock_memory_tool)

    manager.save_decision(
        "Use SQLite",
        {"rationale": "Lightweight and embedded", "alternatives": ["PostgreSQL"]}
    )

    assert len(calls) == 1
    assert calls[0][1]["category"] == "decisions"
    assert calls[0][1]["priority"] == "high"


def test_context_manager_save_error():
    """Test saving error information"""
    calls = []

    def mock_memory_tool(tool_name, **kwargs):
        calls.append((tool_name, kwargs))
        return {"items": []}

    manager = ContextManager(mock_memory_tool)

    manager.save_error(
        agent_name="agent1",
        error_type="TimeoutError",
        error_message="Connection timeout",
        context={"url": "http://example.com"}
    )

    assert len(calls) == 1
    assert calls[0][1]["category"] == "errors"
    assert calls[0][1]["priority"] == "high"


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

def test_infrastructure_integration():
    """Verify all infrastructure modules are importable and usable together"""
    # Create all infrastructure components
    tracker = ErrorTracker()
    logger = StructuredLogger(log_dir="/tmp/test-logs")
    monitor = PerformanceMonitor()

    def mock_memory_tool(tool_name, **kwargs):
        return {"items": []}

    manager = ContextManager(mock_memory_tool)

    # Verify they work together
    assert tracker is not None
    assert logger is not None
    assert monitor is not None
    assert manager is not None

    # Record a complete workflow
    set_trace_id("integration-test")
    logger.agent_start("test-agent", "Integration test")
    monitor.record_execution("test-agent", 100.0, True)
    tracker.record_error("test-agent", "task1", Exception("Test"), {})
    manager.save_session_state({"test": "passed"})

    print("✅ All infrastructure modules integrated successfully")


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    import sys

    # Run with pytest
    exit_code = pytest.main([__file__, "-v", "--tb=short"])

    if exit_code == 0:
        print("\n" + "=" * 80)
        print("✅ ALL INFRASTRUCTURE TESTS PASSED")
        print("=" * 80)
    else:
        print("\n" + "=" * 80)
        print("❌ SOME TESTS FAILED")
        print("=" * 80)

    sys.exit(exit_code)
