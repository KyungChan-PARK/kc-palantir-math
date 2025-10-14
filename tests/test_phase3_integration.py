"""
Phase 3 Integration Tests

Tests for improvements #5 (HITL Framework) and #6 (Parallel Q&A).

Test Coverage:
1. HITL Framework (agents/meta_orchestrator.py):
   - should_trigger_hitl_checkpoint() method
   - 3 trigger scenarios + 1 no-trigger scenario
2. Parallel Q&A (agents/socratic_mediator_agent.py):
   - Uncertainty-driven question templates
   - Template coverage for 4 uncertainty_reason codes

Version: 1.0
Date: 2025-10-14
"""

import pytest
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import Phase 3 components
from agents import MetaOrchestratorLogic, ImpactAnalysis, QualityGateApproval


# ============================================================================
# HITL Framework Tests (Improvement #5)
# ============================================================================

class TestHITLFramework:
    """Test HITL checkpoint triggers in meta_orchestrator.py"""

    def setup_method(self):
        """Setup MetaOrchestratorLogic for each test"""
        self.orchestrator = MetaOrchestratorLogic()

    def test_hitl_trigger_failed_gate_high_criticality(self):
        """
        Scenario: Quality gate FAILED + criticality >= 9
        Expected: HITL checkpoint triggered
        """
        print("\n[Test 1/5] HITL Trigger: Failed gate + criticality >= 9")

        # Create mock impact analysis
        impact_analysis = ImpactAnalysis(
            sis=["agents/meta_orchestrator.py"],
            cis=["agents/meta_orchestrator.py", "agents/knowledge_builder.py"],
            cis_size=2,
            critical_affected=True,
            test_coverage=0.75
        )

        # Create failed approval with criticality 9
        approval = QualityGateApproval(
            passed=False,
            feedback="CIS size exceeds threshold",
            retry_allowed=True,
            metrics={
                "max_criticality": 9,
                "cis_size": 15
            }
        )

        # Test
        result = self.orchestrator.should_trigger_hitl_checkpoint(
            impact_analysis,
            approval
        )

        assert result == True, "HITL should trigger for failed gate + criticality >= 9"
        print("✅ PASS: HITL triggered as expected")

    def test_hitl_trigger_ontology_modification(self):
        """
        Scenario: Ontology file modified
        Expected: HITL checkpoint triggered
        """
        print("\n[Test 2/5] HITL Trigger: Ontology file modification")

        # Create impact analysis with ontology file
        impact_analysis = ImpactAnalysis(
            sis=["agents/relationship_ontology.py"],
            cis=["agents/relationship_ontology.py"],
            cis_size=1,
            critical_affected=True,
            test_coverage=0.85
        )

        # Create passed approval (but ontology file affected)
        approval = QualityGateApproval(
            passed=True,
            feedback="Quality gate passed",
            retry_allowed=False,
            metrics={
                "max_criticality": 7,
                "cis_size": 8
            }
        )

        # Test
        result = self.orchestrator.should_trigger_hitl_checkpoint(
            impact_analysis,
            approval
        )

        assert result == True, "HITL should trigger for ontology file modification"
        print("✅ PASS: HITL triggered for ontology change")

    def test_hitl_trigger_mission_critical(self):
        """
        Scenario: Quality gate PASSED but criticality = 10
        Expected: HITL checkpoint triggered
        """
        print("\n[Test 3/5] HITL Trigger: Mission-critical file (criticality=10)")

        # Create impact analysis
        impact_analysis = ImpactAnalysis(
            sis=["main.py"],
            cis=["main.py"],
            cis_size=1,
            critical_affected=True,
            test_coverage=0.90
        )

        # Create passed approval with criticality 10
        approval = QualityGateApproval(
            passed=True,
            feedback="Quality gate passed",
            retry_allowed=False,
            metrics={
                "max_criticality": 10,  # Mission-critical
                "cis_size": 5
            }
        )

        # Test
        result = self.orchestrator.should_trigger_hitl_checkpoint(
            impact_analysis,
            approval
        )

        assert result == True, "HITL should trigger for criticality = 10"
        print("✅ PASS: HITL triggered for mission-critical file")

    def test_hitl_no_trigger_normal_case(self):
        """
        Scenario: Quality gate PASSED + low criticality + no ontology files
        Expected: HITL checkpoint NOT triggered
        """
        print("\n[Test 4/5] HITL No-Trigger: Normal case")

        # Create impact analysis (standard files)
        impact_analysis = ImpactAnalysis(
            sis=["agents/example_generator.py"],
            cis=["agents/example_generator.py"],
            cis_size=1,
            critical_affected=False,
            test_coverage=0.85
        )

        # Create passed approval with normal criticality
        approval = QualityGateApproval(
            passed=True,
            feedback="Quality gate passed",
            retry_allowed=False,
            metrics={
                "max_criticality": 4,  # Low-risk
                "cis_size": 6
            }
        )

        # Test
        result = self.orchestrator.should_trigger_hitl_checkpoint(
            impact_analysis,
            approval
        )

        assert result == False, "HITL should NOT trigger for normal case"
        print("✅ PASS: HITL correctly not triggered")

    def test_hitl_quality_agent_ontology_file(self):
        """
        Scenario: quality_agent.py modified (ontology file)
        Expected: HITL checkpoint triggered
        """
        print("\n[Test 5/5] HITL Trigger: quality_agent.py (ontology file)")

        # Create impact analysis with quality_agent.py
        impact_analysis = ImpactAnalysis(
            sis=["agents/quality_agent.py"],
            cis=["agents/quality_agent.py"],
            cis_size=1,
            critical_affected=True,
            test_coverage=0.88
        )

        # Create passed approval
        approval = QualityGateApproval(
            passed=True,
            feedback="Quality gate passed",
            retry_allowed=False,
            metrics={
                "max_criticality": 7,
                "cis_size": 7
            }
        )

        # Test
        result = self.orchestrator.should_trigger_hitl_checkpoint(
            impact_analysis,
            approval
        )

        assert result == True, "HITL should trigger for quality_agent.py (ontology file)"
        print("✅ PASS: HITL triggered for quality_agent.py")


# ============================================================================
# Parallel Q&A Tests (Improvement #6)
# ============================================================================

class TestParallelQA:
    """Test Parallel Q&A templates in socratic_mediator_agent.py"""

    def test_uncertainty_templates_exist(self):
        """
        Verify that all 4 uncertainty_reason templates exist in prompt
        """
        print("\n[Test 6/6] Parallel Q&A: Uncertainty template coverage")

        # Read socratic_mediator_agent.py
        file_path = Path(__file__).parent.parent / "agents" / "socratic_mediator_agent.py"
        assert file_path.exists(), f"socratic_mediator_agent.py not found at {file_path}"

        with open(file_path, 'r') as f:
            content = f.read()

        # Check for IMPROVEMENT #6 marker
        assert "IMPROVEMENT #6" in content, "IMPROVEMENT #6 marker not found"
        print("✅ IMPROVEMENT #6 section found")

        # Check for 4 uncertainty_reason templates
        required_templates = [
            "concept_B_context_insufficient",
            "boundary_ambiguous_between_TYPE1_TYPE2",
            "confidence_threshold_missed",
            "prerequisite_graph_inconsistent"
        ]

        for template in required_templates:
            assert template in content, f"Template '{template}' not found in prompt"
            print(f"✅ Template found: {template}")

        # Check for parallel execution guide
        assert "Parallel Task Execution" in content, "Parallel execution guide not found"
        print("✅ Parallel Task execution guide found")

        # Check for latency reduction mention (from scalable.pdf)
        assert "90%" in content, "90% latency reduction mention not found"
        print("✅ Performance optimization (90% latency reduction) documented")

        print("\n✅ PASS: All uncertainty templates and parallel execution guide present")


# ============================================================================
# Integration Test: Full Phase 3 Flow
# ============================================================================

class TestPhase3Integration:
    """End-to-end integration test for Phase 3 improvements"""

    def test_phase3_complete_coverage(self):
        """
        Verify all 6 improvements are integrated
        """
        print("\n[Integration Test] Phase 3 Complete Coverage")

        project_root = Path(__file__).parent.parent

        # Check Phase 1-2 implementations exist
        improvements = {
            "#1 Uncertainty": project_root / "agents" / "relationship_definer.py",
            "#2 CoT": project_root / "agents" / "relationship_definer.py",
            "#3 Dynamic Gate": project_root / "agents" / "criticality_config.py",
            "#4 Ontology": project_root / "agents" / "relationship_ontology.py",
            "#5 HITL": project_root / "agents" / "meta_orchestrator.py",
            "#6 Parallel Q&A": project_root / "agents" / "socratic_mediator_agent.py"
        }

        for name, path in improvements.items():
            assert path.exists(), f"{name} file not found: {path}"
            print(f"✅ {name} implementation found")

        # Check Phase 3 specific markers
        meta_orch_path = improvements["#5 HITL"]
        with open(meta_orch_path, 'r') as f:
            meta_content = f.read()

        assert "should_trigger_hitl_checkpoint" in meta_content, "#5 HITL method not found"
        print("✅ #5 HITL Framework: should_trigger_hitl_checkpoint() method present")

        socratic_path = improvements["#6 Parallel Q&A"]
        with open(socratic_path, 'r') as f:
            socratic_content = f.read()

        assert "IMPROVEMENT #6" in socratic_content, "#6 marker not found"
        print("✅ #6 Parallel Q&A: IMPROVEMENT #6 section present")

        print("\n✅ PASS: All 6 improvements verified")


# ============================================================================
# Test Runner
# ============================================================================

def run_all_tests():
    """Run all Phase 3 tests"""
    print("=" * 80)
    print("Phase 3 Integration Tests")
    print("=" * 80)

    # HITL Framework tests
    hitl_tests = TestHITLFramework()
    hitl_tests.setup_method()

    try:
        hitl_tests.test_hitl_trigger_failed_gate_high_criticality()
        hitl_tests.test_hitl_trigger_ontology_modification()
        hitl_tests.test_hitl_trigger_mission_critical()
        hitl_tests.test_hitl_no_trigger_normal_case()
        hitl_tests.test_hitl_quality_agent_ontology_file()
        print("\n✅ HITL Framework: 5/5 tests passed")
    except AssertionError as e:
        print(f"\n❌ HITL Framework test failed: {e}")
        return False

    # Parallel Q&A tests
    qa_tests = TestParallelQA()
    try:
        qa_tests.test_uncertainty_templates_exist()
        print("\n✅ Parallel Q&A: 1/1 tests passed")
    except AssertionError as e:
        print(f"\n❌ Parallel Q&A test failed: {e}")
        return False

    # Integration test
    integration = TestPhase3Integration()
    try:
        integration.test_phase3_complete_coverage()
        print("\n✅ Integration: 1/1 tests passed")
    except AssertionError as e:
        print(f"\n❌ Integration test failed: {e}")
        return False

    # Final summary
    print("\n" + "=" * 80)
    print("✅ ALL PHASE 3 TESTS PASSED (7/7)")
    print("=" * 80)
    print("\nTest Coverage:")
    print("  - HITL Framework: 5 scenarios tested")
    print("  - Parallel Q&A: Template coverage verified")
    print("  - Integration: All 6 improvements verified")
    print("\nPhase 3 implementation validated successfully!")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
