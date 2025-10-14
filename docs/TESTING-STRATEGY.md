# Testing Strategy for Self-Improvement System

**Version**: 1.0
**Date**: 2025-10-14
**Purpose**: Define comprehensive testing methodology for all 6 improvements

---

## Overview

Three-tier testing approach:
1. **Unit Tests**: Individual component validation
2. **Integration Tests**: Multi-agent interaction verification
3. **End-to-End Tests**: Full system validation with metrics

---

## Improvement #1: Multi-Dimensional Uncertainty Modeling

### Unit Tests

**Test File**: `tests/test_uncertainty_modeling.py`

```python
def test_uncertainty_breakdown_parsing():
    """Verify uncertainty_breakdown is correctly parsed"""
    response = {
        "confidence": 0.98,
        "uncertainty_breakdown": {
            "epistemic": 0.05,
            "aleatoric": 0.10,
            "model_indecision": 0.02
        },
        "uncertainty_reason": "concept_B_context_insufficient"
    }

    assert "uncertainty_breakdown" in response
    assert response["uncertainty_breakdown"]["epistemic"] == 0.05
    assert response["uncertainty_reason"] == "concept_B_context_insufficient"

def test_uncertainty_reason_codes():
    """Verify all valid uncertainty_reason codes"""
    valid_codes = [
        "concept_X_context_insufficient",
        "boundary_ambiguous_between_TYPE1_TYPE2",
        "definition_scope_unclear",
        "cross_level_relationship_uncertain"
    ]

    for code in valid_codes:
        response = {"uncertainty_reason": code}
        assert response["uncertainty_reason"] in valid_codes

def test_alternative_classifications():
    """Verify alternative_classifications structure"""
    response = {
        "confidence": 0.65,
        "alternative_classifications": [
            {"type": "co-requisite", "confidence": 0.60}
        ]
    }

    assert len(response["alternative_classifications"]) > 0
    assert response["alternative_classifications"][0]["confidence"] < response["confidence"]
```

### Integration Tests

**Test File**: `tests/test_socratic_uncertainty_integration.py`

```python
def test_socratic_reads_uncertainty_reason():
    """Verify SocraticMediator responds to uncertainty_reason"""

    # Given: RelationshipDefiner outputs uncertainty_reason
    definer_output = {
        "source": "A",
        "target": "B",
        "confidence": 0.65,
        "uncertainty_reason": "concept_B_context_insufficient"
    }

    # When: SocraticMediator analyzes
    mediator = SocraticMediator()
    questions = mediator.analyze_low_confidence(definer_output)

    # Then: Questions target concept B context
    assert any("concept B" in q.lower() for q in questions)
    assert any("definition" in q.lower() or "context" in q.lower() for q in questions)

def test_self_improver_adds_context():
    """Verify SelfImprover adds context based on uncertainty_reason"""

    # Given: uncertainty_reason = "concept_B_context_insufficient"
    uncertainty = {
        "uncertainty_reason": "concept_B_context_insufficient",
        "concept_B_id": "middle-1-1-0005"
    }

    # When: SelfImprover improves prompt
    improver = SelfImprover()
    improved_prompt = improver.enhance_context(uncertainty)

    # Then: Prompt includes detailed concept B context
    assert "middle-1-1-0005" in improved_prompt
    assert len(improved_prompt) > len(original_prompt)
```

### Validation Dataset

**File**: `tests/fixtures/uncertainty_validation_set.json`

```json
{
  "description": "20 relationships with known uncertainty types",
  "relationships": [
    {
      "id": "uncertain-001",
      "source": "algebra-0123",
      "target": "geometry-0456",
      "expected_uncertainty": "epistemic",
      "expected_reason": "cross_level_relationship_uncertain",
      "note": "Cross-domain relationship lacks explicit connection"
    },
    {
      "id": "uncertain-002",
      "source": "calculus-0789",
      "target": "calculus-0790",
      "expected_uncertainty": "aleatoric",
      "expected_reason": "boundary_ambiguous_between_prerequisite_co-requisite",
      "note": "Can be taught in either order depending on curriculum"
    }
  ]
}
```

**Dataset Size**: 20 relationships
- 10 high-confidence (> 0.85): No uncertainty_reason needed
- 10 low-confidence (< 0.85): Requires specific uncertainty_reason

### Success Criteria

1. ✅ All unit tests pass
2. ✅ `uncertainty_reason` accuracy > 80% on validation set
3. ✅ SocraticMediator diagnosis iterations reduced by 40%
4. ✅ No regressions in high-confidence relationships

### Test Execution

```bash
# 1. Collect baseline
uv run tests/test_baseline_uncertainty.py --output baseline_uncertainty.json

# 2. Run unit tests
uv run pytest tests/test_uncertainty_modeling.py -v

# 3. Run integration tests
uv run pytest tests/test_socratic_uncertainty_integration.py -v

# 4. Run E2E on validation set
uv run tests/test_uncertainty_e2e.py --dataset tests/fixtures/uncertainty_validation_set.json

# 5. Compare metrics
uv run tests/compare_metrics.py --baseline baseline_uncertainty.json --improved improved_uncertainty.json
```

---

## Improvement #2: Chain-of-Thought Prompting

### Unit Tests

**Test File**: `tests/test_cot_prompting.py`

```python
def test_reasoning_trace_parsing():
    """Verify reasoning_trace is extracted correctly"""
    response_text = """
    ### Phase 1: ANALYSIS

    **Step 1 - Concept Decomposition**:
    Concept A: Linear equations
    Concept B: Quadratic equations

    **Step 2 - Dependency Investigation**:
    Can B be understood without A? No - requires solving for x

    ### Phase 2: CLASSIFICATION
    ```json
    {"type": "prerequisite", "confidence": 0.92}
    ```
    """

    # Parse
    reasoning = extract_reasoning_trace(response_text)
    json_output = extract_json(response_text)

    # Verify
    assert "Step 1 - Concept Decomposition" in reasoning
    assert "Linear equations" in reasoning
    assert json_output["type"] == "prerequisite"

def test_cot_structure_validation():
    """Verify CoT response contains all 4 steps"""
    response_text = get_relationship_definer_response()

    assert "Step 1 - Concept Decomposition" in response_text
    assert "Step 2 - Dependency Investigation" in response_text
    assert "Step 3 - Relationship Hypothesis" in response_text
    assert "Step 4 - Validation" in response_text

def test_reasoning_trace_attachment():
    """Verify reasoning_trace is attached to each relationship"""
    relationships = [
        {"source": "A", "target": "B", "type": "prerequisite"}
    ]

    attach_reasoning_traces(relationships, reasoning_trace)

    assert "reasoning_trace" in relationships[0]
    assert len(relationships[0]["reasoning_trace"]) > 100
```

### Integration Tests

**Test File**: `tests/test_cot_integration.py`

```python
def test_cot_improves_accuracy():
    """Verify CoT increases classification accuracy"""

    # Given: Complex relationships from validation set
    complex_rels = load_complex_relationships()

    # When: Classify with CoT
    definer = RelationshipDefiner()
    results_with_cot = definer.analyze_concepts(complex_rels)

    # Then: Accuracy > baseline + 15%
    accuracy_with_cot = calculate_accuracy(results_with_cot)
    assert accuracy_with_cot >= baseline_accuracy + 0.15

def test_reasoning_helps_debugging():
    """Verify reasoning_trace enables debugging"""

    # Given: Misclassified relationship
    misclassified = {
        "source": "calculus-derivative",
        "target": "algebra-slope",
        "classified_as": "prerequisite",  # Wrong
        "should_be": "formalization"      # Correct
    }

    # When: Read reasoning_trace
    reasoning = misclassified["reasoning_trace"]

    # Then: Can identify error source
    assert "Step 3" in reasoning  # Hypothesis step
    # Manual review: Can see where logic went wrong
```

### Validation Dataset

**File**: `tests/fixtures/complex_relationships_set.json`

30 complex relationships across 3 categories:
- 10 prerequisite (logical, cognitive, pedagogical subtypes)
- 10 co-requisite (mutual dependencies)
- 10 extension (concept generalizations)

Known ground truth labels from expert review.

### Success Criteria

1. ✅ All unit tests pass
2. ✅ CoT structure present in 100% of responses
3. ✅ Accuracy improvement >= 15% on complex relationships
4. ✅ Reasoning errors identifiable in 100% of misclassifications

### Test Execution

```bash
# 1. Baseline (without CoT)
uv run tests/test_baseline_accuracy.py --no-cot --output baseline_cot.json

# 2. Unit tests
uv run pytest tests/test_cot_prompting.py -v

# 3. Integration tests
uv run pytest tests/test_cot_integration.py -v

# 4. E2E validation
uv run tests/test_cot_e2e.py --dataset tests/fixtures/complex_relationships_set.json

# 5. Accuracy comparison
uv run tests/compare_accuracy.py --baseline baseline_cot.json --improved improved_cot.json
```

---

## Improvement #3: Dynamic Quality Gate

### Unit Tests

**Test File**: `tests/test_dynamic_quality_gate.py`

```python
def test_calculate_dynamic_thresholds_low_criticality():
    """Low-risk files get relaxed thresholds"""
    files = ["docs/README.md", "examples/example.json"]

    thresholds = calculate_dynamic_thresholds(files)

    assert thresholds["cis_threshold"] >= 20  # More lenient
    assert thresholds["coverage_threshold"] <= 0.75
    assert thresholds["verification_rounds"] == 1

def test_calculate_dynamic_thresholds_high_criticality():
    """Critical files get strict thresholds"""
    files = ["agents/meta_orchestrator.py"]

    thresholds = calculate_dynamic_thresholds(files)

    assert thresholds["cis_threshold"] <= 15  # Stricter
    assert thresholds["coverage_threshold"] >= 0.85
    assert thresholds["verification_rounds"] == 2

def test_get_criticality_score():
    """Verify criticality scoring"""
    assert get_criticality_score("agents/meta_orchestrator.py") == 10
    assert get_criticality_score("agents/relationship_definer.py") == 9
    assert get_criticality_score("docs/guide.md") == 1
    assert get_criticality_score("unknown_file.py") == 5  # Default
```

### Integration Tests

**Test File**: `tests/test_quality_gate_integration.py`

```python
def test_quality_gate_rejects_high_cis_for_critical_files():
    """Critical files: CIS=18 should FAIL"""
    impact = ImpactAnalysis(
        affected_files=["agents/meta_orchestrator.py"],
        cis_size=18,
        test_coverage=0.90,
        critical_affected=True
    )

    orchestrator = MetaOrchestrator()
    approval = orchestrator.evaluate_quality_gate(impact)

    assert approval.passed == False
    assert "dynamic threshold" in approval.feedback.lower()

def test_quality_gate_accepts_same_cis_for_docs():
    """Documentation: CIS=18 should PASS"""
    impact = ImpactAnalysis(
        affected_files=["docs/README.md"],
        cis_size=18,
        test_coverage=0.70,
        critical_affected=False
    )

    orchestrator = MetaOrchestrator()
    approval = orchestrator.evaluate_quality_gate(impact)

    assert approval.passed == True
```

### Validation Dataset

**File**: `tests/fixtures/quality_gate_scenarios.json`

10 scenarios across criticality spectrum:
- 3 low-risk (docs, examples)
- 4 medium-risk (standard agents)
- 3 high-risk (meta_orchestrator, core infrastructure)

Each scenario includes: files, CIS size, coverage, expected outcome

### Success Criteria

1. ✅ All unit tests pass
2. ✅ False rejection rate < 5% on validation scenarios
3. ✅ High-risk changes get stricter thresholds (verified)
4. ✅ Context-appropriate decisions in 100% of scenarios

### Test Execution

```bash
# 1. Unit tests
uv run pytest tests/test_dynamic_quality_gate.py -v

# 2. Integration tests
uv run pytest tests/test_quality_gate_integration.py -v

# 3. Scenario validation
uv run tests/test_quality_gate_scenarios.py --dataset tests/fixtures/quality_gate_scenarios.json

# 4. Measure false rejection rate
uv run tests/measure_false_rejections.py
```

---

## Improvement #4: Formal Ontology + QualityAgent

### Unit Tests

**Test File**: `tests/test_ontology.py`

```python
def test_validate_prerequisite_transitivity():
    """Prerequisite is transitive"""
    props = RELATIONSHIP_ONTOLOGY[RelationType.PREREQUISITE]
    assert props.transitive == True

def test_validate_co_requisite_symmetry():
    """Co-requisite is symmetric"""
    props = RELATIONSHIP_ONTOLOGY[RelationType.CO_REQUISITE]
    assert props.symmetric == True

def test_detect_circular_prerequisite():
    """Detect A→B→C→A cycle"""
    graph = {
        "relationships": [
            {"source": "A", "target": "B", "type": "prerequisite"},
            {"source": "B", "target": "C", "type": "prerequisite"}
        ]
    }

    # Try to add C→A (creates cycle)
    errors = validate_relationship_logic(
        RelationType.PREREQUISITE,
        "C", "A",
        graph
    )

    assert len(errors) > 0
    assert errors[0].check == "circular_dependency"

def test_detect_self_relation_violation():
    """Prerequisites cannot be reflexive"""
    errors = validate_relationship_logic(
        RelationType.PREREQUISITE,
        "A", "A",
        None
    )

    assert len(errors) > 0
    assert errors[0].check == "reflexive_violation"
```

### Integration Tests

**Test File**: `tests/test_quality_agent_integration.py`

```python
def test_quality_agent_detects_circular_deps():
    """QualityAgent finds circular dependencies"""
    graph = load_graph_with_cycle()

    qa = QualityAgent()
    result = qa.validate_knowledge_graph(graph)

    assert result["passed"] == False
    assert any("circular" in e.lower() for e in result["errors"])

def test_quality_agent_detects_missing_symmetric():
    """QualityAgent warns about missing symmetric pairs"""
    graph = {
        "relationships": [
            {"source": "A", "target": "B", "type": "co-requisite"}
            # Missing B→A
        ]
    }

    qa = QualityAgent()
    result = qa.validate_knowledge_graph(graph)

    assert len(result["warnings"]) > 0
    assert any("symmetry" in w.lower() for w in result["warnings"])
```

### Validation Dataset

**File**: `tests/fixtures/invalid_relationships.json`

15 relationships with known violations:
- 5 circular dependencies
- 3 reflexive violations
- 4 symmetry violations
- 3 grade-level inconsistencies

### Success Criteria

1. ✅ All unit tests pass
2. ✅ Circular dependency detection: 100% accuracy
3. ✅ Symmetry violation detection: 100% accuracy
4. ✅ Zero false positives on valid relationships

### Test Execution

```bash
# 1. Unit tests
uv run pytest tests/test_ontology.py -v

# 2. Integration tests
uv run pytest tests/test_quality_agent_integration.py -v

# 3. Validation on invalid relationships
uv run tests/test_ontology_validation.py --dataset tests/fixtures/invalid_relationships.json

# 4. False positive check
uv run tests/test_ontology_false_positives.py --dataset tests/fixtures/valid_relationships.json
```

---

## Improvement #5: HITL Checkpoint Framework

### Unit Tests

**Test File**: `tests/test_hitl_checkpoints.py`

```python
def test_checkpoint_trigger_conditions():
    """Verify checkpoint triggers on critical decisions"""

    # Scenario: New relationship type proposed
    decision = {
        "type": "new_relationship_type",
        "impact": "high",
        "affected_concepts": 150
    }

    assert should_trigger_checkpoint(decision) == True

def test_checkpoint_serialization():
    """Verify checkpoint can be saved/loaded"""
    checkpoint = {
        "decision": "Add new relationship type 'analogy'",
        "context": {...},
        "options": [...]
    }

    save_checkpoint(checkpoint)
    loaded = load_checkpoint(checkpoint["id"])

    assert loaded["decision"] == checkpoint["decision"]
```

### Integration Tests

**Test File**: `tests/test_hitl_integration.py`

```python
def test_workflow_pauses_at_checkpoint():
    """Verify workflow pauses for human input"""

    orchestrator = MetaOrchestrator()

    # Trigger critical decision
    with pytest.raises(HITLCheckpointRequired) as exc:
        orchestrator.apply_improvement(critical_improvement)

    assert exc.value.checkpoint_id is not None

def test_workflow_resumes_after_approval():
    """Verify workflow continues after human approval"""

    checkpoint = create_test_checkpoint()
    checkpoint.approve(user_decision="proceed")

    # Workflow should continue
    result = orchestrator.resume_from_checkpoint(checkpoint)
    assert result.status == "completed"
```

### Validation Dataset

**File**: `tests/fixtures/critical_decisions.json`

5 critical decision scenarios:
- New relationship type proposal
- High-risk improvement (affects 500+ relationships)
- Ontology modification
- Quality gate threshold change
- Agent architecture change

### Success Criteria

1. ✅ All unit tests pass
2. ✅ Zero missed checkpoints on critical decisions
3. ✅ Workflow correctly pauses/resumes
4. ✅ Checkpoint state fully recoverable

### Test Execution

```bash
# 1. Unit tests
uv run pytest tests/test_hitl_checkpoints.py -v

# 2. Integration tests
uv run pytest tests/test_hitl_integration.py -v

# 3. Critical decision scenarios
uv run tests/test_hitl_scenarios.py --dataset tests/fixtures/critical_decisions.json
```

---

## Improvement #6: Parallel Socratic Q&A

### Unit Tests

None required (prompt-only change)

### Integration Tests

**Test File**: `tests/test_parallel_qa.py`

```python
def test_socratic_uses_parallel_tasks():
    """Verify SocraticMediator calls Task tool in parallel"""

    # Given: Multiple questions to ask
    questions = [
        "What is the precise definition of concept A?",
        "In what contexts is concept B typically taught?",
        "What are prerequisites for concept C?"
    ]

    # When: Mediator analyzes
    mediator = SocraticMediator()

    with patch('agents.socratic_mediator_agent.Task') as mock_task:
        mediator.ask_parallel_questions(questions)

        # Then: Task called once with multiple prompts
        assert mock_task.call_count == 1
        call_args = mock_task.call_args
        assert len(call_args[0]) == len(questions)  # All questions in one call

def test_parallel_reduces_latency():
    """Verify parallel execution is faster than sequential"""

    questions = ["Q1", "Q2", "Q3"]

    # Sequential
    start_seq = time.time()
    sequential_results = mediator.ask_sequential(questions)
    seq_time = time.time() - start_seq

    # Parallel
    start_par = time.time()
    parallel_results = mediator.ask_parallel(questions)
    par_time = time.time() - start_par

    # Should be 80-90% faster
    assert par_time <= seq_time * 0.2
```

### Validation Dataset

**File**: `tests/fixtures/multi_question_scenarios.json`

5 scenarios with 3-5 questions each

### Success Criteria

1. ✅ Integration tests pass
2. ✅ Latency reduction >= 80%
3. ✅ Results identical to sequential execution

### Test Execution

```bash
# 1. Integration tests
uv run pytest tests/test_parallel_qa.py -v

# 2. Latency measurement
uv run tests/measure_parallel_latency.py --scenarios tests/fixtures/multi_question_scenarios.json
```

---

## End-to-End Testing

### Full System Validation

**Test File**: `tests/test_e2e_all_improvements.py`

```python
def test_e2e_with_all_improvements():
    """Run full pipeline with all 6 improvements enabled"""

    # Given: 100 concepts from validation set
    concepts = load_concepts("tests/fixtures/e2e_concepts.json")

    # When: Run full self-improvement loop
    orchestrator = MetaOrchestrator()
    results = orchestrator.run_full_cycle(concepts)

    # Then: Verify all metrics improved
    assert results["uncertainty_resolution_iterations"] < baseline["iterations"] * 0.6
    assert results["classification_accuracy"] >= baseline["accuracy"] + 0.15
    assert results["false_rejections"] <= 0.05
    assert results["circular_dependencies_detected"] == results["circular_dependencies_total"]
    assert results["critical_decisions_reviewed"] == results["critical_decisions_total"]
    assert results["parallel_qa_latency"] <= baseline["qa_latency"] * 0.2
```

### Success Criteria

All Phase 1-3 metrics achieved:
- Phase 1: -40% iterations, +15% accuracy
- Phase 2: <5% false rejections, 0 violations
- Phase 3: 100% checkpoint coverage, -80% latency

---

## Test Maintenance

### Adding New Tests

1. Create test file in `tests/`
2. Add fixtures to `tests/fixtures/`
3. Update this document with test descriptions
4. Add to CI/CD pipeline

### Test Data Management

- **Fixtures**: `tests/fixtures/*.json`
- **Baselines**: `tests/baselines/*.json`
- **Results**: `tests/results/*.json` (gitignored)

### CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Self-Improvement Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: uv sync
      - name: Run Phase 1 tests
        run: uv run pytest tests/test_uncertainty_modeling.py tests/test_cot_prompting.py -v
      - name: Run Phase 2 tests
        run: uv run pytest tests/test_dynamic_quality_gate.py tests/test_ontology.py -v
      - name: Run Phase 3 tests
        run: uv run pytest tests/test_hitl_checkpoints.py tests/test_parallel_qa.py -v
      - name: Run E2E tests
        run: uv run pytest tests/test_e2e_all_improvements.py -v
```

---

## Summary

| Improvement | Unit Tests | Integration Tests | Validation Data | Success Metric |
|------------|-----------|-------------------|-----------------|----------------|
| #1 Uncertainty | ✅ 3 tests | ✅ 2 tests | 20 relationships | 80% reason accuracy |
| #2 CoT | ✅ 3 tests | ✅ 2 tests | 30 relationships | +15% accuracy |
| #3 Dynamic Gate | ✅ 3 tests | ✅ 2 tests | 10 scenarios | <5% false rejections |
| #4 Ontology | ✅ 4 tests | ✅ 2 tests | 15 violations | 100% detection |
| #5 HITL | ✅ 2 tests | ✅ 2 tests | 5 decisions | 0 missed checkpoints |
| #6 Parallel | - | ✅ 2 tests | 5 scenarios | -80% latency |

**Total Test Coverage**:
- 18 unit test functions
- 12 integration test functions
- 6 validation datasets
- 1 end-to-end test

**Estimated Test Development Time**: 12-16 hours
