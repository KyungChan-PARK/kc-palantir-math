# Phase 3: Detailed Implementation Specifications

**Version**: 1.0
**Date**: 2025-10-14
**Purpose**: Complete implementation details for Improvements #5 and #6

---

## Overview

Phase 3 improvements (#5 HITL, #6 Parallel Q&A) were marked as placeholders in CODE-IMPROVEMENT-PLAN.md. This document provides complete, implementation-ready specifications.

---

## Improvement #5: HITL Checkpoint Framework

### Problem Statement

All improvements are auto-applied without human review checkpoints. Critical decisions (new relationship types, high-risk changes, ontology modifications) lack expert oversight.

### Impact

- Risk: Automated mistakes on high-impact decisions
- No human validation for system-level changes
- Difficult to trust fully automated self-improvement

### Solution Design

**Human-in-the-Loop (HITL) Framework**: Strategic checkpoints that pause workflow for human review on critical decisions only.

**Design Principles**:
1. **Minimal Disruption**: Only critical decisions trigger checkpoints (<10% of improvements)
2. **Async-Ready**: Checkpoints don't block other work
3. **Context-Aware**: Integration with Quality Gate (#3) and Ontology (#4)
4. **Recoverable**: Full checkpoint state saved for resume

---

### Architecture

```
MetaOrchestrator
    ↓
evaluate_quality_gate() → QualityGateApproval
    ↓
should_trigger_hitl() → Boolean
    ↓ (if True)
create_checkpoint() → HITLCheckpoint
    ↓
save_checkpoint() → checkpoint.json
    ↓
[WORKFLOW PAUSED - Waiting for human input]
    ↓
Human reviews via CLI/Web UI
    ↓
load_checkpoint() → HITLCheckpoint
    ↓
apply_human_decision() → Resume workflow
```

---

### Implementation

#### File 1: `agents/hitl_checkpoints.py` (New)

```python
"""
Human-in-the-Loop (HITL) Checkpoint Framework

Provides strategic human review checkpoints for critical decisions.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Literal
from pathlib import Path
import json
import uuid
from datetime import datetime

@dataclass
class HITLCheckpoint:
    """Human review checkpoint"""

    checkpoint_id: str
    created_at: str
    agent_name: str
    decision_type: Literal[
        "new_relationship_type",
        "ontology_modification",
        "high_risk_improvement",
        "quality_gate_override",
        "system_architecture_change"
    ]
    decision_context: Dict
    options: List[Dict]  # List of choices for human
    recommended_action: str
    risk_level: Literal["high", "critical"]
    impact_scope: str
    status: Literal["pending", "approved", "rejected", "cancelled"]
    human_decision: Optional[Dict] = None
    decided_at: Optional[str] = None
    decided_by: Optional[str] = None

    def to_dict(self) -> Dict:
        """Serialize to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "HITLCheckpoint":
        """Deserialize from dictionary"""
        return cls(**data)


class HITLCheckpointManager:
    """Manage HITL checkpoints"""

    def __init__(self, checkpoint_dir: Path = Path("checkpoints")):
        self.checkpoint_dir = checkpoint_dir
        self.checkpoint_dir.mkdir(exist_ok=True)

    def create_checkpoint(
        self,
        agent_name: str,
        decision_type: str,
        decision_context: Dict,
        options: List[Dict],
        recommended_action: str,
        risk_level: str,
        impact_scope: str
    ) -> HITLCheckpoint:
        """
        Create a new HITL checkpoint

        Args:
            agent_name: Name of the agent requiring review
            decision_type: Type of decision (see HITLCheckpoint.decision_type)
            decision_context: Full context about the decision
            options: List of possible actions
            recommended_action: System's recommended choice
            risk_level: "high" or "critical"
            impact_scope: Description of impact (e.g., "500+ relationships")

        Returns:
            HITLCheckpoint object
        """
        checkpoint = HITLCheckpoint(
            checkpoint_id=str(uuid.uuid4()),
            created_at=datetime.now().isoformat(),
            agent_name=agent_name,
            decision_type=decision_type,
            decision_context=decision_context,
            options=options,
            recommended_action=recommended_action,
            risk_level=risk_level,
            impact_scope=impact_scope,
            status="pending"
        )

        # Save to disk
        self.save_checkpoint(checkpoint)

        return checkpoint

    def save_checkpoint(self, checkpoint: HITLCheckpoint):
        """Save checkpoint to disk"""
        file_path = self.checkpoint_dir / f"{checkpoint.checkpoint_id}.json"
        with open(file_path, 'w') as f:
            json.dump(checkpoint.to_dict(), f, indent=2)

    def load_checkpoint(self, checkpoint_id: str) -> HITLCheckpoint:
        """Load checkpoint from disk"""
        file_path = self.checkpoint_dir / f"{checkpoint_id}.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Checkpoint {checkpoint_id} not found")

        with open(file_path) as f:
            data = json.load(f)

        return HITLCheckpoint.from_dict(data)

    def list_pending_checkpoints(self) -> List[HITLCheckpoint]:
        """List all pending checkpoints"""
        checkpoints = []

        for file_path in self.checkpoint_dir.glob("*.json"):
            with open(file_path) as f:
                data = json.load(f)

            checkpoint = HITLCheckpoint.from_dict(data)
            if checkpoint.status == "pending":
                checkpoints.append(checkpoint)

        # Sort by creation time (oldest first)
        checkpoints.sort(key=lambda c: c.created_at)

        return checkpoints

    def approve_checkpoint(
        self,
        checkpoint_id: str,
        chosen_action: str,
        decided_by: str,
        notes: Optional[str] = None
    ) -> HITLCheckpoint:
        """
        Approve a checkpoint with chosen action

        Args:
            checkpoint_id: Checkpoint ID
            chosen_action: The action human chose
            decided_by: Name/ID of decision maker
            notes: Optional notes from human reviewer

        Returns:
            Updated checkpoint
        """
        checkpoint = self.load_checkpoint(checkpoint_id)

        checkpoint.status = "approved"
        checkpoint.human_decision = {
            "action": chosen_action,
            "notes": notes
        }
        checkpoint.decided_at = datetime.now().isoformat()
        checkpoint.decided_by = decided_by

        self.save_checkpoint(checkpoint)

        return checkpoint

    def reject_checkpoint(
        self,
        checkpoint_id: str,
        reason: str,
        decided_by: str
    ) -> HITLCheckpoint:
        """
        Reject a checkpoint

        Args:
            checkpoint_id: Checkpoint ID
            reason: Reason for rejection
            decided_by: Name/ID of decision maker

        Returns:
            Updated checkpoint
        """
        checkpoint = self.load_checkpoint(checkpoint_id)

        checkpoint.status = "rejected"
        checkpoint.human_decision = {
            "action": "reject",
            "reason": reason
        }
        checkpoint.decided_at = datetime.now().isoformat()
        checkpoint.decided_by = decided_by

        self.save_checkpoint(checkpoint)

        return checkpoint


class HITLCheckpointRequired(Exception):
    """Exception raised when HITL checkpoint is required"""

    def __init__(self, checkpoint: HITLCheckpoint):
        self.checkpoint = checkpoint
        super().__init__(
            f"HITL checkpoint required: {checkpoint.decision_type} "
            f"(ID: {checkpoint.checkpoint_id})"
        )


def should_trigger_hitl_checkpoint(
    improvement: Dict,
    quality_gate_result: Optional[Dict] = None
) -> bool:
    """
    Determine if HITL checkpoint should be triggered

    Args:
        improvement: Improvement proposal
        quality_gate_result: Result from evaluate_quality_gate()

    Returns:
        True if checkpoint required
    """

    # Checkpoint Trigger Conditions:

    # 1. New relationship type proposal
    if improvement.get("type") == "new_relationship_type":
        return True

    # 2. Ontology modification
    ontology_files = [
        "agents/relationship_ontology.py",
        "agents/quality_agent.py"
    ]
    if any(f in improvement.get("affected_files", []) for f in ontology_files):
        return True

    # 3. High-risk improvement (affects 500+ relationships)
    if improvement.get("impact_scope", {}).get("affected_relationships", 0) >= 500:
        return True

    # 4. Quality gate failed but override requested
    if quality_gate_result:
        if not quality_gate_result.get("passed") and improvement.get("force_override"):
            return True

        # Critical files with failed gate
        if quality_gate_result.get("metrics", {}).get("max_criticality", 0) >= 9:
            if not quality_gate_result.get("passed"):
                return True

    # 5. System architecture change
    architecture_files = [
        "agents/meta_orchestrator.py",
        "main.py",
        "agents/improvement_models.py"
    ]
    if any(f in improvement.get("affected_files", []) for f in architecture_files):
        return True

    return False


def format_checkpoint_for_review(checkpoint: HITLCheckpoint) -> str:
    """
    Format checkpoint for human review (CLI display)

    Returns:
        Formatted string for terminal display
    """

    lines = [
        "=" * 60,
        "🚨 HUMAN REVIEW REQUIRED 🚨",
        "=" * 60,
        "",
        f"Checkpoint ID: {checkpoint.checkpoint_id}",
        f"Agent: {checkpoint.agent_name}",
        f"Decision Type: {checkpoint.decision_type}",
        f"Risk Level: {checkpoint.risk_level.upper()}",
        f"Impact Scope: {checkpoint.impact_scope}",
        "",
        "Context:",
        "-" * 60,
    ]

    for key, value in checkpoint.decision_context.items():
        lines.append(f"{key}: {value}")

    lines.extend([
        "",
        "Options:",
        "-" * 60,
    ])

    for i, option in enumerate(checkpoint.options, 1):
        lines.append(f"{i}. {option['name']}")
        lines.append(f"   {option['description']}")
        if option.get("consequences"):
            lines.append(f"   Consequences: {option['consequences']}")
        lines.append("")

    lines.extend([
        f"Recommended: {checkpoint.recommended_action}",
        "",
        "=" * 60,
        "",
        "Commands:",
        f"  Approve: python -m agents.hitl_cli approve {checkpoint.checkpoint_id} --action <action>",
        f"  Reject:  python -m agents.hitl_cli reject {checkpoint.checkpoint_id} --reason <reason>",
        ""
    ])

    return "\n".join(lines)
```

---

#### File 2: `agents/hitl_cli.py` (New - CLI Interface)

```python
"""
CLI interface for HITL checkpoint management
"""

import argparse
from pathlib import Path
from agents.hitl_checkpoints import HITLCheckpointManager, format_checkpoint_for_review


def main():
    parser = argparse.ArgumentParser(description="HITL Checkpoint Manager")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # List pending checkpoints
    list_parser = subparsers.add_parser("list", help="List pending checkpoints")

    # Approve checkpoint
    approve_parser = subparsers.add_parser("approve", help="Approve a checkpoint")
    approve_parser.add_argument("checkpoint_id", help="Checkpoint ID")
    approve_parser.add_argument("--action", required=True, help="Chosen action")
    approve_parser.add_argument("--by", default="human", help="Decision maker name")
    approve_parser.add_argument("--notes", help="Optional notes")

    # Reject checkpoint
    reject_parser = subparsers.add_parser("reject", help="Reject a checkpoint")
    reject_parser.add_argument("checkpoint_id", help="Checkpoint ID")
    reject_parser.add_argument("--reason", required=True, help="Rejection reason")
    reject_parser.add_argument("--by", default="human", help="Decision maker name")

    # Show checkpoint details
    show_parser = subparsers.add_parser("show", help="Show checkpoint details")
    show_parser.add_argument("checkpoint_id", help="Checkpoint ID")

    args = parser.parse_args()

    manager = HITLCheckpointManager()

    if args.command == "list":
        checkpoints = manager.list_pending_checkpoints()
        if not checkpoints:
            print("✅ No pending checkpoints")
        else:
            print(f"📋 {len(checkpoints)} pending checkpoint(s):\n")
            for cp in checkpoints:
                print(f"ID: {cp.checkpoint_id}")
                print(f"  Agent: {cp.agent_name}")
                print(f"  Type: {cp.decision_type}")
                print(f"  Risk: {cp.risk_level}")
                print(f"  Created: {cp.created_at}")
                print()

    elif args.command == "approve":
        checkpoint = manager.approve_checkpoint(
            args.checkpoint_id,
            args.action,
            args.by,
            args.notes
        )
        print(f"✅ Checkpoint {args.checkpoint_id} approved")
        print(f"   Action: {args.action}")
        print(f"   By: {args.by}")

    elif args.command == "reject":
        checkpoint = manager.reject_checkpoint(
            args.checkpoint_id,
            args.reason,
            args.by
        )
        print(f"❌ Checkpoint {args.checkpoint_id} rejected")
        print(f"   Reason: {args.reason}")
        print(f"   By: {args.by}")

    elif args.command == "show":
        checkpoint = manager.load_checkpoint(args.checkpoint_id)
        formatted = format_checkpoint_for_review(checkpoint)
        print(formatted)


if __name__ == "__main__":
    main()
```

---

#### File 3: Integration into `agents/meta_orchestrator.py`

**Modify the `apply_improvement` method** (around line 300):

```python
from agents.hitl_checkpoints import (
    HITLCheckpointManager,
    HITLCheckpointRequired,
    should_trigger_hitl_checkpoint,
    format_checkpoint_for_review
)

class MetaOrchestrator:
    """Meta-orchestrator with HITL integration"""

    def __init__(self):
        # ... existing init ...
        self.hitl_manager = HITLCheckpointManager()

    def apply_improvement(
        self,
        improvement: Improvement,
        quality_gate_result: Optional[QualityGateApproval] = None
    ) -> ImprovementResult:
        """
        Apply improvement with HITL checkpoint support

        Args:
            improvement: Improvement to apply
            quality_gate_result: Optional quality gate result

        Returns:
            ImprovementResult

        Raises:
            HITLCheckpointRequired: If human review needed
        """

        # Check if HITL checkpoint should be triggered
        if should_trigger_hitl_checkpoint(improvement.to_dict(), quality_gate_result):
            # Create checkpoint
            checkpoint = self.hitl_manager.create_checkpoint(
                agent_name=improvement.agent_name,
                decision_type=self._determine_decision_type(improvement),
                decision_context={
                    "improvement_id": improvement.improvement_id,
                    "description": improvement.description,
                    "affected_files": improvement.affected_files,
                    "estimated_impact": improvement.estimated_impact,
                    "quality_gate_passed": quality_gate_result.passed if quality_gate_result else None
                },
                options=self._generate_options(improvement),
                recommended_action=improvement.recommended_action,
                risk_level=self._assess_risk_level(improvement, quality_gate_result),
                impact_scope=improvement.impact_scope
            )

            # Print checkpoint for review
            print("\n" + format_checkpoint_for_review(checkpoint))

            # Raise exception to pause workflow
            raise HITLCheckpointRequired(checkpoint)

        # No checkpoint needed, proceed with improvement
        return self._execute_improvement(improvement)

    def resume_from_checkpoint(self, checkpoint_id: str) -> ImprovementResult:
        """
        Resume workflow after human approval

        Args:
            checkpoint_id: Checkpoint ID

        Returns:
            ImprovementResult
        """

        checkpoint = self.hitl_manager.load_checkpoint(checkpoint_id)

        if checkpoint.status != "approved":
            raise ValueError(f"Checkpoint {checkpoint_id} not approved (status: {checkpoint.status})")

        # Reconstruct improvement from checkpoint context
        improvement = self._reconstruct_improvement(checkpoint.decision_context)

        # Apply human decision
        if checkpoint.human_decision:
            improvement.apply_human_modifications(checkpoint.human_decision)

        # Execute improvement
        return self._execute_improvement(improvement)

    def _determine_decision_type(self, improvement: Improvement) -> str:
        """Determine HITL decision type from improvement"""

        if improvement.type == "new_relationship_type":
            return "new_relationship_type"

        ontology_files = ["agents/relationship_ontology.py", "agents/quality_agent.py"]
        if any(f in improvement.affected_files for f in ontology_files):
            return "ontology_modification"

        if improvement.estimated_impact.get("affected_relationships", 0) >= 500:
            return "high_risk_improvement"

        architecture_files = ["agents/meta_orchestrator.py", "main.py"]
        if any(f in improvement.affected_files for f in architecture_files):
            return "system_architecture_change"

        return "quality_gate_override"

    def _generate_options(self, improvement: Improvement) -> List[Dict]:
        """Generate human-readable options"""

        return [
            {
                "name": "proceed",
                "description": "Proceed with the improvement as proposed",
                "consequences": "System will apply changes immediately"
            },
            {
                "name": "modify",
                "description": "Proceed with modifications",
                "consequences": "You will be prompted to specify modifications"
            },
            {
                "name": "reject",
                "description": "Reject the improvement",
                "consequences": "No changes will be made"
            },
            {
                "name": "defer",
                "description": "Defer decision for later review",
                "consequences": "Checkpoint remains pending"
            }
        ]

    def _assess_risk_level(
        self,
        improvement: Improvement,
        quality_gate_result: Optional[QualityGateApproval]
    ) -> str:
        """Assess risk level (high or critical)"""

        # Critical if mission-critical files affected
        if quality_gate_result:
            if quality_gate_result.metrics.get("max_criticality", 0) >= 10:
                return "critical"

        # Critical if 1000+ relationships affected
        if improvement.estimated_impact.get("affected_relationships", 0) >= 1000:
            return "critical"

        return "high"
```

---

### Usage Example

```python
# In main.py or improvement pipeline

orchestrator = MetaOrchestrator()

try:
    result = orchestrator.apply_improvement(improvement, quality_gate_result)
    print(f"✅ Improvement applied: {result.improvement_id}")

except HITLCheckpointRequired as exc:
    print(f"⏸️  Workflow paused: Human review required")
    print(f"   Checkpoint ID: {exc.checkpoint.checkpoint_id}")
    print(f"   Use CLI to review: python -m agents.hitl_cli show {exc.checkpoint.checkpoint_id}")

    # Workflow pauses here. Human reviews via CLI.
    # After approval, resume:

    checkpoint_id = exc.checkpoint.checkpoint_id
    result = orchestrator.resume_from_checkpoint(checkpoint_id)
    print(f"✅ Resumed and completed: {result.improvement_id}")
```

---

### CLI Workflow

```bash
# 1. List pending checkpoints
python -m agents.hitl_cli list

# Output:
# 📋 1 pending checkpoint(s):
#
# ID: a3f2e8d9-...
#   Agent: relationship_definer
#   Type: ontology_modification
#   Risk: critical
#   Created: 2025-10-14T15:30:00

# 2. Show checkpoint details
python -m agents.hitl_cli show a3f2e8d9-...

# Output:
# 🚨 HUMAN REVIEW REQUIRED 🚨
# [Full formatted checkpoint]

# 3. Approve
python -m agents.hitl_cli approve a3f2e8d9-... --action proceed --by alice --notes "Reviewed and looks good"

# Output:
# ✅ Checkpoint a3f2e8d9-... approved
#    Action: proceed
#    By: alice

# 4. Or reject
python -m agents.hitl_cli reject a3f2e8d9-... --reason "Impact scope too large, needs refinement" --by alice
```

---

### Testing Strategy

See `docs/TESTING-STRATEGY.md` Section "Improvement #5" for unit and integration tests.

---

### Implementation Effort

- **File Creation**: 2 files (~600 lines total)
- **Integration**: 1 file modification (~100 lines)
- **Testing**: 4 test files
- **Total Time**: 12-16 hours

---

## Improvement #6: Parallel Socratic Q&A

### Problem Statement

Sequential Task calls in `socratic_mediator_agent.py` (lines 60-69) incur 90% latency penalty vs parallel execution.

**Current (Sequential)**:
```
Task 1 → 15s
Task 2 → 15s
Task 3 → 15s
Total: 45s
```

**Desired (Parallel)**:
```
Task 1, Task 2, Task 3 (in parallel) → 15s
Total: 15s (67% reduction)
```

### Impact

- Long wait times for multi-question analysis
- Poor user experience
- Inefficient use of Agent SDK

### Solution Design

Enhance `socratic_mediator_agent.py` prompt to include explicit parallel Task examples and instructions.

---

### Implementation

#### Modification to `agents/socratic_mediator_agent.py`

**Location**: Lines 60-74 (prompt section)

**Current Code**:
```python
**First questions** (ask in parallel using Task tool):
1. Target agent: "What is your current success rate and typical execution time?"
2. Target agent: "What are the most common errors you encounter?"
3. Target agent: "Are there any patterns in when failures occur?"

**Follow-up questions** (based on answers):
- If timeout issues → "Which operations are taking the longest?"
- If input errors → "What input validation do you perform?"
- If dependency issues → "Which tools or agents do you depend on?"

**Use Task tool to delegate questions**:
```
Task:
- agent_name: "knowledge-builder"
- task: "Answer this question: What is your current success rate?"
```
```

**New Code** (replace lines 60-74):

```python
**First questions** (ask in parallel using multiple Task tools):

IMPORTANT: To ask multiple questions in parallel, use multiple Task tool calls in a SINGLE response.

**Example - Parallel Task calls** (✅ CORRECT):

Use 3 Task tools simultaneously in one response:

Task tool #1:
- subagent_type: "general-purpose"
- description: "Query agent performance"
- prompt: """
Ask the knowledge-builder agent:
"What is your current success rate and typical execution time?"

Wait for its response and report back.
"""

Task tool #2:
- subagent_type: "general-purpose"
- description: "Query error patterns"
- prompt: """
Ask the knowledge-builder agent:
"What are the most common errors you encounter?"

Wait for its response and report back.
"""

Task tool #3:
- subagent_type: "general-purpose"
- description: "Query failure patterns"
- prompt: """
Ask the knowledge-builder agent:
"Are there any patterns in when failures occur?"

Wait for its response and report back.
"""

This will execute all 3 questions in parallel (~15s total instead of 45s sequential).

**Example - Sequential Task calls** (❌ INCORRECT):

Do NOT call Task, wait for response, then call Task again:

Task → wait → Task → wait → Task
(This takes 3x longer)

**Follow-up questions** (based on parallel results):

After receiving all 3 answers from the parallel Tasks:
- Analyze patterns across all responses
- If timeout issues detected → Ask: "Which operations are taking the longest?"
- If input errors detected → Ask: "What input validation do you perform?"
- If dependency issues detected → Ask: "Which tools or agents do you depend on?"

Follow-ups can be parallel if independent, or sequential if they depend on previous answers.
```

---

### Enhanced Examples Section

**Add to prompt** (after line 208):

```python
## Example 1: Parallel First Questions

```
Issue: knowledge-builder has 30% success rate

You: [Make 3 parallel Task calls in single response]

Task #1: Query knowledge-builder about success rate
Task #2: Query knowledge-builder about error patterns
Task #3: Query knowledge-builder about failure timing

[Wait for all 3 responses - takes ~15s total]

Responses received:
1. "Success rate drops on complex theorems (>3 variables)"
2. "Most errors: 'LaTeX parsing failed' (60% of failures)"
3. "Failures spike during evening hours (7-10pm)"

Analysis: LaTeX parsing is the root cause, exacerbated by complex input.

Follow-up (single sequential Task):
Task: Ask knowledge-builder "What LaTeX validation do you perform before processing?"

Response: "No validation for nested commands"

Root Cause Identified: Missing LaTeX validation for nested structures
```

## Example 2: When NOT to Use Parallel

```
Issue: research-agent timeout after 180s

You: [Single Task to query timeout details]

Task: Ask research-agent "At what point in your workflow does the 180s timeout occur?"

Response: "During web search for obscure mathematical terms"

[Based on this answer, need to ask follow-up about web search]

You: [Sequential Task - depends on previous answer]

Task: Ask research-agent "What is your web search timeout configuration?"

Response: "300s per search, but I make multiple searches"

Analysis: Multiple 300s searches → exceeds overall 180s limit

Root Cause Identified: Web search timeout configuration > overall agent timeout
```

In this case, questions were sequential because each answer informed the next question.
```

---

### Code Review Checklist

When implementing Parallel Q&A, verify:

- ✅ Prompt explicitly mentions "multiple Task tools in SINGLE response"
- ✅ Example shows 3 Task tools in one message
- ✅ Counter-example shows what NOT to do (sequential)
- ✅ Guidance on when to use parallel vs sequential
- ✅ Real-world examples with realistic agent responses

---

### Testing Strategy

See `docs/TESTING-STRATEGY.md` Section "Improvement #6" for integration tests.

Key test: Verify latency reduction

```python
def test_parallel_reduces_latency():
    """Verify parallel execution is 3-5x faster"""

    questions = [
        "What is your success rate?",
        "What errors occur?",
        "When do failures happen?"
    ]

    # Sequential baseline
    start = time.time()
    sequential_results = mediator.ask_sequential(questions)
    seq_time = time.time() - start

    # Parallel improved
    start = time.time()
    parallel_results = mediator.ask_parallel(questions)
    par_time = time.time() - start

    # Verify 3-5x speedup
    assert par_time <= seq_time * 0.33  # At least 67% reduction
    assert parallel_results == sequential_results  # Same answers
```

---

### Implementation Effort

- **File Modification**: 1 file (`socratic_mediator_agent.py`)
- **Lines Changed**: ~30 lines (prompt enhancement)
- **Testing**: 2 integration tests
- **Total Time**: 2-4 hours

---

## Summary

| Improvement | Files Created | Files Modified | Lines of Code | Effort (hrs) |
|------------|--------------|----------------|---------------|--------------|
| #5 HITL Framework | 2 new | 1 modified | ~700 lines | 12-16 |
| #6 Parallel Q&A | 0 new | 1 modified | ~30 lines | 2-4 |
| **Total** | **2 new** | **2 modified** | **~730 lines** | **14-20 hrs** |

---

## Dependencies

### #5 HITL Framework

**Depends on**:
- #3 Dynamic Quality Gate (for criticality-aware checkpoints)
- #4 Ontology + QualityAgent (for ontology modification detection)

**Can proceed without**: Yes, but will have less intelligent checkpoint triggering

### #6 Parallel Q&A

**Depends on**:
- #1 Uncertainty Modeling (for targeted question generation)

**Can proceed without**: Yes, but questions will be generic

---

## Rollback Procedures

See `docs/ROLLBACK-PROCEDURES.md`:
- #5 HITL: Remove 2 new files, revert meta_orchestrator.py (35 min recovery)
- #6 Parallel: Revert socratic_mediator_agent.py prompt (25 min recovery)

---

## Testing Strategy

See `docs/TESTING-STRATEGY.md`:
- #5 HITL: Unit tests (checkpoint logic), Integration tests (workflow pause/resume)
- #6 Parallel: Integration tests (latency measurement, result consistency)

---

## Success Criteria

### #5 HITL Framework

- ✅ 100% critical decision coverage (all 5 test scenarios trigger checkpoints)
- ✅ <20% false trigger rate (non-critical decisions not blocked)
- ✅ Workflow pause/resume functional
- ✅ CLI interface working
- ✅ Checkpoint state fully recoverable

### #6 Parallel Q&A

- ✅ Latency reduction >= 67% (3x faster)
- ✅ Results identical to sequential execution
- ✅ No increase in error rate
- ✅ Prompt clearly instructs parallel Task usage

---

## Next Steps

1. Review this specification
2. Approve for implementation
3. Implement #5 HITL (Week 5-6 of roadmap)
4. Implement #6 Parallel (Week 7 of roadmap)
5. Integration testing (Week 8 of roadmap)

---

**Document Status**: Implementation Ready
**Requires Approval**: Yes
**Estimated Total Effort**: 14-20 hours across 3-4 weeks
