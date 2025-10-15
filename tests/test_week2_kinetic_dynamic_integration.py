"""
Week 2 Cumulative Test: Kinetic + Dynamic Integration

Validates that Kinetic and Dynamic tiers work together.

VERSION: 1.0.0
DATE: 2025-10-16
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from kinetic_layer import KineticTier
from dynamic_layer_orchestrator import DynamicTier, ModelSelectionFactors


def test_kinetic_dynamic_integration():
    """Test: Kinetic execution feeds into Dynamic learning."""
    print("\n" + "="*80)
    print("WEEK 2 CUMULATIVE TEST: Kinetic + Dynamic Integration")
    print("="*80)
    
    # Setup
    kinetic = KineticTier()
    dynamic = DynamicTier()
    
    # Simulate kinetic execution
    import asyncio
    result = asyncio.run(kinetic.execute_task(
        task="Research and build concept",
        agents=["research-agent", "knowledge-builder"],
        context={}
    ))
    
    print(f"\n✓ Kinetic execution completed:")
    print(f"  Duration: {result.duration_ms:.1f}ms")
    print(f"  Steps: {result.metrics['steps_executed']}")
    
    # Dynamic processes execution results
    insights = dynamic.process_execution_results({
        "metrics": {
            "duration_ms": result.duration_ms,
            "success_rate": 1.0 if result.success else 0.0
        },
        "learnings": []
    })
    
    print(f"\n✓ Dynamic learning processed:")
    print(f"  Patterns: {len(insights['patterns'])} categories")
    print(f"  Optimizations: {len(insights['optimizations']['optimizations'])}")
    
    # Model selection
    model = dynamic.select_model_for_task(
        task_description="Resolve ambiguous requirement",
        criticality=9,
        complexity=8
    )
    
    print(f"\n✓ Model selection working:")
    print(f"  Task: High criticality ambiguity")
    print(f"  Selected: {model}")
    assert "sonnet" in model.lower(), "Should select Sonnet for high criticality"
    
    print(f"\n✅ WEEK 2 CUMULATIVE TEST PASSED")
    print(f"   Kinetic + Dynamic integration validated")


if __name__ == '__main__':
    try:
        test_kinetic_dynamic_integration()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

