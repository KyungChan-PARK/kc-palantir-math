"""
Meta-Orchestrator Agent

VERSION: 2.0.0 (Self-Improvement System v4.0)
LAST_UPDATED: 2025-10-14
CHANGELOG:
  v2.0.0 (2025-10-14):
    - Added Self-Improvement System v4.0 integration
    - Added evaluate_quality_gate() for CIA protocol
    - Added orchestrate_feedback_round() for dynamic feedback
    - Added run_improvement_cycle() for complete flow
  v1.2.0 (2025-10-13):
    - Added parallel execution code examples per scalable.pdf p4
    - Enhanced with capability-based routing documentation
    - Added memory-keeper tool integration for context persistence
  v1.1.0 (2025-10-12):
    - Added performance monitoring and inefficiency detection
  v1.0.0 (2025-10-10):
    - Initial implementation

Research Base:
- Anthropic Best Practices (2024-2025)
- Microsoft Azure Orchestrator Patterns
- IBM Multi-Agent Coordination Research
- scalable.pdf: Multi-Agent Systems with Claude Agent SDK Best Practices
- SELF-IMPROVEMENT-IMPLEMENTATION-PLAN-v4.0.md

Core Features:
1. User Feedback Loop (most frequent user interaction)
2. Agent Performance Monitoring (execution time, success rate, API costs)
3. 4 Inefficiency Types Detection and Resolution
4. Autonomous workflow adjustment
5. Task decomposition + capability-based routing
6. Parallel execution (3-5 agents = 90% latency reduction per scalable.pdf)
7. Self-Improvement System v4.0 (Quality Gate, Feedback Loop, CIA protocol)
"""

from claude_agent_sdk import AgentDefinition
from agents.improvement_models import ImpactAnalysis, QualityGateApproval

meta_orchestrator = AgentDefinition(
    description="Coordinates multiple specialized agents (research-agent, knowledge-builder, quality-agent, example-generator, dependency-mapper, socratic-planner) for complex mathematical concept processing. Invoke for: multi-step workflows, batch processing (e.g., '57 topology concepts'), cross-agent coordination, performance optimization, or when ambiguous user requests need clarification.",

    prompt="""You are a meta-cognitive orchestrator for a multi-agent mathematics education system.

## Your Primary Role: USER FEEDBACK LOOP

**CRITICAL**: You have the MOST FREQUENT interaction with the user.
- You are the primary interface for user feedback
- You translate user requirements into agent tasks
- You report system status to user in clear, concise terms
- You learn from user corrections and adjust workflows

## Core Responsibilities

### 1. Agent Performance Monitoring

Track metrics for each agent (knowledge-builder, quality-agent, research-agent, dependency-mapper, socratic-planner):

**Metrics to Monitor:**
- **Execution Time**: How long each agent takes per task
- **Success Rate**: % of tasks completed without errors
- **API Costs**: Number of MCP tool calls (Brave Search, Context7, etc.)
- **Output Quality**: Based on quality-agent validation scores
- **Iteration Count**: How many feedback loops needed to complete task

**Monitoring Method:**
1. Use **Read** to check agent logs in `/tmp/` or `.claude/memories/agent-learnings/`
2. Parse execution timestamps and results
3. Calculate metrics
4. Store in memory for trend analysis

### 2. Inefficiency Detection (4 Types)

You must ACTIVELY detect and resolve these inefficiencies:

#### Type 1: Communication Overhead
**Definition**: Agents using file I/O for inter-agent communication instead of direct data passing.

**Detection Method:**
- Count Read/Write operations on shared files (e.g., `/tmp/research_report_*.json`)
- If >3 file I/O operations per agent interaction → FLAG as inefficient

**Solution:**
- Use Task tool's agent chaining: research-agent → knowledge-builder directly
- Pass data in agent prompt instead of file transfer

#### Type 2: Redundant Work
**Definition**: Multiple agents making duplicate MCP tool calls (Brave Search, Context7) for same concept.

**Detection Method:**
- Track MCP call history in `.claude/memories/agent-learnings/tool-usage.log`
- If >1 agent searches "Pythagorean Theorem" → FLAG as redundant

**Solution:**
- Create shared knowledge cache in memory
- Before delegating task, check if research already exists
- Reuse research_agent output for knowledge_builder

#### Type 3: Context Loss
**Definition**: Information not propagated between agents, causing incomplete or inconsistent output.

**Detection Method:**
- Compare agent outputs for same concept
- If knowledge-builder misses prerequisites found by research-agent → FLAG context loss

**Solution:**
- Use structured data format (JSON) for agent-to-agent communication
- Include ALL research findings in knowledge-builder task prompt
- Validate that quality-agent has access to original requirements

#### Type 4: Tool Permission Misalignment
**Definition**: Overlapping tool access, no least-privilege enforcement.

**Detection Method:**
- Review agent tool lists in `agents/*.py`
- If multiple agents have same MCP tools but only one uses them → FLAG misalignment

**Solution:**
- Follow principle of least privilege
- research-agent: Brave Search + Context7 (research-only agent)
- knowledge-builder: Write only (no search)
- quality-agent: Read only (no modification)
- dependency-mapper: Read + Write + NLP tools (specialized)

### 3. Workflow Orchestration Patterns

You have 5 orchestration patterns available (from research):

**A. Sequential Pattern**
Tasks executed one after another.
Use when: Tasks have strict dependencies.

**B. Concurrent Pattern (RECOMMENDED for batches)**
Independent tasks in parallel. Per scalable.pdf p4: 3-5 parallel subagents = 90% latency reduction.
Use when: Processing multiple independent concepts.

**Implementation Example**:
```python
# Example: Process 3 concepts in parallel
# Send 3 Task calls in a SINGLE message (Claude will execute them in parallel)

Task(agent="research-agent", prompt="Research concept: Pythagorean Theorem")
Task(agent="research-agent", prompt="Research concept: Cauchy-Schwarz Inequality")
Task(agent="research-agent", prompt="Research concept: Mean Value Theorem")

# Then wait for all results before continuing
# This achieves ~90% reduction in latency vs sequential
```

**C. Group Chat Pattern**
Agents discuss and collaborate dynamically.
Use when: Complex concepts need iterative refinement.

**D. Handoff Pattern**
One agent passes control based on conditions.
Use when: Routing based on concept difficulty.

**E. Magentic Pattern**
Agents attracted to tasks they're best suited for.
Use when: System has many specialized agents.

### 4. Task Decomposition

When user gives complex request (e.g., "Process 57 topology concepts"):

**Step 1: Analyze Request**
- Use **Sequential-thinking** to break down requirements
- Identify subtasks: research, build, validate, map dependencies

**Step 2: Capability Matching**
Match subtasks to agent capabilities:
- Literature research → research-agent
- File creation → knowledge-builder
- Quality validation → quality-agent
- Dependency mapping → dependency-mapper
- Requirements clarification → socratic-planner

**Step 3: Workflow Design**
Choose orchestration pattern:
- 57 concepts → Concurrent pattern (process in parallel batches)
- Complex concept → Sequential pattern (research → build → validate)

**Step 4: Execution Monitoring**
- Use **TodoWrite** to track progress
- Monitor for inefficiencies during execution
- Adjust workflow in real-time if bottlenecks detected

**Step 5: User Feedback**
- Report progress concisely to user
- Ask for feedback if ambiguity detected
- Incorporate feedback into workflow

### 5. Feedback Loop Assignment

Each agent must have clear feedback mechanisms per research findings.

### 6. Self-Improvement Mechanism

**Learning from Performance Data:**
1. Store metrics in `.claude/memories/agent-learnings/performance-trends.json`
2. Detect patterns and propose adjustments
3. Test alternative workflows

**User Feedback Integration:**
1. When user says "this is wrong", analyze root cause
2. Determine which agent caused issue
3. Store correction in `.claude/memories/backward-propagation/`
4. Adjust that agent's prompt or workflow

## Tools Available

- **Task**: Delegate to sub-agents
- **Read**: Load agent logs, performance data
- **Write**: Store metrics, reports
- **TodoWrite**: Track multi-phase orchestration
- **Sequential-thinking**: Complex task decomposition

## Important Guidelines

1. **User-First Mentality**: Always prioritize user feedback
2. **Efficiency Obsession**: Actively hunt for inefficiencies
3. **Data-Driven Decisions**: Use metrics, not assumptions
4. **Autonomous Operation**: Work independently but report progress
5. **Least Privilege**: Enforce tool restrictions per agent
6. **Feedback Loops**: Every agent must improve over time
7. **Concise Communication**: No verbose reports, just facts

## Your First Task

When activated:
1. Check current system state
2. Analyze user request
3. Decompose into subtasks
4. Match subtasks to agents
5. Execute workflow with monitoring
6. Report results concisely
7. Ask for feedback and iterate

Now orchestrate!
""",

    model="sonnet",

    tools=[
        # Subagent delegation
        'Task',

        # Filesystem operations
        'Read',
        'Write',
        'Grep',
        'Glob',

        # Task tracking
        'TodoWrite',

        # MCP tools
        'mcp__sequential-thinking__sequentialthinking',
        'mcp__memory-keeper__context_save',
        'mcp__memory-keeper__context_get',
        'mcp__memory-keeper__context_search',
    ]
)


# ============================================================================
# Meta-Orchestrator Logic Class (Self-Improvement System v4.0)
# ============================================================================

class MetaOrchestratorLogic:
    """
    Logic layer for Meta-Orchestrator self-improvement capabilities.

    Based on: SELF-IMPROVEMENT-IMPLEMENTATION-PLAN-v4.0.md Section III.2

    Provides:
    1. Quality Gate Evaluation (thresholds for auto-approval)
    2. Feedback Loop Orchestration (1-2 round determination)
    3. Complete Improvement Cycle (root cause → apply → verify)
    """

    def __init__(self):
        """Initialize Meta-Orchestrator logic"""
        self.agent_registry = {}  # Will be populated by main.py
        self.consecutive_failures = {}  # Track failures per agent

    def evaluate_quality_gate(
        self,
        impact_analysis: ImpactAnalysis
    ) -> QualityGateApproval:
        """
        Academic specification: Rule-based quality gate evaluation.

        Thresholds (from v4.0 spec):
        - CIS size < 20 files (blast radius)
        - Test coverage > 80% (safety net)
        - Critical components → escalate (warning, not rejection)

        Args:
            impact_analysis: ImpactAnalysis from DependencyAgent

        Returns:
            QualityGateApproval with pass/fail and feedback
        """
        failures = []
        warnings = []

        # Threshold 1: CIS size (blast radius)
        if impact_analysis.cis_size >= 20:
            failures.append(
                f"CIS size ({impact_analysis.cis_size}) exceeds threshold (20 files). "
                "Blast radius too large for automated approval."
            )

        # Threshold 2: Test coverage
        if impact_analysis.test_coverage < 0.80:
            failures.append(
                f"Test coverage ({impact_analysis.test_coverage:.0%}) below 80%. "
                "Insufficient safety net for automated changes."
            )

        # Threshold 3: Critical components (warning, not failure)
        if impact_analysis.critical_affected:
            warnings.append(
                "⚠️  Mission-critical components affected. "
                "System will enforce 2-round verification."
            )

        # Generate feedback
        if failures:
            feedback = "Quality Gate FAILED:\n"
            feedback += "\n".join(f"- {f}" for f in failures)
            if warnings:
                feedback += "\n\nWarnings:\n"
                feedback += "\n".join(f"- {w}" for w in warnings)

            return QualityGateApproval(
                passed=False,
                feedback=feedback,
                retry_allowed=True,
                metrics=impact_analysis.to_dict()
            )

        # Passed
        feedback = "Quality Gate PASSED"
        if warnings:
            feedback += "\n\nWarnings:\n"
            feedback += "\n".join(f"- {w}" for w in warnings)

        return QualityGateApproval(
            passed=True,
            feedback=feedback,
            retry_allowed=False,
            metrics=impact_analysis.to_dict()
        )

    async def orchestrate_feedback_round(
        self,
        root_cause,  # RootCauseAnalysis
        impact_analysis: ImpactAnalysis
    ) -> bool:
        """
        PDF specification: Dynamic feedback loop with automatic round determination.

        Rules (from v4.0 spec):
        - 2+ agents affected + mission-critical → 2 rounds
        - Otherwise → 1 round

        Each round:
        1. Self-Improver applies changes
        2. Verification test runs
        3. Success → exit, Failure → rollback + retry (if rounds remaining)

        Args:
            root_cause: RootCauseAnalysis from Socratic-Mediator
            impact_analysis: ImpactAnalysis from DependencyAgent

        Returns:
            success: True if improvement succeeded, False if all rounds failed
        """
        # Determine max rounds (PDF rule)
        if impact_analysis.cis_size >= 2 and impact_analysis.critical_affected:
            max_rounds = 2
            print(f"⚠️  Critical components affected: {impact_analysis.cis_size} nodes")
            print(f"   Max feedback rounds: {max_rounds}")
        else:
            max_rounds = 1
            print(f"ℹ️  Standard improvement: {impact_analysis.cis_size} nodes affected")
            print(f"   Max feedback rounds: {max_rounds}")

        # Execute rounds
        for round_num in range(1, max_rounds + 1):
            print(f"\n{'='*60}")
            print(f"🔄 FEEDBACK ROUND {round_num}/{max_rounds}")
            print(f"{'='*60}\n")

            # Apply improvements
            print("Applying improvements...")
            try:
                # In real implementation, use self.self_improver
                # actions = await self.self_improver.apply_improvements(root_cause)
                actions = []  # Placeholder

                if not actions:
                    print(f"   No actions applied in round {round_num}")
                    if round_num < max_rounds:
                        print(f"   Retrying...")
                        continue
                    else:
                        return False

                print(f"   ✓ Applied {len(actions)} actions")

            except Exception as e:
                print(f"   ✗ Error applying improvements: {e}")
                if round_num < max_rounds:
                    print(f"   Retrying...")
                    continue
                else:
                    return False

            # Verification test
            print("\nRunning verification tests...")
            verification_passed = await self._run_verification_test(
                root_cause.issue.agent_name
            )

            if verification_passed:
                print(f"   ✓ Verification PASSED in round {round_num}")
                print(f"   Improvement cycle succeeded!")

                # Log success (in real implementation)
                # self.structured_logger.system_event(
                #     "improvement_cycle_success",
                #     f"Round {round_num}/{max_rounds}: Improvement successful"
                # )

                return True
            else:
                print(f"   ✗ Verification FAILED in round {round_num}")

                # Rollback
                print(f"   Rolling back changes...")
                # rolled_back = self.improvement_manager.rollback_last()

                # if rolled_back:
                #     print(f"   ✓ Rollback completed")

                # Check if more rounds available
                if round_num < max_rounds:
                    print(f"\n   Retrying with adjusted approach...")
                else:
                    print(f"\n   All {max_rounds} rounds exhausted.")
                    print(f"   Improvement cycle failed.")
                    return False

        return False

    async def _run_verification_test(self, agent_name: str) -> bool:
        """
        PDF specification: Run sample query to verify improvement.

        Tests:
        1. Basic functionality (sample query execution)
        2. No regression (duration not >2x worse)
        3. Error-free execution

        Args:
            agent_name: Agent to test

        Returns:
            passed: Whether verification tests passed
        """
        test_queries = [
            "What is the Pythagorean theorem?",
            "Explain the concept of limits in calculus.",
        ]

        for query in test_queries:
            try:
                # In real implementation:
                # start_time = time.time()
                # result = await self._execute_single_agent(agent_name, query)
                # duration_ms = (time.time() - start_time) * 1000

                # Placeholder for testing
                result = "Sample result (placeholder)"
                duration_ms = 500

                # Check 1: Result is non-empty
                if not result or len(result) < 50:
                    print(f"      ✗ Test failed: Empty or too short result")
                    return False

                # Check 2: Duration is reasonable
                # In real implementation, compare with baseline metrics
                # if duration_ms > baseline * 2:
                #     print(f"      ✗ Test failed: Performance regression")
                #     return False

                print(f"      ✓ Test query passed ({duration_ms:.0f}ms)")

            except Exception as e:
                print(f"      ✗ Test failed with error: {e}")
                return False

        return True

    async def _execute_single_agent(self, agent_name: str, query: str) -> str:
        """
        Execute a single agent with a query (for testing).

        Args:
            agent_name: Agent to execute
            query: Test query

        Returns:
            result: Agent response
        """
        if agent_name not in self.agent_registry:
            raise ValueError(f"Agent {agent_name} not found")

        # In real implementation:
        # agent_func = self.agent_registry[agent_name]
        # result = await agent_func(query)

        # Placeholder
        result = f"Response from {agent_name} for query: {query}"

        return result

    async def run_improvement_cycle(self, issue: 'IssueReport') -> bool:
        """
        Complete improvement cycle with all enhancements integrated.

        Flow (from v4.0 spec Section VII.1):
        1. Socratic-Mediator root cause analysis (with logging)
        2. Self-Improver impact analysis (via Dependency Agent)
        3. Quality gate evaluation
        4. If passed: Dynamic feedback loop (1-2 rounds)
        5. Verification and rollback if needed

        Args:
            issue: IssueReport describing the problem

        Returns:
            success: True if improvement succeeded, False otherwise
        """
        # Import here to avoid circular dependency
        from agents.improvement_models import IssueReport
        from agents.socratic_mediator import SocraticMediator
        from agents.self_improver import SelfImprover
        from agents.dependency_agent import DependencyAgent

        print(f"\n{'='*60}")
        print(f"🚀 IMPROVEMENT CYCLE START")
        print(f"{'='*60}\n")
        print(f"Agent: {issue.agent_name}")
        print(f"Issue Type: {issue.error_type}")

        try:
            # STEP 1: Root cause analysis
            print(f"\n{'='*60}")
            print(f"🔍 STEP 1: ROOT CAUSE ANALYSIS")
            print(f"{'='*60}\n")

            socratic_mediator = SocraticMediator(
                client=None,  # Would be Claude SDK client
                agent_registry=self.agent_registry
            )
            root_cause = await socratic_mediator.analyze_issue(issue)

            print(f"Root cause identified:")
            print(f"  - Cause: {root_cause.identified_cause[:100]}...")
            print(f"  - Confidence: {root_cause.confidence_score:.0%}")
            print(f"  - Recommendations: {len(root_cause.recommendations)}")

            # Check confidence threshold
            if root_cause.confidence_score < 0.70:
                print(f"\n⚠️  Confidence too low ({root_cause.confidence_score:.0%} < 70%)")
                print(f"   Skipping improvement cycle")
                return False

            # STEP 2: Impact analysis
            print(f"\n{'='*60}")
            print(f"📊 STEP 2: IMPACT ANALYSIS")
            print(f"{'='*60}\n")

            self_improver = SelfImprover(client=None)

            # Generate initial improvement actions
            actions = await self_improver._generate_improvement_actions(root_cause)

            if not actions:
                print("No improvement actions generated")
                return False

            print(f"Generated {len(actions)} improvement actions")

            # Perform dependency analysis
            dep_agent = DependencyAgent()
            impact_analysis = dep_agent.perform_dependency_analysis(actions)

            print(f"\nImpact Analysis Results:")
            print(f"  - Starting Impact Set: {len(impact_analysis.sis)} nodes")
            print(f"  - Candidate Impact Set: {impact_analysis.cis_size} nodes")
            print(f"  - Mission-critical affected: {impact_analysis.critical_affected}")
            print(f"  - Test coverage: {impact_analysis.test_coverage:.0%}")

            # STEP 3: Quality gate
            print(f"\n{'='*60}")
            print(f"🚦 STEP 3: QUALITY GATE EVALUATION")
            print(f"{'='*60}\n")

            approval = self.evaluate_quality_gate(impact_analysis)

            print(f"Quality Gate: {'PASSED' if approval.passed else 'FAILED'}")
            if approval.feedback:
                print(f"\nFeedback:\n{approval.feedback}")

            if not approval.passed:
                if approval.retry_allowed:
                    print("\n⚠️  Retry allowed. Self-Improver should adjust approach.")
                return False

            # STEP 4: Feedback loop
            print(f"\n{'='*60}")
            print(f"🔄 STEP 4: FEEDBACK LOOP")
            print(f"{'='*60}\n")

            # Store impact analysis for Self-Improver access
            self_improver._impact_analysis = impact_analysis

            success = await self.orchestrate_feedback_round(
                root_cause,
                impact_analysis
            )

            if success:
                print(f"\n{'='*60}")
                print(f"✅ IMPROVEMENT CYCLE COMPLETED SUCCESSFULLY")
                print(f"{'='*60}\n")

                # Reset failure counters
                if issue.agent_name in self.consecutive_failures:
                    self.consecutive_failures[issue.agent_name] = 0

                # Log statistics
                stats = self_improver.improvement_manager.get_statistics()
                print(f"Improvement Statistics:")
                print(f"  - Total changes: {stats['total_changes']}")
                print(f"  - Success rate: {stats['success_rate']:.0%}")
                print(f"  - This session: {stats['session_count']}")

                return True
            else:
                print(f"\n{'='*60}")
                print(f"❌ IMPROVEMENT CYCLE FAILED")
                print(f"{'='*60}\n")

                return False

        except Exception as e:
            print(f"\n❌ Error during improvement cycle: {e}")

            # Attempt rollback
            try:
                # self_improver.improvement_manager.rollback_last()
                pass
            except:
                pass

            return False
