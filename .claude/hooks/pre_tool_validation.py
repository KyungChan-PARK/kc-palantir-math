#!/usr/bin/env python3
"""
PreToolUse Hook: Semantic Tier Guard & Validation

Validates:
1. Semantic tier immutability (only self-improver can modify)
2. Tier boundary compliance
3. Dangerous command blocking
4. Tool-agent alignment
"""

import json
import sys
import re

# Dangerous command patterns
DANGEROUS_PATTERNS = [
    r'\brm\s+-rf\s+/',
    r'\bsudo\s+rm',
    r'\bdd\s+if=',
    r'\bmkfs\.',
    r'\b>\s*/dev/sd[a-z]',
]

def main():
    try:
        # Read hook input from stdin
        event = json.load(sys.stdin)
        
        tool_name = event.get('tool_name', '')
        tool_input = event.get('tool_input', {})
        
        # 1. Semantic tier immutability validation
        if tool_name == 'Edit':
            file_path = tool_input.get('file_path', '')
            old_string = tool_input.get('old_string', '')
            
            # Protect semantic layer from unauthorized modifications
            if 'semantic_layer.py' in file_path:
                if 'SemanticRole' in old_string or 'SemanticResponsibility' in old_string:
                    # Only self-improver can modify semantic enums
                    output = {
                        "hookSpecificOutput": {
                            "hookEventName": "PreToolUse",
                            "permissionDecision": "ask",
                            "permissionDecisionReason": "Modifying Semantic Tier enum - requires approval. Only self-improver should modify semantic definitions."
                        }
                    }
                    print(json.dumps(output))
                    sys.exit(0)
        
        # 2. Tier boundary validation
        if tool_name == 'Task':
            subagent = tool_input.get('subagent_type', '')
            prompt = tool_input.get('prompt', '').lower()
            
            # Semantic agents should not handle runtime operations
            if 'semantic-manager' in subagent and 'execute' in prompt:
                print("ERROR: Semantic tier cannot perform runtime execution. Use kinetic-execution-agent instead.", file=sys.stderr)
                sys.exit(2)  # Block execution
        
        # 3. Dangerous command blocking
        if tool_name == 'Bash':
            command = tool_input.get('command', '')
            
            for pattern in DANGEROUS_PATTERNS:
                if re.search(pattern, command):
                    output = {
                        "hookSpecificOutput": {
                            "hookEventName": "PreToolUse",
                            "permissionDecision": "deny",
                            "permissionDecisionReason": f"Dangerous command blocked: {pattern}"
                        }
                    }
                    print(json.dumps(output))
                    sys.exit(0)
        
        # 4. Tool-agent alignment check (lightweight)
        # Could expand to check if agent has permission for specific tool
        
        # Allow execution
        sys.exit(0)
        
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Hook execution failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

