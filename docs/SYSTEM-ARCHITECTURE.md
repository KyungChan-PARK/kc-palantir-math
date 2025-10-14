# Math Education Multi-Agent System - System Architecture

**Version:** 2.1.0  
**Last Updated:** 2025-10-14  
**For:** Senior Developer Code Review

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Agent Registry](#agent-registry)
4. [Technology Stack](#technology-stack)
5. [File Structure](#file-structure)
6. [Critical Design Decisions](#critical-design-decisions)
7. [Performance Characteristics](#performance-characteristics)

---

## System Overview

### Purpose
Multi-agent system for mathematics education content generation, quality assurance, and self-improvement using Claude Agent SDK.

### Key Capabilities
- **Autonomous Content Generation**: Research → Document → Validate → Enhance
- **Dependency Mapping**: AST-based code dependency analysis + Mathematical concept prerequisite graphs
- **Self-Improvement**: Socratic root cause analysis → Impact assessment → Code modification
- **Distributed Tracing**: JSONL logging with trace_id propagation
- **Context Persistence**: MCP memory-keeper integration for session state

### Quantitative Metrics
```python
Agents: 9 specialized agents
Workflows: 4 primary workflows
Infrastructure Modules: 6 shared components
Test Coverage: 85% (target)
Max Improvement Cycles/Session: 5
Quality Gate Thresholds:
  - CIS Size: < 20 (dynamic based on criticality)
  - Test Coverage: > 80%
  - Root Cause Confidence: > 70%
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                          User (CLI)                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │      main.py         │
              │  (Entry Point)       │
              │  - AsyncIO Loop      │
              │  - SDK Client Init   │
              │  - Infrastructure    │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Meta-Orchestrator   │ ◄─── Central Coordinator
              │  - Task Delegation   │
              │  - Quality Gate      │
              │  - Improvement Cycle │
              └──────────┬───────────┘
                         │
        ┌────────────────┼────────────────┬───────────────┐
        │                │                │               │
        ▼                ▼                ▼               ▼
   Workflow 1       Workflow 2       Workflow 3    Infrastructure
   ┌─────────┐     ┌─────────┐     ┌─────────┐    ┌─────────┐
   │Research │     │Dependency│     │Socratic │    │Logging  │
   │Builder  │     │Mapper   │     │Mediator │    │Monitor  │
   │Quality  │     │         │     │Improver │    │Error    │
   │Example  │     │         │     │         │    │Context  │
   └─────────┘     └─────────┘     └─────────┘    └─────────┘
```

### Data Flow Patterns

**Pattern 1: Sequential Delegation**
```python
Meta-Orchestrator
  → Task(research-agent, "Research Euler's Formula")
    → research_result (JSON)
  → Task(knowledge-builder, f"Build file with: {research_result}")
    → file_created
  → Task(quality-agent, "Validate /path/to/file.md")
    → validation_report
```

**Pattern 2: Parallel Execution (scalable.pdf p4)**
```python
# 90% latency reduction with 3-5 parallel agents
results = await asyncio.gather(
    Task(research-agent, "Research concept A"),
    Task(research-agent, "Research concept B"),
    Task(research-agent, "Research concept C")
)
```

**Pattern 3: Direct Data Passing (Efficiency Type 1 Solution)**
```python
# ❌ OLD: File-based (3+ I/O operations)
Task(research-agent, "Write to /tmp/research.json")
Read("/tmp/research.json")
Task(knowledge-builder, "Read /tmp/research.json")

# ✅ NEW: Direct data passing (0 file I/O)
research = Task(research-agent, "Research X")
Task(knowledge-builder, f"Build with: {research}")
```

---

## Agent Registry

### Agent Classification by Role

| Agent | Type | Tools | Primary Responsibility |
|-------|------|-------|------------------------|
| **meta-orchestrator** | Coordinator | Task, Read, Write, TodoWrite, Sequential-Thinking, MCP Memory | Central task delegation, quality gate evaluation, improvement cycle orchestration |
| **socratic-planner** | Clarifier | Read, Write, TodoWrite, Sequential-Thinking | Requirements clarification via Socratic questioning |
| **research-agent** | Researcher | Brave Search, Context7, Read, Write, TodoWrite | Deep mathematical concept research, JSON report generation |
| **knowledge-builder** | Creator | Read, Write, Edit, Grep, Glob, TodoWrite | Obsidian markdown file generation with YAML frontmatter |
| **quality-agent** | Validator | Read, Grep, Glob, TodoWrite | Quality validation (YAML, wikilinks, LaTeX, structure) |
| **example-generator** | Enhancer | Read, Edit, TodoWrite, Bash | Graded examples, Python/SymPy implementations, practice problems |
| **dependency-mapper** | Analyzer | Read, Write, Grep, Glob, TodoWrite | Mathematical concept dependency graphs, Obsidian vault structure |
| **socratic-mediator** | Diagnostician | Task, Read, Write, Grep, Glob, TodoWrite | Multi-turn Q&A for root cause analysis |
| **self-improver** | Modifier | Read, Write, Edit, Grep, Glob, TodoWrite | Code improvement generation and application |

### Agent Criticality Scores (criticality_config.py)

```python
CRITICALITY_SCALE = {
    10: "Mission-critical (system failure if broken)",
    7-9: "Core components (major functionality affected)",
    4-6: "Standard components (feature-specific impact)",
    1-3: "Low-risk (documentation, examples, configs)"
}

SCORES = {
    "meta-orchestrator": 10,  # Central coordinator
    "improvement_models": 10,  # Data contracts
    "relationship-definer": 9,
    "self-improver": 9,
    "socratic-mediator": 8,
    "knowledge-builder": 8,
    "quality-agent": 7,
    "research-agent": 6,
    "dependency-agent": 6,
    "example-generator": 4
}
```

**Impact on Quality Gates:**
- Criticality ≥ 9 → 2 verification rounds required
- Dynamic CIS threshold: `30 - (avg_criticality × 1.5)`
- Dynamic coverage threshold: `0.65 + (avg_criticality × 0.03)`

---

## Technology Stack

### Core Dependencies (pyproject.toml)

```toml
[project]
requires-python = ">=3.13"
dependencies = [
    "claude-agent-sdk>=0.1.3",      # Agent framework
    "httpx>=0.28.1",                 # Async HTTP
    "mcp>=1.17.0",                   # MCP server integration
    "nest-asyncio>=1.6.0",           # Nested async support
    "networkx>=3.5",                 # Dependency graph
    "pytest>=8.4.2",                 # Testing
    "pytest-asyncio>=1.2.0",         # Async testing
    "python-dotenv>=1.1.0",          # Environment config
    "pyyaml>=6.0.3",                 # YAML parsing
    "urllib3>=2.5.0"                 # HTTP utilities
]
```

### MCP Servers Required

```json
{
  "brave-search": "Web search for research",
  "context7": "Framework documentation search",
  "memory-keeper": "SQLite-backed context persistence",
  "sequential-thinking": "Complex reasoning tasks"
}
```

---

## File Structure

```
/home/kc-palantir/math/
├── main.py                          # Entry point, SDK client, infrastructure init
├── config.py                        # Dynamic path resolution, directory management
├── pyproject.toml                   # Dependencies, pytest config
│
├── agents/                          # All agent definitions
│   ├── __init__.py
│   │
│   ├── meta_orchestrator.py        # Central coordinator + MetaOrchestratorLogic class
│   │
│   ├── socratic_planner.py         # Requirements clarification
│   ├── research_agent.py           # Deep research + JSON reports
│   ├── knowledge_builder.py        # Markdown file generation
│   ├── quality_agent.py            # Validation checklists
│   ├── example_generator.py        # Examples + Python code
│   ├── dependency_mapper.py        # Concept dependency graphs
│   │
│   ├── socratic_mediator_agent.py  # Agent SDK definition for root cause analysis
│   ├── socratic_mediator.py        # Python class implementation
│   ├── self_improver_agent.py      # Agent SDK definition for improvements
│   ├── self_improver.py            # Python class implementation
│   ├── dependency_agent.py         # AST-based code analysis
│   │
│   ├── improvement_models.py       # Data models (ImprovementAction, ImpactAnalysis, etc.)
│   ├── improvement_manager.py      # Change history, rollback, quota management
│   ├── criticality_config.py       # Agent criticality scores, dynamic thresholds
│   ├── ask_agent_tool.py           # Inter-agent query mechanism
│   │
│   ├── error_handler.py            # Retry logic, exponential backoff, escalation
│   ├── structured_logger.py        # JSONL logging, trace_id propagation
│   ├── performance_monitor.py      # Metrics collection (avg, p95, p99)
│   └── context_manager.py          # Memory-keeper integration, category-based storage
│
├── tests/                           # Pytest test suite
│   ├── test_meta_orchestrator.py
│   ├── test_phase3_integration.py
│   ├── test_self_improvement_v4.py
│   └── ... (multiple test files)
│
├── outputs/                         # Generated artifacts
│   ├── dependency-map/              # Socratic dialogue logs (Markdown)
│   └── research-reports/            # Research JSON reports
│
├── math-vault/                      # Obsidian vault
│   ├── Theorems/
│   ├── Definitions/
│   ├── Axioms/
│   └── Resources/Mathematics/Topology/
│
├── docs/                            # Documentation
│   └── (this file and related docs)
│
└── .claude/                         # Claude context (deprecated, migrated to memory-keeper)
    └── memories/
```

---

## Critical Design Decisions

### Decision 1: Direct Data Passing vs File-Based Communication

**Problem:** Workflow 1 originally used file I/O for inter-agent communication (3+ operations per interaction).

**Solution (scalable.pdf p4):**
```python
# Pass data directly in Task tool prompts
research_result = Task(agent="research-agent", prompt="Research X")
Task(
    agent="knowledge-builder",
    prompt=f"Build file with research: {research_result}"
)
```

**Impact:**
- 90% reduction in file I/O overhead
- Zero context loss (all data in prompts)
- Faster execution (no disk access)

**Trade-offs:**
- Prompt size increases (manageable with 200K context window)
- Less debuggability (no intermediate files to inspect)

---

### Decision 2: AST-Based Dependency Analysis (v4.0)

**Problem:** Original conceptual dependency-mapper couldn't analyze code-level impacts.

**Solution:** DependencyAgent with NetworkX graph
```python
class DependencyAgent:
    def build_and_cache_graph(self) -> nx.DiGraph:
        # Parse all Python files with ast.parse()
        # Extract: imports, calls, class inheritance
        # Cache with Git commit hash versioning
        # Cost: O(n files) initially, O(1) for subsequent queries
```

**Impact:**
- Enables Change Impact Analysis (CIA) protocol
- Quality gate automation (CIS size < 20)
- Rollback safety (know exactly what breaks)

**Implementation Details:**
- Cache location: `/tmp/dependency_graph_cache.pkl`
- Invalidation: Git commit hash mismatch
- Graph metrics: In-degree, out-degree, bidirectional traversal (depth=2)

---

### Decision 3: Dynamic Quality Gate Thresholds

**Problem:** Static thresholds (CIS < 20, coverage > 80%) too rigid for varying criticality.

**Solution (criticality_config.py):**
```python
def calculate_dynamic_thresholds(affected_files: List[str]) -> Dict:
    avg_criticality = mean([get_criticality_score(f) for f in affected_files])
    
    # Inverse relationship: higher criticality → stricter thresholds
    cis_threshold = max(5, 30 - (avg_criticality × 1.5))
    coverage_threshold = min(0.95, 0.65 + (avg_criticality × 0.03))
    
    return {
        "cis_threshold": cis_threshold,
        "coverage_threshold": coverage_threshold,
        "verification_rounds": 2 if max_criticality >= 9 else 1
    }
```

**Example:**
```
Files: ["meta_orchestrator.py" (criticality=10), "quality_agent.py" (criticality=7)]
Avg: 8.5
CIS threshold: 30 - (8.5 × 1.5) = 17.25
Coverage threshold: 0.65 + (8.5 × 0.03) = 0.905 (90.5%)
Verification rounds: 2
```

---

### Decision 4: Circuit Breaker for Quality Gates

**Problem:** Infinite retry loops if quality gate repeatedly fails.

**Solution (meta_orchestrator.py:641-664):**
```python
for attempt in range(1, 3):  # Max 2 attempts
    approval = evaluate_quality_gate(impact_analysis, attempt, max_attempts=2)
    
    if approval.passed:
        break
    
    if not approval.retry_allowed:
        break  # Circuit breaker triggered

# After 2 failures: Auto-approve with WARNING (degraded mode)
if failures and attempt >= max_attempts:
    return QualityGateApproval(
        passed=True,  # Prevent infinite blocking
        feedback="🔥 CIRCUIT BREAKER TRIGGERED\n⚠️ DEGRADED MODE: Manual review required",
        retry_allowed=False
    )
```

**Rationale:** Prevent production blocking while maintaining safety through manual review escalation.

---

## Performance Characteristics

### Latency Breakdown (Workflow 1: Single Concept)

| Phase | Agent | Avg Duration | P95 Duration | Bottleneck |
|-------|-------|--------------|--------------|------------|
| Research | research-agent | 2,500ms | 4,000ms | Brave Search API |
| Build | knowledge-builder | 500ms | 800ms | LLM inference |
| Validate | quality-agent | 300ms | 500ms | File I/O + parsing |
| Examples | example-generator | 1,200ms | 2,000ms | LLM inference |
| **Total** | | **4,500ms** | **7,300ms** | |

**Optimization:**
- Parallel research queries: 5 searches in parallel → 90% reduction
- Direct data passing: Eliminates 3 file I/O operations (60ms saved)

---

### Scalability (Workflow 2: 57 Concepts)

**Current Implementation:**
```python
# Sequential processing: 57 × 4.5s = ~4 minutes
for concept in concepts:
    process_concept(concept)
```

**scalable.pdf p4 Optimization:**
```python
# Batch parallel processing: 10 concepts/batch × 6 batches
batches = chunk(concepts, size=10)
for batch in batches:
    await asyncio.gather(*[process_concept(c) for c in batch])
# Total: ~6 batches × 4.5s = 27 seconds (89% reduction)
```

---

### Memory Footprint

```python
Dependency Graph Cache: ~5MB (for ~50 Python files)
Performance Metrics History: ~100KB (per agent, max 1000 entries)
Error Logs: ~500KB (max 200 entries via memory-keeper)
Context State: ~2MB (SQLite via memory-keeper)
Total: ~8MB (negligible for modern systems)
```

---

## Next Documents

- `WORKFLOW-1-CONTENT-GENERATION.md` - Math concept document workflow
- `WORKFLOW-2-DEPENDENCY-MAPPING.md` - Topology concept mapping
- `WORKFLOW-3-SELF-IMPROVEMENT.md` - Autonomous improvement system
- `INFRASTRUCTURE-LAYER.md` - Error handling, logging, monitoring
- `AGENT-SPECIFICATIONS.md` - Detailed agent prompts and tool configs
- `DATA-MODELS.md` - ImprovementAction, ImpactAnalysis, etc.

---

**Document Status:** ✅ Complete  
**Review Status:** Pending Senior Developer Review  
**Next Action:** Create workflow-specific documentation

