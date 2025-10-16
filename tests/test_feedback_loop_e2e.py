"""
End-to-End Test: Feedback Loop Workflow

Tests complete workflow from OCR to pattern learning.

VERSION: 1.0.0
DATE: 2025-10-16
"""

import pytest
import asyncio
import json
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.mathpix_ocr_tool import extract_math_from_image
from workflows.concept_matcher import identify_concepts
from workflows.math_scaffolding_workflow import (
    query_neo4j_patterns,
    generate_scaffolding,
    extract_patterns_from_feedback,
    store_patterns_neo4j
)


class TestFeedbackLoopE2E:
    """End-to-end tests for feedback loop workflow."""
    
    def setup_method(self):
        """Setup for each test."""
        self.sample_image = str(project_root / "sample.png")
        self.test_data_dir = project_root / "data" / "test_feedback"
        self.test_data_dir.mkdir(parents=True, exist_ok=True)
    
    def test_01_ocr_extraction(self):
        """Test 1: OCR extracts math from sample.png."""
        print("\n" + "="*60)
        print("TEST 1: OCR Extraction")
        print("="*60)
        
        result = extract_math_from_image(self.sample_image)
        
        print(f"Success: {result.get('success')}")
        print(f"Confidence: {result.get('confidence', 0):.2%}")
        print(f"Text length: {len(result.get('text', ''))}")
        print(f"LaTeX length: {len(result.get('latex', ''))}")
        
        # Assertions
        assert result.get("success") is True, "OCR should succeed"
        assert result.get("confidence", 0) > 0.5, "Confidence should be > 50%"
        assert len(result.get("text", "")) > 0, "Should extract some text"
        
        print("✅ Test 1 PASSED")
        return result
    
    def test_02_concept_matching(self):
        """Test 2: Concept identification works."""
        print("\n" + "="*60)
        print("TEST 2: Concept Matching")
        print("="*60)
        
        # Use OCR result from test 1 or create mock
        test_problem = {
            "text": "60을 소인수분해하시오",
            "latex": "60 = 2^2 \\times 3 \\times 5"
        }
        
        concepts = identify_concepts(test_problem, top_k=3)
        
        print(f"Concepts found: {len(concepts)}")
        for i, c in enumerate(concepts, 1):
            print(f"  {i}. {c['name']} (score: {c['relevance_score']:.3f})")
        
        # Assertions
        assert len(concepts) > 0, "Should find at least one concept"
        assert all(0 <= c["relevance_score"] <= 1 for c in concepts), "Scores should be 0-1"
        
        print("✅ Test 2 PASSED")
        return concepts
    
    @pytest.mark.asyncio
    async def test_03_pattern_query(self):
        """Test 3: Pattern query doesn't crash."""
        print("\n" + "="*60)
        print("TEST 3: Pattern Query")
        print("="*60)
        
        concepts = [{"concept_id": "middle-1-1-ch1-1.3.1"}]
        patterns = await query_neo4j_patterns(concepts)
        
        print(f"Patterns found: {len(patterns)}")
        
        # Assertions (should return empty list for now)
        assert isinstance(patterns, list), "Should return list"
        
        print("✅ Test 3 PASSED")
        return patterns
    
    @pytest.mark.asyncio
    async def test_04_scaffolding_generation(self):
        """Test 4: Scaffolding generation produces steps."""
        print("\n" + "="*60)
        print("TEST 4: Scaffolding Generation")
        print("="*60)
        
        problem_text = "60을 소인수분해하시오"
        concepts = [
            {
                "concept_id": "middle-1-1-ch1-1.3.1",
                "name": "소인수분해",
                "relevance_score": 0.92
            }
        ]
        patterns = []
        
        scaffolding = await generate_scaffolding(problem_text, concepts, patterns)
        
        print(f"Problem ID: {scaffolding.get('problem_id')}")
        print(f"Steps generated: {len(scaffolding.get('steps', []))}")
        
        for i, step in enumerate(scaffolding.get('steps', []), 1):
            print(f"  Step {i}: {step.get('question', 'N/A')[:50]}...")
        
        # Assertions
        assert "problem_id" in scaffolding, "Should have problem_id"
        assert "steps" in scaffolding, "Should have steps"
        assert len(scaffolding["steps"]) > 0, "Should generate at least one step"
        assert all("step_id" in s for s in scaffolding["steps"]), "All steps should have step_id"
        assert all("question" in s for s in scaffolding["steps"]), "All steps should have question"
        
        print("✅ Test 4 PASSED")
        return scaffolding
    
    def test_05_feedback_structure(self):
        """Test 5: Feedback session structure is valid."""
        print("\n" + "="*60)
        print("TEST 5: Feedback Structure")
        print("="*60)
        
        # Mock feedback session (simulating user input)
        mock_feedback = {
            "session_id": "fs_test_001",
            "timestamp": "2025-10-16T10:30:00Z",
            "problem_instance": "prob_test_001",
            "image_source": "sample.png",
            "ocr_result": {
                "text": "60을 소인수분해하시오",
                "latex": "60 = 2^2 \\times 3 \\times 5",
                "confidence": 0.95
            },
            "concepts_identified": [
                {
                    "concept_id": "middle-1-1-ch1-1.3.1",
                    "name": "소인수분해",
                    "relevance_score": 0.92
                }
            ],
            "generated_steps": [
                {
                    "step_id": 1,
                    "question": "60은 짝수인가요?",
                    "feedback": {
                        "rating": 5,
                        "comment": "Clear",
                        "suggested_improvement": None
                    }
                },
                {
                    "step_id": 2,
                    "question": "60을 2로 나누면?",
                    "feedback": {
                        "rating": 3,
                        "comment": "Should emphasize smallest prime",
                        "suggested_improvement": "60을 가장 작은 소수로 나누면?"
                    }
                }
            ],
            "overall_feedback": {
                "scaffolding_level": "appropriate",
                "pacing": "good",
                "conceptual_depth": "needs_more"
            }
        }
        
        # Save to file
        test_file = self.test_data_dir / "test_feedback_session.json"
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(mock_feedback, f, indent=2, ensure_ascii=False)
        
        print(f"Mock feedback saved: {test_file}")
        
        # Assertions
        assert "session_id" in mock_feedback
        assert "generated_steps" in mock_feedback
        assert len(mock_feedback["generated_steps"]) > 0
        assert all("feedback" in s for s in mock_feedback["generated_steps"])
        
        print("✅ Test 5 PASSED")
        return mock_feedback
    
    @pytest.mark.asyncio
    async def test_06_pattern_extraction(self):
        """Test 6: Pattern extraction from feedback."""
        print("\n" + "="*60)
        print("TEST 6: Pattern Extraction")
        print("="*60)
        
        # Use mock feedback from test 5
        mock_feedback = self.test_05_feedback_structure()
        
        patterns = await extract_patterns_from_feedback(mock_feedback)
        
        print(f"Patterns extracted: {len(patterns)}")
        for i, p in enumerate(patterns, 1):
            print(f"\n  Pattern {i}:")
            print(f"    ID: {p['pattern_id']}")
            print(f"    Type: {p['type']}")
            print(f"    Confidence: {p['confidence']}")
            print(f"    Rule: {p['rule'][:60]}...")
        
        # Assertions
        assert len(patterns) > 0, "Should extract at least one pattern"
        assert all("pattern_id" in p for p in patterns), "All patterns should have ID"
        assert all("type" in p for p in patterns), "All patterns should have type"
        assert all("confidence" in p for p in patterns), "All patterns should have confidence"
        assert all(0 <= p["confidence"] <= 1 for p in patterns), "Confidence should be 0-1"
        
        print("✅ Test 6 PASSED")
        return patterns
    
    @pytest.mark.asyncio
    async def test_07_pattern_storage(self):
        """Test 7: Patterns are stored correctly."""
        print("\n" + "="*60)
        print("TEST 7: Pattern Storage")
        print("="*60)
        
        # Use patterns from test 6
        patterns = await self.test_06_pattern_extraction()
        
        success = await store_patterns_neo4j(patterns)
        
        print(f"Storage success: {success}")
        
        # Check that backup file was created
        learned_patterns_dir = project_root / "data" / "learned_patterns"
        assert learned_patterns_dir.exists(), "learned_patterns directory should exist"
        
        pattern_files = list(learned_patterns_dir.glob("patterns_*.json"))
        print(f"Pattern files created: {len(pattern_files)}")
        
        if pattern_files:
            latest_file = max(pattern_files, key=lambda p: p.stat().st_mtime)
            print(f"Latest file: {latest_file.name}")
            
            with open(latest_file, 'r', encoding='utf-8') as f:
                saved_patterns = json.load(f)
            
            print(f"Patterns in file: {len(saved_patterns)}")
            
            assert len(saved_patterns) == len(patterns), "All patterns should be saved"
        
        # Assertions
        assert success is True, "Storage should succeed"
        
        print("✅ Test 7 PASSED")
    
    def test_08_end_to_end_structure(self):
        """Test 8: All components work together."""
        print("\n" + "="*60)
        print("TEST 8: End-to-End Structure")
        print("="*60)
        
        # Verify all required directories exist
        required_dirs = [
            project_root / "data" / "ocr_results",
            project_root / "data" / "feedback_sessions",
            project_root / "data" / "learned_patterns",
            project_root / "workflows"
        ]
        
        for dir_path in required_dirs:
            assert dir_path.exists(), f"{dir_path} should exist"
            print(f"✅ {dir_path.name} exists")
        
        # Verify all required files exist
        required_files = [
            project_root / "tools" / "observability_hook.py",
            project_root / "tools" / "mathpix_ocr_tool.py",
            project_root / "tools" / "feedback_collector.py",
            project_root / "workflows" / "hook_events.py",
            project_root / "workflows" / "concept_matcher.py",
            project_root / "workflows" / "feedback_loop_workflow.py",
            project_root / "subagents" / "feedback_learning_agent.py",
            project_root / "scripts" / "run_feedback_loop.py",
            project_root / "neo4j" / "feedback_schema.cypher"
        ]
        
        for file_path in required_files:
            assert file_path.exists(), f"{file_path} should exist"
            print(f"✅ {file_path.name} exists")
        
        print("✅ Test 8 PASSED")
    
    def test_09_imports(self):
        """Test 9: All imports work correctly."""
        print("\n" + "="*60)
        print("TEST 9: Import Validation")
        print("="*60)
        
        try:
            from tools.observability_hook import send_hook_event, get_session_id
            print("✅ observability_hook imports")
            
            from workflows.hook_events import HookEventType
            print("✅ hook_events imports")
            
            from tools.mathpix_ocr_tool import extract_math_from_image
            print("✅ mathpix_ocr_tool imports")
            
            from tools.feedback_collector import collect_step_feedback, collect_interactive_feedback
            print("✅ feedback_collector imports")
            
            from workflows.concept_matcher import identify_concepts
            print("✅ concept_matcher imports")
            
            from workflows.feedback_loop_workflow import run_feedback_loop_workflow
            print("✅ feedback_loop_workflow imports")
            
            from subagents.feedback_learning_agent import feedback_learning_agent
            print("✅ feedback_learning_agent imports")
            
            # Check agent is registered
            from subagents import feedback_learning_agent as fla
            assert fla is not None
            print("✅ feedback_learning_agent registered in subagents")
            
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
        
        print("✅ Test 9 PASSED")
    
    def test_10_observability_hooks(self):
        """Test 10: Observability hooks work."""
        print("\n" + "="*60)
        print("TEST 10: Observability Hooks")
        print("="*60)
        
        from tools.observability_hook import send_hook_event, get_session_id
        from workflows.hook_events import HookEventType
        
        session_id = get_session_id()
        print(f"Session ID: {session_id}")
        assert len(session_id) > 0, "Session ID should be generated"
        
        # Send test event (will fail if server not running, but shouldn't crash)
        result = send_hook_event(
            "test",
            HookEventType.OCR_STARTED,
            {"test": "data"}
        )
        
        print(f"Hook send result: {result}")
        # Don't assert True - observability server might not be running
        # Just verify it doesn't crash
        
        print("✅ Test 10 PASSED")


def run_tests():
    """Run all tests manually."""
    test_suite = TestFeedbackLoopE2E()
    test_suite.setup_method()
    
    tests = [
        ("OCR Extraction", test_suite.test_01_ocr_extraction),
        ("Concept Matching", test_suite.test_02_concept_matching),
        ("Pattern Query", test_suite.test_03_pattern_query),
        ("Scaffolding Generation", test_suite.test_04_scaffolding_generation),
        ("Feedback Structure", test_suite.test_05_feedback_structure),
        ("Pattern Extraction", test_suite.test_06_pattern_extraction),
        ("Pattern Storage", test_suite.test_07_pattern_storage),
        ("E2E Structure", test_suite.test_08_end_to_end_structure),
        ("Imports", test_suite.test_09_imports),
        ("Observability", test_suite.test_10_observability_hooks),
    ]
    
    passed = 0
    failed = 0
    errors = []
    
    print("\n" + "="*70)
    print("RUNNING END-TO-END TEST SUITE")
    print("="*70)
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                asyncio.run(test_func())
            else:
                test_func()
            passed += 1
        except Exception as e:
            failed += 1
            errors.append((test_name, str(e)))
            print(f"❌ Test FAILED: {test_name}")
            print(f"   Error: {e}")
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Total: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {passed / (passed + failed) * 100:.1f}%")
    
    if errors:
        print(f"\nFailed Tests:")
        for test_name, error in errors:
            print(f"  - {test_name}: {error}")
    
    print("="*70)
    
    return passed == len(tests)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    success = run_tests()
    sys.exit(0 if success else 1)

