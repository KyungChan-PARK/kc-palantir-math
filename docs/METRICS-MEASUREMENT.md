# Metrics Measurement Methodology

**Version**: 1.0
**Date**: 2025-10-14
**Purpose**: Define how to collect, measure, and validate success metrics for all 6 improvements

---

## Overview

Each improvement has defined success metrics (from CODE-IMPROVEMENT-PLAN.md):

| Improvement | Key Metric | Target | Measurement Method |
|------------|-----------|--------|-------------------|
| #1 Uncertainty | Diagnosis iterations | -40% | Count SocraticMediator rounds |
| #2 CoT | Classification accuracy | +15% | Validate against ground truth |
| #3 Dynamic Gate | False rejection rate | <5% | Count inappropriate rejections |
| #4 Ontology | Violation detection | 100% | Test on known violations |
| #5 HITL | Checkpoint coverage | 100% | Verify all critical decisions reviewed |
| #6 Parallel | Latency reduction | -80% | Measure execution time |

---

## General Measurement Framework

### Step 1: Baseline Collection

**Before implementing any improvement**, collect baseline metrics:

```python
# Script: tests/collect_baseline.py

from pathlib import Path
import json
from datetime import datetime

class BaselineCollector:
    """Collect baseline metrics before improvements"""

    def __init__(self, output_dir: Path = Path("tests/baselines")):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)

    def collect_all_baselines(self):
        """Run all baseline collections"""
        baselines = {
            "collection_date": datetime.now().isoformat(),
            "system_version": "pre-improvement",
            "metrics": {
                "uncertainty": self.measure_uncertainty_baseline(),
                "cot": self.measure_cot_baseline(),
                "quality_gate": self.measure_quality_gate_baseline(),
                "ontology": self.measure_ontology_baseline(),
                "hitl": self.measure_hitl_baseline(),
                "parallel": self.measure_parallel_baseline()
            }
        }

        output_file = self.output_dir / f"baseline-{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, 'w') as f:
            json.dump(baselines, f, indent=2)

        return baselines
```

### Step 2: Post-Improvement Measurement

After implementing improvement, re-run same measurement:

```python
# Script: tests/measure_improvement.py

class ImprovementMeasurer:
    """Measure metrics after improvement"""

    def measure_improvement(self, improvement_num: int, baseline_file: Path):
        """Compare improvement against baseline"""

        # Load baseline
        with open(baseline_file) as f:
            baseline = json.load(f)

        # Re-run measurement
        current = self.collect_metrics(improvement_num)

        # Calculate delta
        comparison = self.compare_metrics(baseline, current, improvement_num)

        return comparison
```

### Step 3: Statistical Validation

Use appropriate statistical tests:

```python
from scipy import stats

def validate_improvement_significance(
    baseline_samples: List[float],
    improved_samples: List[float],
    improvement_target: float,
    test_type: str = "ttest"
) -> Dict:
    """
    Validate improvement is statistically significant

    Args:
        baseline_samples: Baseline metric samples
        improved_samples: Post-improvement samples
        improvement_target: Expected improvement (e.g., 0.15 for +15%)
        test_type: "ttest" or "wilcoxon"

    Returns:
        Statistical test results
    """

    # Calculate means
    baseline_mean = np.mean(baseline_samples)
    improved_mean = np.mean(improved_samples)
    actual_improvement = (improved_mean - baseline_mean) / baseline_mean

    # Statistical test
    if test_type == "ttest":
        statistic, p_value = stats.ttest_ind(improved_samples, baseline_samples)
    elif test_type == "wilcoxon":
        statistic, p_value = stats.wilcoxon(improved_samples, baseline_samples)

    return {
        "baseline_mean": baseline_mean,
        "improved_mean": improved_mean,
        "actual_improvement": actual_improvement,
        "target_improvement": improvement_target,
        "target_met": actual_improvement >= improvement_target,
        "statistic": statistic,
        "p_value": p_value,
        "significant": p_value < 0.05
    }
```

---

## Improvement #1: Uncertainty Modeling

### Metric: SocraticMediator Diagnosis Iterations

**Target**: -40% reduction
**Baseline**: Average iterations needed to resolve low-confidence relationships

### Baseline Collection

```python
def measure_uncertainty_baseline(self):
    """Measure baseline diagnosis iterations"""

    # Load validation set: 20 low-confidence relationships
    validation_set = load_fixture("tests/fixtures/uncertainty_validation_set.json")

    iterations = []

    for rel in validation_set["relationships"]:
        # Run RelationshipDefiner
        definer = RelationshipDefiner()
        result = definer.analyze_relationship(rel["source"], rel["target"])

        # Count SocraticMediator rounds needed
        if result["confidence"] < 0.85:
            mediator = SocraticMediator()
            rounds = mediator.diagnose_and_improve(result)
            iterations.append(rounds)

    return {
        "avg_iterations": np.mean(iterations),
        "median_iterations": np.median(iterations),
        "max_iterations": np.max(iterations),
        "sample_size": len(iterations),
        "raw_data": iterations
    }
```

### Post-Improvement Measurement

```python
def measure_uncertainty_improved(self):
    """Measure with uncertainty_breakdown available"""

    validation_set = load_fixture("tests/fixtures/uncertainty_validation_set.json")
    iterations = []

    for rel in validation_set["relationships"]:
        # RelationshipDefiner now outputs uncertainty_breakdown
        definer = RelationshipDefiner()
        result = definer.analyze_relationship(rel["source"], rel["target"])

        if result["confidence"] < 0.85:
            # SocraticMediator uses uncertainty_reason
            mediator = SocraticMediator()
            rounds = mediator.diagnose_targeted(result)  # New method
            iterations.append(rounds)

    return {
        "avg_iterations": np.mean(iterations),
        "median_iterations": np.median(iterations),
        "improvement_pct": (baseline_avg - np.mean(iterations)) / baseline_avg,
        "target_met": improvement_pct >= 0.40,
        "raw_data": iterations
    }
```

### Validation

```bash
# 1. Collect baseline
uv run python tests/measure_uncertainty.py --mode baseline --output baseline_uncertainty.json

# 2. Implement improvement #1
# ... (implement uncertainty modeling) ...

# 3. Measure improved
uv run python tests/measure_uncertainty.py --mode improved --output improved_uncertainty.json

# 4. Compare
uv run python tests/compare_metrics.py \
  --baseline baseline_uncertainty.json \
  --improved improved_uncertainty.json \
  --target -0.40 \
  --test ttest

# Expected output:
# ✅ Target met: -42% iterations (target: -40%)
# ✅ Statistically significant (p=0.003)
```

### Success Criteria

- ✅ Average iterations reduced by >= 40%
- ✅ Statistically significant (p < 0.05)
- ✅ No increase in max iterations (prevent outliers)

---

## Improvement #2: Chain-of-Thought Prompting

### Metric: Classification Accuracy

**Target**: +15% improvement
**Baseline**: Accuracy on complex relationships

### Baseline Collection

```python
def measure_cot_baseline(self):
    """Measure baseline accuracy without CoT"""

    # Load ground truth: 30 complex relationships with expert labels
    ground_truth = load_fixture("tests/fixtures/complex_relationships_set.json")

    predictions = []
    actuals = []

    for rel in ground_truth["relationships"]:
        # RelationshipDefiner (no CoT)
        definer = RelationshipDefiner()
        result = definer.analyze_relationship(rel["source"], rel["target"])

        predictions.append(result["type"])
        actuals.append(rel["ground_truth_type"])

    # Calculate accuracy
    accuracy = accuracy_score(actuals, predictions)

    # Per-type accuracy
    per_type = {}
    for rel_type in set(actuals):
        type_mask = [a == rel_type for a in actuals]
        type_acc = accuracy_score(
            [a for a, m in zip(actuals, type_mask) if m],
            [p for p, m in zip(predictions, type_mask) if m]
        )
        per_type[rel_type] = type_acc

    return {
        "overall_accuracy": accuracy,
        "per_type_accuracy": per_type,
        "sample_size": len(ground_truth),
        "confusion_matrix": confusion_matrix(actuals, predictions).tolist()
    }
```

### Post-Improvement Measurement

```python
def measure_cot_improved(self):
    """Measure accuracy with CoT prompting"""

    ground_truth = load_fixture("tests/fixtures/complex_relationships_set.json")

    predictions = []
    actuals = []

    for rel in ground_truth["relationships"]:
        # RelationshipDefiner with CoT
        definer = RelationshipDefiner()
        result = definer.analyze_relationship(rel["source"], rel["target"])

        # Verify reasoning_trace exists
        assert "reasoning_trace" in result

        predictions.append(result["type"])
        actuals.append(rel["ground_truth_type"])

    accuracy = accuracy_score(actuals, predictions)

    return {
        "overall_accuracy": accuracy,
        "improvement_pct": (accuracy - baseline_accuracy) / baseline_accuracy,
        "improvement_abs": accuracy - baseline_accuracy,
        "target_met": accuracy >= baseline_accuracy + 0.15,
        "confusion_matrix": confusion_matrix(actuals, predictions).tolist()
    }
```

### Validation

```bash
# 1. Baseline
uv run python tests/measure_accuracy.py --mode baseline --output baseline_cot.json

# 2. Implement CoT
# ...

# 3. Improved
uv run python tests/measure_accuracy.py --mode improved --output improved_cot.json

# 4. Compare
uv run python tests/compare_metrics.py \
  --baseline baseline_cot.json \
  --improved improved_cot.json \
  --target 0.15 \
  --test mcnemar

# Expected:
# ✅ Accuracy: 0.78 → 0.91 (+16.7%, target: +15%)
# ✅ McNemar test significant (p=0.012)
```

### Success Criteria

- ✅ Overall accuracy improvement >= 15%
- ✅ Improvement on at least 2/3 of relationship types
- ✅ McNemar test significant (p < 0.05)

---

## Improvement #3: Dynamic Quality Gate

### Metric: False Rejection Rate

**Target**: <5%
**Baseline**: Percentage of valid improvements rejected

### Baseline Collection

```python
def measure_quality_gate_baseline(self):
    """Measure false rejection rate with static thresholds"""

    # Load scenarios: 50 improvements (25 valid, 25 invalid)
    scenarios = load_fixture("tests/fixtures/quality_gate_scenarios.json")

    results = []

    for scenario in scenarios["improvements"]:
        # Create ImpactAnalysis
        impact = ImpactAnalysis(
            affected_files=scenario["files"],
            cis_size=scenario["cis"],
            test_coverage=scenario["coverage"],
            critical_affected=scenario["critical"]
        )

        # Static quality gate
        orchestrator = MetaOrchestrator()
        approval = orchestrator.evaluate_quality_gate(impact)

        results.append({
            "scenario_id": scenario["id"],
            "is_valid": scenario["is_valid"],
            "approved": approval.passed,
            "false_rejection": scenario["is_valid"] and not approval.passed
        })

    false_rejections = [r for r in results if r["false_rejection"]]

    return {
        "total_scenarios": len(scenarios),
        "false_rejection_count": len(false_rejections),
        "false_rejection_rate": len(false_rejections) / len(scenarios),
        "false_rejections": false_rejections
    }
```

### Post-Improvement Measurement

```python
def measure_quality_gate_improved(self):
    """Measure with dynamic thresholds"""

    scenarios = load_fixture("tests/fixtures/quality_gate_scenarios.json")
    results = []

    for scenario in scenarios["improvements"]:
        impact = ImpactAnalysis(...)

        # Dynamic quality gate (uses criticality_config.py)
        orchestrator = MetaOrchestrator()
        approval = orchestrator.evaluate_quality_gate(impact)

        results.append({
            "scenario_id": scenario["id"],
            "is_valid": scenario["is_valid"],
            "approved": approval.passed,
            "false_rejection": scenario["is_valid"] and not approval.passed,
            "thresholds": approval.metrics.get("dynamic_thresholds")
        })

    false_rejections = [r for r in results if r["false_rejection"]]

    return {
        "false_rejection_count": len(false_rejections),
        "false_rejection_rate": len(false_rejections) / len(scenarios),
        "target_met": len(false_rejections) / len(scenarios) < 0.05,
        "improvement_pct": (baseline_rate - new_rate) / baseline_rate
    }
```

### Validation

```bash
# 1. Baseline
uv run python tests/measure_quality_gate.py --mode baseline --output baseline_gate.json

# 2. Implement dynamic gate
# ...

# 3. Improved
uv run python tests/measure_quality_gate.py --mode improved --output improved_gate.json

# 4. Compare
uv run python tests/compare_metrics.py \
  --baseline baseline_gate.json \
  --improved improved_gate.json \
  --target_rate 0.05

# Expected:
# ✅ False rejection rate: 18% → 2% (target: <5%)
# ✅ Valid improvements approved: 98%
```

### Success Criteria

- ✅ False rejection rate < 5%
- ✅ No increase in false approvals (invalid improvements passing)
- ✅ Context-appropriate thresholds applied

---

## Improvement #4: Formal Ontology + QualityAgent

### Metric: Violation Detection Accuracy

**Target**: 100%
**Baseline**: Manual validation (no automated detection)

### Baseline Collection

```python
def measure_ontology_baseline(self):
    """Baseline: No ontology validation"""

    # Load known violations: 15 relationships with logical errors
    violations = load_fixture("tests/fixtures/invalid_relationships.json")

    # Without ontology validation, these all pass
    detected = []

    for rel in violations["relationships"]:
        # Basic validation only (syntax)
        definer = RelationshipDefiner()
        validation = definer.validate_relationship(rel)

        if validation.get("error"):
            detected.append(rel["id"])

    return {
        "total_violations": len(violations),
        "detected_count": len(detected),
        "detection_rate": len(detected) / len(violations),
        "missed": [v["id"] for v in violations if v["id"] not in detected]
    }
```

### Post-Improvement Measurement

```python
def measure_ontology_improved(self):
    """Measure with QualityAgent validation"""

    violations = load_fixture("tests/fixtures/invalid_relationships.json")

    detected = []

    for rel in violations["relationships"]:
        # QualityAgent checks ontology rules
        qa = QualityAgent()
        result = qa.validate_knowledge_graph({
            "relationships": [rel],
            "concepts": [...]
        })

        if not result["passed"]:
            detected.append(rel["id"])

    return {
        "total_violations": len(violations),
        "detected_count": len(detected),
        "detection_rate": len(detected) / len(violations),
        "target_met": len(detected) == len(violations),
        "missed": [v["id"] for v in violations if v["id"] not in detected]
    }
```

### Validation

```bash
# 1. Baseline (no ontology)
uv run python tests/measure_ontology.py --mode baseline --output baseline_ontology.json

# Expected: 0-20% detection (only syntax errors caught)

# 2. Implement ontology
# ...

# 3. Improved
uv run python tests/measure_ontology.py --mode improved --output improved_ontology.json

# Expected: 100% detection

# 4. False positive check
uv run python tests/measure_ontology_false_positives.py \
  --dataset tests/fixtures/valid_relationships.json

# Expected: 0 false positives
```

### Success Criteria

- ✅ 100% violation detection (all 15 violations caught)
- ✅ 0% false positive rate (valid relationships not flagged)
- ✅ All violation types detected (circular, reflexive, symmetry)

---

## Improvement #5: HITL Framework

### Metric: Checkpoint Coverage

**Target**: 100%
**Baseline**: 0% (no human review)

### Baseline Collection

```python
def measure_hitl_baseline(self):
    """Baseline: All decisions automated"""

    # Load critical decisions: 5 scenarios
    decisions = load_fixture("tests/fixtures/critical_decisions.json")

    # Without HITL, all auto-approved
    checkpoints_triggered = []

    for decision in decisions["scenarios"]:
        # Run MetaOrchestrator
        orchestrator = MetaOrchestrator()
        result = orchestrator.apply_improvement(decision["improvement"])

        # Check if checkpoint was triggered (should be False)
        if result.get("hitl_checkpoint_triggered"):
            checkpoints_triggered.append(decision["id"])

    return {
        "total_critical_decisions": len(decisions),
        "checkpoints_triggered": len(checkpoints_triggered),
        "coverage": len(checkpoints_triggered) / len(decisions),
        "missed": [d["id"] for d in decisions if d["id"] not in checkpoints_triggered]
    }
```

### Post-Improvement Measurement

```python
def measure_hitl_improved(self):
    """Measure with HITL framework"""

    decisions = load_fixture("tests/fixtures/critical_decisions.json")

    checkpoints_triggered = []

    for decision in decisions["scenarios"]:
        orchestrator = MetaOrchestrator()

        try:
            result = orchestrator.apply_improvement(decision["improvement"])
        except HITLCheckpointRequired as exc:
            # Checkpoint correctly triggered
            checkpoints_triggered.append(decision["id"])

    return {
        "total_critical_decisions": len(decisions),
        "checkpoints_triggered": len(checkpoints_triggered),
        "coverage": len(checkpoints_triggered) / len(decisions),
        "target_met": len(checkpoints_triggered) == len(decisions),
        "missed": [d["id"] for d in decisions if d["id"] not in checkpoints_triggered]
    }
```

### Validation

```bash
# 1. Baseline (no HITL)
uv run python tests/measure_hitl.py --mode baseline --output baseline_hitl.json

# Expected: 0% coverage

# 2. Implement HITL
# ...

# 3. Improved
uv run python tests/measure_hitl.py --mode improved --output improved_hitl.json

# Expected: 100% coverage

# 4. False trigger check
uv run python tests/measure_hitl_false_triggers.py \
  --dataset tests/fixtures/non_critical_decisions.json

# Expected: 0 false triggers
```

### Success Criteria

- ✅ 100% critical decision coverage (all 5 checkpoints triggered)
- ✅ <20% false trigger rate on non-critical decisions
- ✅ Workflow pause/resume functional

---

## Improvement #6: Parallel Socratic Q&A

### Metric: Latency Reduction

**Target**: -80%
**Baseline**: Sequential execution time

### Baseline Collection

```python
def measure_parallel_baseline(self):
    """Measure sequential Q&A latency"""

    # Load multi-question scenarios: 5 scenarios, 3-5 questions each
    scenarios = load_fixture("tests/fixtures/multi_question_scenarios.json")

    latencies = []

    for scenario in scenarios["scenarios"]:
        mediator = SocraticMediator()

        start = time.time()

        # Sequential execution
        answers = []
        for question in scenario["questions"]:
            answer = mediator.ask_task(question)
            answers.append(answer)

        elapsed = time.time() - start
        latencies.append(elapsed)

    return {
        "avg_latency_sec": np.mean(latencies),
        "median_latency_sec": np.median(latencies),
        "total_questions": sum(len(s["questions"]) for s in scenarios),
        "raw_latencies": latencies
    }
```

### Post-Improvement Measurement

```python
def measure_parallel_improved(self):
    """Measure parallel Q&A latency"""

    scenarios = load_fixture("tests/fixtures/multi_question_scenarios.json")

    latencies = []

    for scenario in scenarios["scenarios"]:
        mediator = SocraticMediator()

        start = time.time()

        # Parallel execution
        answers = mediator.ask_parallel(scenario["questions"])

        elapsed = time.time() - start
        latencies.append(elapsed)

    return {
        "avg_latency_sec": np.mean(latencies),
        "median_latency_sec": np.median(latencies),
        "improvement_pct": (baseline_latency - np.mean(latencies)) / baseline_latency,
        "target_met": improvement_pct >= 0.80,
        "raw_latencies": latencies
    }
```

### Validation

```bash
# 1. Baseline (sequential)
uv run python tests/measure_parallel.py --mode baseline --output baseline_parallel.json

# 2. Implement parallel
# ...

# 3. Improved
uv run python tests/measure_parallel.py --mode improved --output improved_parallel.json

# 4. Compare
uv run python tests/compare_metrics.py \
  --baseline baseline_parallel.json \
  --improved improved_parallel.json \
  --target -0.80

# Expected:
# ✅ Latency: 45s → 8s (-82%, target: -80%)

# 5. Result consistency check
uv run python tests/verify_parallel_consistency.py

# Expected: Results identical to sequential
```

### Success Criteria

- ✅ Latency reduction >= 80%
- ✅ Results identical to sequential execution
- ✅ No increase in error rate

---

## Metrics Dashboard

### Automated Dashboard Script

**File**: `scripts/metrics_dashboard.py`

```python
"""
Generate metrics dashboard for all improvements
"""

import json
from pathlib import Path
from datetime import datetime

def generate_dashboard():
    """Create HTML dashboard with all metrics"""

    baselines = load_all_baselines()
    improved = load_all_improved_metrics()

    dashboard = {
        "generated_at": datetime.now().isoformat(),
        "improvements": []
    }

    for i in range(1, 7):
        improvement = {
            "id": i,
            "name": IMPROVEMENT_NAMES[i],
            "baseline": baselines.get(f"improvement_{i}"),
            "improved": improved.get(f"improvement_{i}"),
            "target_met": check_target_met(i, baselines, improved),
            "status": get_status(i, baselines, improved)
        }
        dashboard["improvements"].append(improvement)

    # Generate HTML
    html = render_dashboard_html(dashboard)

    output_path = Path("docs/metrics-dashboard.html")
    output_path.write_text(html)

    print(f"✅ Dashboard generated: {output_path}")

if __name__ == "__main__":
    generate_dashboard()
```

### Dashboard Example Output

```
┌─────────────────────────────────────────────────────────────┐
│          Self-Improvement System Metrics Dashboard          │
│                   Generated: 2025-10-14 15:30               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ #1 Uncertainty Modeling                                     │
├─────────────────────────────────────────────────────────────┤
│ Metric: Diagnosis Iterations                                │
│ Baseline: 8.2 iterations                                    │
│ Improved: 4.7 iterations                                    │
│ Change: -42.7% ✅ (target: -40%)                            │
│ Status: TARGET MET                                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ #2 Chain-of-Thought Prompting                               │
├─────────────────────────────────────────────────────────────┤
│ Metric: Classification Accuracy                             │
│ Baseline: 0.78                                              │
│ Improved: 0.91                                              │
│ Change: +16.7% ✅ (target: +15%)                            │
│ Status: TARGET MET                                          │
└─────────────────────────────────────────────────────────────┘

... (remaining improvements)
```

---

## Summary

| Improvement | Metric | Measurement Method | Statistical Test |
|------------|--------|-------------------|-----------------|
| #1 Uncertainty | Diagnosis iterations | Count rounds | t-test |
| #2 CoT | Accuracy | Confusion matrix | McNemar |
| #3 Dynamic Gate | False rejection rate | Scenario validation | Proportion test |
| #4 Ontology | Detection rate | Known violations | Exact match |
| #5 HITL | Coverage | Checkpoint triggering | Exact match |
| #6 Parallel | Latency | Time measurement | t-test |

**Baseline Collection Time**: 2-3 hours
**Post-Improvement Measurement**: 1-2 hours per improvement
**Statistical Validation**: 30 minutes per improvement

**Total Measurement Overhead**: ~15 hours across all 6 improvements
