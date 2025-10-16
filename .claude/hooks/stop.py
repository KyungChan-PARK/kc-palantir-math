#!/usr/bin/env python3
"""
Stop Hook - Auto-Improvement Trigger

Executes when Claude finishes responding to:
1. Check performance metrics
2. Trigger improvement cycle if needed
3. Send observability event

Based on: learning_hooks.py lines 23-77
Pattern: Stop hook can block stoppage and force continuation

VERSION: 1.0.0
DATE: 2025-10-16
"""

import json
import sys
import subprocess
from pathlib import Path


def analyze_session_performance(transcript_path: str) -> tuple[float, dict]:
    """
    Parse session transcript for performance metrics.
    
    Returns: (success_rate, metrics)
    """
    if not transcript_path or not Path(transcript_path).exists():
        return 1.0, {}
    
    try:
        with open(transcript_path, 'r') as f:
            transcript = f.read()
        
        # Count errors and successes
        error_count = transcript.count('"is_error": true')
        success_count = transcript.count('"type": "result"') - error_count
        total = error_count + success_count
        
        if total == 0:
            return 1.0, {}
        
        success_rate = success_count / total
        
        metrics = {
            'success_count': success_count,
            'error_count': error_count,
            'total_turns': total,
            'success_rate': success_rate
        }
        
        return success_rate, metrics
        
    except Exception as e:
        print(f"⚠ Failed to parse transcript: {e}", file=sys.stderr)
        return 1.0, {}


def main():
    """Main hook execution"""
    # Read input from stdin
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError as e:
        print(f'{{"error": "Invalid JSON: {e}"}}')
        sys.exit(1)
    
    transcript_path = input_data.get('transcript_path', '')
    stop_hook_active = input_data.get('stop_hook_active', False)
    
    # Send observability event (fire-and-forget)
    subprocess.Popen(
        ['python3', '.claude/hooks/send_event.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ).communicate(json.dumps(input_data).encode())
    
    # Prevent infinite loops
    if stop_hook_active:
        print(json.dumps({}))
        sys.exit(0)
    
    # Analyze performance
    success_rate, metrics = analyze_session_performance(transcript_path)
    
    # Trigger improvement if performance is poor
    if success_rate < 0.70 and metrics.get('total_turns', 0) > 3:
        output = {
            "decision": "block",
            "reason": (
                f"⚠️ PERFORMANCE THRESHOLD VIOLATED:\n\n"
                f"Success rate: {success_rate:.0%} (< 70%)\n"
                f"Errors: {metrics.get('error_count', 0)}\n"
                f"Total turns: {metrics.get('total_turns', 0)}\n\n"
                f"Initiating self-improvement cycle.\n"
                f"Run: Task(agent='self-improver', prompt='Analyze session performance')"
            )
        }
        print(json.dumps(output))
        sys.exit(0)
    
    # Normal completion - allow stop
    print(json.dumps({}))
    sys.exit(0)


if __name__ == "__main__":
    main()

