"""
Tier 1: Semantic Layer E2E Tests

Tests the Palantir semantic tier implementation:
- Agent roles and responsibilities
- Semantic relationships
- Schema export
- Migration status

VERSION: 1.0.0
DATE: 2025-10-16
"""

import pytest
import sys
from pathlib import Path
import json

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from semantic_layer import (
    SemanticAgentDefinition,
    SemanticRole,
    SemanticResponsibility,
    PalantirTierOrchestrator
)


class TestSemanticTier:
    """Semantic tier validation tests."""
    
    def test_1_all_agents_have_semantic_roles(self):
        """Test: All migrated agents have semantic roles."""
        print("\n" + "="*80)
        print("TEST 1: Semantic Roles Validation")
        print("="*80)
        
        # Import migrated agents
        from agents.meta_orchestrator import meta_orchestrator, SEMANTIC_LAYER_AVAILABLE
        from agents.socratic_requirements_agent import socratic_requirements_agent
        from agents.test_automation_specialist import test_automation_specialist
        from agents.security_auditor import security_auditor
        from agents.performance_engineer import performance_engineer
        
        assert SEMANTIC_LAYER_AVAILABLE, "Semantic layer not available"
        
        # Verify semantic roles
        agents_to_test = [
            ("meta_orchestrator", meta_orchestrator, SemanticRole.ORCHESTRATOR),
            ("socratic_agent", socratic_requirements_agent, SemanticRole.CLARIFIER),
            ("test_specialist", test_automation_specialist, SemanticRole.SPECIALIST),
            ("security_auditor", security_auditor, SemanticRole.VALIDATOR),
            ("performance_engineer", performance_engineer, SemanticRole.ANALYZER),
        ]
        
        for name, agent, expected_role in agents_to_test:
            assert hasattr(agent, 'semantic_role'), f"{name} missing semantic_role"
            assert agent.semantic_role == expected_role, f"{name} has wrong role"
            print(f"  ✓ {name}: {agent.semantic_role.value}")
        
        print(f"\n✅ TEST 1 PASSED: All 5 migrated agents have correct semantic roles")
    
    def test_2_semantic_responsibilities_defined(self):
        """Test: All agents have semantic responsibilities."""
        print("\n" + "="*80)
        print("TEST 2: Semantic Responsibilities")
        print("="*80)
        
        from agents.meta_orchestrator import meta_orchestrator
        from agents.socratic_requirements_agent import socratic_requirements_agent
        
        # Verify responsibilities
        assert hasattr(meta_orchestrator, 'semantic_responsibility')
        assert meta_orchestrator.semantic_responsibility == SemanticResponsibility.TASK_DELEGATION
        print(f"  ✓ meta_orchestrator: {meta_orchestrator.semantic_responsibility.value}")
        
        assert hasattr(socratic_requirements_agent, 'semantic_responsibility')
        assert socratic_requirements_agent.semantic_responsibility == SemanticResponsibility.AMBIGUITY_RESOLUTION
        print(f"  ✓ socratic_agent: {socratic_requirements_agent.semantic_responsibility.value}")
        
        print(f"\n✅ TEST 2 PASSED: Semantic responsibilities correctly defined")
    
    def test_3_semantic_relationships_consistent(self):
        """Test: Semantic relationships are consistent."""
        print("\n" + "="*80)
        print("TEST 3: Semantic Relationships")
        print("="*80)
        
        # Load schema
        schema_file = Path(__file__).parent.parent / "semantic_schema.json"
        assert schema_file.exists(), "semantic_schema.json not found"
        
        with open(schema_file) as f:
            schema = json.load(f)
        
        # Verify structure
        assert 'agents' in schema
        assert 'hooks' in schema
        assert 'patterns' in schema
        
        # Check relationships
        agents = schema['agents']
        meta = agents.get('meta-orchestrator', {})
        
        assert 'semantic_relationships' in meta
        relationships = meta['semantic_relationships']
        
        assert 'delegates_to' in relationships
        assert relationships['delegates_to'] == ["*"]  # Can delegate to any
        
        print(f"  ✓ Schema structure valid")
        print(f"  ✓ Relationships defined: {list(relationships.keys())}")
        print(f"\n✅ TEST 3 PASSED: Semantic relationships are consistent")
    
    def test_4_semantic_schema_export(self):
        """Test: Agents can export semantic schema."""
        print("\n" + "="*80)
        print("TEST 4: Schema Export Functionality")
        print("="*80)
        
        from agents.meta_orchestrator import meta_orchestrator
        
        # Export schema
        schema = meta_orchestrator.to_semantic_schema()
        
        # Verify structure
        assert isinstance(schema, dict)
        assert 'role' in schema
        assert 'responsibility' in schema
        assert 'relationships' in schema
        assert 'capabilities' in schema
        
        # Verify content
        assert schema['role'] == 'orchestrator'
        assert schema['responsibility'] == 'task_delegation_coordination'
        
        print(f"  ✓ Schema export successful")
        print(f"  ✓ Role: {schema['role']}")
        print(f"  ✓ Responsibility: {schema['responsibility']}")
        print(f"  ✓ Keys: {list(schema.keys())}")
        
        print(f"\n✅ TEST 4 PASSED: Schema export works correctly")
    
    def test_5_semantic_migration_status(self):
        """Test: Track migration progress."""
        print("\n" + "="*80)
        print("TEST 5: Migration Status")
        print("="*80)
        
        from semantic_layer import SemanticAgentDefinition
        from claude_agent_sdk import AgentDefinition
        
        # Count migrated agents
        migrated_agents = []
        non_migrated_agents = []
        
        agent_files = [
            'meta_orchestrator',
            'socratic_requirements_agent',
            'test_automation_specialist',
            'security_auditor',
            'performance_engineer',
            'knowledge_builder',
            'research_agent',
            'quality_agent'
        ]
        
        for agent_name in agent_files:
            try:
                module = __import__(f'agents.{agent_name}', fromlist=[agent_name])
                agent = getattr(module, agent_name)
                
                if isinstance(agent, SemanticAgentDefinition):
                    migrated_agents.append(agent_name)
                else:
                    non_migrated_agents.append(agent_name)
            except:
                pass
        
        print(f"  ✓ Migrated to SemanticAgentDefinition: {len(migrated_agents)}")
        for name in migrated_agents:
            print(f"    - {name}")
        
        print(f"  ✓ Still using AgentDefinition: {len(non_migrated_agents)}")
        for name in non_migrated_agents:
            print(f"    - {name}")
        
        # Should have at least 5 migrated
        assert len(migrated_agents) >= 5, f"Expected >=5 migrated, got {len(migrated_agents)}"
        
        print(f"\n✅ TEST 5 PASSED: Migration tracking working ({len(migrated_agents)} migrated)")


if __name__ == '__main__':
    # Run tests
    tester = TestSemanticTier()
    
    try:
        tester.test_1_all_agents_have_semantic_roles()
        tester.test_2_semantic_responsibilities_defined()
        tester.test_3_semantic_relationships_consistent()
        tester.test_4_semantic_schema_export()
        tester.test_5_semantic_migration_status()
        
        print("\n" + "="*80)
        print("🎉 ALL TIER 1 TESTS PASSED (5/5)")
        print("="*80)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

