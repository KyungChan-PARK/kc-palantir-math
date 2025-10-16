#!/usr/bin/env python3
"""
PostToolUse Hook - Quality Checks and Observability

Executes after every tool call to:
1. Validate output quality
2. Check for errors
3. Send observability event

Based on: claude-code-2-0-deduplicated-final.md lines 14661-14695
Pattern: PostToolUse can provide feedback to Claude

VERSION: 1.0.0
DATE: 2025-10-16
"""

import json
import sys
import subprocess


def check_output_quality(tool_name: str, tool_response: dict) -> tuple[bool, list[str]]:
    """
    Check tool output quality.
    
    Returns: (passed, issues)
    """
    issues = []
    
    # Check Write operations
    if tool_name == 'Write':
        bytes_written = tool_response.get('bytes_written', 0)
        if bytes_written < 10:
            issues.append('File appears empty (< 10 bytes)')
    
    # Check Edit operations
    if tool_name == 'Edit':
        replacements = tool_response.get('replacements', 0)
        if replacements == 0:
            issues.append('No replacements made - old_string not found?')
    
    # Check Task (subagent) results
    if tool_name == 'Task':
        result = tool_response.get('result', '')
        if not result or len(result) < 20:
            issues.append('Subagent returned minimal/empty result')
    
    return len(issues) == 0, issues


def main():
    """Main hook execution"""
    # Read input from stdin
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError as e:
        print(f'{{"error": "Invalid JSON: {e}"}}')
        sys.exit(1)
    
    tool_name = input_data.get('tool_name', '')
    tool_response = input_data.get('tool_response', {})
    
    # Send observability event (fire-and-forget)
    subprocess.Popen(
        ['python3', '.claude/hooks/send_event.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ).communicate(json.dumps(input_data).encode())
    
    # Quality checks
    passed, issues = check_output_quality(tool_name, tool_response)
    
    if not passed:
        # Provide feedback to Claude
        output = {
            "decision": "block",
            "reason": "⚠️ Quality issues detected:\n" + "\n".join(f"- {issue}" for issue in issues),
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": f"Tool {tool_name} produced unexpected output"
            }
        }
        print(json.dumps(output))
        sys.exit(0)
    
    # All checks passed
    print(json.dumps({}))
    sys.exit(0)


if __name__ == "__main__":
    main()

