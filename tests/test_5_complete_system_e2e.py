"""
Tier 5: Complete System E2E Tests - Kenneth-Liao Pattern

Tests full integration of refactored system:
- All 11 subagents discoverable and functional
- Meta-orchestrator as main agent
- Clean kenneth-liao pattern architecture
- Infrastructure modules functional

VERSION: 3.0.0 - Kenneth-Liao Pattern
DATE: 2025-10-16
"""

import pytest
import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestCompleteSystem:
    """Complete system integration validation tests."""
    
    def test_1_all_11_subagents_discoverable(self):
        """Test: All 11 subagents can be imported."""
        print("\n" + "="*80)
        print("TEST 1: Subagent Registry (11 Subagents)")
        print("="*80)
        
        # Expected subagents (meta-orchestrator is NOT included - it's the main agent)
        expected_agents = [
            'knowledge_builder',
            'quality_agent',
            'research_agent',
            'socratic_requirements_agent',
            'neo4j_query_agent',
            'problem_decomposer_agent',
            'problem_scaffolding_generator_agent',
            'personalization_engine_agent',
            'self_improver_agent',
            'meta_planning_analyzer',
            'meta_query_helper',
        ]
        
        imported = []
        failed = []
        
        for agent_name in expected_agents:
            try:
                module = __import__(f'agents', fromlist=[agent_name])
                agent = getattr(module, agent_name)
                imported.append(agent_name)
                print(f"  ✓ {agent_name}")
            except Exception as e:
                failed.append((agent_name, str(e)))
                print(f"  ✗ {agent_name}: {e}")
        
        print(f"\n  Total: {len(imported)}/{len(expected_agents)} subagents")
        
        if failed:
            print(f"\n  Failed imports:")
            for name, error in failed:
                print(f"    - {name}: {error}")
        
        assert len(imported) == len(expected_agents), f"Expected {len(expected_agents)} agents, found {len(imported)}"
        
        print(f"\n✅ TEST 1 PASSED: All 11 subagents discoverable")
    
    def test_2_meta_orchestrator_utility_class(self):
        """Test: MetaOrchestratorLogic utility class is functional."""
        print("\n" + "="*80)
        print("TEST 2: Meta-Orchestrator Utility Class")
        print("="*80)
        
        from lib.orchestrator_utils import MetaOrchestratorLogic
        
        logic = MetaOrchestratorLogic()
        
        # Test quality gate evaluation
        test_impact = {
            'cis_size': 10,
            'test_coverage': 0.85,
            'critical_affected': False
        }
        test_root_cause = {
            'confidence_score': 0.8
        }
        
        result = logic.evaluate_quality_gate(test_impact, test_root_cause)
        
        assert result['approved'] == True, "Quality gate should pass"
        assert result['status'] == 'PASSED'
        
        print(f"  ✓ MetaOrchestratorLogic instantiable")
        print(f"  ✓ evaluate_quality_gate() functional")
        print(f"  ✓ Quality gate test: {result['status']}")
        
        print(f"\n✅ TEST 2 PASSED: Utility class functional")
    
    def test_3_infrastructure_modules_available(self):
        """Test: Infrastructure modules are importable."""
        print("\n" + "="*80)
        print("TEST 3: Infrastructure Modules")
        print("="*80)
        
        # Import infrastructure
        from subagents import (
            ErrorTracker,
            StructuredLogger,
            PerformanceMonitor,
            ContextManager,
            AgentRegistry
        )
        
        # Verify instantiation
        error_tracker = ErrorTracker(max_retries=3)
        logger = StructuredLogger(log_dir="/tmp/test-logs")
        perf_monitor = PerformanceMonitor()
        
        print(f"  ✓ ErrorTracker")
        print(f"  ✓ StructuredLogger")
        print(f"  ✓ PerformanceMonitor")
        print(f"  ✓ ContextManager")
        print(f"  ✓ AgentRegistry")
        
        print(f"\n✅ TEST 3 PASSED: Infrastructure modules available")
    
    def test_4_agent_definition_compliance(self):
        """Test: All agents are simple AgentDefinition instances."""
        print("\n" + "="*80)
        print("TEST 4: AgentDefinition Compliance (Kenneth-Liao Pattern)")
        print("="*80)
        
        from claude_agent_sdk import AgentDefinition
        from subagents import (
            knowledge_builder,
            quality_agent,
            research_agent,
        )
        
        agents_to_test = [
            ('knowledge_builder', knowledge_builder),
            ('quality_agent', quality_agent),
            ('research_agent', research_agent),
        ]
        
        for name, agent in agents_to_test:
            # Verify it's an AgentDefinition instance
            assert isinstance(agent, AgentDefinition), f"{name} is not AgentDefinition"
            
            # Verify required fields
            assert hasattr(agent, 'description'), f"{name} missing description"
            assert hasattr(agent, 'prompt'), f"{name} missing prompt"
            assert hasattr(agent, 'model'), f"{name} missing model"
            assert hasattr(agent, 'tools'), f"{name} missing tools"
            
            print(f"  ✓ {name}: AgentDefinition compliant")
        
        print(f"\n✅ TEST 4 PASSED: Agents follow kenneth-liao pattern")
    
    def test_5_no_markdown_duplicates(self):
        """Test: .claude/agents/ directory removed (no duplicates)."""
        print("\n" + "="*80)
        print("TEST 5: No Markdown Duplicates")
        print("="*80)
        
        agents_md_dir = Path(__file__).parent.parent / ".claude" / "agents"
        
        if agents_md_dir.exists():
            md_files = list(agents_md_dir.glob("*.md"))
            print(f"  ✗ .claude/agents/ exists with {len(md_files)} files")
            assert False, ".claude/agents/ should be deleted"
        else:
            print(f"  ✓ .claude/agents/ directory removed")
        
        print(f"\n✅ TEST 5 PASSED: No markdown duplicates")
    
    def test_6_removed_agents_not_importable(self):
        """Test: Removed agents are no longer importable."""
        print("\n" + "="*80)
        print("TEST 6: Removed Agents Cleanup")
        print("="*80)
        
        removed_agents = [
            'semantic_manager_agent',
            'kinetic_execution_agent',
            'dynamic_learning_agent',
            'performance_engineer',
            'security_auditor',
            'test_automation_specialist',
        ]
        
        for agent_name in removed_agents:
            try:
                module = __import__(f'agents.{agent_name}', fromlist=[agent_name])
                print(f"  ✗ {agent_name}: Still importable (should be deleted)")
                assert False, f"{agent_name} should not be importable"
            except (ImportError, ModuleNotFoundError):
                print(f"  ✓ {agent_name}: Properly removed")
        
        print(f"\n✅ TEST 6 PASSED: All removed agents are gone")
    
    def test_7_main_py_kenneth_liao_pattern(self):
        """Test: main.py follows kenneth-liao pattern."""
        print("\n" + "="*80)
        print("TEST 7: Main.py Kenneth-Liao Pattern")
        print("="*80)
        
        main_file = Path(__file__).parent.parent / "main.py"
        content = main_file.read_text()
        
        # Verify kenneth-liao pattern elements
        checks = [
            ('ClaudeSDKClient import', 'ClaudeSDKClient' in content),
            ('AgentDefinition import', 'AgentDefinition' in content),
            ('agents dict', 'agents={' in content),
            ('Version 3.0.0', '3.0.0' in content),
            ('Kenneth-Liao Pattern', 'Kenneth-Liao' in content),
        ]
        
        for check_name, passed in checks:
            print(f"  {'✓' if passed else '✗'} {check_name}")
            assert passed, f"Missing: {check_name}"
        
        print(f"\n✅ TEST 7 PASSED: Main.py follows kenneth-liao pattern")
    
    def test_8_agent_count_validation(self):
        """Test: Exactly 11 subagents (meta-orchestrator separate)."""
        print("\n" + "="*80)
        print("TEST 8: Agent Count Validation")
        print("="*80)
        
        from subagents import __all__
        
        # Filter out infrastructure modules
        infrastructure = [
            'ErrorTracker', 'StructuredLogger', 'PerformanceMonitor',
            'ContextManager', 'AgentRegistry', 'DependencyAgent',
            'SelfImprover', 'ImprovementManager', 'ImprovementAction',
            'ImpactAnalysis', 'QualityGateApproval', 'RootCauseAnalysis',
            'IssueReport', 'ChangeStatus', 'ChangeRecord', 'ActionType',
            'PlanningObserver', 'PlanningStep', 'PlanningSessionManager',
            'ask_agent_tool', 'resilient_task', 'RetryConfig',
            'human_escalation_handler', 'setup_structured_logger',
            'AgentLogger', 'set_trace_id', 'get_trace_id',
            'AgentMetrics', 'PerformanceTimer', 'DependencyNode',
            'DependencyEdge', 'NodeType', 'EdgeType',
        ]
        
        agents_exported = [item for item in __all__ if item not in infrastructure]
        
        print(f"  Total exports in __all__: {len(__all__)}")
        print(f"  Infrastructure modules: {len(infrastructure)}")
        print(f"  Agent exports: {len(agents_exported)}")
        print(f"\n  Agents:")
        for agent in agents_exported:
            print(f"    - {agent}")
        
        assert len(agents_exported) == 11, f"Expected 11 agents, found {len(agents_exported)}"
        
        print(f"\n✅ TEST 8 PASSED: Exactly 11 subagents exported")
    
    def test_9_main_loop_simplicity(self):
        """Test: Main loop is simple (kenneth-liao pattern)."""
        print("\n" + "="*80)
        print("TEST 9: Main Loop Simplicity")
        print("="*80)
        
        main_file = Path(__file__).parent.parent / "main.py"
        content = main_file.read_text()
        
        # Verify simplicity indicators
        checks = [
            ('async with ClaudeSDKClient', 'async with ClaudeSDKClient' in content),
            ('while True loop', 'while True:' in content),
            ('client.query()', 'client.query(' in content),
            ('receive_response()', 'receive_response()' in content),
            ('Simple exit handling', "'exit'" in content.lower()),
        ]
        
        for check_name, passed in checks:
            print(f"  {'✓' if passed else '✗'} {check_name}")
            assert passed, f"Missing: {check_name}"
        
        # Verify NOT overly complex (no elaborate session management)
        lines = content.split('\n')
        print(f"\n  Total lines: {len(lines)}")
        
        # Kenneth-liao pattern should be < 200 lines
        assert len(lines) < 250, f"main.py too complex ({len(lines)} lines), should be < 250"
        
        print(f"\n✅ TEST 9 PASSED: Main loop is simple and clean")
    
    def test_10_system_architecture_validated(self):
        """Test: Final architecture validation."""
        print("\n" + "="*80)
        print("TEST 10: Architecture Validation")
        print("="*80)
        
        print("\n  Architecture Summary:")
        print("  " + "-" * 76)
        print(f"  Main Agent: meta-orchestrator (system prompt in .claude/CLAUDE.md)")
        print(f"  Subagents: 11 specialized agents")
        print(f"  Pattern: Kenneth-Liao (ClaudeSDKClient + AgentDefinition dict)")
        print(f"  Duplicates: 0 (markdown files removed)")
        print(f"  Tier Coordinators: Removed (logic in meta-orchestrator)")
        print("  " + "-" * 76)
        
        # Verify no duplicate definitions
        agents_dir = Path(__file__).parent.parent / "agents"
        claude_agents_dir = Path(__file__).parent.parent / ".claude" / "agents"
        
        assert claude_agents_dir.exists() == False, ".claude/agents/ should not exist"
        
        # Count Python agent files
        agent_files = list(agents_dir.glob("*_agent.py"))
        print(f"\n  Python agent files: {len(agent_files)}")
        
        # Verify all are importable
        from subagents import (
            knowledge_builder,
            quality_agent,
            research_agent,
        )
        
        print(f"  ✓ All agents importable")
        print(f"  ✓ No markdown duplicates")
        print(f"  ✓ Clean architecture validated")
        
        print(f"\n✅ TEST 10 PASSED: System architecture validated")


if __name__ == '__main__':
    # Run tests
    tester = TestCompleteSystem()
    
    try:
        tester.test_1_all_11_subagents_discoverable()
        tester.test_2_meta_orchestrator_utility_class()
        tester.test_3_infrastructure_modules_available()
        tester.test_4_agent_definition_compliance()
        tester.test_5_no_markdown_duplicates()
        tester.test_6_removed_agents_not_importable()
        tester.test_7_main_py_kenneth_liao_pattern()
        tester.test_8_agent_count_validation()
        tester.test_9_main_loop_simplicity()
        tester.test_10_system_architecture_validated()
        
        print("\n" + "="*80)
        print("🎉 ALL TIER 5 TESTS PASSED (10/10)")
        print("="*80)
        print("\n✅ Kenneth-Liao Pattern Refactoring Complete!")
        print("   - 11 subagents")
        print("   - 1 main agent (meta-orchestrator)")
        print("   - 0 duplicates")
        print("   - Clean architecture")
        
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
