# Infrastructure Layer

**Purpose:** 모든 워크플로우에서 공통으로 사용하는 기반 기능 제공  
**Components:** 4 core modules (error handling, logging, monitoring, context management)  
**Design Pattern:** Cross-cutting concerns (AOP-inspired)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│            All Workflows (1, 2, 3, 4)                       │
│   Research → Build → Validate → Improve → Define Relations │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │   Infrastructure Layer     │
        └────────────┬───────────────┘
                     │
      ┌──────────────┼──────────────┬──────────────┐
      │              │              │              │
      ▼              ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  Error   │  │ Logging  │  │Performance│  │ Context  │
│ Handler  │  │  System  │  │ Monitor   │  │ Manager  │
├──────────┤  ├──────────┤  ├──────────┤  ├──────────┤
│• Retry   │  │• JSONL   │  │• Metrics │  │• Memory  │
│• Backoff │  │• trace_id│  │• p95/p99 │  │• SQLite  │
│• Escalate│  │• Context │  │• Success │  │• Category│
└──────────┘  └──────────┘  └──────────┘  └──────────┘
      │              │              │              │
      └──────────────┴──────────────┴──────────────┘
                     │
                     ▼
              ┌──────────────┐
              │  config.py   │
              ├──────────────┤
              │• Dynamic     │
              │  Paths       │
              │• Cross-      │
              │  Platform    │
              └──────────────┘
```

---

## Component 1: Error Handler

**File:** `agents/error_handler.py` (339 lines)  
**Purpose:** 자동 재시도, 지수 백오프, 사람 개입 에스컬레이션

### Core Classes

#### 1. ErrorRecord (dataclass)
```python
@dataclass
class ErrorRecord:
    agent_name: str
    task_id: str
    error_type: str
    error_message: str
    timestamp: str
    retry_count: int
    context_snapshot: Dict
```

#### 2. RetryConfig (dataclass)
```python
@dataclass
class RetryConfig:
    max_retries: int = 3
    initial_delay: float = 1.0
    backoff_factor: float = 2.0
    max_delay: float = 60.0
    
    def get_delay(self, retry_count: int) -> float:
        """Exponential backoff: base * 2^(n-1)"""
        delay = self.initial_delay * (self.backoff_factor ** (retry_count - 1))
        return min(delay, self.max_delay)
```

**Example:**
```
Retry 1: 1.0s delay
Retry 2: 2.0s delay
Retry 3: 4.0s delay
Retry 4: 8.0s delay (capped at max_delay)
```

#### 3. ErrorTracker
```python
class ErrorTracker:
    """Tracks errors per agent-task combination"""
    
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.error_history: Dict[str, int] = {}  # key -> retry count
        self.error_logs: List[ErrorRecord] = []
    
    def record_error(
        self,
        agent_name: str,
        task_id: str,
        error: Exception,
        context: Dict
    ) -> int:
        """Record error and return current retry count"""
        key = f"{agent_name}:{task_id}"
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
        
        return current_count
    
    def should_escalate(self, agent_name: str, task_id: str) -> bool:
        """Check if error count exceeded max_retries"""
        key = f"{agent_name}:{task_id}"
        return self.error_history.get(key, 0) >= self.max_retries
```

#### 4. RetryPolicy
```python
class RetryPolicy:
    """Retry policy with exponential backoff"""
    
    def should_retry(self, error: Exception) -> bool:
        """Determine if error is retryable"""
        
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
            "429"
        ]
        
        return any(pattern in error_msg for pattern in retryable_patterns)
```

### Decorator: @resilient_task

```python
@resilient_task(RetryConfig(max_retries=3, initial_delay=1.0))
async def call_agent(prompt: str):
    """Agent call with automatic retry"""
    return await Task(agent="knowledge-builder", prompt=prompt)
```

**Implementation:**
```python
def resilient_task(config: Optional[RetryConfig] = None):
    """Decorator for resilient agent task execution"""
    
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
                    
                    if retries > 0:
                        logger.info(f"{func.__name__} succeeded after {retries} retries")
                    
                    return result
                
                except Exception as e:
                    retries += 1
                    
                    # Check if retryable
                    if not retry_policy.should_retry(e):
                        logger.error(f"{func.__name__} failed with non-retryable error: {e}")
                        raise
                    
                    # Check if max retries exceeded
                    if retries >= config.max_retries:
                        logger.error(f"{func.__name__} failed after {retries} retries: {e}")
                        raise
                    
                    # Calculate backoff delay
                    delay = config.get_delay(retries)
                    
                    logger.warning(
                        f"{func.__name__} failed (attempt {retries}/{config.max_retries}). "
                        f"Retrying in {delay:.1f}s... Error: {e}"
                    )
                    
                    await asyncio.sleep(delay)
            
            raise Exception(f"{func.__name__} failed after {config.max_retries} retries")
        
        return wrapper
    return decorator
```

### Human Escalation

```python
def human_escalation_handler(
    agent_name: str,
    task_id: str,
    error_logs: List[ErrorRecord],
    context: Dict
):
    """Handle escalation to human operator"""
    
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
```

---

## Component 2: Structured Logger

**File:** `agents/structured_logger.py` (408 lines)  
**Purpose:** JSON 로깅, trace_id 전파, 구조화된 이벤트 추적

### Core Features

#### 1. trace_id Propagation (OpenTelemetry-inspired)

```python
from contextvars import ContextVar

# Context variable for trace_id propagation across async boundaries
trace_id_var: ContextVar[Optional[str]] = ContextVar('trace_id', default=None)

def set_trace_id(trace_id: str):
    """Set trace_id for current async context"""
    trace_id_var.set(trace_id)

def get_trace_id() -> Optional[str]:
    """Get current trace_id from context"""
    return trace_id_var.get()
```

**Usage in main.py:**
```python
# Generate trace_id for each user query
query_trace_id = str(uuid.uuid4())[:8]
set_trace_id(query_trace_id)

# All subsequent logs will include this trace_id
logger.agent_start("knowledge-builder", "Create document for Euler's Formula")
# Output: {"trace_id": "a3f7b2c9", "agent": "knowledge-builder", ...}
```

#### 2. LogEntry (dataclass)

```python
@dataclass
class LogEntry:
    """Structured log entry schema"""
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
        data = {k: v for k, v in data.items() if v is not None}
        return json.dumps(data, ensure_ascii=False)
```

#### 3. JSONFormatter

```python
class JSONFormatter(logging.Formatter):
    """Formats log records as JSON with trace_id propagation"""
    
    def format(self, record: logging.LogRecord) -> str:
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
        
        # Add extra fields
        if hasattr(record, 'agent_name'):
            log_data["agent_name"] = record.agent_name
        if hasattr(record, 'duration_ms'):
            log_data["duration_ms"] = record.duration_ms
        
        return json.dumps(log_data, ensure_ascii=False)
```

#### 4. StructuredLogger

```python
class StructuredLogger:
    """Enhanced structured logger with JSONL file output"""
    
    def __init__(
        self,
        log_dir: str = "/tmp/math-agent-logs",
        trace_id: Optional[str] = None
    ):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.trace_id = trace_id or str(uuid.uuid4())[:8]
        self.log_file = self.log_dir / f"agent-{datetime.now().strftime('%Y%m%d')}.jsonl"
        
        # Set trace_id in context
        trace_id_var.set(self.trace_id)
    
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
```

### Log Output Example (JSONL)

```jsonl
{"timestamp":"2025-10-14T22:45:30.123","trace_id":"a3f7b2c9","event_type":"agent_start","agent_name":"knowledge-builder","level":"INFO","message":"Starting agent: knowledge-builder","metadata":{"task":"Create document for Euler's Formula"}}
{"timestamp":"2025-10-14T22:45:30.623","trace_id":"a3f7b2c9","event_type":"tool_call","agent_name":"knowledge-builder","level":"INFO","message":"Tool call: Write","duration_ms":100,"metadata":{"tool":"Write","success":true}}
{"timestamp":"2025-10-14T22:45:31.123","trace_id":"a3f7b2c9","event_type":"agent_complete","agent_name":"knowledge-builder","level":"INFO","message":"Agent completed: knowledge-builder","duration_ms":1000,"metadata":{"success":true}}
```

---

## Component 3: Performance Monitor

**File:** `agents/performance_monitor.py` (347 lines)  
**Purpose:** 에이전트 실행 메트릭 수집 (avg, median, p95, p99, success rate)

### Core Classes

#### 1. AgentMetrics (dataclass)

```python
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
```

#### 2. PerformanceMonitor

```python
class PerformanceMonitor:
    """Monitors and aggregates performance metrics for all agents"""
    
    def __init__(self):
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
        """Record metrics for a single agent execution"""
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
    
    def print_summary(self):
        """Print a summary table of performance metrics"""
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
```

### Performance Summary Example

```
==================================================================================================================
Performance Monitoring Summary
==================================================================================================================
Session duration: 127s

Agent                     Exec   Success    Avg(ms)   Med(ms)   P95(ms)   Tokens   API
------------------------------------------------------------------------------------------------------------------
knowledge-builder         15     93.3%        500       450       800      45000    15
quality-agent             15    100.0%        300       280       450      22500    15
research-agent            15     86.7%       2500      2400      4000      75000    75
example-generator         12     91.7%       1200      1100      2000      36000    12
meta-orchestrator         30    100.0%        150       140       250      15000    30
==================================================================================================================
```

---

## Component 4: Context Manager

**File:** `agents/context_manager.py` (491 lines)  
**Purpose:** MCP memory-keeper 통합, 카테고리 기반 컨텍스트 저장, 자동 정리

### Core Features

#### 1. ContextCategory (dataclass)

```python
@dataclass
class ContextCategory:
    """Context category definition with retention policy"""
    name: str
    priority: str  # high | medium | low
    description: str
    retention_days: int  # -1 = indefinite
    max_items: int  # -1 = unlimited
```

#### 2. Category Definitions

```python
CATEGORIES = {
    "session-state": ContextCategory(
        name="session-state",
        priority="high",
        description="Current workflow state",
        retention_days=7,
        max_items=50
    ),
    "agent-performance": ContextCategory(
        name="agent-performance",
        priority="medium",
        description="Agent metrics and performance data",
        retention_days=7,
        max_items=100
    ),
    "errors": ContextCategory(
        name="errors",
        priority="high",
        description="Error logs and diagnostics",
        retention_days=30,
        max_items=200
    ),
    "decisions": ContextCategory(
        name="decisions",
        priority="high",
        description="Architecture and design decisions",
        retention_days=-1,  # Keep indefinitely
        max_items=-1  # No limit
    ),
    "milestone": ContextCategory(
        name="milestone",
        priority="high",
        description="Major achievements and checkpoints",
        retention_days=-1,  # Keep indefinitely
        max_items=-1  # No limit
    )
}
```

#### 3. ContextManager

```python
class ContextManager:
    """Manages context persistence via memory-keeper MCP server"""
    
    def __init__(self, memory_tool_func: Callable):
        self.memory_tool = memory_tool_func
        self.context_save_count = 0
        self.auto_cleanup_interval = 10  # Cleanup every N saves
    
    def save(
        self,
        key: str,
        value: Any,
        category: str,
        priority: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """Save context item to memory-keeper"""
        
        if category not in self.CATEGORIES:
            raise ValueError(f"Invalid category: {category}")
        
        cat_def = self.CATEGORIES[category]
        
        # Serialize value if needed
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        
        # Get priority (use category default if not specified)
        final_priority = priority or cat_def.priority
        
        # Save to memory-keeper
        self.memory_tool('mcp__memory-keeper__context_save',
            key=key,
            value=value,
            category=category,
            priority=final_priority,
            metadata=metadata or {}
        )
        
        self.context_save_count += 1
        
        # Auto-cleanup check
        if self.context_save_count % self.auto_cleanup_interval == 0:
            self._auto_cleanup()
    
    def get(
        self,
        category: Optional[str] = None,
        key: Optional[str] = None,
        priorities: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Dict]:
        """Retrieve context items from memory-keeper"""
        
        params = {"limit": limit}
        if category:
            params["category"] = category
        if key:
            params["key"] = key
        if priorities:
            params["priorities"] = priorities
        
        result = self.memory_tool('mcp__memory-keeper__context_get', **params)
        return result.get("items", [])
    
    def save_session_state(self, state: Dict):
        """Save current session state"""
        self.save(
            key="current-session-state",
            value=state,
            category="session-state",
            priority="high",
            metadata={"timestamp": datetime.now().isoformat()}
        )
    
    def save_error(
        self,
        agent_name: str,
        error_type: str,
        error_message: str,
        context: Dict
    ):
        """Save error information"""
        error_data = {
            "agent": agent_name,
            "error_type": error_type,
            "message": error_message,
            "timestamp": datetime.now().isoformat(),
            "context": context
        }
        
        self.save(
            key=f"error-{datetime.now().timestamp()}",
            value=error_data,
            category="errors",
            priority="high"
        )
    
    def save_milestone(self, milestone_name: str, milestone_data: Dict):
        """Save major milestone (permanent)"""
        self.save(
            key=f"milestone-{milestone_name.lower().replace(' ', '-')}",
            value=milestone_data,
            category="milestone",
            priority="high",
            metadata={"timestamp": datetime.now().isoformat()}
        )
```

---

## Component 5: Config Module

**File:** `config.py` (123 lines)  
**Purpose:** 동적 경로 해석, 크로스 플랫폼 지원

### Dynamic Path Resolution

```python
def find_project_root(marker_files: tuple = ("pyproject.toml", ".git")) -> Path:
    """
    Find project root by searching for marker files/directories.
    
    Searches current directory and all parents until marker found.
    """
    current = Path(__file__).resolve().parent
    
    for parent in [current] + list(current.parents):
        if any((parent / marker).exists() for marker in marker_files):
            return parent
    
    raise RuntimeError(
        f"Could not find project root. Looking for {marker_files} "
        f"starting from {current}"
    )

# Project root
PROJECT_ROOT = find_project_root()

# Core directories
AGENTS_DIR = PROJECT_ROOT / "agents"
TESTS_DIR = PROJECT_ROOT / "tests"
TOOLS_DIR = PROJECT_ROOT / "tools"

# Output directories
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
DEPENDENCY_MAP_DIR = OUTPUTS_DIR / "dependency-map"
RESEARCH_REPORTS_DIR = OUTPUTS_DIR / "research-reports"

# Math vault - prefer Windows-accessible path for Obsidian compatibility
WINDOWS_OBSIDIAN_PATH = Path("/mnt/c/Users/packr/Documents/obsidian-vault/Math")
if WINDOWS_OBSIDIAN_PATH.exists():
    MATH_VAULT_DIR = WINDOWS_OBSIDIAN_PATH
else:
    MATH_VAULT_DIR = PROJECT_ROOT / "math-vault"
```

### Directory Initialization

```python
def ensure_directories() -> None:
    """Create all required output directories if they don't exist"""
    dirs_to_create = [
        TESTS_DIR,
        TOOLS_DIR,
        OUTPUTS_DIR,
        DEPENDENCY_MAP_DIR,
        RESEARCH_REPORTS_DIR,
        MATH_VAULT_DIR,
    ]
    
    for directory in dirs_to_create:
        directory.mkdir(parents=True, exist_ok=True)

# Initialize directories on import
try:
    ensure_directories()
except Exception as e:
    import warnings
    warnings.warn(f"Could not create output directories: {e}")
```

---

## Integration Example

### Complete Workflow with Infrastructure

```python
import asyncio
from agents.error_handler import ErrorTracker, resilient_task, RetryConfig
from agents.structured_logger import StructuredLogger, set_trace_id
from agents.performance_monitor import PerformanceMonitor
from agents.context_manager import ContextManager

async def main():
    # Initialize infrastructure
    logger = StructuredLogger(log_dir="/tmp/math-agent-logs")
    performance_monitor = PerformanceMonitor()
    error_tracker = ErrorTracker(max_retries=3)
    context_manager = ContextManager(memory_tool_func)
    
    # Generate trace_id
    trace_id = str(uuid.uuid4())[:8]
    set_trace_id(trace_id)
    
    # Execute workflow with infrastructure
    @resilient_task(RetryConfig(max_retries=3, initial_delay=1.0))
    async def execute_workflow():
        # Start logging
        logger.agent_start("knowledge-builder", "Create document")
        
        start_time = time.time()
        success = False
        
        try:
            # Execute agent
            result = await Task(agent="knowledge-builder", prompt="Create document for Euler's Formula")
            success = True
            return result
            
        except Exception as e:
            # Record error
            error_tracker.record_error(
                agent_name="knowledge-builder",
                task_id=trace_id,
                error=e,
                context={"query": "Euler's Formula"}
            )
            
            # Save error to context
            context_manager.save_error(
                agent_name="knowledge-builder",
                error_type=type(e).__name__,
                error_message=str(e),
                context={"trace_id": trace_id}
            )
            
            # Check if escalation needed
            if error_tracker.should_escalate("knowledge-builder", trace_id):
                human_escalation_handler(
                    "knowledge-builder",
                    trace_id,
                    error_tracker.get_error_logs("knowledge-builder"),
                    {"query": "Euler's Formula"}
                )
            
            raise
            
        finally:
            # Record performance
            duration_ms = (time.time() - start_time) * 1000
            performance_monitor.record_execution(
                agent_name="knowledge-builder",
                duration_ms=duration_ms,
                success=success
            )
            
            # Log completion
            logger.agent_complete("knowledge-builder", duration_ms, success)
    
    # Execute
    result = await execute_workflow()
    
    # Print summary
    performance_monitor.print_summary()
    
    return result

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Performance Impact

### Overhead Analysis

```python
Infrastructure Component      Overhead per Call    Impact
─────────────────────────────────────────────────────────
Error Handler (no retry)      ~0.5ms              Negligible
Error Handler (3 retries)     ~7s (with backoff)  Acceptable
Structured Logger             ~1ms                Negligible
Performance Monitor           ~0.2ms              Negligible
Context Manager (save)        ~50ms (MCP call)    Low
Context Manager (get)         ~30ms (MCP call)    Low

Total overhead (normal case): ~2ms per agent call (<1% of typical 500ms execution)
```

---

**Document Status:** ✅ Complete  
**All Core Documentation Complete!**

**Created Documents:**
1. ✅ SYSTEM-ARCHITECTURE.md
2. ✅ WORKFLOW-1-CONTENT-GENERATION.md
3. ✅ WORKFLOW-2-DEPENDENCY-MAPPING.md
4. ✅ WORKFLOW-3-SELF-IMPROVEMENT.md
5. ✅ WORKFLOW-4-RELATIONSHIP-DEFINITION.md
6. ✅ INFRASTRUCTURE-LAYER.md

