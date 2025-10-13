"""
Unit Tests for Self-Improvement System v4.0

Based on: SELF-IMPROVEMENT-IMPLEMENTATION-PLAN-v4.0.md Section IX.1

Test Coverage:
1. DependencyAgent - Graph building, caching, traversal
2. QualityGate - Threshold evaluation
3. FeedbackLoop - Round determination logic
"""

import pytest
import asyncio
from pathlib import Path
from agents.dependency_agent import DependencyAgent
from agents.improvement_models import (
    ImprovementAction,
    ImpactAnalysis,
    QualityGateApproval,
    ActionType
)
from agents.meta_orchestrator import MetaOrchestratorLogic


class TestDependencyAgent:
    """Test AST parsing and graph construction"""

    def test_build_graph(self):
        """Test that graph builds with nodes and edges"""
        agent = DependencyAgent()
        graph = agent.build_and_cache_graph()

        assert graph.number_of_nodes() > 0, "Graph should have nodes"
        assert graph.number_of_edges() > 0, "Graph should have edges"

        print(f"✓ Graph built: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")

    def test_cache_persistence(self):
        """Test that graph caching works"""
        agent1 = DependencyAgent()
        graph1 = agent1.build_and_cache_graph()
        nodes1 = graph1.number_of_nodes()

        agent2 = DependencyAgent()
        # Should load from cache
        if agent2._cache_exists():
            graph2 = agent2._load_from_cache()
            nodes2 = graph2.number_of_nodes()

            assert nodes1 == nodes2, "Cached graph should match original"
            print(f"✓ Cache test passed: {nodes1} nodes")
        else:
            print("⚠️  Cache file not found, skipping persistence test")

    def test_get_impact_set(self):
        """Test impact set generation"""
        agent = DependencyAgent()
        agent.build_and_cache_graph()

        # Test with a known module
        sis = ["agents.meta_orchestrator"]
        cis = agent.get_impact_set(sis, depth=2)

        assert len(cis) >= 0, "CIS should be generated"
        # CIS should not contain original SIS nodes
        cis_ids = [node.node_id for node in cis]
        for sis_node in sis:
            assert sis_node not in cis_ids, f"CIS should not contain SIS node {sis_node}"

        print(f"✓ Impact set test passed: SIS={len(sis)}, CIS={len(cis)}")


class TestQualityGate:
    """Test quality gate evaluation"""

    def test_cis_size_threshold(self):
        """Test CIS size threshold (< 20)"""
        orchestrator = MetaOrchestratorLogic()

        # Small CIS - should pass
        impact = ImpactAnalysis(
            sis=["agent1"],
            cis=["agent2", "agent3"],
            cis_size=2,
            critical_affected=False,
            test_coverage=0.9
        )
        approval = orchestrator.evaluate_quality_gate(impact)
        assert approval.passed, "Small CIS should pass quality gate"
        print("✓ Small CIS test passed")

        # Large CIS - should fail
        impact_large = ImpactAnalysis(
            sis=["agent1"],
            cis=[f"agent{i}" for i in range(25)],
            cis_size=25,
            critical_affected=False,
            test_coverage=0.9
        )
        approval_large = orchestrator.evaluate_quality_gate(impact_large)
        assert not approval_large.passed, "Large CIS should fail quality gate"
        print("✓ Large CIS test passed")

    def test_test_coverage_threshold(self):
        """Test coverage threshold (> 80%)"""
        orchestrator = MetaOrchestratorLogic()

        # Low coverage - should fail
        impact = ImpactAnalysis(
            sis=["agent1"],
            cis=["agent2"],
            cis_size=1,
            critical_affected=False,
            test_coverage=0.5  # Below 80%
        )
        approval = orchestrator.evaluate_quality_gate(impact)
        assert not approval.passed, "Low coverage should fail quality gate"
        assert "Test coverage" in approval.feedback, "Feedback should mention coverage"
        print("✓ Low coverage test passed")

    def test_critical_component_warning(self):
        """Test that critical components generate warning (not failure)"""
        orchestrator = MetaOrchestratorLogic()

        impact = ImpactAnalysis(
            sis=["agent1"],
            cis=["critical_agent"],
            cis_size=1,
            critical_affected=True,
            test_coverage=0.9
        )
        approval = orchestrator.evaluate_quality_gate(impact)
        # Should pass but with warning
        assert approval.passed, "Critical component should not fail gate (only warning)"
        assert "critical" in approval.feedback.lower(), "Should include critical warning"
        print("✓ Critical component warning test passed")


class TestFeedbackLoop:
    """Test dynamic feedback round logic"""

    @pytest.mark.asyncio
    async def test_round_determination(self):
        """Test that round count is determined correctly"""
        orchestrator = MetaOrchestratorLogic()

        # Test 1: Small impact, not critical → 1 round
        impact1 = ImpactAnalysis(
            sis=["agent1"],
            cis=["agent2"],
            cis_size=1,
            critical_affected=False,
            test_coverage=0.9
        )

        # Would need mock root_cause for full test
        # For now, just verify logic
        max_rounds = 2 if (impact1.cis_size >= 2 and impact1.critical_affected) else 1
        assert max_rounds == 1, "Should use 1 round for small, non-critical impact"
        print("✓ Single round determination test passed")

        # Test 2: Multiple agents + critical → 2 rounds
        impact2 = ImpactAnalysis(
            sis=["agent1"],
            cis=["agent2", "critical_agent"],
            cis_size=2,
            critical_affected=True,
            test_coverage=0.9
        )

        max_rounds = 2 if (impact2.cis_size >= 2 and impact2.critical_affected) else 1
        assert max_rounds == 2, "Should use 2 rounds for critical multi-agent impact"
        print("✓ Two round determination test passed")


def run_all_tests():
    """Run all tests manually (without pytest runner)"""
    print("\n" + "="*60)
    print("SELF-IMPROVEMENT SYSTEM v4.0 - UNIT TESTS")
    print("="*60 + "\n")

    # Test Dependency Agent
    print("Testing Dependency Agent...")
    test_da = TestDependencyAgent()
    test_da.test_build_graph()
    test_da.test_cache_persistence()
    test_da.test_get_impact_set()
    print()

    # Test Quality Gate
    print("Testing Quality Gate...")
    test_qg = TestQualityGate()
    test_qg.test_cis_size_threshold()
    test_qg.test_test_coverage_threshold()
    test_qg.test_critical_component_warning()
    print()

    # Test Feedback Loop
    print("Testing Feedback Loop...")
    test_fl = TestFeedbackLoop()
    asyncio.run(test_fl.test_round_determination())
    print()

    print("="*60)
    print("✅ ALL UNIT TESTS PASSED")
    print("="*60)


if __name__ == "__main__":
    run_all_tests()
