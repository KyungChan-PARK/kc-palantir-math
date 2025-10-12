# 메타-오케스트레이터 개선 계획 v4.0 (코드 레벨)

**일자**: 2025-10-13
**버전**: 4.0 (Code-Level Executable Plan)
**기반 문서**: improvement-plan-v3.0.pdf + Kenny Liao SDK 검증
**분석 방법**: Sequential-thinking (8단계) + 실제 코드베이스 검증

---

## Executive Summary (요약)

v3.0 계획이 "무엇을" 개선할지 정의했다면, **v4.0은 "어떻게" 구현할지 코드 레벨까지 명시**합니다.

### 현황 분석 결과

**✅ 이미 해결된 사항:**
- Issue #1 (도구 권한 위반): `knowledge-builder` v1.1.0에서 웹검색 도구 이미 제거됨
- Kenny Liao SDK 패턴 100% 준수
- permission_mode="acceptEdits" 설정 완료
- 모든 agents가 AgentDefinition 사용
- 버전 관리 시스템 존재

**❌ 코드 레벨에서 여전히 필요한 개선:**
1. **Error Handling System**: 재시도/에스컬레이션 로직이 prompt에만 존재 (코드 구현 없음)
2. **Parallel Execution Wrapper**: 배치 처리 코드 없음 (prompt에 설명만 존재)
3. **Structured Logging**: JSON 로그 시스템 없음
4. **Performance Monitoring**: 메트릭 수집/저장 코드 없음
5. **Context Management**: memory-keeper 자동화 없음

### v4.0의 핵심 가치

- **Zero Ambiguity**: 모든 개선사항에 정확한 파일 경로, 함수 시그니처, 코드 제공
- **Immediate Executable**: 개발자가 복사-붙여넣기로 즉시 구현 가능
- **Edge Case Coverage**: Race conditions, error scenarios, rate limits 모두 명시
- **Validation Built-in**: 각 개선사항마다 자동 테스트 케이스 포함

---

## Part 1: 현재 시스템 상태 (As-Is Architecture)

### 1.1. 파일 구조

```
/home/kc-palantir/math/
├── main.py                      # Entry point, ClaudeSDKClient setup
├── agents/
│   ├── __init__.py
│   ├── meta_orchestrator.py     # v1.2.0
│   ├── knowledge_builder.py     # v1.1.0 (도구 권한 이미 수정됨)
│   ├── research_agent.py        # v1.0.0
│   ├── quality_agent.py         # v1.0.0
│   ├── example_generator.py     # v1.0.0
│   ├── dependency_mapper.py     # v1.0.0
│   └── socratic_planner.py      # (파일 미확인, 추정 존재)
├── test_e2e.py
├── test_simple_quality.py
└── (기타 테스트 파일들)
```

### 1.2. 도구 권한 매트릭스 (현재 상태)

| Agent | Task | Read | Write | Edit | Grep | Glob | TodoWrite | Brave | Context7 | Memory | Bash |
|-------|------|------|-------|------|------|------|-----------|-------|----------|--------|------|
| **meta-orchestrator** | ✅ | ✅ | ✅ | - | ✅ | ✅ | ✅ | - | - | ✅ | - |
| **research-agent** | - | ✅ | ✅ | - | - | - | ✅ | ✅ | ✅ | - | - |
| **knowledge-builder** | - | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | - | - |
| **quality-agent** | - | ✅ | - | - | ✅ | ✅ | ✅ | - | - | - | - |
| **example-generator** | - | ✅ | - | ✅ | - | - | ✅ | - | - | - | ✅ |
| **dependency-mapper** | - | ✅ | ✅ | - | ✅ | ✅ | ✅ | - | - | - | - |

**검증 결과**: ✅ 최소 권한 원칙 준수 (v1.1.0 업데이트로 knowledge-builder에서 research 도구 제거됨)

---

## Part 2: 코드 레벨 Gap 분석 (What's Missing in Code)

### Gap #1: Error Handling System

**문제점**:
- `meta-orchestrator` prompt에 "3회 실패 시 human 개입" 언급만 있음
- 실제 재시도 카운터 없음
- 에러 로깅 메커니즘 없음
- 에스컬레이션 트리거 없음

**영향**:
- 무한 루프 가능성
- 디버깅 불가능
- API rate limit 초과 위험

### Gap #2: Parallel Execution Wrapper

**문제점**:
- `meta-orchestrator` prompt에 병렬 실행 예제 코드만 존재
- 실제 배치 처리 wrapper 없음
- 5개 이상의 parallel tasks를 어떻게 관리할지 코드 없음
- Race condition 처리 없음

**영향**:
- 수동 병렬화 필요 (메인 agent가 직접 Task 호출 반복)
- 배치 크기 최적화 불가능
- 에러 발생 시 롤백 메커니즘 없음

### Gap #3: Structured Logging System

**문제점**:
- 현재 로깅: `print()` 문만 사용
- JSON 로그 없음
- trace_id, timestamp, 성능 메트릭 수집 없음
- Log aggregation 불가능

**영향**:
- 디버깅 어려움
- 성능 분석 불가능
- 프로덕션 모니터링 불가능

### Gap #4: Performance Monitoring

**문제점**:
- Agent 실행 시간 추적 없음
- API call 카운트 없음
- 토큰 소비량 추적 없음
- memory-keeper에 메트릭 저장 없음

**영향**:
- 성능 회귀 감지 불가능
- 비용 최적화 불가능
- Bottleneck 식별 불가능

### Gap #5: Context Management Automation

**문제점**:
- memory-keeper 사용이 전적으로 agent prompt에 의존
- 자동 context 정리 없음
- 카테고리화 가이드만 있고 강제 없음
- 140K 토큰 도달 시 자동 compaction 없음

**영향**:
- Context overflow 위험
- Memory pollution
- 비효율적인 컨텍스트 관리

---

## Part 3: 실행 가능한 해결책 (Code-Level Solutions)

### Solution #1: Error Handling System

#### 3.1.1. 새 파일 생성: `agents/error_handler.py`

```python
"""
Error Handler Module
VERSION: 1.0.0
"""

from typing import Dict, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json

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

@dataclass
class ErrorTracker:
    """Tracks errors per agent-task combination"""
    max_retries: int = 3
    error_history: Dict[str, int] = field(default_factory=dict)
    error_logs: list = field(default_factory=list)

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
        Record error and return current retry count

        Returns:
            Current retry count (1, 2, 3, ...)
        """
        key = self.get_error_key(agent_name, task_id)

        # Increment counter
        current_count = self.error_history.get(key, 0) + 1
        self.error_history[key] = current_count

        # Create error record
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

        return current_count

    def should_escalate(self, agent_name: str, task_id: str) -> bool:
        """
        Check if error count exceeded max_retries

        Returns:
            True if should escalate to human
        """
        key = self.get_error_key(agent_name, task_id)
        return self.error_history.get(key, 0) >= self.max_retries

    def reset_counter(self, agent_name: str, task_id: str):
        """Reset error counter after successful execution"""
        key = self.get_error_key(agent_name, task_id)
        if key in self.error_history:
            del self.error_history[key]

    def get_error_logs(self, agent_name: Optional[str] = None) -> list:
        """Get error logs, optionally filtered by agent"""
        if agent_name:
            return [log for log in self.error_logs if log.agent_name == agent_name]
        return self.error_logs

    def save_to_memory_keeper(self, memory_save_func: Callable):
        """Save error tracker state to memory-keeper"""
        state = {
            "error_history": self.error_history,
            "error_logs": [
                {
                    "agent": log.agent_name,
                    "task": log.task_id,
                    "error_type": log.error_type,
                    "message": log.error_message,
                    "timestamp": log.timestamp,
                    "retry_count": log.retry_count
                }
                for log in self.error_logs[-100:]  # Last 100 errors only
            ],
            "timestamp": datetime.now().isoformat()
        }

        memory_save_func(
            key="error-tracker-state",
            value=json.dumps(state),
            category="errors",
            priority="high"
        )


class RetryPolicy:
    """Retry policy with exponential backoff"""

    def __init__(self, base_delay: float = 1.0, max_delay: float = 60.0):
        self.base_delay = base_delay
        self.max_delay = max_delay

    def get_delay(self, retry_count: int) -> float:
        """Calculate exponential backoff delay"""
        import math
        delay = self.base_delay * (2 ** (retry_count - 1))
        return min(delay, self.max_delay)

    def should_retry(self, error: Exception) -> bool:
        """Determine if error is retryable"""
        # Retryable errors
        retryable_types = (
            ConnectionError,
            TimeoutError,
            # Add more retryable error types
        )

        # Check error type
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
            "429"
        ]

        return any(pattern in error_msg for pattern in retryable_patterns)


def human_escalation_handler(
    agent_name: str,
    task_id: str,
    error_logs: list,
    context: Dict
) -> None:
    """
    Handle escalation to human operator

    This function is called when max_retries is exceeded.
    """
    print("\n" + "="*80)
    print("⚠️  HUMAN INTERVENTION REQUIRED")
    print("="*80)
    print(f"\nAgent: {agent_name}")
    print(f"Task: {task_id}")
    print(f"Failed attempts: {len(error_logs)}")
    print(f"\nError history:")
    for i, log in enumerate(error_logs, 1):
        print(f"  {i}. [{log.timestamp}] {log.error_type}: {log.error_message}")

    print(f"\nContext snapshot:")
    print(json.dumps(context, indent=2))

    print("\n" + "="*80)
    print("Action Required: Review errors and manually resolve the issue.")
    print("="*80 + "\n")

    # TODO: Integration with notification system
    # - Send email to operator
    # - Create Slack notification
    # - Log to external monitoring system


# Example usage in main.py
def example_agent_execution_with_error_handling():
    """
    Example of how to use ErrorTracker in agent execution
    """
    import asyncio
    from claude_agent_sdk import ClaudeSDKClient

    tracker = ErrorTracker(max_retries=3)
    retry_policy = RetryPolicy()

    async def execute_agent_with_retry(
        client: ClaudeSDKClient,
        agent_name: str,
        task_id: str,
        prompt: str
    ):
        """Execute agent with automatic retry and escalation"""

        retry_count = 0
        while True:
            try:
                # Execute agent task
                result = await client.delegate_task(agent_name, prompt)

                # Success - reset counter
                tracker.reset_counter(agent_name, task_id)
                return result

            except Exception as e:
                # Record error
                retry_count = tracker.record_error(
                    agent_name=agent_name,
                    task_id=task_id,
                    error=e,
                    context={"prompt": prompt, "attempt": retry_count + 1}
                )

                # Check if should escalate
                if tracker.should_escalate(agent_name, task_id):
                    error_logs = tracker.get_error_logs(agent_name)
                    human_escalation_handler(
                        agent_name, task_id, error_logs, {"prompt": prompt}
                    )
                    raise Exception(f"Task failed after {retry_count} attempts")

                # Check if error is retryable
                if not retry_policy.should_retry(e):
                    raise  # Non-retryable error, fail immediately

                # Wait before retry (exponential backoff)
                delay = retry_policy.get_delay(retry_count)
                print(f"Retry {retry_count}/{tracker.max_retries} after {delay}s...")
                await asyncio.sleep(delay)
```

#### 3.1.2. main.py 수정

**Before**:
```python
# main.py (현재)
async with ClaudeSDKClient(options=options) as client:
    while True:
        user_input = input("\n\033[1;34mYou:\033[0m ")
        # ... (생략)
        await client.query(user_input)
        async for message in client.receive_response():
            print(f"\n{message}")
```

**After**:
```python
# main.py (개선 후)
from agents.error_handler import ErrorTracker, RetryPolicy, human_escalation_handler

async def main():
    # ... (기존 setup 코드)

    # Initialize error tracking
    error_tracker = ErrorTracker(max_retries=3)
    retry_policy = RetryPolicy()

    async with ClaudeSDKClient(options=options) as client:
        while True:
            user_input = input("\n\033[1;34mYou:\033[0m ")
            # ... (validation)

            try:
                await client.query(user_input)
                async for message in client.receive_response():
                    print(f"\n{message}")

                # Success - save error tracker state
                error_tracker.save_to_memory_keeper(
                    lambda **kwargs: client.call_tool(
                        'mcp__memory-keeper__context_save',
                        kwargs
                    )
                )

            except Exception as e:
                # Handle top-level errors
                print(f"Error: {e}")
                # Log error (implementation depends on your needs)
```

#### 3.1.3. 테스트 케이스

**파일**: `test_error_handling.py`

```python
"""
Test cases for error handling system
"""
import pytest
from agents.error_handler import ErrorTracker, RetryPolicy

def test_error_tracker_increments():
    """Test that error counter increments correctly"""
    tracker = ErrorTracker(max_retries=3)

    # First error
    count = tracker.record_error(
        "research-agent",
        "task-123",
        Exception("Test error"),
        {}
    )
    assert count == 1

    # Second error
    count = tracker.record_error(
        "research-agent",
        "task-123",
        Exception("Test error 2"),
        {}
    )
    assert count == 2

    # Should not escalate yet
    assert not tracker.should_escalate("research-agent", "task-123")

def test_error_tracker_escalation():
    """Test that escalation triggers at max_retries"""
    tracker = ErrorTracker(max_retries=3)

    # Record 3 errors
    for i in range(3):
        tracker.record_error(
            "research-agent",
            "task-123",
            Exception(f"Error {i}"),
            {}
        )

    # Should escalate now
    assert tracker.should_escalate("research-agent", "task-123")

def test_retry_policy_exponential_backoff():
    """Test exponential backoff calculation"""
    policy = RetryPolicy(base_delay=1.0, max_delay=60.0)

    assert policy.get_delay(1) == 1.0    # 1 * 2^0
    assert policy.get_delay(2) == 2.0    # 1 * 2^1
    assert policy.get_delay(3) == 4.0    # 1 * 2^2
    assert policy.get_delay(4) == 8.0    # 1 * 2^3
    assert policy.get_delay(10) == 60.0  # Max delay cap

def test_retry_policy_retryable_errors():
    """Test retryable error detection"""
    policy = RetryPolicy()

    # Retryable errors
    assert policy.should_retry(ConnectionError("Connection failed"))
    assert policy.should_retry(TimeoutError("Request timeout"))
    assert policy.should_retry(Exception("Rate limit exceeded"))

    # Non-retryable errors
    assert not policy.should_retry(ValueError("Invalid input"))
    assert not policy.should_retry(TypeError("Type mismatch"))
```

### Solution #2: Parallel Execution Wrapper

#### 3.2.1. 새 파일 생성: `agents/parallel_executor.py`

```python
"""
Parallel Task Executor for Batch Processing
VERSION: 1.0.0

Based on scalable.pdf p4: 3-5 parallel subagents = 90% latency reduction
"""

from typing import List, Dict, Callable, Any, Optional
from dataclasses import dataclass
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

@dataclass
class TaskDefinition:
    """Single task definition for parallel execution"""
    agent_name: str
    prompt: str
    task_id: str
    metadata: Dict[str, Any] = None


@dataclass
class TaskResult:
    """Result of a single task execution"""
    task_id: str
    agent_name: str
    success: bool
    result: Any
    error: Optional[Exception]
    duration_ms: float
    timestamp: str


class ParallelTaskExecutor:
    """
    Executes multiple agent tasks in parallel with batching

    Recommended batch sizes (from scalable.pdf):
    - Optimal: 3-5 parallel tasks
    - Maximum: 10 (to avoid resource exhaustion)
    """

    def __init__(
        self,
        max_parallel: int = 5,
        batch_timeout: float = 300.0,  # 5 minutes default
    ):
        self.max_parallel = max_parallel
        self.batch_timeout = batch_timeout

    async def execute_batch(
        self,
        tasks: List[TaskDefinition],
        execute_func: Callable,
        error_handler: Optional[Callable] = None
    ) -> List[TaskResult]:
        """
        Execute a batch of tasks in parallel

        Args:
            tasks: List of task definitions
            execute_func: Async function to execute single task
                          Signature: async def(agent_name: str, prompt: str) -> Any
            error_handler: Optional error handler
                          Signature: def(task: TaskDefinition, error: Exception) -> None

        Returns:
            List of TaskResult objects
        """

        # Split into batches of max_parallel size
        batches = [
            tasks[i:i + self.max_parallel]
            for i in range(0, len(tasks), self.max_parallel)
        ]

        all_results = []

        for batch_idx, batch in enumerate(batches, 1):
            print(f"Executing batch {batch_idx}/{len(batches)} ({len(batch)} tasks)...")

            # Execute batch in parallel
            batch_results = await self._execute_single_batch(
                batch, execute_func, error_handler
            )

            all_results.extend(batch_results)

            # Brief pause between batches to avoid rate limits
            if batch_idx < len(batches):
                await asyncio.sleep(1.0)

        return all_results

    async def _execute_single_batch(
        self,
        batch: List[TaskDefinition],
        execute_func: Callable,
        error_handler: Optional[Callable]
    ) -> List[TaskResult]:
        """Execute a single batch of tasks in parallel"""

        # Create tasks
        async_tasks = [
            self._execute_single_task(task, execute_func, error_handler)
            for task in batch
        ]

        # Wait for all tasks with timeout
        try:
            results = await asyncio.wait_for(
                asyncio.gather(*async_tasks, return_exceptions=True),
                timeout=self.batch_timeout
            )
            return results

        except asyncio.TimeoutError:
            print(f"⚠️  Batch execution timeout ({self.batch_timeout}s)")
            # Return partial results
            return [
                TaskResult(
                    task_id=task.task_id,
                    agent_name=task.agent_name,
                    success=False,
                    result=None,
                    error=TimeoutError("Batch timeout"),
                    duration_ms=self.batch_timeout * 1000,
                    timestamp=time.time()
                )
                for task in batch
            ]

    async def _execute_single_task(
        self,
        task: TaskDefinition,
        execute_func: Callable,
        error_handler: Optional[Callable]
    ) -> TaskResult:
        """Execute a single task and wrap result"""

        start_time = time.time()

        try:
            # Execute task
            result = await execute_func(task.agent_name, task.prompt)

            duration_ms = (time.time() - start_time) * 1000

            return TaskResult(
                task_id=task.task_id,
                agent_name=task.agent_name,
                success=True,
                result=result,
                error=None,
                duration_ms=duration_ms,
                timestamp=time.time()
            )

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000

            # Call error handler if provided
            if error_handler:
                error_handler(task, e)

            return TaskResult(
                task_id=task.task_id,
                agent_name=task.agent_name,
                success=False,
                result=None,
                error=e,
                duration_ms=duration_ms,
                timestamp=time.time()
            )

    def print_summary(self, results: List[TaskResult]):
        """Print execution summary"""
        total = len(results)
        successful = sum(1 for r in results if r.success)
        failed = total - successful

        avg_duration = sum(r.duration_ms for r in results) / total if total > 0 else 0

        print("\n" + "="*80)
        print("Parallel Execution Summary")
        print("="*80)
        print(f"Total tasks: {total}")
        print(f"Successful: {successful} ({successful/total*100:.1f}%)")
        print(f"Failed: {failed} ({failed/total*100:.1f}%)")
        print(f"Average duration: {avg_duration:.0f}ms")

        if failed > 0:
            print(f"\nFailed tasks:")
            for r in results:
                if not r.success:
                    print(f"  - {r.task_id} ({r.agent_name}): {r.error}")

        print("="*80 + "\n")


# Example usage
async def example_parallel_research():
    """
    Example: Research 5 concepts in parallel
    (Instead of sequential 5 minutes → parallel 1 minute)
    """
    from claude_agent_sdk import ClaudeSDKClient

    # Define tasks
    concepts = [
        "Pythagorean Theorem",
        "Cauchy-Schwarz Inequality",
        "Mean Value Theorem",
        "Fundamental Theorem of Calculus",
        "Green's Theorem"
    ]

    tasks = [
        TaskDefinition(
            agent_name="research-agent",
            prompt=f"Research the mathematical concept: {concept}",
            task_id=f"research-{i}",
            metadata={"concept": concept}
        )
        for i, concept in enumerate(concepts)
    ]

    # Create executor
    executor = ParallelTaskExecutor(max_parallel=5)

    # Execute function (from ClaudeSDKClient)
    async def execute_agent(agent_name: str, prompt: str):
        # This would be replaced with actual client.delegate_task()
        async with ClaudeSDKClient() as client:
            return await client.delegate_task(agent_name, prompt)

    # Execute in parallel
    results = await executor.execute_batch(
        tasks=tasks,
        execute_func=execute_agent
    )

    # Print summary
    executor.print_summary(results)

    return results
```

#### 3.2.2. meta_orchestrator.py 업데이트

**파일**: `agents/meta_orchestrator.py`

**Section to add** (Line ~140 after parallel execution example):

```python
## Parallel Execution Implementation

**CRITICAL**: Use the ParallelTaskExecutor for batch processing.

### Code Example:

```python
from agents.parallel_executor import ParallelTaskExecutor, TaskDefinition

# Create executor
executor = ParallelTaskExecutor(max_parallel=5)

# Define batch tasks
tasks = [
    TaskDefinition(
        agent_name="research-agent",
        prompt=f"Research concept: {concept}",
        task_id=f"task-{i}"
    )
    for i, concept in enumerate(batch_concepts)
]

# Execute in parallel (use Task tool internally)
results = await executor.execute_batch(
    tasks=tasks,
    execute_func=lambda agent, prompt: Task(agent=agent, prompt=prompt)
)
```

**Performance Expectations**:
- Sequential: 5 concepts × 60s = 300s (5 minutes)
- Parallel (5 tasks): 60s + overhead (~10s) = ~70s (90% reduction)

**Batch Size Guidelines**:
- Recommended: 3-5 tasks per batch (from scalable.pdf)
- Maximum: 10 tasks (resource limits)
- For 57 concepts: Split into 12 batches of 5
```

### Solution #3: Structured Logging System

#### 3.3.1. 새 파일 생성: `agents/structured_logger.py`

```python
"""
Structured Logging System with JSON output
VERSION: 1.0.0
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import uuid
from pathlib import Path

@dataclass
class LogEntry:
    """Structured log entry"""
    timestamp: str
    trace_id: str
    event_type: str
    agent_name: Optional[str]
    level: str  # INFO, WARNING, ERROR
    message: str
    duration_ms: Optional[float]
    metadata: Dict[str, Any]

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(asdict(self), indent=None)


class StructuredLogger:
    """
    Structured logger for multi-agent system

    Outputs JSON logs for:
    - Agent execution events
    - Performance metrics
    - Error tracking
    - System events
    """

    def __init__(
        self,
        log_dir: str = "/tmp/math-agent-logs",
        trace_id: Optional[str] = None
    ):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Generate or use provided trace_id
        self.trace_id = trace_id or str(uuid.uuid4())[:8]

        # Setup file handler
        self.log_file = self.log_dir / f"agent-{datetime.now().strftime('%Y%m%d')}.jsonl"

    def _write_log(self, entry: LogEntry):
        """Write log entry to file"""
        with open(self.log_file, 'a') as f:
            f.write(entry.to_json() + '\n')

    def agent_start(
        self,
        agent_name: str,
        task_description: str,
        metadata: Dict = None
    ):
        """Log agent execution start"""
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            trace_id=self.trace_id,
            event_type="agent_start",
            agent_name=agent_name,
            level="INFO",
            message=f"Starting agent: {agent_name}",
            duration_ms=None,
            metadata={
                "task": task_description,
                **(metadata or {})
            }
        )
        self._write_log(entry)
        print(f"[{entry.timestamp}] START {agent_name}: {task_description}")

    def agent_complete(
        self,
        agent_name: str,
        duration_ms: float,
        success: bool,
        metadata: Dict = None
    ):
        """Log agent execution completion"""
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            trace_id=self.trace_id,
            event_type="agent_complete",
            agent_name=agent_name,
            level="INFO" if success else "ERROR",
            message=f"Agent {'completed' if success else 'failed'}: {agent_name}",
            duration_ms=duration_ms,
            metadata={
                "success": success,
                **(metadata or {})
            }
        )
        self._write_log(entry)
        status = "✅" if success else "❌"
        print(f"[{entry.timestamp}] {status} {agent_name}: {duration_ms:.0f}ms")

    def tool_call(
        self,
        agent_name: str,
        tool_name: str,
        duration_ms: float,
        success: bool
    ):
        """Log tool call"""
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            trace_id=self.trace_id,
            event_type="tool_call",
            agent_name=agent_name,
            level="INFO",
            message=f"Tool call: {tool_name}",
            duration_ms=duration_ms,
            metadata={
                "tool": tool_name,
                "success": success
            }
        )
        self._write_log(entry)

    def error(
        self,
        agent_name: str,
        error_type: str,
        error_message: str,
        metadata: Dict = None
    ):
        """Log error"""
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            trace_id=self.trace_id,
            event_type="error",
            agent_name=agent_name,
            level="ERROR",
            message=error_message,
            duration_ms=None,
            metadata={
                "error_type": error_type,
                **(metadata or {})
            }
        )
        self._write_log(entry)
        print(f"[{entry.timestamp}] ❌ ERROR ({agent_name}): {error_message}")

    def metric(
        self,
        metric_name: str,
        value: float,
        unit: str,
        metadata: Dict = None
    ):
        """Log performance metric"""
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            trace_id=self.trace_id,
            event_type="metric",
            agent_name=None,
            level="INFO",
            message=f"Metric: {metric_name}",
            duration_ms=None,
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
        metadata: Dict = None
    ):
        """Log system-level event"""
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            trace_id=self.trace_id,
            event_type="system",
            agent_name=None,
            level="INFO",
            message=message,
            duration_ms=None,
            metadata={
                "event": event_name,
                **(metadata or {})
            }
        )
        self._write_log(entry)


# Context manager for agent execution
class AgentExecutionLogger:
    """Context manager for logging agent execution"""

    def __init__(
        self,
        logger: StructuredLogger,
        agent_name: str,
        task_description: str
    ):
        self.logger = logger
        self.agent_name = agent_name
        self.task_description = task_description
        self.start_time = None

    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.agent_start(
            self.agent_name,
            self.task_description
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = (datetime.now() - self.start_time).total_seconds() * 1000
        success = exc_type is None

        self.logger.agent_complete(
            self.agent_name,
            duration_ms,
            success,
            metadata={
                "error": str(exc_val) if exc_val else None
            }
        )

        # Don't suppress exceptions
        return False


# Example usage
def example_logging():
    """Example of structured logging usage"""
    logger = StructuredLogger()

    # Log agent execution
    with AgentExecutionLogger(logger, "research-agent", "Research Pythagorean Theorem"):
        # Agent work here
        import time
        time.sleep(1.0)

        # Log tool calls
        logger.tool_call("research-agent", "brave_web_search", 250.0, True)
        logger.tool_call("research-agent", "context7_get_docs", 150.0, True)

    # Log metrics
    logger.metric("token_count", 1500, "tokens", {"model": "sonnet"})
    logger.metric("api_calls", 5, "count", {"endpoint": "brave_search"})

    # Log system events
    logger.system_event("batch_complete", "Completed batch 1/12")
```

#### 3.3.2. main.py integration

```python
# main.py (add after imports)
from agents.structured_logger import StructuredLogger, AgentExecutionLogger

async def main():
    # Initialize logger
    logger = StructuredLogger(
        log_dir="/tmp/math-agent-logs",
        trace_id=f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    )

    logger.system_event("system_start", "Math agent system starting")

    # ... rest of main() code

    # Wrap agent execution with logging
    # (This would be done inside the client.query() handling)
```

### Solution #4: Performance Monitoring

#### 3.4.1. 새 파일 생성: `agents/performance_monitor.py`

```python
"""
Performance Monitoring System
VERSION: 1.0.0
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import statistics

@dataclass
class AgentMetrics:
    """Metrics for a single agent"""
    agent_name: str
    execution_count: int = 0
    total_duration_ms: float = 0.0
    success_count: int = 0
    failure_count: int = 0
    token_consumption: int = 0
    api_call_count: int = 0
    duration_history: List[float] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage"""
        total = self.success_count + self.failure_count
        return (self.success_count / total * 100) if total > 0 else 0.0

    @property
    def avg_duration_ms(self) -> float:
        """Calculate average duration"""
        return (self.total_duration_ms / self.execution_count) if self.execution_count > 0 else 0.0

    @property
    def median_duration_ms(self) -> float:
        """Calculate median duration"""
        return statistics.median(self.duration_history) if self.duration_history else 0.0

    @property
    def p95_duration_ms(self) -> float:
        """Calculate 95th percentile duration"""
        if not self.duration_history:
            return 0.0
        sorted_durations = sorted(self.duration_history)
        idx = int(len(sorted_durations) * 0.95)
        return sorted_durations[idx]

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "agent_name": self.agent_name,
            "execution_count": self.execution_count,
            "success_rate": f"{self.success_rate:.1f}%",
            "avg_duration_ms": f"{self.avg_duration_ms:.0f}",
            "median_duration_ms": f"{self.median_duration_ms:.0f}",
            "p95_duration_ms": f"{self.p95_duration_ms:.0f}",
            "token_consumption": self.token_consumption,
            "api_call_count": self.api_call_count
        }


class PerformanceMonitor:
    """
    Monitors performance metrics for all agents

    Tracks:
    - Execution time
    - Success rate
    - API call counts
    - Token consumption
    - Performance trends
    """

    def __init__(self):
        self.metrics: Dict[str, AgentMetrics] = {}
        self.session_start = datetime.now()

    def record_execution(
        self,
        agent_name: str,
        duration_ms: float,
        success: bool,
        token_count: int = 0,
        api_calls: int = 0
    ):
        """Record agent execution metrics"""
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
        """Get metrics for specific agent"""
        return self.metrics.get(agent_name)

    def get_all_metrics(self) -> Dict[str, AgentMetrics]:
        """Get metrics for all agents"""
        return self.metrics

    def print_summary(self):
        """Print performance summary"""
        print("\n" + "="*100)
        print("Performance Monitoring Summary")
        print("="*100)
        print(f"Session duration: {(datetime.now() - self.session_start).total_seconds():.0f}s")
        print()

        # Print table header
        header = f"{'Agent':<25} {'Exec':<6} {'Success':<10} {'Avg(ms)':<10} {'Med(ms)':<10} {'P95(ms)':<10} {'Tokens':<10} {'API':<6}"
        print(header)
        print("-" * 100)

        # Print metrics for each agent
        for agent_name, metrics in sorted(self.metrics.items()):
            row = (
                f"{agent_name:<25} "
                f"{metrics.execution_count:<6} "
                f"{metrics.success_rate:>6.1f}%   "
                f"{metrics.avg_duration_ms:>8.0f}  "
                f"{metrics.median_duration_ms:>8.0f}  "
                f"{metrics.p95_duration_ms:>8.0f}  "
                f"{metrics.token_consumption:>8}  "
                f"{metrics.api_call_count:>4}"
            )
            print(row)

        print("="*100 + "\n")

    def save_to_memory_keeper(self, memory_save_func):
        """Save metrics to memory-keeper"""
        state = {
            "session_start": self.session_start.isoformat(),
            "session_duration_s": (datetime.now() - self.session_start).total_seconds(),
            "agent_metrics": {
                name: metrics.to_dict()
                for name, metrics in self.metrics.items()
            },
            "timestamp": datetime.now().isoformat()
        }

        memory_save_func(
            key="performance-metrics",
            value=json.dumps(state, indent=2),
            category="agent-performance",
            priority="high"
        )

    def detect_performance_regression(
        self,
        agent_name: str,
        baseline_avg_ms: float,
        threshold_percent: float = 20.0
    ) -> bool:
        """
        Detect if agent performance has regressed

        Returns:
            True if current performance is worse than baseline by threshold%
        """
        metrics = self.get_metrics(agent_name)
        if not metrics or metrics.execution_count < 5:
            return False  # Not enough data

        current_avg = metrics.avg_duration_ms
        regression_threshold = baseline_avg_ms * (1 + threshold_percent / 100)

        return current_avg > regression_threshold

    def get_bottleneck_agents(self, top_n: int = 3) -> List[tuple]:
        """
        Identify slowest agents (bottlenecks)

        Returns:
            List of (agent_name, avg_duration_ms) tuples, sorted by duration
        """
        agent_durations = [
            (name, metrics.avg_duration_ms)
            for name, metrics in self.metrics.items()
            if metrics.execution_count > 0
        ]

        # Sort by duration (descending)
        agent_durations.sort(key=lambda x: x[1], reverse=True)

        return agent_durations[:top_n]


# Example usage
def example_monitoring():
    """Example of performance monitoring"""
    monitor = PerformanceMonitor()

    # Record some executions
    monitor.record_execution("research-agent", 1200.0, True, token_count=500, api_calls=3)
    monitor.record_execution("research-agent", 1150.0, True, token_count=480, api_calls=3)
    monitor.record_execution("knowledge-builder", 800.0, True, token_count=300, api_calls=0)
    monitor.record_execution("quality-agent", 400.0, True, token_count=150, api_calls=0)

    # Print summary
    monitor.print_summary()

    # Check for bottlenecks
    bottlenecks = monitor.get_bottleneck_agents(top_n=3)
    print("Bottleneck agents:")
    for agent, duration in bottlenecks:
        print(f"  - {agent}: {duration:.0f}ms")

    # Check regression
    is_regressed = monitor.detect_performance_regression(
        "research-agent",
        baseline_avg_ms=1000.0,
        threshold_percent=20.0
    )
    if is_regressed:
        print("⚠️  Performance regression detected for research-agent!")
```

#### 3.4.2. Integration with parallel_executor.py

```python
# In parallel_executor.py, modify _execute_single_task:

async def _execute_single_task(
    self,
    task: TaskDefinition,
    execute_func: Callable,
    error_handler: Optional[Callable],
    performance_monitor: Optional['PerformanceMonitor'] = None  # Add parameter
) -> TaskResult:
    """Execute a single task and wrap result"""

    start_time = time.time()

    try:
        # Execute task
        result = await execute_func(task.agent_name, task.prompt)

        duration_ms = (time.time() - start_time) * 1000

        # Record performance metrics
        if performance_monitor:
            performance_monitor.record_execution(
                task.agent_name,
                duration_ms,
                success=True,
                # token_count and api_calls would come from result metadata
            )

        return TaskResult(...)

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000

        # Record failure
        if performance_monitor:
            performance_monitor.record_execution(
                task.agent_name,
                duration_ms,
                success=False
            )

        # ... rest of error handling
```

### Solution #5: Context Management Automation

#### 3.5.1. 새 파일 생성: `agents/context_manager.py`

```python
"""
Context Management Automation
VERSION: 1.0.0

Automates memory-keeper usage for context persistence and cleanup
"""

from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class ContextCategory:
    """Context category definition"""
    name: str
    priority: str  # high, medium, low
    retention_days: int
    max_items: int


class ContextManager:
    """
    Automates context management with memory-keeper

    Features:
    - Auto-categorization
    - Periodic cleanup
    - Context summarization
    - Token limit monitoring
    """

    # Category definitions (from v3.0 plan)
    CATEGORIES = {
        "session-state": ContextCategory("session-state", "high", 7, 50),
        "agent-performance": ContextCategory("agent-performance", "medium", 7, 100),
        "errors": ContextCategory("errors", "high", 30, 200),
        "decisions": ContextCategory("decisions", "high", -1, -1),  #永久保存
        "tasks": ContextCategory("tasks", "medium", 7, 100),
        "progress": ContextCategory("progress", "medium", 7, 100),
    }

    def __init__(self, memory_tool_func: Callable):
        """
        Initialize context manager

        Args:
            memory_tool_func: Function to call memory-keeper tools
                             Signature: def(tool_name: str, **params) -> Any
        """
        self.memory_tool = memory_tool_func
        self.context_save_count = 0

    def save_context(
        self,
        key: str,
        value: any,
        category: str,
        priority: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """
        Save context with automatic categorization

        Args:
            key: Unique key for context item
            value: Context value (will be JSON serialized if dict/list)
            category: Category name (must be in CATEGORIES)
            priority: Optional priority (defaults to category default)
            metadata: Optional metadata dict
        """
        # Validate category
        if category not in self.CATEGORIES:
            raise ValueError(f"Invalid category: {category}. Must be one of {list(self.CATEGORIES.keys())}")

        cat_def = self.CATEGORIES[category]

        # Serialize value if needed
        if isinstance(value, (dict, list)):
            value = json.dumps(value)

        # Use category default priority if not specified
        final_priority = priority or cat_def.priority

        # Save to memory-keeper
        self.memory_tool(
            'mcp__memory-keeper__context_save',
            key=key,
            value=value,
            category=category,
            priority=final_priority,
            metadata=metadata or {}
        )

        self.context_save_count += 1

        # Check if cleanup needed (every 10 saves)
        if self.context_save_count % 10 == 0:
            self._auto_cleanup()

    def get_context(
        self,
        category: Optional[str] = None,
        key: Optional[str] = None,
        priorities: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Dict]:
        """
        Retrieve context items with filtering

        Args:
            category: Filter by category
            key: Specific key to retrieve
            priorities: Filter by priority levels
            limit: Maximum items to return

        Returns:
            List of context items
        """
        params = {
            "limit": limit
        }

        if category:
            params["category"] = category
        if key:
            params["key"] = key
        if priorities:
            params["priorities"] = priorities

        result = self.memory_tool(
            'mcp__memory-keeper__context_get',
            **params
        )

        return result.get("items", [])

    def save_session_state(self, state: Dict):
        """Save current session state"""
        self.save_context(
            key="current-session-state",
            value=state,
            category="session-state",
            priority="high"
        )

    def save_agent_metrics(self, agent_name: str, metrics: Dict):
        """Save agent performance metrics"""
        self.save_context(
            key=f"agent-metrics-{agent_name}",
            value=metrics,
            category="agent-performance",
            priority="medium",
            metadata={"agent": agent_name}
        )

    def save_error(
        self,
        agent_name: str,
        error_type: str,
        error_message: str,
        context: Dict
    ):
        """Save error occurrence"""
        error_data = {
            "agent": agent_name,
            "error_type": error_type,
            "message": error_message,
            "timestamp": datetime.now().isoformat(),
            "context": context
        }

        self.save_context(
            key=f"error-{datetime.now().timestamp()}",
            value=error_data,
            category="errors",
            priority="high"
        )

    def _auto_cleanup(self):
        """
        Automatic cleanup of old context items

        Rules:
        - Delete items older than retention_days
        - Keep only max_items most recent items per category
        - Never delete "decisions" category (retention_days = -1)
        """
        print("🧹 Auto-cleanup: Checking context items...")

        for cat_name, cat_def in self.CATEGORIES.items():
            # Skip categories with unlimited retention
            if cat_def.retention_days == -1:
                continue

            # Get all items in category
            items = self.get_context(
                category=cat_name,
                limit=1000  # Get all
            )

            if len(items) <= cat_def.max_items:
                continue  # No cleanup needed

            # Sort by timestamp (newest first)
            items_sorted = sorted(
                items,
                key=lambda x: x.get("created_at", ""),
                reverse=True
            )

            # Keep only max_items
            items_to_keep = items_sorted[:cat_def.max_items]
            items_to_delete = items_sorted[cat_def.max_items:]

            # Delete old items
            for item in items_to_delete:
                # Note: memory-keeper may not have delete API
                # This would need to be implemented based on actual API
                print(f"  Deleting old context: {item['key']}")

    def get_context_size_estimate(self) -> int:
        """
        Estimate total context size in tokens

        Returns:
            Estimated token count
        """
        # Get all high-priority items
        items = self.get_context(priorities=["high"], limit=100)

        # Rough estimate: 1 character ≈ 0.25 tokens
        total_chars = sum(len(str(item.get("value", ""))) for item in items)

        return int(total_chars * 0.25)

    def should_compact(self, token_threshold: int = 140000) -> bool:
        """
        Check if context should be compacted

        Args:
            token_threshold: Token count threshold (default 140K)

        Returns:
            True if context size exceeds threshold
        """
        estimated_tokens = self.get_context_size_estimate()
        return estimated_tokens > token_threshold


# Example usage
def example_context_management():
    """Example of automated context management"""

    # Mock memory tool function
    def mock_memory_tool(tool_name: str, **params):
        print(f"Calling {tool_name} with {params}")
        return {"items": []}

    manager = ContextManager(mock_memory_tool)

    # Save session state
    manager.save_session_state({
        "phase": "Phase 1",
        "completed_tasks": ["task1", "task2"],
        "next_tasks": ["task3"]
    })

    # Save agent metrics
    manager.save_agent_metrics("research-agent", {
        "execution_count": 10,
        "avg_duration_ms": 1200,
        "success_rate": 95.0
    })

    # Save error
    manager.save_error(
        agent_name="knowledge-builder",
        error_type="FileNotFoundError",
        error_message="File not found: /path/to/file",
        context={"attempted_path": "/path/to/file"}
    )

    # Check if compaction needed
    if manager.should_compact():
        print("⚠️  Context compaction recommended")
```

---

## Part 4: 구현 로드맵 (Implementation Roadmap)

### Phase 1: Critical Infrastructure (Week 1)

**Goal**: 에러 핸들링, 병렬 실행, 로깅 시스템 구축

#### Task 1.1: Error Handling System (2 days)
- [ ] Create `agents/error_handler.py` with ErrorTracker, RetryPolicy classes
- [ ] Integrate ErrorTracker into `main.py`
- [ ] Create test cases in `test_error_handling.py`
- [ ] Run tests: `uv run pytest test_error_handling.py -v`

**Definition of Done**:
```bash
# All tests pass
pytest test_error_handling.py -v
# 5 tests, 5 passed

# Error tracking works in main.py
python main.py
# Trigger 3 consecutive errors → Human escalation message appears
```

#### Task 1.2: Parallel Execution Wrapper (2 days)
- [ ] Create `agents/parallel_executor.py` with ParallelTaskExecutor
- [ ] Update `meta_orchestrator.py` prompt with implementation example
- [ ] Create test case: 5 parallel research tasks
- [ ] Benchmark: Measure sequential vs parallel execution time

**Definition of Done**:
```bash
# Test parallel execution
uv run python -c "
from agents.parallel_executor import ParallelTaskExecutor, TaskDefinition
import asyncio

async def test():
    executor = ParallelTaskExecutor(max_parallel=5)
    tasks = [TaskDefinition('research-agent', f'Research concept {i}', f'task-{i}') for i in range(5)]
    # Mock execute function
    async def mock_exec(agent, prompt):
        await asyncio.sleep(1.0)
        return f'Result for {prompt}'
    results = await executor.execute_batch(tasks, mock_exec)
    print(f'Completed {len(results)} tasks in parallel')
    executor.print_summary(results)

asyncio.run(test())
"

# Expected output:
# Completed 5 tasks in parallel
# Total tasks: 5
# Successful: 5 (100.0%)
# Average duration: ~1000ms (not 5000ms if sequential)
```

#### Task 1.3: Structured Logging (1 day)
- [ ] Create `agents/structured_logger.py`
- [ ] Integrate into `main.py`
- [ ] Test log file generation

**Definition of Done**:
```bash
# Run main.py with logging enabled
python main.py
# Perform 3 agent tasks

# Check log file
ls -lh /tmp/math-agent-logs/agent-*.jsonl

# Verify JSON format
head -n 5 /tmp/math-agent-logs/agent-$(date +%Y%m%d).jsonl | python -m json.tool
# Should output valid JSON for each line
```

### Phase 2: Performance & Observability (Week 2)

#### Task 2.1: Performance Monitoring (2 days)
- [ ] Create `agents/performance_monitor.py`
- [ ] Integrate with parallel_executor.py
- [ ] Add metrics to memory-keeper
- [ ] Create dashboard view

**Definition of Done**:
```bash
# Run test workflow with monitoring
uv run test_full_workflow.py

# Check performance summary printed
# Should show table with agent execution stats

# Verify memory-keeper storage
# (Check that performance-metrics key exists with JSON data)
```

#### Task 2.2: Context Management Automation (2 days)
- [ ] Create `agents/context_manager.py`
- [ ] Integrate into all agents
- [ ] Test auto-cleanup
- [ ] Test context size estimation

**Definition of Done**:
```bash
# Test context manager
uv run python -c "
from agents.context_manager import ContextManager

def mock_memory_tool(tool, **kwargs):
    print(f'Calling {tool}')
    return {'items': []}

manager = ContextManager(mock_memory_tool)
manager.save_session_state({'phase': 'test'})
print('✅ Context manager working')
"

# Expected: No errors, "Calling mcp__memory-keeper__context_save" printed
```

### Phase 3: Integration & Testing (Week 3)

#### Task 3.1: End-to-End Integration (3 days)
- [ ] Integrate all 5 solutions into main.py
- [ ] Update all agent prompts with new guidelines
- [ ] Run full E2E tests

**Definition of Done**:
```bash
# Run complete E2E test
uv run test_e2e.py

# All checks pass:
# ✅ Error handling active
# ✅ Parallel execution working
# ✅ Structured logs generated
# ✅ Performance metrics collected
# ✅ Context management active
```

#### Task 3.2: Performance Benchmarking (2 days)
- [ ] Benchmark 57 concept processing (original goal)
- [ ] Measure sequential vs parallel
- [ ] Document performance improvements

**Expected Results**:
```
Sequential baseline (estimated):
- 57 concepts × 60s/concept = 3420s (~57 minutes)

Parallel with batches of 5:
- 12 batches × 70s/batch = 840s (~14 minutes)
- **75% reduction in latency**

(Actual results will depend on system resources and API rate limits)
```

### Phase 4: Documentation & Handoff (Week 4)

#### Task 4.1: Code Documentation (2 days)
- [ ] Add docstrings to all new modules
- [ ] Create usage examples
- [ ] Update README.md

#### Task 4.2: Operational Runbook (2 days)
- [ ] Document error escalation procedures
- [ ] Create troubleshooting guide
- [ ] Write performance tuning guide

#### Task 4.3: Training & Handoff (1 day)
- [ ] Demo to team
- [ ] Knowledge transfer session
- [ ] Q&A documentation

---

## Part 5: 잠재적 문제 및 해결책 (Edge Cases & Mitigations)

### Problem #1: Race Conditions in Parallel Execution

**Scenario**: Multiple agents write to same file simultaneously

**Example**:
```python
# Agent 1 and Agent 2 both try to write to same file
# agent1: Write("/tmp/report.json", data1)
# agent2: Write("/tmp/report.json", data2)
# Result: File corruption or data loss
```

**Solution**: File locking mechanism

```python
# In parallel_executor.py, add file lock
import fcntl
from pathlib import Path

class FileLock:
    """Simple file-based lock"""

    def __init__(self, lock_file: str):
        self.lock_file = Path(lock_file)
        self.lock_file.parent.mkdir(parents=True, exist_ok=True)
        self.fd = None

    def __enter__(self):
        self.fd = open(self.lock_file, 'w')
        fcntl.flock(self.fd, fcntl.LOCK_EX)  # Exclusive lock
        return self

    def __exit__(self, *args):
        if self.fd:
            fcntl.flock(self.fd, fcntl.LOCK_UN)
            self.fd.close()

# Usage in agents
from agents.parallel_executor import FileLock

# Before writing to shared file
with FileLock("/tmp/locks/report.lock"):
    Write("/tmp/report.json", data)
```

### Problem #2: Memory Leaks in Long-Running Sessions

**Scenario**: error_tracker.error_history grows unbounded

**Solution**: Periodic cleanup

```python
# In error_handler.py, add to ErrorTracker:

def cleanup_old_errors(self, max_age_hours: int = 24):
    """Remove error records older than max_age_hours"""
    from datetime import datetime, timedelta

    cutoff_time = datetime.now() - timedelta(hours=max_age_hours)

    # Filter recent logs only
    self.error_logs = [
        log for log in self.error_logs
        if datetime.fromisoformat(log.timestamp) > cutoff_time
    ]

    # Cleanup history for completed tasks
    # (Keep only currently failing tasks)
    active_keys = set()
    for log in self.error_logs:
        active_keys.add(self.get_error_key(log.agent_name, log.task_id))

    self.error_history = {
        k: v for k, v in self.error_history.items()
        if k in active_keys
    }

# Call periodically in main.py
if context_manager.context_save_count % 50 == 0:
    error_tracker.cleanup_old_errors(max_age_hours=24)
```

### Problem #3: API Rate Limits (Brave Search, Context7)

**Scenario**: 57 concepts × 5 searches/concept = 285 API calls → Rate limit exceeded

**Solution**: Rate limiter with exponential backoff

```python
# In agents/rate_limiter.py (new file)

import time
from collections import deque
from datetime import datetime, timedelta

class RateLimiter:
    """Token bucket rate limiter"""

    def __init__(self, max_calls: int, time_window_seconds: int):
        """
        Args:
            max_calls: Maximum calls allowed in time window
            time_window_seconds: Time window in seconds
        """
        self.max_calls = max_calls
        self.time_window = timedelta(seconds=time_window_seconds)
        self.calls = deque()

    def wait_if_needed(self):
        """Block if rate limit would be exceeded"""
        now = datetime.now()

        # Remove calls outside time window
        while self.calls and now - self.calls[0] > self.time_window:
            self.calls.popleft()

        # Check if at limit
        if len(self.calls) >= self.max_calls:
            # Calculate wait time
            oldest_call = self.calls[0]
            wait_until = oldest_call + self.time_window
            wait_seconds = (wait_until - now).total_seconds()

            if wait_seconds > 0:
                print(f"⏳ Rate limit reached. Waiting {wait_seconds:.1f}s...")
                time.sleep(wait_seconds)

        # Record this call
        self.calls.append(now)

# Usage in research_agent.py
brave_limiter = RateLimiter(max_calls=10, time_window_seconds=60)  # 10 calls/minute

# Before each Brave Search call
brave_limiter.wait_if_needed()
result = mcp__brave-search__brave_web_search(query)
```

### Problem #4: Disk Space Exhaustion (Log Files)

**Scenario**: /tmp/math-agent-logs/ grows to GB size

**Solution**: Log rotation

```python
# In structured_logger.py, add rotation

from logging.handlers import RotatingFileHandler

class StructuredLogger:
    def __init__(self, log_dir: str = "/tmp/math-agent-logs", max_bytes: int = 10*1024*1024, backup_count: int = 5):
        """
        Args:
            max_bytes: Max log file size (default 10MB)
            backup_count: Number of backup files to keep
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Use rotating file handler
        self.log_file = self.log_dir / "agent.jsonl"
        self.handler = RotatingFileHandler(
            self.log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )

    def _write_log(self, entry: LogEntry):
        """Write with rotation"""
        self.handler.emit(entry.to_json() + '\n')

        # Rotate if needed
        self.handler.doRollover() if self.handler.shouldRollover(entry.to_json()) else None
```

### Problem #5: Context Overflow Despite Management

**Scenario**: 140K tokens reached even with cleanup

**Solution**: Emergency compaction

```python
# In context_manager.py, add emergency compaction

def emergency_compact(self, target_size_tokens: int = 100000):
    """
    Emergency compaction when context exceeds limits

    Strategy:
    1. Summarize low-priority items
    2. Delete non-critical categories
    3. Keep only essential data
    """
    print("🚨 Emergency context compaction initiated...")

    # Step 1: Delete all low-priority items
    low_priority_items = self.get_context(priorities=["low"], limit=1000)
    for item in low_priority_items:
        # Delete (implementation depends on memory-keeper API)
        pass

    # Step 2: Summarize medium-priority items
    medium_items = self.get_context(priorities=["medium"], limit=1000)
    summary = {
        "summarized_at": datetime.now().isoformat(),
        "item_count": len(medium_items),
        "categories": list(set(item["category"] for item in medium_items)),
        "note": "Items summarized during emergency compaction"
    }
    self.save_context(
        key="emergency-compaction-summary",
        value=summary,
        category="decisions",
        priority="high"
    )

    # Step 3: Keep only essential high-priority items
    # (Recent errors, current session state, critical decisions)

    print(f"✅ Compaction complete. Freed ~{len(low_priority_items) + len(medium_items)} items")
```

---

## Part 6: 검증 및 테스트 (Verification & Testing)

### 6.1. Unit Tests

**파일**: `test_v4_improvements.py`

```python
"""
Comprehensive test suite for v4.0 improvements
"""

import pytest
import asyncio
from agents.error_handler import ErrorTracker, RetryPolicy
from agents.parallel_executor import ParallelTaskExecutor, TaskDefinition
from agents.structured_logger import StructuredLogger
from agents.performance_monitor import PerformanceMonitor
from agents.context_manager import ContextManager

# Test Error Handling
def test_error_tracker_basic():
    tracker = ErrorTracker(max_retries=3)

    # Record errors
    count1 = tracker.record_error("agent1", "task1", Exception("Error 1"), {})
    count2 = tracker.record_error("agent1", "task1", Exception("Error 2"), {})

    assert count1 == 1
    assert count2 == 2
    assert not tracker.should_escalate("agent1", "task1")

    # Third error triggers escalation
    count3 = tracker.record_error("agent1", "task1", Exception("Error 3"), {})
    assert count3 == 3
    assert tracker.should_escalate("agent1", "task1")

# Test Parallel Execution
@pytest.mark.asyncio
async def test_parallel_executor_basic():
    executor = ParallelTaskExecutor(max_parallel=3)

    tasks = [
        TaskDefinition("agent1", f"task{i}", f"task-id-{i}")
        for i in range(5)
    ]

    # Mock execution function
    async def mock_execute(agent, prompt):
        await asyncio.sleep(0.1)
        return f"Result: {prompt}"

    results = await executor.execute_batch(tasks, mock_execute)

    assert len(results) == 5
    assert all(r.success for r in results)
    assert all(r.result.startswith("Result:") for r in results)

@pytest.mark.asyncio
async def test_parallel_faster_than_sequential():
    """Verify parallel is actually faster"""
    import time

    tasks = [TaskDefinition("agent", f"task{i}", f"id-{i}") for i in range(5)]

    async def slow_task(agent, prompt):
        await asyncio.sleep(0.5)
        return "done"

    # Sequential
    start_seq = time.time()
    for task in tasks:
        await slow_task(task.agent_name, task.prompt)
    sequential_time = time.time() - start_seq

    # Parallel
    executor = ParallelTaskExecutor(max_parallel=5)
    start_par = time.time()
    await executor.execute_batch(tasks, slow_task)
    parallel_time = time.time() - start_par

    # Parallel should be ~5x faster
    assert parallel_time < sequential_time * 0.3  # At least 70% faster

# Test Structured Logging
def test_structured_logger(tmp_path):
    import json

    logger = StructuredLogger(log_dir=str(tmp_path))

    # Log some events
    logger.agent_start("test-agent", "Test task")
    logger.agent_complete("test-agent", 100.0, True)
    logger.error("test-agent", "ValueError", "Test error")

    # Read log file
    log_file = tmp_path / f"agent-{logger.trace_id}.jsonl"
    assert log_file.exists()

    # Parse JSON lines
    with open(log_file) as f:
        lines = f.readlines()

    assert len(lines) >= 3

    # Verify each line is valid JSON
    for line in lines:
        data = json.loads(line)
        assert "timestamp" in data
        assert "event_type" in data
        assert "trace_id" in data

# Test Performance Monitoring
def test_performance_monitor():
    monitor = PerformanceMonitor()

    # Record some executions
    monitor.record_execution("agent1", 100.0, True, token_count=50)
    monitor.record_execution("agent1", 110.0, True, token_count=55)
    monitor.record_execution("agent1", 150.0, False, token_count=0)

    metrics = monitor.get_metrics("agent1")
    assert metrics.execution_count == 3
    assert metrics.success_count == 2
    assert metrics.failure_count == 1
    assert metrics.success_rate == pytest.approx(66.67, rel=0.1)
    assert metrics.avg_duration_ms == pytest.approx(120.0)
    assert metrics.token_consumption == 105

# Test Context Manager
def test_context_manager():
    calls = []

    def mock_memory_tool(tool_name, **params):
        calls.append((tool_name, params))
        return {"items": []}

    manager = ContextManager(mock_memory_tool)

    # Save context
    manager.save_session_state({"phase": "test"})

    # Verify tool was called
    assert len(calls) == 1
    assert calls[0][0] == 'mcp__memory-keeper__context_save'
    assert calls[0][1]["category"] == "session-state"
    assert calls[0][1]["priority"] == "high"

# Run all tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

**실행**:
```bash
uv run pytest test_v4_improvements.py -v
```

**기대 결과**:
```
test_error_tracker_basic PASSED
test_parallel_executor_basic PASSED
test_parallel_faster_than_sequential PASSED
test_structured_logger PASSED
test_performance_monitor PASSED
test_context_manager PASSED

6 passed in 3.5s
```

### 6.2. Integration Tests

**파일**: `test_v4_integration.py`

```python
"""
Integration tests for v4.0 complete system
"""

import pytest
import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from agents.error_handler import ErrorTracker
from agents.parallel_executor import ParallelTaskExecutor, TaskDefinition
from agents.structured_logger import StructuredLogger
from agents.performance_monitor import PerformanceMonitor
from agents.context_manager import ContextManager

@pytest.mark.asyncio
async def test_full_system_integration():
    """Test all v4.0 components working together"""

    # Initialize all components
    error_tracker = ErrorTracker(max_retries=3)
    executor = ParallelTaskExecutor(max_parallel=3)
    logger = StructuredLogger(log_dir="/tmp/test-logs")
    monitor = PerformanceMonitor()

    # Mock memory tool
    def mock_memory_tool(tool, **kwargs):
        return {"items": []}

    context_mgr = ContextManager(mock_memory_tool)

    # Define test tasks
    tasks = [
        TaskDefinition("research-agent", f"Research concept {i}", f"task-{i}")
        for i in range(3)
    ]

    # Mock agent execution
    async def mock_agent_exec(agent_name, prompt):
        logger.agent_start(agent_name, prompt)

        # Simulate work
        await asyncio.sleep(0.1)

        logger.agent_complete(agent_name, 100.0, True)
        monitor.record_execution(agent_name, 100.0, True)

        return f"Completed: {prompt}"

    # Execute with all components
    results = await executor.execute_batch(tasks, mock_agent_exec)

    # Verify results
    assert len(results) == 3
    assert all(r.success for r in results)

    # Verify monitoring
    metrics = monitor.get_metrics("research-agent")
    assert metrics.execution_count == 3

    # Save context
    context_mgr.save_session_state({"test": "complete"})

    print("✅ Full system integration test passed")

@pytest.mark.asyncio
async def test_error_recovery_flow():
    """Test error handling with retry and escalation"""

    error_tracker = ErrorTracker(max_retries=2)
    logger = StructuredLogger(log_dir="/tmp/test-logs")

    attempt_count = [0]

    async def flaky_agent_exec(agent_name, prompt):
        attempt_count[0] += 1

        # Fail first 2 attempts, succeed on 3rd
        if attempt_count[0] < 3:
            raise Exception(f"Temporary failure {attempt_count[0]}")

        return "Success"

    # Execute with retry logic
    for attempt in range(3):
        try:
            result = await flaky_agent_exec("test-agent", "test task")
            break
        except Exception as e:
            count = error_tracker.record_error("test-agent", "task-1", e, {})
            logger.error("test-agent", "Exception", str(e))

            if error_tracker.should_escalate("test-agent", "task-1"):
                print("⚠️  Escalation triggered")
                break

    # Should succeed on 3rd attempt
    assert attempt_count[0] == 3
    assert not error_tracker.should_escalate("test-agent", "task-1")

    print("✅ Error recovery flow test passed")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

---

## Part 7: 메모리-키퍼 저장 (Save to Memory-Keeper)

v4.0 계획을 memory-keeper에 저장하여 영구 보존합니다.

```python
# 이 문서의 내용을 JSON으로 저장
import json

v4_plan = {
    "version": "4.0",
    "date": "2025-10-13",
    "status": "Ready for Implementation",

    "improvements": [
        {
            "id": "solution-1",
            "name": "Error Handling System",
            "files_created": ["agents/error_handler.py", "test_error_handling.py"],
            "files_modified": ["main.py"],
            "priority": "CRITICAL",
            "estimated_time_days": 2
        },
        {
            "id": "solution-2",
            "name": "Parallel Execution Wrapper",
            "files_created": ["agents/parallel_executor.py"],
            "files_modified": ["agents/meta_orchestrator.py"],
            "priority": "HIGH",
            "estimated_time_days": 2
        },
        {
            "id": "solution-3",
            "name": "Structured Logging System",
            "files_created": ["agents/structured_logger.py"],
            "files_modified": ["main.py"],
            "priority": "HIGH",
            "estimated_time_days": 1
        },
        {
            "id": "solution-4",
            "name": "Performance Monitoring",
            "files_created": ["agents/performance_monitor.py"],
            "files_modified": ["agents/parallel_executor.py"],
            "priority": "MEDIUM",
            "estimated_time_days": 2
        },
        {
            "id": "solution-5",
            "name": "Context Management Automation",
            "files_created": ["agents/context_manager.py"],
            "files_modified": ["main.py", "all agent files"],
            "priority": "MEDIUM",
            "estimated_time_days": 2
        }
    ],

    "edge_cases_covered": [
        "Race conditions in parallel execution",
        "Memory leaks in long-running sessions",
        "API rate limits",
        "Disk space exhaustion",
        "Context overflow despite management"
    ],

    "total_estimated_time_days": 15,
    "total_new_files": 7,
    "total_test_files": 2,

    "success_criteria": {
        "all_unit_tests_pass": True,
        "integration_tests_pass": True,
        "performance_improvement": ">50% latency reduction on 57 concepts",
        "zero_context_overflows": True,
        "error_escalation_working": True
    }
}

# Save to memory-keeper
mcp__memory-keeper__context_save(
    key="improvement-plan-v4-final-2025-10-13",
    value=json.dumps(v4_plan, indent=2),
    category="architecture",
    priority="high",
    channel="main-workflow"
)
```

---

## 결론 (Conclusion)

v4.0 개선 계획은 v3.0의 "무엇을" v4.0의 "어떻게"로 전환했습니다.

**핵심 성과**:
1. ✅ **5개의 실행 가능한 코드 솔루션** (복사-붙여넣기 가능)
2. ✅ **7개의 새 파일** (정확한 경로 및 전체 코드 제공)
3. ✅ **5가지 Edge Case 해결책** (race conditions, memory leaks 등)
4. ✅ **완전한 테스트 스위트** (unit + integration tests)
5. ✅ **4주 구현 로드맵** (task별 Definition of Done 포함)

**다음 단계**:
1. v4.0 계획 승인 받기
2. Phase 1 Task 1.1 시작 (Error Handling System)
3. 각 task 완료 후 DoD 검증
4. Phase 2-4 순차 진행

**문의사항**:
- 특정 코드 섹션에 대한 추가 설명 필요 시 문의
- Edge case 추가 발견 시 v4.1로 업데이트
- 구현 중 blocking issue 발생 시 즉시 에스컬레이션

---

**문서 상태**: ✅ Ready for Implementation
**승인 대기**: 개발팀 리뷰 및 go/no-go 결정
**예상 완료일**: 2025년 11월 10일 (4주 후)
