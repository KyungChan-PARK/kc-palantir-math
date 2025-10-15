#!/usr/bin/env python3
"""
Terminal Test Script for Hook Integration

Run this in WSL terminal to test hooks are working correctly.

Usage:
    python3 test_hooks_terminal.py
"""

import asyncio
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))


async def test_hook_import():
    """Test 1: Verify hooks can be imported."""
    print("="*80)
    print("TEST 1: Hook Import Verification")
    print("="*80)
    
    try:
        from hooks import (
            validate_sdk_parameters,
            check_agent_exists,
            auto_quality_check_after_write,
            auto_trigger_improvement,
            detect_ambiguity_before_execution,
        )
        print("✅ All hooks imported successfully\n")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}\n")
        return False


async def test_hook_execution():
    """Test 2: Verify hooks can execute."""
    print("="*80)
    print("TEST 2: Hook Execution Test")
    print("="*80)
    
    try:
        from hooks.validation_hooks import validate_sdk_parameters
        
        # Create test input
        test_input = {
            'tool_name': 'Task',
            'tool_input': {
                'subagent_type': 'test-agent',
                'prompt': 'Test with thinking parameter'  # Should trigger warning
            }
        }
        
        class MockContext:
            signal = None
        
        # Execute hook
        result = await validate_sdk_parameters(test_input, None, MockContext())
        
        if result:
            print("✅ Hook executed successfully")
            print(f"   Result type: {type(result)}")
            print(f"   Contains hookSpecificOutput: {'hookSpecificOutput' in result}")
            if 'hookSpecificOutput' in result:
                print(f"   Permission decision: {result['hookSpecificOutput'].get('permissionDecision')}")
        else:
            print("✅ Hook executed (no validation issues)")
        
        print()
        return True
        
    except Exception as e:
        print(f"❌ Hook execution failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


async def test_agent_integration():
    """Test 3: Verify agents have hook support."""
    print("="*80)
    print("TEST 3: Agent Integration Test")
    print("="*80)
    
    try:
        from agents.meta_orchestrator import meta_orchestrator, HOOKS_AVAILABLE
        from agents.socratic_requirements_agent import socratic_requirements_agent
        
        print(f"Meta-Orchestrator:")
        print(f"  ✅ Loaded successfully")
        print(f"  ✅ HOOKS_AVAILABLE = {HOOKS_AVAILABLE}")
        print(f"  ✅ Description: {meta_orchestrator.description[:80]}...")
        
        print(f"\nSocratic Requirements Agent:")
        print(f"  ✅ Loaded successfully")
        print(f"  ✅ Description: {socratic_requirements_agent.description[:80]}...")
        
        print()
        return True
        
    except Exception as e:
        print(f"❌ Agent integration test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


async def test_hook_integrator():
    """Test 4: Verify hook integrator utilities."""
    print("="*80)
    print("TEST 4: Hook Integrator Test")
    print("="*80)
    
    try:
        from hooks.hook_integrator import (
            get_default_meta_orchestrator_hooks,
            get_default_socratic_agent_hooks
        )
        
        meta_hooks = get_default_meta_orchestrator_hooks()
        socratic_hooks = get_default_socratic_agent_hooks()
        
        print(f"Meta-Orchestrator Hooks:")
        for event_type, matchers in meta_hooks.items():
            print(f"  ✅ {event_type}: {len(matchers)} matcher(s)")
        
        print(f"\nSocratic Agent Hooks:")
        for event_type, matchers in socratic_hooks.items():
            print(f"  ✅ {event_type}: {len(matchers)} matcher(s)")
        
        print()
        return True
        
    except Exception as e:
        print(f"❌ Hook integrator test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests."""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*20 + "HOOK INTEGRATION TERMINAL TEST" + " "*28 + "║")
    print("╚" + "="*78 + "╝\n")
    
    tests = [
        ("Import Verification", test_hook_import),
        ("Hook Execution", test_hook_execution),
        ("Agent Integration", test_agent_integration),
        ("Hook Integrator", test_hook_integrator),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}\n")
            results.append((test_name, False))
    
    # Summary
    print("="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n" + "🎉 " * 20)
        print("ALL TESTS PASSED - HOOKS ARE READY FOR USE!")
        print("🎉 " * 20)
        
        print("\n" + "="*80)
        print("QUICK START GUIDE")
        print("="*80)
        print("""
To use hooks in your terminal:

1. Start Python REPL:
   $ python3

2. Run this code:
   >>> import asyncio
   >>> from hooks.hook_integrator import get_default_meta_orchestrator_hooks
   >>> hooks = get_default_meta_orchestrator_hooks()
   >>> print(f"Hooks loaded: {list(hooks.keys())}")

3. With Claude Agent SDK:
   >>> from claude_agent_sdk import query, ClaudeAgentOptions
   >>> options = ClaudeAgentOptions(hooks=hooks)
   >>> # Now your queries will have automatic validation!

See HOOK-INTEGRATION-GUIDE.md for full examples.
""")
    else:
        print("\n⚠️ Some tests failed. Review errors above.")
    
    return passed == total


if __name__ == '__main__':
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

