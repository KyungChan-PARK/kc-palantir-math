"""
Week 3 Cumulative Test: Complete 3-Tier Integration

Validates Semantic + Kinetic + Dynamic all working together.

VERSION: 1.0.0
DATE: 2025-10-16
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.orchestrator_utils import MetaOrchestratorLogic


def test_complete_3_tier_integration():
    """Test: All 3 tiers coordinated by meta-orchestrator."""
    print("\n" + "="*80)
    print("WEEK 3 CUMULATIVE TEST: Complete 3-Tier Integration")
    print("="*80)
    
    # Setup meta with tier coordination
    meta_logic = MetaOrchestratorLogic()
    
    # Test Tier 1: Semantic
    print(f"\n✓ Testing Tier 1 (Semantic):")
    semantic_result = meta_logic.orchestrate_semantic(
        operation="discover",
        capability="testing"
    )
    print(f"  Operation: {semantic_result['operation']}")
    print(f"  Status: {semantic_result['status']}")
    assert semantic_result['tier'] == 'semantic'
    
    # Test Tier 2: Kinetic
    print(f"\n✓ Testing Tier 2 (Kinetic):")
    kinetic_result = meta_logic.orchestrate_kinetic(
        task="Research concept",
        agents=["research-agent"],
        context={}
    )
    print(f"  Success: {kinetic_result['success']}")
    print(f"  Duration: {kinetic_result['duration_ms']:.1f}ms")
    print(f"  State: {kinetic_result['state']}")
    assert kinetic_result['success'] == True
    
    # Test Tier 3: Dynamic  
    print(f"\n✓ Testing Tier 3 (Dynamic):")
    dynamic_result = meta_logic.orchestrate_dynamic(
        learning_data={"metrics": kinetic_result['metrics']}
    )
    print(f"  Status: {dynamic_result['status']}")
    assert dynamic_result['tier'] == 'dynamic'
    
    # Verify all 3 methods exist
    print(f"\n✓ All tier orchestration methods:")
    print(f"  orchestrate_semantic: ✅")
    print(f"  orchestrate_kinetic: ✅")
    print(f"  orchestrate_dynamic: ✅")
    
    print(f"\n✅ WEEK 3 CUMULATIVE TEST PASSED")
    print(f"   All 3 tiers integrated and coordinated by meta-orchestrator")


if __name__ == '__main__':
    try:
        test_complete_3_tier_integration()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

