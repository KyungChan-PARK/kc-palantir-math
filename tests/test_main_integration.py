"""
Main Integration Test - Verify main.py loads feedback-learning-agent

Tests that main.py correctly imports and registers the new agent.

VERSION: 1.0.0
DATE: 2025-10-16
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_main_imports():
    """Test that main.py imports all 12 agents."""
    print("\n" + "="*70)
    print("TEST: main.py Imports")
    print("="*70)
    
    # Import main module
    import main
    
    # Verify all imports worked
    from subagents import (
        knowledge_builder,
        quality_agent,
        research_agent,
        socratic_requirements_agent,
        neo4j_query_agent,
        problem_decomposer_agent,
        problem_scaffolding_generator_agent,
        personalization_engine_agent,
        feedback_learning_agent,  # NEW
        self_improver_agent,
        meta_planning_analyzer,
        meta_query_helper,
    )
    
    agents = [
        knowledge_builder,
        quality_agent,
        research_agent,
        socratic_requirements_agent,
        neo4j_query_agent,
        problem_decomposer_agent,
        problem_scaffolding_generator_agent,
        personalization_engine_agent,
        feedback_learning_agent,  # NEW
        self_improver_agent,
        meta_planning_analyzer,
        meta_query_helper,
    ]
    
    print(f"✅ All {len(agents)} agents imported successfully")
    
    # Verify feedback_learning_agent is properly defined
    assert feedback_learning_agent is not None
    assert hasattr(feedback_learning_agent, 'description')
    assert hasattr(feedback_learning_agent, 'prompt')
    assert hasattr(feedback_learning_agent, 'model')
    assert hasattr(feedback_learning_agent, 'tools')
    
    print(f"✅ feedback-learning-agent is properly defined:")
    print(f"   Description: {feedback_learning_agent.description[:60]}...")
    print(f"   Model: {feedback_learning_agent.model}")
    print(f"   Tools: {len(feedback_learning_agent.tools)} tools")
    print(f"   Prompt length: {len(feedback_learning_agent.prompt)} chars")
    
    # Verify agent has required tools
    required_tools = ["read_file", "write", "Task"]
    has_tools = [tool in feedback_learning_agent.tools for tool in required_tools]
    
    print(f"✅ Required tools present:")
    for tool, present in zip(required_tools, has_tools):
        status = "✅" if present else "❌"
        print(f"   {status} {tool}")
    
    assert all(has_tools), "feedback-learning-agent should have required tools"
    
    print("\n✅ TEST PASSED: main.py integration verified")
    return True


def test_agent_count():
    """Test that system recognizes 12 agents."""
    print("\n" + "="*70)
    print("TEST: Agent Count")
    print("="*70)
    
    import subagents
    
    # Check __all__ exports
    agent_names = subagents.__all__
    
    print(f"Registered agents: {len(agent_names)}")
    for i, name in enumerate(agent_names, 1):
        print(f"  {i:2d}. {name}")
    
    assert len(agent_names) == 12, f"Expected 12 agents, got {len(agent_names)}"
    assert "feedback_learning_agent" in agent_names, "feedback_learning_agent should be registered"
    
    print("\n✅ TEST PASSED: 12 agents registered")
    return True


def test_subagents_init():
    """Test that subagents/__init__.py is correct."""
    print("\n" + "="*70)
    print("TEST: Subagents Module")
    print("="*70)
    
    init_file = project_root / "subagents" / "__init__.py"
    
    with open(init_file, 'r') as f:
        content = f.read()
    
    # Check for feedback_learning_agent import
    assert "from .feedback_learning_agent import feedback_learning_agent" in content, \
        "Should import feedback_learning_agent"
    
    # Check for comment update
    assert "Extended Functionality Subagents (4" in content or \
           "Extended Functionality (4" in content, \
        "Comment should reflect 4 extended functionality agents"
    
    # Check __all__ includes new agent
    assert '"feedback_learning_agent"' in content, \
        "__all__ should include feedback_learning_agent"
    
    print("✅ Import statement: Present")
    print("✅ __all__ export: Present")
    print("✅ Comment updated: Extended Functionality (4)")
    
    print("\n✅ TEST PASSED: subagents/__init__.py correct")
    return True


def run_all():
    """Run all main integration tests."""
    print("\n" + "="*70)
    print("MAIN INTEGRATION TEST SUITE")
    print("="*70)
    
    tests = [
        ("main.py Imports", test_main_imports),
        ("Agent Count", test_agent_count),
        ("Subagents Init", test_subagents_init),
    ]
    
    passed = 0
    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"\n❌ {test_name} FAILED: {e}")
        except Exception as e:
            print(f"\n❌ {test_name} ERROR: {e}")
    
    print(f"\n" + "="*70)
    print("SUMMARY")
    print(f"="*70)
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Success Rate: {passed/len(tests)*100:.1f}%")
    print("="*70)
    
    return passed == len(tests)


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)

