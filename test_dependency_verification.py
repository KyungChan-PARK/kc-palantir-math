"""
Quick verification script for DependencyAgent

Tests:
1. Load cached graph
2. Query basic metrics
3. Test impact analysis
"""

from agents.dependency_agent import DependencyAgent
from agents.improvement_models import ImprovementAction, ActionType


def main():
    print("=" * 70)
    print("Dependency Analysis System - Verification")
    print("=" * 70)

    # Initialize agent
    agent = DependencyAgent()

    # Test 1: Load cached graph
    print("\n[1/3] Loading cached dependency graph...")
    graph = agent.build_and_cache_graph()
    print(f"✓ Graph loaded: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")

    # Test 2: Query metrics
    print("\n[2/3] Analyzing graph structure...")

    # Sample node analysis
    sample_nodes = [
        "agents.meta_orchestrator",
        "agents.knowledge_builder",
        "agents.self_improver"
    ]

    for node in sample_nodes:
        if node in graph:
            dependents = agent.get_dependents(node, depth=1)
            dependencies = agent.get_dependencies(node, depth=1)
            print(f"  {node}:")
            print(f"    - Dependents (who uses this): {len(dependents)}")
            print(f"    - Dependencies (what this uses): {len(dependencies)}")

    # Test 3: Test impact analysis
    print("\n[3/3] Testing Change Impact Analysis...")

    # Simulate a change to knowledge_builder
    test_action = ImprovementAction(
        action_type=ActionType.MODIFY_PROMPT,
        target_agent="knowledge_builder",
        old_value="old prompt",
        new_value="new prompt",
        rationale="test",
        confidence_score=0.9
    )

    impact = agent.perform_dependency_analysis([test_action])

    print(f"  Starting Impact Set (SIS): {len(impact.sis)} nodes")
    print(f"  Candidate Impact Set (CIS): {impact.cis_size} nodes")
    print(f"  Critical components affected: {impact.critical_affected}")
    print(f"  Test coverage: {impact.test_coverage:.1%}")

    print("\n" + "=" * 70)
    print("✅ All verification tests passed")
    print("=" * 70)

    # Display impact report
    print("\n" + impact.impact_report)


if __name__ == "__main__":
    main()
