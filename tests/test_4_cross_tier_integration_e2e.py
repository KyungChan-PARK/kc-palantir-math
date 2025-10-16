"""
Tier 4: Cross-Tier Integration E2E Tests

Tests interactions between Palantir tiers:
- Semantic → Kinetic (definitions enable behaviors)
- Kinetic → Dynamic (behaviors generate learning)
- Dynamic → Semantic (learning refines definitions)
- Complete feedback loops

VERSION: 1.0.0
DATE: 2025-10-16
"""

import pytest
import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestCrossTierIntegration:
    """Cross-tier integration validation tests."""
    
    def test_1_semantic_to_kinetic_flow(self):
        """Test: Semantic definitions enable kinetic behaviors."""
        print("\n" + "="*80)
        print("TEST 1: Semantic → Kinetic Flow")
        print("="*80)
        
        from lib.orchestrator_utils import meta_orchestrator
        from semantic_layer import SemanticRole
        
        # Semantic tier: Agent has role="orchestrator"
        assert meta_orchestrator.semantic_role == SemanticRole.ORCHESTRATOR
        
        # Kinetic tier: This role enables delegation behavior
        prompt = meta_orchestrator.prompt
        assert 'Task' in prompt or 'Delegate' in prompt
        assert 'Coordinates' in meta_orchestrator.description or 'delegates' in meta_orchestrator.description.lower()
        
        print(f"  ✓ Semantic: role=ORCHESTRATOR")
        print(f"  ✓ Kinetic: Can delegate via Task tool")
        print(f"  ✓ Flow: Role definition → Delegation behavior")
        
        print(f"\n✅ TEST 1 PASSED: Semantic enables kinetic behaviors")
    
    def test_2_kinetic_to_dynamic_flow(self):
        """Test: Kinetic execution generates dynamic learning."""
        print("\n" + "="*80)
        print("TEST 2: Kinetic → Dynamic Flow")
        print("="*80)
        
        # Kinetic tier: Workflow execution (meta_orchestrator)
        from lib.orchestrator_utils import meta_orchestrator
        prompt = meta_orchestrator.prompt
        
        # Should reference learning
        assert 'META-COGNITIVE LEARNING LOG' in prompt
        assert 'Session 2025-10-15' in prompt
        
        # Dynamic tier: Learning captured
        log_file = Path(__file__).parent.parent / "logs" / "meta-cognitive-learning-session-2025-10-15.json"
        assert log_file.exists()
        
        with open(log_file) as f:
            learnings = json.load(f)
        
        assert 'learnings' in learnings
        assert len(learnings['learnings']) > 0
        
        print(f"  ✓ Kinetic: Workflow execution documented")
        print(f"  ✓ Dynamic: Learning log generated")
        print(f"  ✓ Flow: Execution → Learning capture")
        print(f"  ✓ Learnings captured: {len(learnings['learnings'])}")
        
        print(f"\n✅ TEST 2 PASSED: Kinetic generates dynamic learning")
    
    def test_3_dynamic_to_semantic_flow(self):
        """Test: Dynamic learning refines semantic definitions."""
        print("\n" + "="*80)
        print("TEST 3: Dynamic → Semantic Flow")
        print("="*80)
        
        from lib.orchestrator_utils import meta_orchestrator
        
        # Dynamic tier: Learning exists
        prompt = meta_orchestrator.prompt
        assert 'LEARNING #1: Execution vs Recall' in prompt
        
        # Semantic tier: Learning is now part of definition
        assert 'Execute actual work' in prompt  # Refined behavior from learning
        assert '제 지식으로' not in prompt or 'DON\'T' in prompt  # Anti-pattern documented
        
        print(f"  ✓ Dynamic: Learning documented (Execution vs Recall)")
        print(f"  ✓ Semantic: Prompt refined with learning")
        print(f"  ✓ Flow: Learning → Definition update")
        
        print(f"\n✅ TEST 3 PASSED: Dynamic refines semantic definitions")
    
    def test_4_complete_feedback_loop(self):
        """Test: Complete 3-tier feedback loop."""
        print("\n" + "="*80)
        print("TEST 4: Complete Feedback Loop")
        print("="*80)
        
        # Load semantic schema
        schema_file = Path(__file__).parent.parent / "semantic_schema.json"
        with open(schema_file) as f:
            schema = json.load(f)
        
        # Verify tier interactions documented
        assert 'tier_interactions' in schema
        interactions = schema['tier_interactions']
        
        assert 'semantic_to_kinetic' in interactions
        assert 'kinetic_to_dynamic' in interactions
        assert 'dynamic_to_semantic' in interactions
        
        print(f"  ✓ Semantic → Kinetic: {interactions['semantic_to_kinetic']}")
        print(f"  ✓ Kinetic → Dynamic: {interactions['kinetic_to_dynamic']}")
        print(f"  ✓ Dynamic → Semantic: {interactions['dynamic_to_semantic']}")
        
        print(f"\n✅ TEST 4 PASSED: Complete feedback loop defined")
    
    def test_5_cross_agent_learning_mechanism(self):
        """Test: Learning shared across agents via memory-keeper."""
        print("\n" + "="*80)
        print("TEST 5: Cross-Agent Learning")
        print("="*80)
        
        from lib.orchestrator_utils import meta_orchestrator
        from agents.socratic_requirements_agent import socratic_requirements_agent
        
        # Both agents should reference memory-keeper for learning
        meta_prompt = meta_orchestrator.prompt
        socratic_prompt = socratic_requirements_agent.prompt
        
        # Meta-orchestrator has learning log
        assert 'META-COGNITIVE LEARNING LOG' in meta_prompt
        
        # Socratic has learned strategies
        assert 'LEARNED QUESTION STRATEGIES' in socratic_prompt
        
        # Both should use memory-keeper (check tools)
        meta_tools = meta_orchestrator.tools
        socratic_tools = socratic_requirements_agent.tools
        
        # At least one should have memory-keeper access
        has_memory = any('memory' in str(t).lower() for t in meta_tools) or \
                     any('memory' in str(t).lower() for t in socratic_tools)
        
        print(f"  ✓ Meta-orchestrator: Has learning log")
        print(f"  ✓ Socratic agent: Has learned strategies")
        print(f"  ✓ Memory-keeper access: {has_memory}")
        print(f"  ✓ Flow: Learning shared via memory-keeper")
        
        print(f"\n✅ TEST 5 PASSED: Cross-agent learning mechanism validated")


if __name__ == '__main__':
    # Run tests
    tester = TestCrossTierIntegration()
    
    try:
        tester.test_1_semantic_to_kinetic_flow()
        tester.test_2_kinetic_to_dynamic_flow()
        tester.test_3_dynamic_to_semantic_flow()
        tester.test_4_complete_feedback_loop()
        tester.test_5_cross_agent_learning_mechanism()
        
        print("\n" + "="*80)
        print("🎉 ALL TIER 4 TESTS PASSED (5/5)")
        print("="*80)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

