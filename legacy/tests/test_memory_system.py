#!/usr/bin/env python3
"""
Comprehensive Test Suite for Memory System with Context Editing
Tests all Sonnet 4.5 features integration
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add src to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from memory_system import (
    get_memory_handler,
    get_thinking_integration,
    get_context_manager,
    think_and_remember,
    StopReason
)


class TestMemorySystem:
    """Test suite for memory system"""

    def __init__(self):
        self.memory = get_memory_handler()
        self.thinking = get_thinking_integration("test-session")
        self.context_manager = get_context_manager()
        self.passed = 0
        self.failed = 0

    def run_all_tests(self):
        """Run all test scenarios"""
        print("=" * 70)
        print("🧪 MEMORY SYSTEM TEST SUITE")
        print("=" * 70)
        print()

        tests = [
            ("Memory Handler", self.test_memory_handler),
            ("Thinking Integration", self.test_thinking_integration),
            ("Sequential Thinking + Memory", self.test_sequential_thinking_memory),
            ("Context Manager", self.test_context_manager),
            ("Checkpoint Creation", self.test_checkpoint_creation),
            ("Recovery from Compact", self.test_recovery),
            ("Stop Reason Handling", self.test_stop_reasons),
            ("Token Tracking", self.test_token_tracking),
        ]

        for test_name, test_func in tests:
            print(f"\n{'─' * 70}")
            print(f"📋 Test: {test_name}")
            print(f"{'─' * 70}")

            try:
                test_func()
                self.passed += 1
                print(f"✅ {test_name} PASSED")
            except AssertionError as e:
                self.failed += 1
                print(f"❌ {test_name} FAILED: {e}")
            except Exception as e:
                self.failed += 1
                print(f"💥 {test_name} ERROR: {e}")

        self._print_summary()

    def test_memory_handler(self):
        """Test basic memory operations"""
        print("Testing basic memory operations...")

        # Test create
        result = self.memory.create(
            "test/sample.txt",
            "Test content\nLine 2\nLine 3"
        )
        assert result['status'] == 'success', "Create failed"
        print("  ✓ Create file")

        # Test view
        result = self.memory.view("test/sample.txt")
        assert result['status'] == 'success', "View failed"
        assert "Test content" in result['content'], "Content mismatch"
        print("  ✓ View file")

        # Test str_replace
        result = self.memory.str_replace(
            "test/sample.txt",
            "Line 2",
            "Modified Line 2"
        )
        assert result['status'] == 'success', "Replace failed"
        print("  ✓ String replace")

        # Test insert
        result = self.memory.insert(
            "test/sample.txt",
            2,
            "Inserted line\n"
        )
        assert result['status'] == 'success', "Insert failed"
        print("  ✓ Insert line")

        # Test view directory
        result = self.memory.view("test")
        assert result['status'] == 'success', "View directory failed"
        assert "sample.txt" in result['content'], "File not listed"
        print("  ✓ View directory")

    def test_thinking_integration(self):
        """Test thinking-memory integration"""
        print("Testing thinking integration...")

        # Test recording thinking steps
        result = self.thinking.record_thinking_step(
            "This is a test thought",
            thought_number=1,
            total_thoughts=3
        )
        assert result['status'] == 'success', "Record thought failed"
        print("  ✓ Record thinking step")

        # Test recording decision
        result = self.thinking.record_decision(
            decision="Use XML format",
            rationale="Structured and readable",
            alternatives=["JSON", "YAML"]
        )
        assert result['status'] == 'success', "Record decision failed"
        print("  ✓ Record decision")

        # Test recording progress
        result = self.thinking.record_progress(
            task="Test task",
            status="completed",
            details="Successfully tested"
        )
        assert result['status'] == 'success', "Record progress failed"
        print("  ✓ Record progress")

        # Test generating summary
        summary = self.thinking.generate_summary()
        assert len(summary) > 0, "Summary is empty"
        assert "Session ID" in summary, "Summary missing key info"
        print("  ✓ Generate summary")

    def test_sequential_thinking_memory(self):
        """Test sequential thinking with automatic memory storage"""
        print("Testing sequential thinking + memory...")

        # Simulate thinking process
        thoughts = [
            "First, I need to understand the problem structure",
            "Then, I should break it down into components",
            "Finally, I'll implement each component"
        ]

        for i, thought in enumerate(thoughts, 1):
            result = think_and_remember(
                thought=thought,
                thought_number=i,
                total_thoughts=len(thoughts)
            )
            assert result['status'] == 'success', f"Thought {i} failed"

        print(f"  ✓ Stored {len(thoughts)} thinking steps")

        # Verify thinking log exists
        log_result = self.memory.view(self.thinking.thinking_log_path)
        assert log_result['status'] == 'success', "Log not found"
        assert "First, I need to understand" in log_result['content'], "Content missing"
        print("  ✓ Thinking log verified")

    def test_context_manager(self):
        """Test context manager functionality"""
        print("Testing context manager...")

        # Test token checking
        result = self.context_manager.check_token_usage(50000)
        assert result['status'] == 'ok', "Token check failed for normal usage"
        print("  ✓ Normal token usage check")

        result = self.context_manager.check_token_usage(140000)
        assert result['status'] == 'warning', "Token check failed for warning"
        print("  ✓ Warning threshold check")

        result = self.context_manager.check_token_usage(150000)
        assert result['status'] == 'critical', "Token check failed for critical"
        print("  ✓ Critical threshold check")

        # Test config generation
        config = self.context_manager.get_context_editing_config()
        assert 'betas' in config, "Config missing betas"
        assert 'context_management' in config, "Config missing context_management"
        print("  ✓ Context editing config")

    def test_checkpoint_creation(self):
        """Test checkpoint creation and loading"""
        print("Testing checkpoint creation...")

        # Create checkpoint
        state = {
            "phase": "Test Phase",
            "completed_tasks": ["Task 1", "Task 2"],
            "next_tasks": ["Task 3", "Task 4"]
        }

        result = self.thinking.create_recovery_checkpoint(
            checkpoint_name="test-checkpoint",
            state=state
        )
        assert result['status'] == 'success', "Checkpoint creation failed"
        print("  ✓ Checkpoint created")

        # Verify checkpoint file
        checkpoint_result = self.memory.view("phase-progress")
        assert checkpoint_result['status'] == 'success', "Cannot view checkpoints"
        assert "checkpoint-test-checkpoint" in checkpoint_result['content'], "Checkpoint not found"
        print("  ✓ Checkpoint file verified")

    def test_recovery(self):
        """Test recovery from checkpoint"""
        print("Testing recovery from checkpoint...")

        # Create a checkpoint
        state = {
            "phase": "Recovery Test",
            "completed_tasks": ["Setup", "Config"],
            "next_tasks": ["Implementation"]
        }

        self.thinking.create_recovery_checkpoint(
            checkpoint_name="recovery-test",
            state=state
        )

        # Create pre-compact checkpoint
        result = self.context_manager.create_pre_compact_checkpoint(
            current_state=state,
            tool_results_to_preserve=[]
        )
        assert result['status'] == 'success', "Pre-compact checkpoint failed"
        print("  ✓ Pre-compact checkpoint created")

        # Test recovery
        recovered = self.context_manager.recover_from_compact()
        assert recovered is not None, "Recovery failed"
        assert recovered['current_state']['phase'] == "Recovery Test", "State mismatch"
        print("  ✓ Recovery successful")

    def test_stop_reasons(self):
        """Test enhanced stop reason handling"""
        print("Testing stop reason handling...")

        stop_reasons = [
            ("end_turn", "completed"),
            ("max_tokens", "truncated"),
            ("stop_sequence", "stopped"),
            ("tool_use", "tool_pending"),
        ]

        for reason, expected_status in stop_reasons:
            result = self.context_manager.handle_stop_reason(reason)
            assert result['status'] == expected_status, f"Wrong status for {reason}"
            print(f"  ✓ {reason} → {expected_status}")

    def test_token_tracking(self):
        """Test token usage tracking"""
        print("Testing token tracking...")

        # Mock token usage
        test_tokens = [
            (50000, 'ok'),
            (100000, 'ok'),
            (140000, 'warning'),
            (150000, 'critical')
        ]

        for tokens, expected_status in test_tokens:
            result = self.context_manager.check_token_usage(tokens)
            assert result['status'] == expected_status, f"Wrong status for {tokens}"
            print(f"  ✓ {tokens:,} tokens → {expected_status}")

    def _print_summary(self):
        """Print test summary"""
        total = self.passed + self.failed

        print()
        print("=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)
        print(f"Total tests: {total}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"Success rate: {(self.passed/total*100):.1f}%")
        print("=" * 70)

        if self.failed == 0:
            print("🎉 All tests passed!")
        else:
            print("⚠️  Some tests failed. Please review.")


def run_demo_scenario():
    """Run a complete demo scenario simulating real usage"""
    print("\n\n")
    print("=" * 70)
    print("🎬 DEMO SCENARIO: Simulating Phase 1 Work with Context Reset")
    print("=" * 70)
    print()

    memory = get_memory_handler()
    thinking = get_thinking_integration("demo-session")
    context_manager = get_context_manager()

    # Simulate Phase 1 work
    print("📍 Phase 1: Setting up infrastructure")
    thinking.update_context(phase="Phase 1: Infrastructure")

    # Simulate thinking process
    thoughts = [
        "Need to create project structure with .claude/ and .ontology/ directories",
        "Should define 5 sub-agents: Mathematical Content, Knowledge Graph, Documentation, Validation, Feedback",
        "Must integrate memory system with sequential thinking",
        "Context editing needs to be configured for Sonnet 4.5",
        "Everything should be backed up to memory for context recovery"
    ]

    print("\n🧠 Thinking process:")
    for i, thought in enumerate(thoughts, 1):
        print(f"   {i}. {thought[:60]}...")
        think_and_remember(thought, i, len(thoughts))

    # Simulate decisions
    print("\n📋 Recording decisions:")
    thinking.record_decision(
        decision="Use XML format for thinking logs",
        rationale="Structured, human-readable, and easy to parse",
        alternatives=["JSON format", "Plain text"]
    )
    print("   ✓ Decision recorded")

    # Simulate progress
    print("\n⚡ Recording progress:")
    tasks = [
        "Create directory structure",
        "Implement memory handler",
        "Integrate sequential thinking",
        "Configure context editing"
    ]

    for task in tasks:
        thinking.record_progress(task, "completed", f"Successfully completed {task}")
        print(f"   ✓ {task}")

    # Create checkpoint
    print("\n💾 Creating checkpoint...")
    checkpoint_result = thinking.create_recovery_checkpoint(
        checkpoint_name="phase1-infrastructure-complete",
        state={
            "phase": "Phase 1: Infrastructure",
            "completed_tasks": tasks,
            "next_tasks": ["Define sub-agents", "Setup Obsidian vault"],
            "decisions": ["Use XML for logs", "Enable context editing"],
            "token_usage": 45000
        }
    )

    if checkpoint_result['status'] == 'success':
        print("   ✅ Checkpoint created successfully")

    # Simulate context warning
    print("\n⚠️  Simulating context warning at 140K tokens...")
    context_manager.create_pre_compact_checkpoint(
        current_state={
            "phase": "Phase 1: Infrastructure",
            "completed_tasks": tasks,
            "token_count": 140000
        },
        tool_results_to_preserve=[]
    )
    print("   💾 Emergency checkpoint created")

    # Simulate context reset
    print("\n♻️  Simulating context reset (context editing triggered)...")
    print("   🔄 Context compacted, old tool results cleared")

    # Simulate recovery
    print("\n📥 Recovering from memory...")
    recovered_state = context_manager.recover_from_compact()

    if recovered_state:
        print("   ✅ State recovered successfully!")
        print(f"   📍 Phase: {recovered_state.get('current_state', {}).get('phase')}")
        print(f"   ✅ Completed: {len(recovered_state.get('current_state', {}).get('completed_tasks', []))} tasks")
        print(f"   🎯 Continuing seamlessly...")
    else:
        print("   ❌ Recovery failed")

    print("\n" + "=" * 70)
    print("🎉 Demo completed! Memory system works across context resets.")
    print("=" * 70)


if __name__ == "__main__":
    # Run tests
    test_suite = TestMemorySystem()
    test_suite.run_all_tests()

    # Run demo scenario
    run_demo_scenario()

    print("\n\n✨ All tests and demos completed!")
