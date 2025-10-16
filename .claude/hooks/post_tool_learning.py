#!/usr/bin/env python3
"""
PostToolUse Hook: Dynamic Learning Collector

Collects execution metrics for Dynamic Tier learning:
1. Tool usage patterns
2. Execution duration
3. Success/failure rates
4. Agent performance metrics

Feeds data to DynamicTier for adaptation and optimization.
"""

import json
import sys
import time
from pathlib import Path

def main():
    try:
        # Read hook input from stdin
        event = json.load(sys.stdin)
        
        tool_name = event.get('tool_name', '')
        tool_input = event.get('tool_input', {})
        tool_response = event.get('tool_response', {})
        session_id = event.get('session_id', 'unknown')
        
        # Create learning log file
        log_file = Path('/home/kc-palantir/math/.claude/dynamic_learning.jsonl')
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Collect metrics for Dynamic Tier
        if tool_name == 'Task':
            # Subagent execution metrics
            subagent = tool_input.get('subagent_type', 'unknown')
            result = tool_response.get('result', '')
            duration_ms = tool_response.get('duration_ms', 0)
            success = 'error' not in result.lower() and 'failed' not in result.lower()
            
            learning_event = {
                "timestamp": time.time(),
                "session_id": session_id,
                "event_type": "subagent_execution",
                "subagent": subagent,
                "duration_ms": duration_ms,
                "success": success,
                "tokens_used": tool_response.get('usage', {}).get('output_tokens', 0),
                "cost_usd": tool_response.get('total_cost_usd', 0)
            }
            
            # Append to learning log
            with open(log_file, 'a') as f:
                f.write(json.dumps(learning_event) + '\n')
        
        elif tool_name in ['Edit', 'Write']:
            # File operation metrics
            file_path = tool_input.get('file_path', '')
            success = tool_response.get('success', True)
            
            learning_event = {
                "timestamp": time.time(),
                "session_id": session_id,
                "event_type": "file_operation",
                "tool": tool_name,
                "file_path": file_path,
                "success": success
            }
            
            with open(log_file, 'a') as f:
                f.write(json.dumps(learning_event) + '\n')
        
        # Allow continuation
        sys.exit(0)
        
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Non-blocking error - log but allow continuation
        print(f"WARNING: Learning collection failed: {e}", file=sys.stderr)
        sys.exit(0)  # Don't block workflow

if __name__ == "__main__":
    main()

