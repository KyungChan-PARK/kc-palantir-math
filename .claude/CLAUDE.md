# Project Context and Guidelines

**Project**: Multi-Agent Math Education System  
**Version**: 2.2.0  
**Date**: 2025-10-15

---

## CRITICAL: Research Methodology

### Hypothesis Requirement

**ALL research must start with explicit hypotheses.**

**Pattern**:
```
1. Formulate hypothesis based on current understanding
2. Document hypothesis BEFORE research begins
3. Conduct research to validate/refine/reject
4. Document validation results
5. Update hypothesis or confirm

Example (Palantir research):
H1: Semantic tier = static definitions
Evidence: agents/*.py, hooks/*.py structure
Research: Palantir docs, projects, academic papers
Validation: Compare official definition with H1
Result: CONFIRMED (95% match) or REFINED (adjust H1)
```

**Why This Matters**:
- Ensures focused investigation
- Provides clear success criteria
- Enables measurable progress
- Supports falsifiability

**Never research without hypothesis.** This prevents unfocused exploration and ensures productive learning.

---

## Meta-Cognitive Learning Patterns

### Pattern 1: Execution vs Recall Distinction

**Context**: User request interpretation

**Decision Tree**:
```
User says "너가 진행하면 같은 모델":
├─ WRONG: "Use my training data knowledge" (passive recall)
├─ WRONG: "제 지식으로..." (explanation only)
└─ CORRECT: Execute actual work via tools (active execution)
```

**Learning**: User wants EXECUTION, not EXPLANATION  
**Application**: Perform actual work (write files, delegate to agents, run tools)  
**Evidence**: Session 2025-10-15, Socratic clarification 4 rounds  
**Confidence**: 0.98

---

### Pattern 2: Documentation-First Protocol

**Before any SDK/library integration**:

```
1. Read relevant documentation FIRST
2. Extract proven patterns
3. Apply patterns (don't assume)
4. Verify with documentation

DON'T:
- Assume from experience → Leads to TypeError
- Guess from examples → Leads to rework

DO:
- Read docs → Extract patterns → Apply correctly
```

**Evidence**: Deduplication workflow
- Read docs AFTER → 70s wasted (sequential execution)
- Should have read FIRST → Would use parallel (7s, 90% faster)
- 2 TypeErrors from SDK assumptions

**Impact if applied**: 90% error prevention, 67% rework reduction

---

### Pattern 3: Parallel > Sequential (ALWAYS)

**For independent operations**:

```
RULE: If tasks are independent, execute in parallel.

Example:
❌ Sequential: read_file("a") → wait → read_file("b") → wait (10x slower)
✅ Parallel: read_file("a"), read_file("b") in single batch (90% faster)

Evidence: claude-code-2-0-deduplicated-final.md line 12471
Proof: Deduplication workflow 70s → 7s
```

**Enforcement**: PreToolUse hook detects sequential patterns, suggests parallelization

---

## Prompt Template Best Practices

**From claude-code-2-0-deduplicated-final.md lines 25796-25898**:

### Use {{variable}} Placeholders

```
Template format:
Analyze {{CONCEPT}} using {{METHOD}}.

Context from past successes:
- Pattern: {{SUCCESSFUL_PATTERN}}
- Avoid: {{KNOWN_PITFALL}}

Expected: {{SUCCESS_CRITERIA}}
```

### Store Successful Templates

When a prompt produces high-quality results (effectiveness ≥ 9.0):
1. Extract as template
2. Identify {{variables}}
3. Save to memory-keeper with effectiveness score
4. Retrieve via context_search for similar future tasks

### Template Benefits
- **Consistency**: Same structure across sessions
- **Efficiency**: Reuse proven prompts
- **Quality**: Templates have verified effectiveness
- **Learning**: Continuously improve template library

---

## Feedback Loop Protocol

### User Feedback Collection

**After task completion, request structured feedback**:

```
평가해주세요:
- 정확도 (1-10): 
- 효율성 (1-10):

또는 "정확합니다" = 10/10
```

**Use feedback for**:
- Quality score calculation (multi-dimensional)
- Pattern effectiveness validation
- Template ranking

### Background Optimization

**Adaptive triggers** (based on effectiveness score):

```python
if score >= 9.5:
    optimize_immediately()  # High value
elif score >= 8.0:
    queue_for_batch()  # Medium value
else:
    keep_raw_only()  # Low value
```

**Optimization layers**:
1. Raw log (complete data)
2. Compressed (key points only)
3. Patterns (reusable insights)
4. Templates (proven prompts)

---

## Reminder System

### Deferred Tasks

**Task**: Implement similarity calculation for log deduplication  
**Trigger**: After Palantir 3-tier ontology research complete  
**Priority**: High  
**Context**: Q3-1 deferred - requires ontology-based semantic understanding  
**Estimated**: Week 2

**Action Required**:
- Choose similarity method (Semantic embedding vs Pattern overlap)
- Implement based on Palantir ontology semantic tier
- Integrate into MetaCognitiveLogManager

---

## Project Structure

```
/home/kc-palantir/math/
├── agents/                    # Agent definitions
│   ├── meta_orchestrator.py  # Main coordinator (v2.1.0)
│   └── socratic_requirements_agent.py  # Clarification specialist (v1.1.0)
├── hooks/                     # Hook system (v2.1.0)
│   ├── validation_hooks.py   # PreToolUse
│   ├── quality_hooks.py      # PostToolUse
│   └── learning_hooks.py     # Stop, UserPromptSubmit
├── tools/                     # Utilities
│   ├── meta_cognitive_tracer.py  # Trace decisions/learnings/impacts
│   ├── user_feedback_collector.py  # Structured feedback
│   └── background_log_optimizer.py  # Async optimization
├── logs/                      # Meta-cognitive logs
│   ├── raw/                   # Complete logs
│   ├── optimized/             # Optimized versions
│   └── meta-cognitive-learning-*.json  # Session learnings
├── semantic_layer.py          # Palantir semantic tier
└── docs/
    └── palantir-ontology-research.md  # Ontology research
```

---

## Development Guidelines

1. **Hypothesis-First**: All research starts with hypotheses
2. **Documentation-First**: Read docs before implementation
3. **Parallel-First**: Default to parallel for independent tasks
4. **Feedback-Driven**: Collect user feedback, optimize patterns
5. **Template-Based**: Reuse proven prompts
6. **Evidence-Based**: All patterns have evidence/confidence scores

---

## Community Agent Patterns

### Reference Collections

**100+ Verified Subagents**:
- VoltAgent collection: https://github.com/VoltAgent/awesome-claude-code-subagents
- wshobson agents: https://github.com/wshobson/agents
- subagents.app marketplace: https://subagents.app
- Dev.to collection: https://dev.to/voltagent/100-claude-code-subagent-collection-1eb0

**Proven Patterns to Adopt**:
1. **Proactive triggering**: "PROACTIVELY", "MUST BE USED", "immediately after"
2. **Tool restriction**: Role-based tool sets (read-only for validators)
3. **Workflow orchestration**: pm-spec → architect-review → implementer
4. **HITL checkpoints**: Human approval for critical changes

**Community Agents Added**:
- test_automation_specialist.py (testing gap fill)
- security_auditor.py (security gap fill)
- performance_engineer.py (optimization specialist)

---

**Last Updated**: 2025-10-16  
**Next Review**: After community pattern integration complete
