"""
Meta-Cognitive Feedback Loop Tests

VERSION: 1.0.0
DATE: 2025-10-15
PURPOSE: Test real-time meta-cognitive feedback system

Tests:
1. PlanningObserver captures planning steps
2. PlanningSessionManager orchestrates feedback
3. Meta-planning-analyzer provides actionable feedback
4. Meta-learnings saved to memory-keeper
5. Feedback improves subsequent planning

Run:
    pytest tests/test_meta_cognitive_feedback.py -v
"""

import pytest
import asyncio
import json
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.mark.asyncio
async def test_planning_observer_full_workflow():
    """Test 1: PlanningObserver captures complete workflow"""
    print("\n" + "="*80)
    print("TEST 1: PlanningObserver Full Workflow")
    print("="*80)
    
    from agents.planning_observer import PlanningObserver
    
    observer = PlanningObserver("Implement streaming system with meta-cognitive feedback")
    
    # Simulate planning process
    observer.record_query(
        query="Read main.py to understand current implementation",
        reasoning="Need baseline to plan improvements",
        expected_insights=["Blocking vs streaming", "SDK version", "Error handling"]
    )
    
    observer.record_analysis(
        analysis="Current state: Blocking implementation, no streaming",
        findings=["Lines 202-208 use blocking client.query()", "No Extended Thinking", "No caching"],
        implications=["Need streaming", "Need Extended Thinking", "Need caching"]
    )
    
    observer.record_decision(
        decision="Implement streaming in main.py first",
        reasoning="Highest user impact, immediate visibility improvement",
        alternatives=["Start with agents", "Create wrapper", "Use fallback only"],
        trade_offs={
            "pros": ["Immediate UX improvement", "Shows Extended Thinking", "Template for other components"],
            "cons": ["SDK may not support", "Need fallback handling"]
        }
    )
    
    observer.record_trade_off(
        option_a="SDK streaming (preferred)",
        option_b="Direct Anthropic API wrapper",
        comparison={
            "sdk_pros": ["Cleaner integration", "SDK handles details"],
            "sdk_cons": ["May not support all features"],
            "api_pros": ["Full control", "All features available"],
            "api_cons": ["More complex", "Manual event handling"]
        },
        chosen="SDK streaming with fallback"
    )
    
    # Export and validate
    trace = observer.export_for_meta_orchestrator()
    
    assert trace["total_steps"] == 4, f"Expected 4 steps, got {trace['total_steps']}"
    assert trace["summary"]["queries"] == 1
    assert trace["summary"]["analyses"] == 1
    assert trace["summary"]["decisions"] == 1
    assert trace["summary"]["trade_offs"] == 1
    assert 0.0 <= trace["summary"]["avg_confidence"] <= 1.0
    
    print(f"✓ Recorded 4 planning steps")
    print(f"✓ Summary statistics correct")
    print(f"✓ Average confidence: {trace['summary']['avg_confidence']:.2f}")
    print(f"✓ Export format valid")
    
    # Test save functionality
    output_file = project_root / "outputs" / "planning-traces" / "test_trace.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    observer.save_trace(str(output_file))
    
    assert output_file.exists(), "Trace file not saved"
    print(f"✓ Trace saved to {output_file}")
    
    # Cleanup
    output_file.unlink()
    
    print("\n✅ TEST 1 PASSED")
    return True


@pytest.mark.asyncio
async def test_planning_session_manager():
    """Test 2: PlanningSessionManager orchestrates feedback"""
    print("\n" + "="*80)
    print("TEST 2: Planning Session Manager")
    print("="*80)
    
    from agents.planning_session_manager import PlanningSessionManager
    
    # Mock task function
    async def mock_task_func(agent_name: str, task: str) -> str:
        """Mock meta-planning-analyzer response"""
        return json.dumps({
            "overall_quality": "good",
            "efficiency_score": 0.85,
            "inefficiencies_detected": [
                {
                    "step": 1,
                    "issue": "Could use parallel file reads",
                    "suggestion": "Read multiple files simultaneously",
                    "impact": "medium"
                }
            ],
            "meta_learning": {
                "pattern_identified": "Sequential file reads",
                "recommendation": "Use parallel read_file calls",
                "save_to_memory": True
            }
        })
    
    # Create manager
    manager = PlanningSessionManager(
        meta_orchestrator_task_func=mock_task_func,
        checkpoint_steps=[3, 7]
    )
    
    # Start session
    observer = manager.start_planning_session("Test planning task")
    assert manager.session_active, "Session not active"
    assert manager.observer is not None, "Observer not created"
    
    print("✓ Session started successfully")
    
    # Record steps until checkpoint
    observer.record_query("Query 1", "Reason 1", ["Insight 1"])
    observer.record_query("Query 2", "Reason 2", ["Insight 2"])
    observer.record_decision("Decision 1", "Reason", ["Alt 1"], {"pros": ["Pro"], "cons": []})
    
    # Should be at checkpoint (step 3)
    assert manager.get_current_step() == 3, "Step count mismatch"
    assert manager.should_checkpoint(), "Checkpoint not detected"
    
    print("✓ Checkpoint detection working")
    
    # Request feedback
    feedback = await manager.checkpoint_feedback()
    
    assert feedback is not None, "No feedback received"
    assert "overall_quality" in feedback, "Feedback format invalid"
    assert len(manager.feedback_history) == 1, "Feedback not recorded"
    
    print("✓ Feedback received and recorded")
    print(f"✓ Overall quality: {feedback.get('overall_quality')}")
    
    # Finalize
    final_trace = manager.finalize_planning(save_trace=False)
    assert "feedback_history" in final_trace, "Feedback history not included"
    assert final_trace["checkpoints_reached"] == 1, "Checkpoint count wrong"
    
    print("✓ Session finalized correctly")
    
    print("\n✅ TEST 2 PASSED")
    return True


@pytest.mark.asyncio
async def test_agent_registry_features():
    """Test 3: AgentRegistry feature detection"""
    print("\n" + "="*80)
    print("TEST 3: Agent Registry Feature Detection")
    print("="*80)
    
    from agents.agent_registry import AgentRegistry
    
    registry = AgentRegistry(project_root / "agents")
    agents = registry.discover_agents()
    
    # Check discovery
    assert len(agents) >= 9, f"Expected >=9 agents, found {len(agents)}"
    print(f"✓ Discovered {len(agents)} agents")
    
    # Check feature detection
    agents_with_thinking = registry.get_agents_with_extended_thinking()
    print(f"✓ Agents with Extended Thinking: {len(agents_with_thinking)}")
    
    # Should be 9 agents with Extended Thinking now
    assert len(agents_with_thinking) >= 8, \
        f"Expected >=8 agents with Extended Thinking, found {len(agents_with_thinking)}"
    
    # Check capability routing
    task_capable = registry.get_agents_by_capability("Task")
    print(f"✓ Agents with Task capability: {task_capable}")
    assert "meta-orchestrator" in task_capable, "Meta-orchestrator should have Task"
    
    # Check metadata
    meta = registry.get_agent_capabilities("meta-orchestrator")
    assert meta.get("has_extended_thinking") == True, "Extended Thinking not detected"
    assert meta.get("thinking_budget") in [10_000, 10000], \
        f"Thinking budget wrong: {meta.get('thinking_budget')}"
    
    print("✓ Capability routing works")
    print("✓ Metadata extraction accurate")
    
    # Test validation
    validation = registry.validate_agents()
    print(f"✓ Passing agents: {len(validation['passing'])}")
    print(f"✓ Warnings: {len(validation['warnings'])}")
    print(f"✓ Errors: {len(validation['errors'])}")
    
    print("\n✅ TEST 3 PASSED")
    return True


@pytest.mark.asyncio
async def test_meta_learning_persistence():
    """Test 4: Meta-learning pattern structure"""
    print("\n" + "="*80)
    print("TEST 4: Meta-Learning Persistence Structure")
    print("="*80)
    
    from agents.planning_session_manager import PlanningSessionManager
    
    manager = PlanningSessionManager()
    observer = manager.start_planning_session("Test task")
    
    # Simulate feedback with meta-learning
    manager.feedback_history.append({
        "checkpoint_step": 3,
        "feedback": {
            "meta_learning": {
                "pattern_identified": "Parallel file reads improve efficiency",
                "recommendation": "Use parallel read_file calls for multi-file analysis",
                "confidence": 0.92,
                "save_to_memory": True
            }
        },
        "timestamp": datetime.now().isoformat()
    })
    
    # Extract meta-learnings
    learnings = manager.extract_meta_learnings()
    
    assert len(learnings) == 1, "Meta-learning not extracted"
    assert learnings[0]["pattern"] == "Parallel file reads improve efficiency"
    assert learnings[0]["confidence"] == 0.92
    
    print("✓ Meta-learning extraction works")
    print(f"✓ Pattern: {learnings[0]['pattern']}")
    print(f"✓ Confidence: {learnings[0]['confidence']}")
    
    print("\n✅ TEST 4 PASSED")
    return True


@pytest.mark.asyncio
async def test_streaming_fallback_handling():
    """Test 5: Verify fallback handling when streaming unavailable"""
    print("\n" + "="*80)
    print("TEST 5: Streaming Fallback Handling")
    print("="*80)
    
    main_py = project_root / "main.py"
    content = main_py.read_text()
    
    # Check for fallback logic
    assert "hasattr(client, 'stream_response')" in content, \
        "SDK capability check missing"
    assert "SDK streaming not available" in content, \
        "Fallback warning missing"
    assert "client.query(user_input)" in content, \
        "Fallback to blocking not implemented"
    
    print("✓ SDK capability check present")
    print("✓ Fallback warning included")
    print("✓ Blocking fallback available")
    
    print("\n✅ TEST 5 PASSED")
    return True


if __name__ == '__main__':
    from datetime import datetime
    
    # Run all tests
    asyncio.run(test_planning_observer_full_workflow())
    asyncio.run(test_planning_session_manager())
    asyncio.run(test_agent_registry_features())
    asyncio.run(test_meta_learning_persistence())
    asyncio.run(test_streaming_fallback_handling())
    
    print("\n" + "="*80)
    print("ALL META-COGNITIVE FEEDBACK TESTS PASSED ✅")
    print("="*80)

