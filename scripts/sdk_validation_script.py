#!/usr/bin/env python3
"""
SDK Parameter Validation Script
Phase 0: Verify actual SDK parameters before implementation

PURPOSE: Prevent TypeErrors by checking actual SDK signatures
DATE: 2025-10-16
"""

import inspect
import sys


def validate_agent_definition():
    """Verify AgentDefinition available parameters"""
    try:
        from claude_agent_sdk import AgentDefinition
        
        sig = inspect.signature(AgentDefinition.__init__)
        params = list(sig.parameters.keys())
        
        print("=" * 70)
        print("AgentDefinition.__init__ Parameters:")
        print("=" * 70)
        for param in params:
            print(f"  ✓ {param}")
        
        # Check for commonly assumed but invalid parameters
        invalid_assumptions = {
            'thinking': 'Extended Thinking config (low-level SDK only)',
            'cache_control': 'Prompt caching (low-level SDK only)',
            'system': 'Use "prompt" field instead',
        }
        
        print("\n" + "=" * 70)
        print("Common Invalid Assumptions:")
        print("=" * 70)
        for param, note in invalid_assumptions.items():
            status = "❌ INVALID" if param not in params else "✓ VALID"
            print(f"  {status}: {param} - {note}")
        
        return params
        
    except ImportError as e:
        print(f"❌ Failed to import AgentDefinition: {e}")
        return None


def validate_options():
    """Verify ClaudeAgentOptions available parameters"""
    try:
        from claude_agent_sdk import ClaudeAgentOptions
        
        sig = inspect.signature(ClaudeAgentOptions.__init__)
        params = list(sig.parameters.keys())
        
        print("\n" + "=" * 70)
        print("ClaudeAgentOptions.__init__ Parameters:")
        print("=" * 70)
        for param in params:
            print(f"  ✓ {param}")
        
        # Critical parameters for our use case
        critical = ['system_prompt', 'hooks', 'agents', 'mcp_servers', 'setting_sources']
        
        print("\n" + "=" * 70)
        print("Critical Parameters for Runtime Integration:")
        print("=" * 70)
        for param in critical:
            status = "✓ AVAILABLE" if param in params else "❌ MISSING"
            print(f"  {status}: {param}")
        
        return params
        
    except ImportError as e:
        print(f"❌ Failed to import ClaudeAgentOptions: {e}")
        return None


def validate_client_methods():
    """Verify ClaudeSDKClient available methods"""
    try:
        from claude_agent_sdk import ClaudeSDKClient
        
        methods = [m for m in dir(ClaudeSDKClient) if not m.startswith('_')]
        
        print("\n" + "=" * 70)
        print("ClaudeSDKClient Available Methods:")
        print("=" * 70)
        for method in sorted(methods):
            print(f"  ✓ {method}")
        
        # Check for commonly assumed but invalid methods
        invalid_methods = ['stream_response', 'stream', 'send']
        
        print("\n" + "=" * 70)
        print("Invalid Method Assumptions:")
        print("=" * 70)
        for method in invalid_methods:
            status = "❌ DOES NOT EXIST" if method not in methods else "✓ EXISTS"
            print(f"  {status}: {method}()")
        
        return methods
        
    except ImportError as e:
        print(f"❌ Failed to import ClaudeSDKClient: {e}")
        return None


def test_hook_execution():
    """Test hook script execution pattern"""
    import subprocess
    import json
    import tempfile
    from pathlib import Path
    
    print("\n" + "=" * 70)
    print("Hook Execution Test:")
    print("=" * 70)
    
    # Create minimal test hook
    test_hook = """#!/usr/bin/env python3
import json
import sys

# Read stdin
data = json.loads(sys.stdin.read())
print(f"Received: {data.get('tool_name', 'unknown')}", file=sys.stderr)

# Return success
print(json.dumps({"decision": "allow"}))
sys.exit(0)
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_hook)
        hook_path = f.name
    
    try:
        # Test execution
        test_input = json.dumps({"tool_name": "Read", "tool_input": {}})
        result = subprocess.run(
            ["python3", hook_path],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        print(f"  Exit code: {result.returncode}")
        print(f"  Stdout: {result.stdout}")
        print(f"  Stderr: {result.stderr}")
        
        if result.returncode == 0:
            print("  ✓ Hook execution successful")
        else:
            print("  ❌ Hook execution failed")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"  ❌ Hook test failed: {e}")
        return False
    finally:
        Path(hook_path).unlink(missing_ok=True)


def main():
    """Run all validations"""
    print("╔" + "=" * 68 + "╗")
    print("║" + " SDK VALIDATION - PHASE 0".center(68) + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    results = {
        'agent_definition': validate_agent_definition(),
        'agent_options': validate_options(),
        'client_methods': validate_client_methods(),
        'hook_execution': test_hook_execution(),
    }
    
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY:")
    print("=" * 70)
    
    all_passed = all(results.values())
    
    if all_passed:
        print("✅ ALL VALIDATIONS PASSED - Safe to proceed with implementation")
        return 0
    else:
        print("❌ SOME VALIDATIONS FAILED - Review issues before proceeding")
        for key, value in results.items():
            status = "✓" if value else "✗"
            print(f"  {status} {key}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

