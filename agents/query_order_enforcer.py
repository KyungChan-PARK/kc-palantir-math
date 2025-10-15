"""
Query Order Enforcer - Structural Enforcement of Correct Query Sequencing

VERSION: 1.0.0
DATE: 2025-10-15
PURPOSE: Force correct query order for SDK integration tasks to prevent TypeErrors

Meta-Learning Source:
- Learned from: streaming implementation session (2025-10-15)
- Pattern detected: AI implemented SDK features without verification queries
- Result: 2 TypeErrors, 90 minutes wasted
- Prevention: Force verification queries BEFORE implementation

This is STRUCTURAL enforcement - AI cannot bypass even if it wants to.

Architecture:
- State machine tracks query history per task
- Blocks implementation until required queries complete
- Different task types have different required query sequences

Example:
    enforcer = QueryOrderEnforcer()
    
    # Start SDK integration task
    enforcer.start_task("add-streaming", TaskType.SDK_INTEGRATION)
    
    # Try to implement without verification
    can_impl, msg = enforcer.can_implement("add-streaming")
    # Returns: (False, "Missing required queries: inspect.signature")
    
    # Run required query
    enforcer.record_query("add-streaming", "inspect.signature")
    
    # Now can implement
    can_impl, msg = enforcer.can_implement("add-streaming")
    # Returns: (True, "All verifications complete")
"""

from typing import Dict, Set, Tuple, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class TaskType(Enum):
    """Types of tasks with different query requirements"""
    SDK_INTEGRATION = "sdk_integration"
    FILE_MODIFICATION = "file_modification"
    BATCH_OPERATION = "batch_operation"
    GENERAL = "general"


@dataclass
class TaskState:
    """State of a tracked task"""
    task_id: str
    task_type: TaskType
    queries_completed: Set[str]
    implementation_allowed: bool
    started_at: datetime
    metadata: Dict


class QueryOrderEnforcer:
    """
    Enforces correct query order for different task types.
    
    Prevents mistakes by BLOCKING implementation until required queries complete.
    This is structural enforcement - cannot be bypassed by prompts or instructions.
    
    Meta-Cognitive Integration:
    - Records query patterns for analysis
    - Learns from blocked attempts
    - Provides educational feedback when blocking
    """
    
    def __init__(self):
        """Initialize query order enforcer"""
        self.active_tasks: Dict[str, TaskState] = {}
        
        # Define required queries for each task type
        # These are MANDATORY and CANNOT be skipped
        self.required_queries: Dict[TaskType, Set[str]] = {
            TaskType.SDK_INTEGRATION: {
                "inspect.signature",  # MUST verify SDK signatures
                "dir(sdk_client)"     # MUST check available methods
            },
            TaskType.FILE_MODIFICATION: {
                "read_file"  # MUST read before edit
            },
            TaskType.BATCH_OPERATION: {
                "test_single"  # MUST test with n=1 before batch
            },
            TaskType.GENERAL: set()  # No special requirements
        }
        
        # Statistics for meta-learning
        self.blocks_prevented = 0
        self.implementations_allowed = 0
        self.queries_recorded = 0
    
    def start_task(
        self,
        task_id: str,
        task_type: TaskType,
        metadata: Optional[Dict] = None
    ):
        """
        Register new task that needs query enforcement.
        
        Args:
            task_id: Unique identifier for this task
            task_type: Type of task (determines required queries)
            metadata: Optional metadata about the task
        """
        self.active_tasks[task_id] = TaskState(
            task_id=task_id,
            task_type=task_type,
            queries_completed=set(),
            implementation_allowed=False,
            started_at=datetime.now(),
            metadata=metadata or {}
        )
        
        required = self.required_queries[task_type]
        if required:
            print(f"📋 Task '{task_id}' started (type: {task_type.value})")
            print(f"   Required queries: {required}")
    
    def record_query(self, task_id: str, query_signature: str):
        """
        Record that a query was executed.
        
        Automatically checks if all required queries are now complete.
        
        Args:
            task_id: Task identifier
            query_signature: Signature/type of query executed
                            (e.g., "inspect.signature", "read_file", "dir()")
        """
        if task_id not in self.active_tasks:
            return  # No enforcement for untracked tasks
        
        task = self.active_tasks[task_id]
        task.queries_completed.add(query_signature)
        self.queries_recorded += 1
        
        print(f"✓ Query recorded for '{task_id}': {query_signature}")
        
        # Check if all required queries now complete
        required = self.required_queries[task.task_type]
        completed = task.queries_completed
        
        if required.issubset(completed):
            task.implementation_allowed = True
            self.implementations_allowed += 1
            print(f"✅ All required queries complete for '{task_id}'")
            print(f"   Implementation is now ALLOWED")
        else:
            missing = required - completed
            print(f"   Still missing: {missing}")
    
    def can_implement(self, task_id: str) -> Tuple[bool, str]:
        """
        Check if implementation is allowed for this task.
        
        This is the BLOCKING function - returns False if queries incomplete.
        
        Args:
            task_id: Task identifier
        
        Returns:
            (allowed: bool, message: str)
                If allowed=False, implementation is BLOCKED
        """
        # No tracking = no enforcement (allow general tasks)
        if task_id not in self.active_tasks:
            return (True, "No query enforcement for this task")
        
        task = self.active_tasks[task_id]
        
        # Check if implementation allowed
        if task.implementation_allowed:
            return (True, "All required queries completed. Implementation allowed.")
        
        # BLOCK implementation
        self.blocks_prevented += 1
        
        required = self.required_queries[task.task_type]
        completed = task.queries_completed
        missing = required - completed
        
        # Educational blocking message
        message = f"""
🚫 IMPLEMENTATION BLOCKED

Task: {task_id}
Type: {task.task_type.value}

Required queries: {sorted(required)}
Completed: {sorted(completed)}
Missing: {sorted(missing)}

You MUST complete missing queries before implementing.

Why this is enforced:
- Prevents TypeError from invalid SDK parameters
- Prevents editing files without reading them first  
- Prevents batch changes without testing n=1

Meta-Learning:
This enforcement was learned from real mistakes in streaming session (2025-10-15):
- AI assumed SDK parameters existed → TypeError x2
- AI made batch changes without testing → 10 files rollback
- Time wasted: 90 minutes

This structural enforcement prevents repetition.

Next step: Complete missing queries, then try again.

Statistics:
- Implementations blocked: {self.blocks_prevented}
- Implementations allowed: {self.implementations_allowed}
- Block prevention rate: {self.blocks_prevented / (self.blocks_prevented + max(1, self.implementations_allowed)) * 100:.0f}%
"""
        
        return (False, message)
    
    def end_task(self, task_id: str):
        """Clean up completed task"""
        if task_id in self.active_tasks:
            del self.active_tasks[task_id]
    
    def get_statistics(self) -> Dict:
        """Get enforcer statistics for meta-learning"""
        return {
            "active_tasks": len(self.active_tasks),
            "blocks_prevented": self.blocks_prevented,
            "implementations_allowed": self.implementations_allowed,
            "queries_recorded": self.queries_recorded,
            "prevention_effectiveness": f"{self.blocks_prevented / max(1, self.blocks_prevented + self.implementations_allowed) * 100:.0f}%"
        }


# Global instance for reuse
_global_enforcer = QueryOrderEnforcer()


def start_enforced_task(task_id: str, task_type: str, metadata: Optional[Dict] = None):
    """Global function to start enforced task"""
    task_type_enum = TaskType[task_type.upper()]
    _global_enforcer.start_task(task_id, task_type_enum, metadata)


def record_query_execution(task_id: str, query_sig: str):
    """Global function to record query"""
    _global_enforcer.record_query(task_id, query_sig)


def check_can_implement(task_id: str) -> Tuple[bool, str]:
    """Global function to check implementation permission"""
    return _global_enforcer.can_implement(task_id)


def end_enforced_task(task_id: str):
    """Global function to end task"""
    _global_enforcer.end_task(task_id)


def get_enforcer_statistics() -> Dict:
    """Global function to get statistics"""
    return _global_enforcer.get_statistics()

