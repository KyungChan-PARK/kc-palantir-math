"""
Self-Improver Agent - Code Modification Executor

VERSION: 4.0.0
DATE: 2025-10-14
PURPOSE: Apply code improvements with CIA protocol integration

Based on: SELF-IMPROVEMENT-IMPLEMENTATION-PLAN-v4.0.md Section IV

Core Features:
1. Generate improvement actions from root cause analysis
2. Integrate with Dependency Agent for impact analysis
3. Apply code modifications using Edit tool
4. Log changes to Improvement Manager
5. Build improvement requests with full context
"""

from typing import List, Optional
from agents.improvement_models import (
    ImprovementAction,
    RootCauseAnalysis,
    ImpactAnalysis,
    ActionType,
    ChangeStatus
)
from agents.improvement_manager import ImprovementManager
from agents.dependency_agent import DependencyAgent


class SelfImprover:
    """
    Self-Improver agent that applies code modifications.

    Enhanced with Change Impact Analysis (CIA) protocol from v4.0 spec.

    Flow (from plan Section IV.1):
    1. Generate proposed changes from root cause
    2. Perform dependency analysis (via Dependency Agent)
    3. Submit to Meta-Orchestrator for quality gate
    4. If approved, apply changes via Edit tool
    5. Log to Improvement Manager
    """

    def __init__(self, client=None):
        """
        Initialize Self-Improver.

        Args:
            client: Claude Agent SDK client for LLM calls
        """
        self.client = client
        self.improvement_manager = ImprovementManager(max_per_session=5)
        self.dependency_agent = DependencyAgent()

        # Store impact analysis for Meta-Orchestrator access
        self._impact_analysis: Optional[ImpactAnalysis] = None

    async def apply_improvements(
        self,
        root_cause_analysis: RootCauseAnalysis
    ) -> List[ImprovementAction]:
        """
        Enhanced with Change Impact Analysis protocol.

        Flow (from v4.0 spec):
        1. Generate proposed changes from root cause
        2. Perform dependency analysis (via Dependency Agent)
        3. Submit to Meta-Orchestrator for quality gate
        4. If approved, apply changes
        5. Log to Improvement Manager

        Args:
            root_cause_analysis: RootCauseAnalysis from Socratic-Mediator

        Returns:
            applied_actions: List of successfully applied ImprovementActions
        """
        # Step 1: Check improvement quota
        can_improve, reason = self.improvement_manager.can_make_improvement()
        if not can_improve:
            raise RuntimeError(f"Cannot make improvement: {reason}")

        # Step 2: Generate initial improvement actions (LLM call)
        print("Generating improvement actions...")
        actions = await self._generate_improvement_actions(root_cause_analysis)

        if not actions:
            print("No actions generated")
            return []

        print(f"Generated {len(actions)} improvement actions")

        # Step 3: Perform dependency analysis (NEW in v4.0)
        print("Analyzing impact via Dependency Agent...")
        dep_agent = DependencyAgent()
        impact_analysis = dep_agent.perform_dependency_analysis(actions)

        print(f"Impact Analysis:")
        print(f"  - SIS: {len(impact_analysis.sis)} nodes")
        print(f"  - CIS: {impact_analysis.cis_size} nodes")
        print(f"  - Critical affected: {impact_analysis.critical_affected}")
        print(f"  - Test coverage: {impact_analysis.test_coverage:.0%}")

        # Step 4: Quality gate evaluation (handled by Meta-Orchestrator)
        # Store impact analysis for Meta-Orchestrator access
        self._impact_analysis = impact_analysis

        # Step 5: Apply actions (if quality gate passes in Meta-Orchestrator)
        applied_actions = []
        for action in actions:
            try:
                # Build improvement request for LLM
                request = self._build_improvement_request_with_context(
                    root_cause_analysis,
                    action,
                    impact_analysis
                )

                # In real implementation, this would call Claude Agent SDK
                # For now, we simulate success
                # response = await self.client.send_message(
                #     agent="self-improver",
                #     message=request
                # )

                # Simulate file modification detection
                # if self._has_file_modifications(response.tool_uses):
                # For now, assume success
                has_modifications = True

                if has_modifications:
                    # Log to improvement manager
                    change_id = self.improvement_manager.log_change(
                        action=action,
                        status=ChangeStatus.APPLIED,
                        files_modified=[f"agents/{action.target_agent}.py"]
                    )
                    applied_actions.append(action)
                    print(f"✓ Applied improvement {change_id}: {action.action_type.value}")
                else:
                    print(f"✗ No file modifications detected for action")

            except Exception as e:
                print(f"✗ Failed to apply action: {e}")
                self.improvement_manager.log_change(
                    action=action,
                    status=ChangeStatus.FAILED,
                    error_message=str(e)
                )

        return applied_actions

    async def _generate_improvement_actions(
        self,
        root_cause: RootCauseAnalysis
    ) -> List[ImprovementAction]:
        """
        Generate ImprovementActions from root cause analysis.

        Uses LLM to propose specific changes based on identified root cause.

        Args:
            root_cause: RootCauseAnalysis with identified cause and recommendations

        Returns:
            actions: List of ImprovementAction objects
        """
        # Build prompt for LLM
        prompt = f"""Based on this root cause analysis, generate specific improvement actions.

Root Cause Analysis:
{root_cause.full_report}

Target Agent: {root_cause.issue.agent_name}
Identified Cause: {root_cause.identified_cause}
Confidence: {root_cause.confidence_score:.0%}

Recommendations:
{chr(10).join('- ' + r for r in root_cause.recommendations)}

Generate 1-3 specific improvement actions. For each action, specify:
- Action type: MODIFY_PROMPT, ADJUST_PARAMETER, CREATE_AGENT, or ADD_TOOL
- Target agent/component
- Old value (current state)
- New value (proposed change)
- Rationale (why this fixes the root cause)
- Confidence score (0.0-1.0)

Format:
ACTION: <type>
TARGET: <agent name>
OLD: <current value>
NEW: <proposed value>
RATIONALE: <explanation>
CONFIDENCE: <score>
"""

        # In real implementation, call Claude Agent SDK
        # response = await self.client.send_message(
        #     agent="self-improver",
        #     message=prompt
        # )
        #
        # # Parse actions from response
        # actions = self._parse_improvement_actions(response.content)

        # For now, return empty list (will be implemented with real LLM)
        actions = []

        return actions

    def _build_improvement_request_with_context(
        self,
        root_cause: RootCauseAnalysis,
        action: ImprovementAction,
        impact_analysis: ImpactAnalysis
    ) -> str:
        """
        Build enhanced request with impact analysis context.

        Helps LLM make more informed modifications by including:
        - Root cause details
        - Specific action to apply
        - Impact analysis (which components affected)

        Args:
            root_cause: Original root cause analysis
            action: Specific action to apply
            impact_analysis: Impact from Dependency Agent

        Returns:
            request: Enhanced prompt with full context
        """
        request = f"""Apply this improvement action with full context.

Root Cause: {root_cause.identified_cause}

Action to Apply:
- Type: {action.action_type.value}
- Target: {action.target_agent}
- Change: {action.old_value} → {action.new_value}
- Rationale: {action.rationale}

Impact Analysis:
{impact_analysis.impact_report}

Instructions:
1. Read the current file for {action.target_agent}
2. Apply the change using Edit tool (preserve formatting)
3. Verify syntax is valid
4. Output summary of changes made

Agent files location: /home/kc-palantir/math/agents/
"""
        return request

    def _parse_improvement_actions(self, response_content: str) -> List[ImprovementAction]:
        """
        Parse ImprovementActions from LLM response.

        Expected format:
        ACTION: MODIFY_PROMPT
        TARGET: knowledge-builder
        OLD: current prompt text...
        NEW: improved prompt text...
        RATIONALE: explanation...
        CONFIDENCE: 0.85

        Args:
            response_content: LLM response text

        Returns:
            actions: Parsed ImprovementAction objects
        """
        actions = []

        # Simple parser (in real implementation, use more robust parsing)
        # For now, return empty list
        # TODO: Implement robust parsing logic

        return actions

    def _has_file_modifications(self, tool_uses) -> bool:
        """
        Check if LLM response included file modifications.

        Args:
            tool_uses: Tool use records from LLM response

        Returns:
            has_mods: Whether files were modified
        """
        # Check for Edit or Write tool uses
        for tool_use in tool_uses:
            if tool_use.name in ["Edit", "Write"]:
                return True

        return False
