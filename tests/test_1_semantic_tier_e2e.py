"""
Tier 1: Semantic Layer E2E Tests - Kenneth-Liao Pattern

Tests the refactored kenneth-liao pattern implementation with new directory structure:
- Subagents in subagents/
- Infrastructure in infrastructure/
- Lib utilities in lib/

VERSION: 3.1.0 - Directory Optimization
DATE: 2025-10-16
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestSemanticTier:
    """Semantic tier validation tests for optimized directory structure."""
    
    def test_1_subagents_importable(self):
        """Test: All 11 subagents can be imported from subagents/."""
        print("\n" + "="*80)
        print("TEST 1: Subagent Imports from subagents/")
        print("="*80)
        
        from claude_agent_sdk import AgentDefinition
        from subagents import (
            knowledge_builder,
            quality_agent,
            research_agent,
            socratic_requirements_agent,
            neo4j_query_agent,
            problem_decomposer_agent,
            problem_scaffolding_generator_agent,
            personalization_engine_agent,
            self_improver_agent,
            meta_planning_analyzer,
            meta_query_helper,
        )
        
        agents = [
            ("knowledge_builder", knowledge_builder),
            ("quality_agent", quality_agent),
            ("research_agent", research_agent),
            ("socratic_requirements_agent", socratic_requirements_agent),
            ("neo4j_query_agent", neo4j_query_agent),
            ("problem_decomposer_agent", problem_decomposer_agent),
            ("problem_scaffolding_generator_agent", problem_scaffolding_generator_agent),
            ("personalization_engine_agent", personalization_engine_agent),
            ("self_improver_agent", self_improver_agent),
            ("meta_planning_analyzer", meta_planning_analyzer),
            ("meta_query_helper", meta_query_helper),
        ]
        
        for name, agent in agents:
            assert isinstance(agent, AgentDefinition), f"{name} is not AgentDefinition"
            print(f"  ✓ {name}")
        
        print(f"\n✅ TEST 1 PASSED: All 11 subagents importable from subagents/")
    
    def test_2_infrastructure_importable(self):
        """Test: Infrastructure modules importable from infrastructure/."""
        print("\n" + "="*80)
        print("TEST 2: Infrastructure Imports from infrastructure/")
        print("="*80)
        
        from infrastructure import (
            ErrorTracker,
            StructuredLogger,
            PerformanceMonitor,
            ContextManager,
            AgentRegistry
        )
        
        # Verify instantiation
        error_tracker = ErrorTracker(max_retries=3)
        logger = StructuredLogger(log_dir="/tmp/test")
        perf_monitor = PerformanceMonitor()
        
        print(f"  ✓ ErrorTracker")
        print(f"  ✓ StructuredLogger")
        print(f"  ✓ PerformanceMonitor")
        print(f"  ✓ ContextManager")
        print(f"  ✓ AgentRegistry")
        
        print(f"\n✅ TEST 2 PASSED: Infrastructure modules importable")
    
    def test_3_lib_utilities_importable(self):
        """Test: Lib utilities importable from lib/."""
        print("\n" + "="*80)
        print("TEST 3: Lib Utilities from lib/")
        print("="*80)
        
        from lib import (
            MetaOrchestratorLogic,
            DependencyAgent,
            SelfImprover,
            ImprovementManager,
        )
        
        # Verify instantiation
        logic = MetaOrchestratorLogic()
        
        print(f"  ✓ MetaOrchestratorLogic")
        print(f"  ✓ DependencyAgent")
        print(f"  ✓ SelfImprover")
        print(f"  ✓ ImprovementManager")
        
        print(f"\n✅ TEST 3 PASSED: Lib utilities importable")
    
    def test_4_directory_structure_clean(self):
        """Test: Directory structure is optimized."""
        print("\n" + "="*80)
        print("TEST 4: Directory Structure Optimization")
        print("="*80)
        
        project_root = Path(__file__).parent.parent
        
        # Verify new directories exist
        assert (project_root / "subagents").exists(), "subagents/ missing"
        assert (project_root / "infrastructure").exists(), "infrastructure/ missing"
        assert (project_root / "lib").exists(), "lib/ missing"
        
        # Verify old agents/ directory removed
        assert not (project_root / "agents").exists(), "agents/ should be removed"
        
        # Count files in each directory
        subagent_count = len(list((project_root / "subagents").glob("*.py"))) - 1  # Exclude __init__.py
        infra_count = len(list((project_root / "infrastructure").glob("*.py"))) - 1
        lib_count = len(list((project_root / "lib").glob("*.py"))) - 1
        
        print(f"  ✓ subagents/: {subagent_count} files")
        print(f"  ✓ infrastructure/: {infra_count} files")
        print(f"  ✓ lib/: {lib_count} files")
        print(f"  ✓ agents/: removed")
        
        assert subagent_count == 11, f"Expected 11 subagents, found {subagent_count}"
        
        print(f"\n✅ TEST 4 PASSED: Directory structure optimized")
    
    def test_5_root_level_clean(self):
        """Test: Root level has minimal files."""
        print("\n" + "="*80)
        print("TEST 5: Root Level Cleanup")
        print("="*80)
        
        project_root = Path(__file__).parent.parent
        
        # Count markdown files in root
        root_md_files = list(project_root.glob("*.md"))
        root_md_count = len(root_md_files)
        
        print(f"  Root .md files: {root_md_count}")
        for f in sorted(root_md_files):
            print(f"    - {f.name}")
        
        # Should have minimal files (README, standards, guides)
        assert root_md_count <= 5, f"Too many root .md files ({root_md_count}), should be <= 5"
        
        # Verify archive exists
        archive_dir = project_root / "docs" / "archive"
        assert archive_dir.exists(), "docs/archive/ should exist"
        
        archived_count = len(list(archive_dir.glob("*.md")))
        print(f"\n  docs/archive/: {archived_count} files")
        
        print(f"\n✅ TEST 5 PASSED: Root level cleaned")


if __name__ == '__main__':
    tester = TestSemanticTier()
    
    try:
        tester.test_1_subagents_importable()
        tester.test_2_infrastructure_importable()
        tester.test_3_lib_utilities_importable()
        tester.test_4_directory_structure_clean()
        tester.test_5_root_level_clean()
        
        print("\n" + "="*80)
        print("🎉 ALL TIER 1 TESTS PASSED (5/5)")
        print("="*80)
        print("\n✅ Directory Optimization Validated!")
        
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
