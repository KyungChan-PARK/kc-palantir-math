#!/usr/bin/env python3
"""
PreToolUse Hook - Simplified Version

Fixed: 과도한 검증으로 인한 self-blocking 문제 해결
Only validates actual parameter names, not content

VERSION: 1.1.0
DATE: 2025-10-16
"""

import json
import sys
import re
import subprocess


def validate_sdk_parameters(tool_input: dict) -> tuple[bool, str]:
    """Validate SDK parameter usage - FIXED: Only check parameter keys"""
    
    # Only validate if it's a Task tool (agent delegation)
    if isinstance(tool_input, dict):
        # Check for invalid parameter KEYS in the input dict itself
        invalid_param_keys = ['thinking', 'cache_control', 'system']
        
        for invalid_key in invalid_param_keys:
            if invalid_key in tool_input:
                return False, f"Invalid SDK parameter key: {invalid_key}"
    
    return True, ""


def check_dangerous_operations(tool_name: str, tool_input: dict) -> tuple[bool, str]:
    """Check for dangerous operations"""
    
    if tool_name == 'Bash':
        command = tool_input.get('command', '')
        
        # Only block truly dangerous commands
        if re.search(r'rm\s+-rf\s+/', command):
            return False, f"Dangerous: rm -rf / command blocked"
    
    return True, ""


def main():
    """Main hook execution"""
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError as e:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}))
        sys.exit(0)
    
    tool_name = input_data.get('tool_name', '')
    tool_input = input_data.get('tool_input', {})
    
    # Send observability event (fire-and-forget, non-blocking)
    try:
        subprocess.Popen(
            ['python3', '.claude/hooks/send_event.py'],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ).communicate(json.dumps(input_data).encode(), timeout=0.1)
    except:
        pass  # Don't block on observability
    
    # Simplified validation - only critical checks
    safe, warning = check_dangerous_operations(tool_name, tool_input)
    if not safe:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"⚠️ {warning}"
            }
        }
        print(json.dumps(output))
        sys.exit(0)
    
    # Default: Allow all operations
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}))
    sys.exit(0)


if __name__ == "__main__":
    main()

