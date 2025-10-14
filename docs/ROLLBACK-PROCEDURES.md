# Rollback Procedures for Self-Improvement System

**Version**: 1.0
**Date**: 2025-10-14
**Purpose**: Define rollback conditions, methods, and verification for all 6 improvements

---

## Overview

**Safety-First Principle**: Every improvement must be reversible with minimal disruption.

**Rollback Triggers**:
1. Automated test failures
2. Performance degradation
3. Accuracy below baseline
4. Production issues within 24 hours of deployment

**Rollback Guarantee**: < 30 minutes from decision to verification complete

---

## General Rollback Procedure

```
1. DETECT failure (automated monitoring or manual report)
   ↓
2. CREATE rollback branch: rollback/improvement-N-YYYYMMDD
   ↓
3. REVERT changes (git, files, configs)
   ↓
4. RUN verification tests
   ↓
5. VERIFY metrics returned to baseline
   ↓
6. MERGE rollback to main
   ↓
7. DOCUMENT failure cause + lessons learned
   ↓
8. PLAN remediation
```

---

## Improvement #1: Multi-Dimensional Uncertainty Modeling

### Rollback Conditions

**Automated Triggers**:
- Unit tests fail (uncertainty_breakdown parsing)
- Integration tests fail (SocraticMediator integration)
- Accuracy < baseline on validation set
- `uncertainty_reason` accuracy < 60%

**Manual Triggers**:
- Production errors related to uncertainty parsing
- SocraticMediator crashes or produces invalid output
- Increased diagnosis iterations (opposite of goal)

### Rollback Method

**Files to Revert**:
- `agents/relationship_definer.py` (lines 60-177: system prompt)
- `agents/relationship_definer.py` (lines 254-262: response parsing)

**Git Commands**:
```bash
# 1. Create rollback branch
git checkout -b rollback/uncertainty-modeling-$(date +%Y%m%d)

# 2. Revert specific file
git checkout HEAD~1 -- agents/relationship_definer.py

# 3. Verify git diff shows only uncertainty changes reverted
git diff HEAD

# 4. Commit
git add agents/relationship_definer.py
git commit -m "Rollback: Revert uncertainty modeling (failed validation)"

# 5. Run verification
uv run pytest tests/test_baseline_uncertainty.py -v

# 6. If verification passes
git checkout main
git merge rollback/uncertainty-modeling-$(date +%Y%m%d)
```

### Impact Scope

**Directly Affected**:
- `RelationshipDefiner` agent

**Indirectly Affected**:
- `SocraticMediator` (loses uncertainty diagnostics, reverts to generic questions)

**Not Affected**:
- Other agents
- Knowledge graph structure
- Existing relationship data

### Verification Tests

```bash
# 1. Baseline accuracy restored
uv run tests/test_baseline_uncertainty.py --compare baseline_uncertainty.json

# Expected: Accuracy >= baseline (no degradation)

# 2. No parse errors
uv run tests/test_relationship_definer.py --sample 50

# Expected: 0 parsing errors

# 3. SocraticMediator functional
uv run tests/test_socratic_basic.py

# Expected: All tests pass
```

### Recovery Time

- Detection: < 5 minutes (automated tests)
- Revert: 5 minutes (git operations)
- Verification: 10 minutes (test suite)
- Merge: 5 minutes

**Total: ~25 minutes**

### Post-Rollback Actions

1. Document failure mode in `docs/failure-reports/uncertainty-modeling-YYYYMMDD.md`
2. Analyze test logs to identify root cause
3. If prompt issue: Revise prompt wording
4. If parsing issue: Improve JSON extraction logic
5. Re-test on smaller validation set before re-deployment

---

## Improvement #2: Chain-of-Thought Prompting

### Rollback Conditions

**Automated Triggers**:
- Accuracy improvement < 10% (target: 15%)
- Unit tests fail (reasoning_trace parsing)
- Response parsing errors > 5%
- Increased latency > 50%

**Manual Triggers**:
- CoT reasoning contains hallucinations
- Debugging using reasoning_trace proves ineffective
- Token costs exceed budget

### Rollback Method

**Files to Revert**:
- `agents/relationship_definer.py` (lines 103-154: CoT prompt section)
- `agents/relationship_definer.py` (lines 159-182: response parsing)

**Git Commands**:
```bash
# 1. Create rollback branch
git checkout -b rollback/cot-prompting-$(date +%Y%m%d)

# 2. Revert CoT changes
git checkout HEAD~1 -- agents/relationship_definer.py

# Alternatively: Use patch file if multiple commits involved
git diff improvement-2-baseline..HEAD -- agents/relationship_definer.py > cot_changes.patch
git apply -R cot_changes.patch

# 3. Verify
git diff HEAD

# 4. Commit
git add agents/relationship_definer.py
git commit -m "Rollback: Revert CoT prompting (accuracy target not met)"

# 5. Verification
uv run pytest tests/test_baseline_accuracy.py -v

# 6. Merge
git checkout main
git merge rollback/cot-prompting-$(date +%Y%m%d)
```

### Impact Scope

**Directly Affected**:
- `RelationshipDefiner` agent (reasoning_trace field removed)

**Indirectly Affected**:
- Debugging workflow (reverts to black-box classification)

**Not Affected**:
- Other agents
- Accuracy (returns to baseline, not degraded)
- Data structures

### Verification Tests

```bash
# 1. Baseline accuracy maintained
uv run tests/test_baseline_accuracy.py --compare baseline_cot.json

# Expected: Accuracy == baseline (no degradation)

# 2. No parsing errors
uv run tests/test_relationship_definer.py --sample 100

# Expected: 0 parsing errors, all JSON valid

# 3. Latency restored
uv run tests/measure_latency.py

# Expected: Latency <= baseline latency
```

### Recovery Time

- Detection: < 5 minutes
- Revert: 5 minutes
- Verification: 15 minutes (accuracy tests)
- Merge: 5 minutes

**Total: ~30 minutes**

### Post-Rollback Actions

1. Analyze accuracy results: Which relationship types improved/degraded?
2. Review CoT prompt: Was reasoning structure clear?
3. Check parsing: Were reasoning traces correctly extracted?
4. Consider hybrid: Keep CoT for complex relationships only
5. Re-test on targeted subset before re-deployment

---

## Improvement #3: Dynamic Quality Gate

### Rollback Conditions

**Automated Triggers**:
- False rejection rate > 10%
- Unit tests fail (threshold calculation logic)
- Integration tests fail (MetaOrchestrator)
- Critical files incorrectly classified

**Manual Triggers**:
- Valid improvements rejected repeatedly
- Threshold calculations appear incorrect
- System too lenient or too strict

### Rollback Method

**Files to Revert**:
- `agents/criticality_config.py` (DELETE - new file)
- `agents/meta_orchestrator.py` (lines 437-505: evaluate_quality_gate)

**Git Commands**:
```bash
# 1. Create rollback branch
git checkout -b rollback/dynamic-quality-gate-$(date +%Y%m%d)

# 2. Remove new file
git rm agents/criticality_config.py

# 3. Revert MetaOrchestrator changes
git checkout HEAD~2 -- agents/meta_orchestrator.py
# (HEAD~2 assumes #3 was 2 commits ago)

# 4. Verify
git diff HEAD

# 5. Commit
git add agents/criticality_config.py agents/meta_orchestrator.py
git commit -m "Rollback: Revert dynamic quality gate (false rejection rate too high)"

# 6. Verification
uv run pytest tests/test_quality_gate_integration.py -v

# 7. Merge
git checkout main
git merge rollback/dynamic-quality-gate-$(date +%Y%m%d)
```

### Impact Scope

**Directly Affected**:
- `MetaOrchestrator.evaluate_quality_gate()` method
- `criticality_config.py` (deleted)

**Indirectly Affected**:
- Quality gate decisions (reverts to static thresholds)
- All improvements passing through quality gate

**Not Affected**:
- Other MetaOrchestrator methods
- Agents
- Data

### Verification Tests

```bash
# 1. Static thresholds restored
uv run tests/test_static_quality_gate.py

# Expected: CIS threshold == 20, Coverage == 0.80 (hardcoded)

# 2. False rejection rate baseline
uv run tests/measure_false_rejections.py --mode static

# Expected: False rejection rate <= baseline

# 3. MetaOrchestrator functional
uv run tests/test_meta_orchestrator_basic.py

# Expected: All tests pass
```

### Recovery Time

- Detection: < 5 minutes
- Revert: 10 minutes (2 files)
- Verification: 15 minutes (quality gate scenarios)
- Merge: 5 minutes

**Total: ~35 minutes** (slightly longer due to 2 files)

### Post-Rollback Actions

1. Review criticality scores: Were they accurate?
2. Check threshold formula: `cis_threshold = max(5, 30 - (avg_criticality * 1.5))`
3. Analyze false rejections: Which scenarios failed?
4. Consider simpler formula or manual overrides
5. Re-test on smaller validation set

---

## Improvement #4: Formal Ontology + QualityAgent

### Rollback Conditions

**Automated Triggers**:
- False positives > 5% (valid relationships flagged as invalid)
- Unit tests fail (ontology validation logic)
- Performance degradation > 30% (cycle detection overhead)
- Integration tests fail (QualityAgent)

**Manual Triggers**:
- QualityAgent blocks valid relationships
- Circular dependency detection produces false positives
- System becomes too slow

### Rollback Method

**Files to Revert**:
- `agents/relationship_ontology.py` (DELETE - new file)
- `agents/quality_agent.py` (DELETE - new file)
- `agents/relationship_definer.py` (lines 322-851: validation integration)

**Git Commands**:
```bash
# 1. Create rollback branch
git checkout -b rollback/ontology-$(date +%Y%m%d)

# 2. Remove new files
git rm agents/relationship_ontology.py
git rm agents/quality_agent.py

# 3. Revert RelationshipDefiner changes
git checkout HEAD~3 -- agents/relationship_definer.py
# (HEAD~3 assumes #4 was 3 commits ago)

# 4. Verify
git diff HEAD
git status

# 5. Commit
git add agents/relationship_ontology.py agents/quality_agent.py agents/relationship_definer.py
git commit -m "Rollback: Revert ontology system (false positive rate exceeded threshold)"

# 6. Verification
uv run pytest tests/test_relationship_definer.py tests/test_baseline_performance.py -v

# 7. Merge
git checkout main
git merge rollback/ontology-$(date +%Y%m%d)
```

### Impact Scope

**Directly Affected**:
- `RelationshipDefiner` (loses ontology validation)
- `QualityAgent` (deleted)
- `relationship_ontology.py` (deleted)

**Indirectly Affected**:
- Knowledge graph validation (reverts to basic syntax checks)
- Circular dependency detection (disabled)

**Not Affected**:
- Other agents
- Existing relationships (but invalid ones may pass)

### Verification Tests

```bash
# 1. Baseline validation restored
uv run tests/test_baseline_validation.py

# Expected: Basic syntax validation works, no ontology checks

# 2. No false positives
uv run tests/test_ontology_false_positives.py --dataset tests/fixtures/valid_relationships.json

# Expected: 0 false positives (all valid relationships pass)

# 3. Performance restored
uv run tests/benchmark_relationship_definer.py

# Expected: Performance == baseline (no overhead)
```

### Recovery Time

- Detection: < 5 minutes
- Revert: 15 minutes (3 files)
- Verification: 20 minutes (comprehensive tests)
- Merge: 5 minutes

**Total: ~45 minutes** (longest rollback due to complexity)

### Post-Rollback Actions

1. Analyze false positives: Which valid relationships were flagged?
2. Review ontology rules: Are formal properties too strict?
3. Check cycle detection: DFS algorithm bug?
4. Profile performance: Where is bottleneck?
5. Consider lightweight version: Only check critical violations
6. Re-test incrementally: Enable one check at a time

---

## Improvement #5: HITL Checkpoint Framework

### Rollback Conditions

**Automated Triggers**:
- Workflow blocks > 5 minutes (waiting for human input)
- False checkpoint triggers > 20% (non-critical decisions blocked)
- Unit tests fail (checkpoint logic)
- Integration tests fail (workflow pause/resume)

**Manual Triggers**:
- HITL framework causes workflow delays
- Checkpoints trigger too frequently
- Human review becomes bottleneck

### Rollback Method

**Files to Revert**:
- `agents/hitl_checkpoints.py` (DELETE - new file)
- `agents/meta_orchestrator.py` (HITL integration code)

**Git Commands**:
```bash
# 1. Create rollback branch
git checkout -b rollback/hitl-$(date +%Y%m%d)

# 2. Remove new file
git rm agents/hitl_checkpoints.py

# 3. Revert MetaOrchestrator HITL integration
git checkout HEAD~4 -- agents/meta_orchestrator.py
# (HEAD~4 assumes #5 was implemented after #1-#4)

# 4. Verify
git diff HEAD

# 5. Commit
git add agents/hitl_checkpoints.py agents/meta_orchestrator.py
git commit -m "Rollback: Revert HITL framework (false trigger rate too high)"

# 6. Verification
uv run pytest tests/test_meta_orchestrator_auto_flow.py -v

# 7. Merge
git checkout main
git merge rollback/hitl-$(date +%Y%m%d)
```

### Impact Scope

**Directly Affected**:
- `MetaOrchestrator` (removes HITL checkpoints)
- `hitl_checkpoints.py` (deleted)

**Indirectly Affected**:
- Workflow (reverts to fully automated, no human review)
- Critical decisions (auto-approved without oversight)

**Not Affected**:
- Other agents
- Relationship classification
- Quality gate

### Verification Tests

```bash
# 1. Automated workflow restored
uv run tests/test_workflow_auto_complete.py

# Expected: Workflow completes without human input

# 2. No blocking
uv run tests/test_workflow_latency.py

# Expected: No delays > 1 minute

# 3. MetaOrchestrator functional
uv run tests/test_meta_orchestrator_basic.py

# Expected: All tests pass
```

### Recovery Time

- Detection: < 5 minutes
- Revert: 10 minutes (2 files)
- Verification: 15 minutes (workflow tests)
- Merge: 5 minutes

**Total: ~35 minutes**

### Post-Rollback Actions

1. Review trigger conditions: Were checkpoints too sensitive?
2. Analyze false triggers: Which decisions were non-critical?
3. Consider adjustable sensitivity: Low/medium/high checkpoint modes
4. Async checkpoints: Don't block workflow, notify in background
5. Re-test with stricter trigger conditions

---

## Improvement #6: Parallel Socratic Q&A

### Rollback Conditions

**Automated Triggers**:
- Results differ from sequential execution
- Integration tests fail (parallel Task pattern)
- Error rate increases > 10%
- Parallel calls fail or timeout

**Manual Triggers**:
- Parallel execution produces incorrect results
- Task tool errors related to parallel calls
- Inconsistent output quality

### Rollback Method

**Files to Revert**:
- `agents/socratic_mediator_agent.py` (lines 60-69: parallel Task prompt)

**Git Commands**:
```bash
# 1. Create rollback branch
git checkout -b rollback/parallel-qa-$(date +%Y%m%d)

# 2. Revert SocraticMediator changes
git checkout HEAD~1 -- agents/socratic_mediator_agent.py

# 3. Verify
git diff HEAD

# 4. Commit
git add agents/socratic_mediator_agent.py
git commit -m "Rollback: Revert parallel Q&A (result inconsistency)"

# 5. Verification
uv run pytest tests/test_socratic_sequential.py -v

# 6. Merge
git checkout main
git merge rollback/parallel-qa-$(date +%Y%m%d)
```

### Impact Scope

**Directly Affected**:
- `SocraticMediator` (reverts to sequential Task calls)

**Indirectly Affected**:
- Analysis latency (increases 5x)

**Not Affected**:
- Other agents
- Analysis quality (results should be identical)

### Verification Tests

```bash
# 1. Sequential execution restored
uv run tests/test_socratic_sequential.py

# Expected: Questions asked sequentially, all answered

# 2. Result consistency
uv run tests/test_socratic_result_consistency.py --compare baseline_sequential.json

# Expected: Results identical to baseline

# 3. No errors
uv run tests/test_socratic_error_rate.py

# Expected: Error rate <= baseline
```

### Recovery Time

- Detection: < 5 minutes
- Revert: 5 minutes (1 file, simple change)
- Verification: 10 minutes (consistency tests)
- Merge: 5 minutes

**Total: ~25 minutes** (fastest rollback)

### Post-Rollback Actions

1. Review parallel Task pattern: Was it used correctly?
2. Check Claude Code docs: Is parallel Task supported?
3. Test simple parallel example: Isolate issue
4. Consider alternative: asyncio for parallel execution
5. Re-test with corrected parallel pattern

---

## Rollback Decision Matrix

| Improvement | Auto Rollback Threshold | Manual Review Required | Recovery Time |
|-------------|------------------------|------------------------|---------------|
| #1 Uncertainty | Accuracy < baseline | No | 25 min |
| #2 CoT | Accuracy < baseline + 10% | No | 30 min |
| #3 Dynamic Gate | False rejection > 10% | Yes (if > 20%) | 35 min |
| #4 Ontology | False positive > 5% | Yes (if > 10%) | 45 min |
| #5 HITL | False trigger > 20% | Yes (if blocking) | 35 min |
| #6 Parallel | Result inconsistency | No | 25 min |

**Auto Rollback**: Triggered automatically by CI/CD tests
**Manual Review**: Human decision required before rollback

---

## Rollback Communication

### Internal Notification

```
ALERT: Improvement #N Rollback Initiated

Reason: [Failure condition]
Triggered by: [Automated test | Manual report]
Affected components: [List]
Expected recovery time: [N minutes]
Status dashboard: [Link]
```

### Post-Rollback Report

```markdown
## Rollback Report: Improvement #N

**Date**: YYYY-MM-DD
**Duration**: [N minutes]
**Trigger**: [Condition]

### Failure Analysis
- Root cause: [Description]
- Test results: [Links to logs]
- Affected metrics: [Before/after]

### Remediation Plan
1. [Action 1]
2. [Action 2]
3. [Re-test date]

### Lessons Learned
- [Lesson 1]
- [Lesson 2]
```

---

## Automated Rollback Script

**File**: `scripts/rollback.sh`

```bash
#!/bin/bash

# Usage: ./scripts/rollback.sh <improvement_number> <reason>

IMPROVEMENT_NUM=$1
REASON=$2
DATE=$(date +%Y%m%d)

if [ -z "$IMPROVEMENT_NUM" ] || [ -z "$REASON" ]; then
    echo "Usage: ./scripts/rollback.sh <1-6> <reason>"
    exit 1
fi

echo "🚨 Initiating rollback for Improvement #$IMPROVEMENT_NUM"
echo "Reason: $REASON"
echo "Date: $DATE"

# Create rollback branch
git checkout -b "rollback/improvement-$IMPROVEMENT_NUM-$DATE"

# Revert based on improvement number
case $IMPROVEMENT_NUM in
    1)
        echo "Reverting uncertainty modeling..."
        git checkout HEAD~1 -- agents/relationship_definer.py
        ;;
    2)
        echo "Reverting CoT prompting..."
        git checkout HEAD~1 -- agents/relationship_definer.py
        ;;
    3)
        echo "Reverting dynamic quality gate..."
        git rm agents/criticality_config.py
        git checkout HEAD~2 -- agents/meta_orchestrator.py
        ;;
    4)
        echo "Reverting ontology system..."
        git rm agents/relationship_ontology.py
        git rm agents/quality_agent.py
        git checkout HEAD~3 -- agents/relationship_definer.py
        ;;
    5)
        echo "Reverting HITL framework..."
        git rm agents/hitl_checkpoints.py
        git checkout HEAD~4 -- agents/meta_orchestrator.py
        ;;
    6)
        echo "Reverting parallel Q&A..."
        git checkout HEAD~1 -- agents/socratic_mediator_agent.py
        ;;
    *)
        echo "Invalid improvement number: $IMPROVEMENT_NUM"
        exit 1
        ;;
esac

# Commit
git add -A
git commit -m "Rollback: Improvement #$IMPROVEMENT_NUM - $REASON"

# Run verification tests
echo "🧪 Running verification tests..."
uv run pytest tests/test_baseline_*.py -v

if [ $? -eq 0 ]; then
    echo "✅ Verification passed"
    echo "Ready to merge to main"
else
    echo "❌ Verification failed"
    echo "Manual investigation required"
    exit 1
fi
```

---

## Summary

| Improvement | Files to Revert | Recovery Time | Risk Level |
|-------------|----------------|---------------|------------|
| #1 Uncertainty | 1 file | 25 min | Low |
| #2 CoT | 1 file | 30 min | Low |
| #3 Dynamic Gate | 2 files | 35 min | Medium |
| #4 Ontology | 3 files | 45 min | High |
| #5 HITL | 2 files | 35 min | Medium |
| #6 Parallel | 1 file | 25 min | Low |

**Average Recovery Time**: 32.5 minutes
**Maximum Recovery Time**: 45 minutes (Improvement #4)

All rollbacks are designed to be:
- **Fast**: < 1 hour from decision to completion
- **Safe**: Automated verification before merge
- **Documented**: Clear failure analysis and remediation
- **Reversible**: Changes can be re-applied after fixing issues
