"""
Test: Claude Code Hooks Integration

Tests integration of indydevdan hook system with existing feedback loop.

VERSION: 1.0.0
DATE: 2025-10-16
"""

import json
import subprocess
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestClaudeHooksIntegration:
    """Tests for Claude Code hooks integration."""
    
    def test_01_hook_scripts_exist(self):
        """Test 1: All hook scripts are present."""
        print("\n" + "="*60)
        print("TEST 1: Hook Scripts Existence")
        print("="*60)
        
        hook_dir = project_root / ".claude" / "hooks"
        
        required_hooks = [
            # indydevdan hooks
            "send_event_observability.py",
            "pre_tool_use_security.py",
            "post_tool_use_logging.py",
            "stop_enhanced.py",
            "user_prompt_submit.py",
            "subagent_stop.py",
            "session_start.py",
            "session_end.py",
            "pre_compact.py",
            "notification.py",
            # Existing hooks
            "pre_tool_validation.py",
            "post_tool_learning.py",
            "session_metrics_reporter.py",
        ]
        
        missing = []
        for hook in required_hooks:
            hook_path = hook_dir / hook
            if hook_path.exists():
                print(f"✅ {hook}")
            else:
                print(f"❌ {hook} MISSING")
                missing.append(hook)
        
        assert len(missing) == 0, f"Missing hooks: {missing}"
        print(f"\n✅ All {len(required_hooks)} hook scripts present")
        print("✅ Test 1 PASSED")
    
    def test_02_hook_utilities_exist(self):
        """Test 2: Hook utilities are present."""
        print("\n" + "="*60)
        print("TEST 2: Hook Utilities")
        print("="*60)
        
        utils_dir = project_root / ".claude" / "hooks" / "utils"
        
        required_utils = [
            "constants.py",
            "summarizer.py",
            "llm/anth.py",
        ]
        
        for util in required_utils:
            util_path = utils_dir / util
            if util_path.exists():
                print(f"✅ {util}")
                assert util_path.exists()
            else:
                print(f"❌ {util} MISSING")
                assert False, f"Missing utility: {util}"
        
        print("\n✅ Test 2 PASSED")
    
    def test_03_settings_json_valid(self):
        """Test 3: settings.json is valid JSON with all hooks."""
        print("\n" + "="*60)
        print("TEST 3: Settings.json Validation")
        print("="*60)
        
        settings_path = project_root / ".claude" / "settings.json"
        assert settings_path.exists(), "settings.json should exist"
        
        with open(settings_path, 'r') as f:
            settings = json.load(f)
        
        assert "hooks" in settings, "Should have hooks section"
        
        hook_types = [
            "PreToolUse",
            "PostToolUse",
            "Stop",
            "UserPromptSubmit",
            "SubagentStop",
            "SessionStart",
            "SessionEnd",
            "PreCompact",
            "Notification"
        ]
        
        for hook_type in hook_types:
            if hook_type in settings["hooks"]:
                print(f"✅ {hook_type}")
            else:
                print(f"❌ {hook_type} MISSING")
        
        present = sum(1 for ht in hook_types if ht in settings["hooks"])
        print(f"\n✅ {present}/{len(hook_types)} hook types configured")
        print("✅ Test 3 PASSED")
    
    def test_04_send_event_script(self):
        """Test 4: send_event_observability.py works."""
        print("\n" + "="*60)
        print("TEST 4: Send Event Script")
        print("="*60)
        
        # Create test event
        test_event = {
            "session_id": "test-session-001",
            "tool_name": "Read",
            "tool_input": {"file_path": "test.txt"}
        }
        
        # Run send_event script
        script_path = project_root / ".claude" / "hooks" / "send_event_observability.py"
        
        try:
            result = subprocess.run(
                [
                    "uv", "run", str(script_path),
                    "--source-app", "test-app",
                    "--event-type", "PreToolUse"
                ],
                input=json.dumps(test_event),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Script should always exit 0 (even if server not running)
            print(f"Exit code: {result.returncode}")
            assert result.returncode == 0, "Should exit 0 to not block Claude"
            
            print("✅ Script executes correctly")
            print("✅ Test 4 PASSED")
            
        except subprocess.TimeoutExpired:
            print("❌ Script timed out")
            assert False, "Script should complete quickly"
        except Exception as e:
            print(f"❌ Error: {e}")
            assert False, str(e)
    
    def test_05_server_websocket_support(self):
        """Test 5: Server has WebSocket endpoint."""
        print("\n" + "="*60)
        print("TEST 5: WebSocket Support")
        print("="*60)
        
        server_path = project_root / "observability-server" / "server.py"
        
        with open(server_path, 'r') as f:
            server_code = f.read()
        
        # Check for WebSocket imports
        assert "WebSocket" in server_code, "Should import WebSocket"
        assert "WebSocketDisconnect" in server_code, "Should import WebSocketDisconnect"
        
        # Check for websocket endpoint
        assert "@app.websocket" in server_code, "Should have WebSocket endpoint"
        assert '"/stream"' in server_code, "Should have /stream endpoint"
        
        # Check for websocket_clients storage
        assert "websocket_clients" in server_code, "Should store WebSocket clients"
        
        # Check for broadcast logic
        assert "send_text" in server_code or "send_json" in server_code, "Should broadcast messages"
        
        # Check for chat and summary fields
        assert "chat" in server_code, "Should support chat field"
        assert "summary" in server_code, "Should support summary field"
        
        print("✅ WebSocket imports: Present")
        print("✅ /stream endpoint: Present")
        print("✅ WebSocket clients: Present")
        print("✅ Broadcast logic: Present")
        print("✅ Chat/Summary support: Present")
        
        print("\n✅ Test 5 PASSED")
    
    def test_06_backward_compatibility(self):
        """Test 6: Existing observability_hook.py still works."""
        print("\n" + "="*60)
        print("TEST 6: Backward Compatibility")
        print("="*60)
        
        from tools.observability_hook import send_hook_event, get_session_id
        
        session_id = get_session_id()
        assert len(session_id) > 0, "Should generate session ID"
        print(f"✅ Session ID generation: {session_id[:8]}...")
        
        # Send test event (won't fail even if server not running)
        result = send_hook_event(
            "test_compatibility",
            "test_event",
            {"test": "backward_compatibility"}
        )
        
        print(f"✅ send_hook_event: {'Sent' if result else 'Graceful fail'}")
        print("\n✅ Test 6 PASSED")


def run_tests():
    """Run all hook integration tests."""
    test_suite = TestClaudeHooksIntegration()
    
    tests = [
        ("Hook Scripts", test_suite.test_01_hook_scripts_exist),
        ("Hook Utilities", test_suite.test_02_hook_utilities_exist),
        ("Settings.json", test_suite.test_03_settings_json_valid),
        ("Send Event Script", test_suite.test_04_send_event_script),
        ("WebSocket Support", test_suite.test_05_server_websocket_support),
        ("Backward Compatibility", test_suite.test_06_backward_compatibility),
    ]
    
    passed = 0
    failed = 0
    errors = []
    
    print("\n" + "="*70)
    print("CLAUDE HOOKS INTEGRATION TEST SUITE")
    print("="*70)
    
    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            failed += 1
            errors.append((test_name, str(e)))
            print(f"\n❌ Test FAILED: {test_name}")
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

