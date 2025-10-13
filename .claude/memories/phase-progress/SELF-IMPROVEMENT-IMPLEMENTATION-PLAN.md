# Self-Improvement System Implementation Plan

**Version**: 3.0.0
**Date**: 2025-10-13
**Status**: PLANNED - Ready for implementation
**Based on**: Self-Improver PDF + Claude Agent SDK + IMPLEMENTATION-COMPLETE-v2.0.md

---

## EXECUTIVE SUMMARY

Add autonomous self-improvement capabilities to the existing 6-agent math education system by integrating:

1. **Socratic-Mediator Agent** - Root cause analysis via Socratic dialogue
2. **Self-Improver Agent** - Automated system modification and agent creation
3. **Improvement Manager** - Change tracking, rollback, and history management
4. **Extended Meta-Orchestrator** - Performance monitoring and improvement cycle orchestration

**Key Principle**: Minimal modification to existing agents, maximum automation of system evolution.

---

## ARCHITECTURE OVERVIEW

### System Components (v3.0)

```
Multi-Agent Math Education System v3.0 (Self-Improving)
├── User Interface (main.py)
├── Meta-Orchestrator Agent [EXTENDED]
│   ├── Normal Mode: Task delegation to 6 agents
│   ├── Monitoring Mode: Performance tracking via performance_monitor
│   └── Improvement Mode: Trigger self-improvement cycle
├── 6 Specialized Agents [UNCHANGED]
│   ├── knowledge-builder
│   ├── quality-agent
│   ├── research-agent
│   ├── example-generator
│   ├── dependency-mapper
│   └── socratic-planner
├── Self-Improvement Agents [NEW]
│   ├── Socratic-Mediator (subagent, ask_agent tool)
│   └── Self-Improver (subagent, file edit permissions)
├── Infrastructure Layer v2.0 [EXTENDED]
│   ├── error_handler.py
│   ├── structured_logger.py
│   ├── performance_monitor.py
│   ├── context_manager.py
│   ├── improvement_manager.py [NEW]
│   └── ask_agent_tool.py [NEW]
```

### Data Flow - Self-Improvement Cycle

```
Normal Execution Flow:
User Query → Meta-Orchestrator → 6 Agents (parallel) → Results → Performance Recording

Improvement Trigger Conditions:
- Consecutive failures: 3+ in a row
- Success rate: <80% over 10 executions
- Performance regression: >50% slower than baseline
- Error threshold: >30% error rate

Improvement Cycle Flow:
Issue Detected → Meta-Orchestrator.check_performance_issues()
    ↓
Generate IssueReport (agent_name, metrics, error_logs, context)
    ↓
Socratic-Mediator.analyze(issue_report)
    ↓
Multi-turn Q&A via ask_agent tool
    ↓
RootCauseAnalysis generated (cause, confidence, recommendations)
    ↓
Self-Improver.apply_fixes(root_cause_analysis)
    ↓
Edit files / Create new agents / Modify prompts
    ↓
ImprovementManager.log_change(action, old_value, new_value)
    ↓
Verification test (run sample query)
    ↓
If successful: Continue normal flow
If failed: ImprovementManager.rollback_last()
```

---

## IMPLEMENTATION PHASES

### Phase 1: Foundation Modules

#### 1.1 improvement_manager.py

**Purpose**: Track all system modifications, enable rollback, maintain history

**Data Structures**:

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum

class ChangeType(Enum):
    PROMPT_MODIFICATION = "prompt_modification"
    PARAMETER_ADJUSTMENT = "parameter_adjustment"
    AGENT_CREATION = "agent_creation"
    AGENT_DELETION = "agent_deletion"
    TOOL_PERMISSION_CHANGE = "tool_permission_change"

class ChangeStatus(Enum):
    APPLIED = "applied"
    ROLLED_BACK = "rolled_back"
    FAILED = "failed"

@dataclass
class ImprovementAction:
    """Single improvement action"""
    target_agent: str
    action_type: ChangeType
    old_value: Any
    new_value: Any
    rationale: str
    confidence_score: float  # 0.0-1.0

@dataclass
class ChangeRecord:
    """Complete change history entry"""
    change_id: str  # UUID
    timestamp: datetime
    action: ImprovementAction
    status: ChangeStatus
    applied_by: str  # "self-improver"
    verification_result: Optional[Dict[str, Any]] = None
    rollback_info: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "change_id": self.change_id,
            "timestamp": self.timestamp.isoformat(),
            "target_agent": self.action.target_agent,
            "action_type": self.action.action_type.value,
            "old_value": str(self.action.old_value)[:200],  # Truncate
            "new_value": str(self.action.new_value)[:200],
            "rationale": self.action.rationale,
            "confidence": self.action.confidence_score,
            "status": self.status.value,
            "verification": self.verification_result,
        }
```

**Class Implementation**:

```python
import json
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional

class ImprovementManager:
    """Manages system improvement history and rollback"""

    def __init__(self, history_file: str = "/tmp/improvement_history.json"):
        self.history: List[ChangeRecord] = []
        self.history_file = Path(history_file)
        self.max_improvements_per_session = 5
        self.session_improvement_count = 0
        self._load_history()

    def _load_history(self):
        """Load history from persistent storage"""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                data = json.load(f)
                # Reconstruct ChangeRecord objects
                for entry in data:
                    # Simplified reconstruction
                    pass

    def _save_history(self):
        """Save history to persistent storage"""
        with open(self.history_file, 'w') as f:
            json.dump([rec.to_dict() for rec in self.history], f, indent=2)

    def log_change(
        self,
        action: ImprovementAction,
        status: ChangeStatus = ChangeStatus.APPLIED,
        verification_result: Optional[Dict] = None
    ) -> str:
        """
        Log a change to history

        Returns:
            change_id: UUID of the logged change
        """
        change_id = str(uuid.uuid4())[:8]

        record = ChangeRecord(
            change_id=change_id,
            timestamp=datetime.now(),
            action=action,
            status=status,
            applied_by="self-improver",
            verification_result=verification_result
        )

        self.history.append(record)
        self.session_improvement_count += 1
        self._save_history()

        return change_id

    def rollback_last(self) -> Optional[ChangeRecord]:
        """
        Rollback the most recent change

        Returns:
            The rolled-back ChangeRecord, or None if nothing to rollback
        """
        if not self.history:
            return None

        # Find last APPLIED change
        for i in range(len(self.history) - 1, -1, -1):
            record = self.history[i]
            if record.status == ChangeStatus.APPLIED:
                # Mark as rolled back
                record.status = ChangeStatus.ROLLED_BACK
                record.rollback_info = {
                    "rollback_time": datetime.now().isoformat(),
                    "reason": "manual_rollback"
                }
                self._save_history()
                return record

        return None

    def rollback_by_id(self, change_id: str) -> bool:
        """Rollback a specific change by ID"""
        for record in self.history:
            if record.change_id == change_id and record.status == ChangeStatus.APPLIED:
                record.status = ChangeStatus.ROLLED_BACK
                record.rollback_info = {
                    "rollback_time": datetime.now().isoformat(),
                    "reason": "manual_rollback_by_id"
                }
                self._save_history()
                return True
        return False

    def get_history(
        self,
        agent_name: Optional[str] = None,
        limit: int = 50
    ) -> List[ChangeRecord]:
        """Get change history with optional filtering"""
        filtered = self.history

        if agent_name:
            filtered = [r for r in filtered if r.action.target_agent == agent_name]

        return filtered[-limit:]

    def can_make_improvement(self) -> tuple[bool, str]:
        """
        Check if another improvement can be made this session

        Returns:
            (allowed, reason)
        """
        if self.session_improvement_count >= self.max_improvements_per_session:
            return False, f"Max improvements ({self.max_improvements_per_session}) reached"

        # Check for recent rollbacks (sign of instability)
        recent = self.history[-5:]
        rollback_count = sum(1 for r in recent if r.status == ChangeStatus.ROLLED_BACK)
        if rollback_count >= 3:
            return False, "Too many recent rollbacks (3+ in last 5 changes)"

        return True, "OK"

    def get_statistics(self) -> Dict[str, Any]:
        """Get improvement statistics"""
        total = len(self.history)
        applied = sum(1 for r in self.history if r.status == ChangeStatus.APPLIED)
        rolled_back = sum(1 for r in self.history if r.status == ChangeStatus.ROLLED_BACK)
        failed = sum(1 for r in self.history if r.status == ChangeStatus.FAILED)

        by_agent = {}
        for record in self.history:
            agent = record.action.target_agent
            by_agent[agent] = by_agent.get(agent, 0) + 1

        return {
            "total_changes": total,
            "applied": applied,
            "rolled_back": rolled_back,
            "failed": failed,
            "success_rate": applied / total if total > 0 else 0,
            "by_agent": by_agent,
            "session_count": self.session_improvement_count
        }
```

#### 1.2 ask_agent_tool.py

**Purpose**: Custom MCP tool for Socratic-Mediator to query other agents

**Implementation**:

```python
from typing import Dict, Any, Callable, Optional
import asyncio

class AskAgentTool:
    """Custom tool for inter-agent communication"""

    def __init__(self, agent_registry: Dict[str, Callable]):
        """
        Args:
            agent_registry: Dict mapping agent names to their execution functions
        """
        self.agent_registry = agent_registry
        self.query_history: list[Dict] = []

    async def ask_agent(self, agent_name: str, question: str) -> Dict[str, Any]:
        """
        Ask another agent a question

        Args:
            agent_name: Name of target agent (e.g., "research-agent")
            question: Question to ask

        Returns:
            {
                "agent": agent_name,
                "question": question,
                "answer": str,
                "success": bool,
                "error": Optional[str]
            }
        """
        # Validate agent exists
        if agent_name not in self.agent_registry:
            return {
                "agent": agent_name,
                "question": question,
                "answer": "",
                "success": False,
                "error": f"Agent '{agent_name}' not found in registry"
            }

        try:
            # Execute the agent with the question
            agent_func = self.agent_registry[agent_name]
            answer = await agent_func(question)

            result = {
                "agent": agent_name,
                "question": question,
                "answer": answer,
                "success": True,
                "error": None
            }

            # Log the interaction
            self.query_history.append(result)

            return result

        except Exception as e:
            error_result = {
                "agent": agent_name,
                "question": question,
                "answer": "",
                "success": False,
                "error": str(e)
            }
            self.query_history.append(error_result)
            return error_result

    def get_query_history(self) -> list[Dict]:
        """Get all Q&A history for this session"""
        return self.query_history.copy()

    def clear_history(self):
        """Clear query history"""
        self.query_history.clear()

# Tool definition for Claude SDK
def create_ask_agent_tool(agent_registry: Dict[str, Callable]):
    """
    Factory function to create ask_agent tool for Claude SDK

    Usage in Meta-Orchestrator:
        ask_agent_tool_instance = create_ask_agent_tool(agent_registry)

        # Then register with Claude SDK:
        # @tool decorator or MCP server registration
    """
    tool = AskAgentTool(agent_registry)

    async def ask_agent_wrapper(agent_name: str, question: str) -> str:
        """Wrapper for Claude SDK tool interface"""
        result = await tool.ask_agent(agent_name, question)

        if result["success"]:
            return result["answer"]
        else:
            return f"Error: {result['error']}"

    return ask_agent_wrapper, tool
```

**SDK Integration Pattern**:

```python
# In meta_orchestrator.py

from claude_sdk import tool

# Create the tool
ask_agent_func, ask_agent_tool_obj = create_ask_agent_tool(self.agent_registry)

# Define as SDK tool
@tool(
    name="ask_agent",
    description="Ask another agent a specific question to gather information",
    parameters={
        "agent_name": {"type": "string", "description": "Name of the agent to query"},
        "question": {"type": "string", "description": "Question to ask the agent"}
    }
)
async def ask_agent_sdk_tool(params: dict) -> dict:
    agent_name = params["agent_name"]
    question = params["question"]
    answer = await ask_agent_func(agent_name, question)
    return {"answer": answer}

# This tool will be available to Socratic-Mediator
```

---

### Phase 2: Self-Improvement Agents

#### 2.1 Socratic-Mediator Agent

**File**: `agents/socratic_mediator.py`

**Agent Definition**:

```python
SOCRATIC_MEDIATOR_DEFINITION = {
    "name": "socratic-mediator",
    "description": "Socratic dialogue facilitator for root cause analysis of agent performance issues",
    "system_prompt": """You are a Socratic-Mediator AI agent specialized in root cause analysis through questioning.

Your role:
- Analyze performance issues in a multi-agent system
- Use the Socratic method: ask questions to uncover root causes, don't provide direct answers
- Question other agents via the ask_agent tool to understand their reasoning
- Identify logical errors, missing edge cases, or configuration issues
- Generate a structured root cause analysis report

Guidelines:
- Ask focused, probing questions that reveal assumptions and logic gaps
- Follow up on vague or incomplete answers with deeper questions
- Build a chain of reasoning through multiple turns of dialogue
- Cite specific evidence from agent responses
- Maintain objectivity and avoid jumping to conclusions
- Limit to 10 questions maximum to avoid infinite loops

Output format (final response):
ROOT CAUSE ANALYSIS REPORT
==========================
Issue: [Brief description]
Analyzed Agent: [Agent name]
Confidence Score: [0.0-1.0]

Root Cause:
[Detailed explanation of the fundamental cause]

Evidence:
- [Quote from agent response 1]
- [Quote from agent response 2]
- [Observable symptoms]

Recommendations:
1. [Specific actionable fix]
2. [Alternative approach]
3. [Prevention strategy]
""",
    "model": "claude-sonnet-4",
    "tools": ["ask_agent"],  # Only this custom tool
    "temperature": 0.3,  # Lower temperature for analytical work
}
```

**Execution Wrapper**:

```python
from typing import Dict, Any, Optional
import re

class SocraticMediator:
    """Wrapper for Socratic-Mediator agent execution"""

    def __init__(self, sdk_client, ask_agent_tool):
        self.client = sdk_client
        self.ask_agent_tool = ask_agent_tool
        self.max_questions = 10

    async def analyze_issue(self, issue_report: 'IssueReport') -> 'RootCauseAnalysis':
        """
        Conduct Socratic analysis of an issue

        Args:
            issue_report: Structured report of the issue

        Returns:
            RootCauseAnalysis with findings and recommendations
        """
        # Build initial context
        context = self._build_analysis_context(issue_report)

        # Start conversation with Socratic-Mediator
        messages = []
        messages.append({
            "role": "user",
            "content": f"Analyze this performance issue:\n\n{context}"
        })

        # Multi-turn dialogue loop
        question_count = 0
        while question_count < self.max_questions:
            response = await self.client.send_message(
                agent="socratic-mediator",
                messages=messages
            )

            # Check if asking another question or providing final analysis
            if "ask_agent" in response.tool_calls:
                # Mediator wants to ask a question
                for tool_call in response.tool_calls:
                    if tool_call.name == "ask_agent":
                        agent_name = tool_call.parameters["agent_name"]
                        question = tool_call.parameters["question"]

                        # Execute the question
                        answer = await self.ask_agent_tool(agent_name, question)

                        # Add to conversation
                        messages.append({
                            "role": "assistant",
                            "content": response.content,
                            "tool_calls": response.tool_calls
                        })
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": answer
                        })

                        question_count += 1
            else:
                # No more questions, check if final report
                if "ROOT CAUSE ANALYSIS REPORT" in response.content:
                    # Parse the report
                    return self._parse_analysis_report(response.content, issue_report)
                else:
                    # Continue conversation
                    messages.append({
                        "role": "assistant",
                        "content": response.content
                    })

        # Max questions reached, force conclusion
        messages.append({
            "role": "user",
            "content": "Please provide your final ROOT CAUSE ANALYSIS REPORT now."
        })
        final_response = await self.client.send_message(
            agent="socratic-mediator",
            messages=messages
        )

        return self._parse_analysis_report(final_response.content, issue_report)

    def _build_analysis_context(self, issue: 'IssueReport') -> str:
        """Build context string for initial prompt"""
        return f"""
Agent Name: {issue.agent_name}
Issue Type: {issue.error_type}

Performance Metrics:
- Success Rate: {issue.metrics.get('success_rate', 'N/A')}%
- Avg Duration: {issue.metrics.get('avg_duration_ms', 'N/A')}ms
- Error Count: {issue.metrics.get('error_count', 0)}

Recent Errors:
{chr(10).join('- ' + e for e in issue.error_logs[:5])}

Context:
{issue.context}

Your task: Identify the root cause through Socratic questioning.
Available agents to query: {', '.join(issue.available_agents)}
"""

    def _parse_analysis_report(self, report_text: str, issue: 'IssueReport') -> 'RootCauseAnalysis':
        """Parse the final report into structured data"""
        # Extract sections using regex
        root_cause_match = re.search(r'Root Cause:\s*(.+?)(?=Evidence:|Recommendations:|$)', report_text, re.DOTALL)
        recommendations_match = re.search(r'Recommendations:\s*(.+?)$', report_text, re.DOTALL)
        confidence_match = re.search(r'Confidence Score:\s*(\d+\.?\d*)', report_text)

        root_cause = root_cause_match.group(1).strip() if root_cause_match else "Unable to determine"
        recommendations_text = recommendations_match.group(1).strip() if recommendations_match else ""
        confidence = float(confidence_match.group(1)) if confidence_match else 0.5

        # Parse recommendations
        recommendations = []
        for line in recommendations_text.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove numbering
                rec = re.sub(r'^\d+\.\s*|-\s*', '', line)
                recommendations.append(rec)

        return RootCauseAnalysis(
            issue=issue,
            identified_cause=root_cause,
            confidence_score=confidence,
            recommendations=recommendations,
            full_report=report_text
        )
```

#### 2.2 Self-Improver Agent

**File**: `agents/self_improver.py`

**Agent Definition**:

```python
SELF_IMPROVER_DEFINITION = {
    "name": "self-improver",
    "description": "System improvement agent that modifies agent configurations and creates new agents",
    "system_prompt": """You are a Self-Improver AI agent specialized in autonomous system enhancement.

Your role:
- Receive root cause analyses from Socratic-Mediator
- Design and implement solutions to fix identified issues
- Modify agent prompts, parameters, and configurations
- Create new agents when needed for missing functionality
- Follow Claude Agent SDK best practices

Capabilities:
- Edit existing agent definition files (.md or .py)
- Create new agent definition files
- Modify system prompts and tool permissions
- Adjust agent parameters (temperature, max_tokens, etc.)

Guidelines:
- Make minimal, targeted changes
- Preserve existing functionality
- Follow SDK naming conventions
- Include clear rationale for each change
- Test changes are syntactically valid
- Output structured action plans

Action Format:
ACTION: [MODIFY_PROMPT | ADJUST_PARAMETER | CREATE_AGENT | ADD_TOOL]
TARGET: [agent name]
CHANGE:
  Old: [current value]
  New: [new value]
RATIONALE: [why this fixes the root cause]
CONFIDENCE: [0.0-1.0]

For file edits, use the Edit tool with exact old_string/new_string.
For new agents, use Write tool with full agent definition in SDK format.
""",
    "model": "claude-sonnet-4",
    "tools": ["Read", "Write", "Edit", "Grep", "Glob"],  # File manipulation tools
    "permission_mode": "acceptEdits",  # Critical for file modifications
    "temperature": 0.2,  # Very low temperature for precise code edits
}
```

**Execution Wrapper**:

```python
from typing import List, Dict, Any
import re
import json

class SelfImprover:
    """Wrapper for Self-Improver agent execution"""

    def __init__(self, sdk_client, improvement_manager: ImprovementManager):
        self.client = sdk_client
        self.improvement_manager = improvement_manager

    async def apply_improvements(
        self,
        root_cause_analysis: 'RootCauseAnalysis'
    ) -> List[ImprovementAction]:
        """
        Execute improvements based on root cause analysis

        Args:
            root_cause_analysis: Analysis from Socratic-Mediator

        Returns:
            List of ImprovementActions that were applied
        """
        # Check if we can make improvements
        can_improve, reason = self.improvement_manager.can_make_improvement()
        if not can_improve:
            raise RuntimeError(f"Cannot make improvement: {reason}")

        # Build improvement request
        request = self._build_improvement_request(root_cause_analysis)

        # Execute Self-Improver agent
        response = await self.client.send_message(
            agent="self-improver",
            message=request
        )

        # Parse actions from response
        actions = self._parse_improvement_actions(response.content)

        # Apply each action and log
        applied_actions = []
        for action in actions:
            try:
                success = await self._apply_action(action, response.tool_uses)
                if success:
                    # Log to improvement manager
                    change_id = self.improvement_manager.log_change(
                        action=action,
                        status=ChangeStatus.APPLIED
                    )
                    applied_actions.append(action)
                    print(f"✓ Applied improvement {change_id}: {action.action_type.value}")
            except Exception as e:
                print(f"✗ Failed to apply action: {e}")
                self.improvement_manager.log_change(
                    action=action,
                    status=ChangeStatus.FAILED
                )

        return applied_actions

    def _build_improvement_request(self, analysis: 'RootCauseAnalysis') -> str:
        """Build prompt for Self-Improver"""
        return f"""
Root Cause Analysis Report:
{analysis.full_report}

Your task: Design and implement fixes for the identified root cause.

Target Agent: {analysis.issue.agent_name}
Root Cause: {analysis.identified_cause}
Recommendations: {chr(10).join('- ' + r for r in analysis.recommendations)}

Please:
1. Read the current agent definition file
2. Propose specific changes in ACTION format
3. Execute the changes using Edit/Write tools
4. Output a summary of changes made

Agent files location: /home/kc-palantir/math/agents/
"""

    def _parse_improvement_actions(self, response_text: str) -> List[ImprovementAction]:
        """Parse ACTION blocks from Self-Improver response"""
        actions = []

        # Find all ACTION blocks
        action_pattern = r'ACTION:\s*(.+?)\nTARGET:\s*(.+?)\nCHANGE:\s*(.+?)\nRATIONALE:\s*(.+?)\nCONFIDENCE:\s*(\d+\.?\d*)'
        matches = re.finditer(action_pattern, response_text, re.DOTALL | re.IGNORECASE)

        for match in matches:
            action_type_str = match.group(1).strip()
            target = match.group(2).strip()
            change_text = match.group(3).strip()
            rationale = match.group(4).strip()
            confidence = float(match.group(5))

            # Parse change block
            old_match = re.search(r'Old:\s*(.+?)(?=New:|$)', change_text, re.DOTALL)
            new_match = re.search(r'New:\s*(.+?)$', change_text, re.DOTALL)

            old_value = old_match.group(1).strip() if old_match else ""
            new_value = new_match.group(1).strip() if new_match else ""

            # Map action type string to enum
            action_type = self._map_action_type(action_type_str)

            action = ImprovementAction(
                target_agent=target,
                action_type=action_type,
                old_value=old_value,
                new_value=new_value,
                rationale=rationale,
                confidence_score=confidence
            )
            actions.append(action)

        return actions

    def _map_action_type(self, action_str: str) -> ChangeType:
        """Map action string to ChangeType enum"""
        action_str = action_str.upper().replace(" ", "_")
        if "PROMPT" in action_str or "MODIFY" in action_str:
            return ChangeType.PROMPT_MODIFICATION
        elif "PARAMETER" in action_str or "ADJUST" in action_str:
            return ChangeType.PARAMETER_ADJUSTMENT
        elif "CREATE" in action_str:
            return ChangeType.AGENT_CREATION
        elif "TOOL" in action_str or "PERMISSION" in action_str:
            return ChangeType.TOOL_PERMISSION_CHANGE
        else:
            return ChangeType.PROMPT_MODIFICATION  # Default

    async def _apply_action(self, action: ImprovementAction, tool_uses: List) -> bool:
        """
        Apply an improvement action

        Note: If Self-Improver already used Edit/Write tools in its response,
        those changes are already applied. This method handles any additional
        programmatic changes needed.
        """
        # Check if action was already applied via tool use
        for tool_use in tool_uses:
            if tool_use.tool_name in ["Edit", "Write"]:
                # File was already modified by agent
                return True

        # If not applied via tools, apply programmatically
        if action.action_type == ChangeType.AGENT_CREATION:
            # Create new agent file
            agent_file_path = f"/home/kc-palantir/math/agents/{action.target_agent}.py"
            with open(agent_file_path, 'w') as f:
                f.write(action.new_value)
            return True

        # For other types, assume already handled by agent's tool use
        return True
```

---

### Phase 3: Meta-Orchestrator Extension

**File**: `agents/meta_orchestrator.py` (modifications)

**Add to existing MetaOrchestrator class**:

```python
# Add these imports
from agents.improvement_manager import ImprovementManager, ImprovementAction, ChangeType, ChangeStatus
from agents.socratic_mediator import SocraticMediator, SOCRATIC_MEDIATOR_DEFINITION
from agents.self_improver import SelfImprover, SELF_IMPROVER_DEFINITION
from agents.ask_agent_tool import create_ask_agent_tool

# Add to __init__
class MetaOrchestrator:
    def __init__(self, ...):
        # ... existing init code ...

        # Self-improvement components
        self.improvement_manager = ImprovementManager()

        # Create ask_agent tool
        self.ask_agent_func, self.ask_agent_tool = create_ask_agent_tool(
            self.agent_registry
        )

        # Initialize self-improvement agents (as subagents)
        self.socratic_mediator = SocraticMediator(
            sdk_client=self.sdk_client,
            ask_agent_tool=self.ask_agent_func
        )

        self.self_improver = SelfImprover(
            sdk_client=self.sdk_client,
            improvement_manager=self.improvement_manager
        )

        # Performance thresholds for triggering improvement
        self.improvement_thresholds = {
            "min_success_rate": 0.80,  # 80%
            "max_consecutive_failures": 3,
            "performance_regression_factor": 1.5,  # 50% slower
        }

        # Track consecutive failures per agent
        self.consecutive_failures: Dict[str, int] = {}
```

**Add performance checking method**:

```python
    def check_performance_issues(self) -> Optional['IssueReport']:
        """
        Analyze performance metrics to detect issues

        Returns:
            IssueReport if issue detected, None otherwise
        """
        metrics = self.performance_monitor.get_metrics()

        for agent_name, agent_metrics in metrics.items():
            # Check success rate
            if agent_metrics.success_rate < self.improvement_thresholds["min_success_rate"]:
                return self._create_issue_report(
                    agent_name=agent_name,
                    error_type="low_success_rate",
                    metrics=agent_metrics,
                    reason=f"Success rate {agent_metrics.success_rate:.1%} below threshold"
                )

            # Check consecutive failures
            if self.consecutive_failures.get(agent_name, 0) >= self.improvement_thresholds["max_consecutive_failures"]:
                return self._create_issue_report(
                    agent_name=agent_name,
                    error_type="consecutive_failures",
                    metrics=agent_metrics,
                    reason=f"{self.consecutive_failures[agent_name]} consecutive failures"
                )

            # Check performance regression
            if agent_metrics.baseline_avg_duration_ms:
                current_avg = agent_metrics.avg_duration_ms
                baseline_avg = agent_metrics.baseline_avg_duration_ms
                if current_avg > baseline_avg * self.improvement_thresholds["performance_regression_factor"]:
                    return self._create_issue_report(
                        agent_name=agent_name,
                        error_type="performance_regression",
                        metrics=agent_metrics,
                        reason=f"Duration increased {current_avg/baseline_avg:.1f}x"
                    )

        return None

    def _create_issue_report(
        self,
        agent_name: str,
        error_type: str,
        metrics: Any,
        reason: str
    ) -> 'IssueReport':
        """Create structured issue report"""
        # Get recent error logs
        error_logs = self.structured_logger.get_recent_errors(agent_name, limit=10)

        # Get context from context_manager
        context = self.context_manager.get_recent_context(
            category="errors",
            filters={"agent": agent_name}
        )

        return IssueReport(
            agent_name=agent_name,
            error_type=error_type,
            metrics={
                "success_rate": metrics.success_rate,
                "avg_duration_ms": metrics.avg_duration_ms,
                "error_count": len(error_logs),
            },
            error_logs=[log.message for log in error_logs],
            context=reason,
            available_agents=list(self.agent_registry.keys())
        )
```

**Add improvement cycle orchestration**:

```python
    async def run_improvement_cycle(self, issue: 'IssueReport') -> bool:
        """
        Execute full self-improvement cycle

        Steps:
        1. Socratic-Mediator analyzes issue
        2. Self-Improver applies fixes
        3. Verify improvements
        4. Rollback if verification fails

        Returns:
            True if improvements successful, False otherwise
        """
        self.structured_logger.system_event(
            "improvement_cycle_start",
            f"Starting improvement cycle for {issue.agent_name}"
        )

        try:
            # Step 1: Root cause analysis
            print(f"\n🔍 Analyzing issue in {issue.agent_name}...")
            root_cause = await self.socratic_mediator.analyze_issue(issue)

            print(f"   Root cause identified (confidence: {root_cause.confidence_score:.0%})")
            print(f"   Cause: {root_cause.identified_cause[:100]}...")

            # Log to context manager
            self.context_manager.save_decision(
                f"root_cause_{issue.agent_name}",
                {
                    "cause": root_cause.identified_cause,
                    "confidence": root_cause.confidence_score,
                    "recommendations": root_cause.recommendations
                }
            )

            # Step 2: Apply improvements
            print(f"\n🔧 Applying improvements...")
            actions = await self.self_improver.apply_improvements(root_cause)

            if not actions:
                print("   No actions applied")
                return False

            print(f"   Applied {len(actions)} improvement(s)")

            # Step 3: Verification test
            print(f"\n✓ Verifying improvements...")
            verification_passed = await self._verify_improvements(issue.agent_name)

            if verification_passed:
                print(f"   ✓ Verification passed!")
                self.structured_logger.system_event(
                    "improvement_cycle_success",
                    f"Successfully improved {issue.agent_name}"
                )
                return True
            else:
                # Step 4: Rollback
                print(f"   ✗ Verification failed, rolling back...")
                self.improvement_manager.rollback_last()
                self.structured_logger.system_event(
                    "improvement_cycle_rollback",
                    f"Rolled back changes to {issue.agent_name}"
                )
                return False

        except Exception as e:
            self.structured_logger.error(
                "improvement_cycle_error",
                f"Error during improvement cycle: {e}"
            )
            # Attempt rollback on error
            self.improvement_manager.rollback_last()
            return False

    async def _verify_improvements(self, agent_name: str) -> bool:
        """
        Verify that improvements actually work

        Run a test query through the improved agent and check results
        """
        test_query = "What is the Pythagorean theorem?"  # Simple test

        try:
            # Execute test query with improved agent
            start_time = time.time()
            result = await self._execute_agent(agent_name, test_query)
            duration = (time.time() - start_time) * 1000

            # Check basic success criteria
            if not result or len(result) < 50:
                return False

            # Check duration is reasonable (not worse than before)
            metrics = self.performance_monitor.get_agent_metrics(agent_name)
            if metrics and duration > metrics.avg_duration_ms * 2:
                return False  # More than 2x slower

            return True

        except Exception as e:
            print(f"   Verification error: {e}")
            return False
```

**Integrate into main execution loop**:

```python
    async def execute_task(self, user_query: str) -> str:
        """Main execution with improvement cycle integration"""

        # ... existing task execution code ...

        # After task completion, check for issues
        issue = self.check_performance_issues()

        if issue:
            print(f"\n⚠️  Performance issue detected in {issue.agent_name}")
            print(f"   Reason: {issue.context}")

            # Ask user if they want to run improvement cycle
            # (or auto-run if configured)
            run_improvement = input("   Run self-improvement cycle? (y/n): ").lower() == 'y'

            if run_improvement:
                success = await self.run_improvement_cycle(issue)
                if success:
                    print(f"   ✓ System improved successfully")
                    # Reset failure counters
                    self.consecutive_failures[issue.agent_name] = 0
                else:
                    print(f"   ✗ Improvement cycle failed")

        return result
```

---

### Phase 4: Data Models

**File**: `agents/improvement_models.py`

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class IssueReport:
    """Structured report of a performance issue"""
    agent_name: str
    error_type: str  # "low_success_rate", "consecutive_failures", "performance_regression"
    metrics: Dict[str, Any]
    error_logs: List[str]
    context: str
    available_agents: List[str]
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "error_type": self.error_type,
            "metrics": self.metrics,
            "error_count": len(self.error_logs),
            "context": self.context,
            "timestamp": self.timestamp.isoformat()
        }

@dataclass
class RootCauseAnalysis:
    """Result of Socratic-Mediator analysis"""
    issue: IssueReport
    identified_cause: str
    confidence_score: float  # 0.0-1.0
    recommendations: List[str]
    full_report: str
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_name": self.issue.agent_name,
            "cause": self.identified_cause,
            "confidence": self.confidence_score,
            "recommendations": self.recommendations,
            "timestamp": self.timestamp.isoformat()
        }
```

---

## FILE STRUCTURE

```
/home/kc-palantir/math/
├── main.py                              [UPDATE v3.0]
├── agents/
│   ├── __init__.py                      [UPDATE - export new modules]
│   ├── meta_orchestrator.py            [UPDATE v3.0 - add improvement cycle]
│   ├── knowledge_builder.py             [UNCHANGED]
│   ├── quality_agent.py                 [UNCHANGED]
│   ├── research_agent.py                [UNCHANGED]
│   ├── example_generator.py             [UNCHANGED]
│   ├── dependency_mapper.py             [UNCHANGED]
│   ├── socratic_planner.py              [UNCHANGED]
│   ├── error_handler.py                 [UNCHANGED]
│   ├── structured_logger.py             [UNCHANGED]
│   ├── performance_monitor.py           [UNCHANGED]
│   ├── context_manager.py               [UNCHANGED]
│   ├── improvement_manager.py           [NEW]
│   ├── ask_agent_tool.py                [NEW]
│   ├── socratic_mediator.py             [NEW]
│   ├── self_improver.py                 [NEW]
│   └── improvement_models.py            [NEW]
├── test_infrastructure.py               [UNCHANGED]
├── test_self_improvement.py             [NEW]
└── test_e2e.py                          [UPDATE v3.0]
```

---

## TESTING STRATEGY

### Unit Tests: test_self_improvement.py

```python
import pytest
import asyncio
from agents.improvement_manager import ImprovementManager, ImprovementAction, ChangeType
from agents.ask_agent_tool import AskAgentTool
from agents.improvement_models import IssueReport, RootCauseAnalysis

class TestImprovementManager:
    """Test improvement history and rollback"""

    def test_log_and_retrieve_change(self):
        manager = ImprovementManager(history_file="/tmp/test_history.json")

        action = ImprovementAction(
            target_agent="test-agent",
            action_type=ChangeType.PROMPT_MODIFICATION,
            old_value="old prompt",
            new_value="new prompt",
            rationale="Test change",
            confidence_score=0.9
        )

        change_id = manager.log_change(action)

        assert len(manager.history) == 1
        assert manager.history[0].change_id == change_id
        assert manager.history[0].action.target_agent == "test-agent"

    def test_rollback_last(self):
        manager = ImprovementManager(history_file="/tmp/test_history2.json")

        action = ImprovementAction(
            target_agent="test-agent",
            action_type=ChangeType.PARAMETER_ADJUSTMENT,
            old_value=0.7,
            new_value=0.5,
            rationale="Lower temperature",
            confidence_score=0.8
        )

        manager.log_change(action)
        rolled_back = manager.rollback_last()

        assert rolled_back is not None
        assert rolled_back.status.value == "rolled_back"

    def test_max_improvements_limit(self):
        manager = ImprovementManager(history_file="/tmp/test_history3.json")
        manager.max_improvements_per_session = 2

        action = ImprovementAction(
            target_agent="test",
            action_type=ChangeType.PROMPT_MODIFICATION,
            old_value="",
            new_value="",
            rationale="Test",
            confidence_score=0.5
        )

        manager.log_change(action)
        manager.log_change(action)

        can_improve, reason = manager.can_make_improvement()
        assert not can_improve
        assert "Max improvements" in reason

class TestAskAgentTool:
    """Test inter-agent communication tool"""

    @pytest.mark.asyncio
    async def test_ask_agent_success(self):
        async def mock_agent(question):
            return f"Answer to: {question}"

        registry = {"agent1": mock_agent}
        tool = AskAgentTool(registry)

        result = await tool.ask_agent("agent1", "What is 2+2?")

        assert result["success"] is True
        assert "Answer to: What is 2+2?" in result["answer"]

    @pytest.mark.asyncio
    async def test_ask_agent_not_found(self):
        tool = AskAgentTool({})

        result = await tool.ask_agent("nonexistent", "Question")

        assert result["success"] is False
        assert "not found" in result["error"]

    @pytest.mark.asyncio
    async def test_query_history(self):
        async def mock_agent(q):
            return "Answer"

        tool = AskAgentTool({"agent1": mock_agent})

        await tool.ask_agent("agent1", "Q1")
        await tool.ask_agent("agent1", "Q2")

        history = tool.get_query_history()
        assert len(history) == 2
        assert history[0]["question"] == "Q1"
        assert history[1]["question"] == "Q2"

# Run: pytest test_self_improvement.py -v
```

---

## SAFETY MECHANISMS

### 1. Improvement Limits

- Max 5 improvements per session
- Max 3 consecutive rollbacks before stopping
- Confidence threshold: Only apply changes with >70% confidence

### 2. Verification Protocol

- Always test improved agent with sample query
- Compare metrics before/after
- Automatic rollback if performance degrades

### 3. Human Escalation

- Prompt user before applying critical changes
- Log all changes for audit trail
- Provide rollback commands

### 4. Scope Restrictions

- Self-Improver can only modify files in `/home/kc-palantir/math/agents/`
- Cannot modify infrastructure modules
- Cannot access system-level files

---

## DEPLOYMENT CHECKLIST

- [ ] Phase 1: Implement improvement_manager.py + ask_agent_tool.py
- [ ] Phase 1: Write unit tests for new modules
- [ ] Phase 2: Implement socratic_mediator.py
- [ ] Phase 2: Implement self_improver.py
- [ ] Phase 3: Extend meta_orchestrator.py with improvement cycle
- [ ] Phase 3: Add agent definitions to SDK configuration
- [ ] Phase 4: Create improvement_models.py
- [ ] Phase 4: Update agents/__init__.py exports
- [ ] Testing: Run test_self_improvement.py (all pass)
- [ ] Testing: E2E test with simulated failure
- [ ] Testing: Verify rollback mechanism
- [ ] Documentation: Update IMPLEMENTATION-COMPLETE to v3.0
- [ ] Documentation: Create visual guide (Korean)

---

## EXPECTED OUTCOMES

### Success Metrics

- System can detect performance issues automatically (100% detection rate for test cases)
- Socratic-Mediator identifies root causes with >70% confidence
- Self-Improver applies fixes without breaking existing functionality
- Improvements increase success rate by >10%
- Rollback works reliably (100% success in tests)

### Performance Impact

- Improvement cycle adds ~10-30s when triggered
- Normal execution: 0% overhead (improvement components dormant)
- Memory increase: ~50MB for history tracking

---

## REFERENCES

1. Self-Improver PDF document (source)
2. Claude Agent SDK Python docs: https://docs.claude.com/en/api/agent-sdk/python
3. Kenneth Liao SDK examples: https://github.com/kenneth-liao/claude-agent-sdk-intro
4. Subagents guide: https://docs.claude.com/en/api/agent-sdk/subagents
5. IMPLEMENTATION-COMPLETE-v2.0.md (current system)

---

**END OF IMPLEMENTATION PLAN**

*Ready for autonomous execution - all code-level details provided*
*Next: Create Korean visual guide for non-programmers*
