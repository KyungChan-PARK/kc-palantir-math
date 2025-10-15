# Comprehensive E2E Test Plan - Semantic Layer Based

**Date**: 2025-10-16  
**Scope**: Complete project root integration testing  
**Based on**: meta_orchestrator.py workflows + Palantir 3-tier ontology  
**Approach**: Delete 20 legacy tests → Create 5 new tier-based tests

---

## Overview

Replace fragmented legacy tests with systematic tier-based E2E testing that validates:
- Semantic layer (definitions, roles, relationships)
- Kinetic layer (workflows, data flows, inefficiencies)
- Dynamic layer (learning, adaptation, optimization)
- Cross-tier integration (feedback loops)
- Complete system (all components working together)

---

## Plan

### Phase 1: Cleanup (5 minutes)

**Delete 20 legacy test files**:
```bash
rm tests/test_*.py
rm tests/__pycache__/*
```

**Keep**:
- `tests/` directory structure
- `tests/__init__.py` if exists

---

### Phase 2: Tier 1 - Semantic Layer E2E (30 minutes)

**File**: `tests/test_1_semantic_tier_e2e.py`

**Purpose**: Validate Palantir semantic tier implementation

**Tests**:

1. **test_all_agents_have_semantic_roles**
   - Load all 13 agents
   - Verify each has semantic_role attribute
   - Check roles are valid SemanticRole enums
   - Validate: orchestrator, clarifier, specialist, validator, analyzer

2. **test_semantic_responsibilities_defined**
   - Verify semantic_responsibility for each agent
   - Check non-overlapping responsibilities
   - Validate against SemanticResponsibility enum

3. **test_semantic_relationships_consistent**
   - Load semantic_schema.json
   - Verify all relationships are bidirectional
   - Example: If A delegates_to B, B should be in registry

4. **test_semantic_schema_export**
   - Call to_semantic_schema() on all agents
   - Verify JSON structure
   - Check completeness (role, responsibility, relationships, capabilities)

5. **test_semantic_migration_status**
   - Count migrated agents (should be 5: meta, socratic, test, security, performance)
   - Verify SemanticAgentDefinition vs AgentDefinition
   - Check SEMANTIC_LAYER_AVAILABLE flag

**Success Criteria**: 5/5 tests pass

---

### Phase 3: Tier 2 - Kinetic Layer E2E (45 minutes)

**File**: `tests/test_2_kinetic_tier_e2e.py`

**Purpose**: Validate runtime behaviors, workflows, data flows

**Tests**:

1. **test_sequential_workflow**
   ```python
   # Simulate: research → build → validate
   # Verify: Each step completes
   # Verify: Data flows correctly
   ```

2. **test_concurrent_workflow**
   ```python
   # Simulate: Parallel 3 concept processing
   # Verify: All 3 complete
   # Verify: 90% latency reduction vs sequential
   ```

3. **test_direct_data_passing**
   ```python
   # Verify: No file I/O for inter-agent communication
   # Verify: Result passed directly in prompt
   # Measure: I/O operations should be 0
   ```

4. **test_inefficiency_detection_type1_communication**
   ```python
   # Trigger: File-based communication pattern
   # Verify: Inefficiency detected
   # Verify: Warning issued
   ```

5. **test_inefficiency_detection_type2_redundant**
   ```python
   # Trigger: Duplicate research attempt
   # Verify: Redundancy detected
   # Verify: Existing data reused
   ```

6. **test_inefficiency_detection_type3_context_loss**
   ```python
   # Trigger: Missing information in delegation
   # Verify: Context loss detected
   # Verify: Complete context enforced
   ```

7. **test_inefficiency_detection_type4_tool_misalignment**
   ```python
   # Verify: Agents have appropriate tools only
   # Verify: Least privilege enforced
   # Example: quality-agent has no Write
   ```

8. **test_hook_execution_flow**
   ```python
   # Verify: PreToolUse → Execute → PostToolUse
   # Verify: Hooks don't block workflow
   # Measure: Hook overhead < 5%
   ```

**Success Criteria**: 8/8 tests pass

---

### Phase 4: Tier 3 - Dynamic Layer E2E (45 minutes)

**File**: `tests/test_3_dynamic_tier_e2e.py`

**Purpose**: Validate learning, adaptation, optimization

**Tests**:

1. **test_meta_cognitive_tracing**
   ```python
   # Execute workflow with tracer
   # Verify: Decisions logged
   # Verify: Learnings captured
   # Verify: Impacts recorded
   ```

2. **test_user_feedback_collection**
   ```python
   # Simulate user feedback: "정확도: 9, 효율성: 8"
   # Verify: Parsed correctly
   # Verify: Quality score calculated
   ```

3. **test_background_log_optimization**
   ```python
   # Queue log with effectiveness 9.5
   # Verify: Immediate optimization triggered
   # Verify: Template generated
   ```

4. **test_dynamic_weight_adjustment**
   ```python
   # Test error_rate = 0.25 (high)
   # Verify: Quality weight = 0.6
   # Test error_rate = 0.03 (low)
   # Verify: Efficiency weight = 0.4
   ```

5. **test_pattern_learning_and_reuse**
   ```python
   # Session 1: Execute workflow, save pattern
   # Session 2: Query memory for pattern
   # Verify: Pattern retrieved and applied
   # Measure: Efficiency improvement
   ```

6. **test_socratic_optimization_loop**
   ```python
   # Session 1: 21 questions → 98% precision
   # Save effectiveness data
   # Session 2: Should use optimized strategy
   # Target: 15 questions → 98% precision
   ```

7. **test_self_improvement_trigger**
   ```python
   # Simulate success_rate < 70%
   # Verify: Stop hook blocks
   # Verify: Improvement cycle triggered
   # Verify: Session continues after improvement
   ```

**Success Criteria**: 7/7 tests pass

---

### Phase 5: Tier 4 - Cross-Tier Integration (30 minutes)

**File**: `tests/test_4_cross_tier_integration_e2e.py`

**Purpose**: Validate tier interactions and feedback loops

**Tests**:

1. **test_semantic_to_kinetic_flow**
   ```python
   # Semantic: AgentDefinition with role="orchestrator"
   # Kinetic: Delegates tasks based on role
   # Verify: Semantic properties enable kinetic behaviors
   ```

2. **test_kinetic_to_dynamic_flow**
   ```python
   # Kinetic: Execute task, collect metrics
   # Dynamic: Learn from execution
   # Verify: Execution data → Learning data
   ```

3. **test_dynamic_to_semantic_flow**
   ```python
   # Dynamic: Learn "documentation-first pattern"
   # Semantic: Update meta_orchestrator prompt
   # Verify: Learning refines definition
   ```

4. **test_complete_feedback_loop**
   ```python
   # Execute: Semantic def → Kinetic execution → Dynamic learning
   # Verify: Learning saves to memory-keeper
   # Next session: Learning applied to semantic
   # Measure: Improvement (error rate, efficiency)
   ```

5. **test_cross_agent_learning**
   ```python
   # Meta-orchestrator learns pattern
   # Pattern saved to memory-keeper
   # Socratic-agent queries memory
   # Verify: Pattern shared across agents
   ```

**Success Criteria**: 5/5 tests pass

---

### Phase 6: Tier 5 - Complete System E2E (60 minutes)

**File**: `tests/test_5_complete_system_e2e.py`

**Purpose**: Full integration test covering entire project

**Tests**:

1. **test_agent_registry_complete**
   ```python
   # Verify: All 13 agents discoverable
   # Verify: Correct roles assigned
   # Verify: No missing agents
   ```

2. **test_hook_system_integration**
   ```python
   # Execute workflow with hooks
   # Verify: PreToolUse validates
   # Verify: PostToolUse learns
   # Verify: Stop triggers improvement
   # Verify: UserPromptSubmit detects ambiguity
   ```

3. **test_end_to_end_user_workflow**
   ```python
   # Simulate: User request → Meta-orchestrator → Subagents → Response
   # Steps:
   #   1. User: "피타고라스 정리 분석"
   #   2. Meta: Delegates to research-agent
   #   3. Research: Gathers information
   #   4. Meta: Delegates to knowledge-builder
   #   5. Builder: Creates file
   #   6. Meta: Delegates to quality-agent
   #   7. Quality: Validates
   #   8. Meta: Reports to user
   # Verify: Each step completes
   # Verify: Final output exists and is valid
   ```

4. **test_semantic_layer_full_coverage**
   ```python
   # Load semantic_schema.json
   # Verify: All 13 agents mapped
   # Verify: All 4 hooks defined
   # Verify: All 5 patterns documented
   # Verify: Tier interactions defined
   ```

5. **test_palantir_ontology_validation**
   ```python
   # Verify: H1 (Semantic) mapping correct
   # Verify: H2 (Kinetic) mapping correct
   # Verify: H3 (Dynamic) mapping correct
   # Load docs/palantir-ontology-research.md
   # Validate against implementation
   ```

6. **test_meta_cognitive_system_integration**
   ```python
   # Execute task with tracer
   # Collect user feedback
   # Trigger background optimization
   # Query optimized templates
   # Verify: Complete cycle works
   ```

7. **test_community_agents_integration**
   ```python
   # Verify: 3 new agents importable
   # Verify: Proactive keywords present
   # Verify: Tools correctly restricted
   # Test: test_automation_specialist
   # Test: security_auditor
   # Test: performance_engineer
   ```

8. **test_streaming_with_semantic_layer**
   ```python
   # Start ClaudeSDKClient
   # Execute query with semantic agents
   # Verify: Streaming works
   # Verify: Extended thinking displays
   # Verify: Tool usage tracked
   ```

9. **test_main_py_integration**
   ```python
   # Import main.py
   # Verify: Hook integration active
   # Verify: Semantic layer loaded
   # Verify: All agents registered
   # Verify: Version 2.2.0
   ```

10. **test_documentation_completeness**
   ```python
   # Verify: CLAUDE.md exists
   # Verify: Palantir research exists
   # Verify: All learning logs present
   # Verify: Community references included
   ```

**Success Criteria**: 10/10 tests pass

---

## Test Execution Order

```
1. test_1_semantic_tier_e2e.py      (5 tests)
2. test_2_kinetic_tier_e2e.py       (8 tests)
3. test_3_dynamic_tier_e2e.py       (7 tests)
4. test_4_cross_tier_integration_e2e.py  (5 tests)
5. test_5_complete_system_e2e.py    (10 tests)

Total: 35 comprehensive tests
Target: 100% pass rate
```

---

## Success Metrics

**Coverage**:
- ✅ Semantic tier: 100% (all definitions)
- ✅ Kinetic tier: 100% (all workflows)
- ✅ Dynamic tier: 100% (all learning)
- ✅ Cross-tier: 100% (all interactions)
- ✅ System: 100% (all components)

**Quality**:
- All tests independent
- All tests repeatable
- All tests validate real functionality
- No mock-heavy tests (real integration)

---

## Implementation Todos

### Cleanup
- [ ] Delete 20 legacy test files
- [ ] Clear __pycache__
- [ ] Keep tests/ directory

### Tier 1: Semantic
- [ ] Create test_1_semantic_tier_e2e.py
- [ ] Write 5 semantic validation tests
- [ ] Run and verify 5/5 pass

### Tier 2: Kinetic
- [ ] Create test_2_kinetic_tier_e2e.py
- [ ] Write 8 workflow tests
- [ ] Run and verify 8/8 pass

### Tier 3: Dynamic
- [ ] Create test_3_dynamic_tier_e2e.py
- [ ] Write 7 learning tests
- [ ] Run and verify 7/7 pass

### Tier 4: Cross-Tier
- [ ] Create test_4_cross_tier_integration_e2e.py
- [ ] Write 5 integration tests
- [ ] Run and verify 5/5 pass

### Tier 5: Complete System
- [ ] Create test_5_complete_system_e2e.py
- [ ] Write 10 system tests
- [ ] Run and verify 10/10 pass

### Validation
- [ ] All 35 tests pass
- [ ] 100% coverage of meta_orchestrator workflows
- [ ] All Palantir tiers validated
- [ ] Complete system integration verified

---

**Status**: Plan complete, ready for execution  
**Estimated Time**: 3-4 hours total  
**Success Target**: 35/35 tests (100%)

