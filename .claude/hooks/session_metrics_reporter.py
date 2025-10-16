#!/usr/bin/env python3
"""
Stop Hook: Session Metrics Reporter

Aggregates session metrics and triggers self-improvement if needed:
1. Calculate success rate
2. Analyze performance patterns
3. Trigger self-improvement if success_rate < 70%
4. Save session summary
"""

import json
import sys
from pathlib import Path

def main():
    try:
        # Read hook input from stdin
        event = json.load(sys.stdin)
        
        session_id = event.get('session_id', 'unknown')
        
        # Read learning log
        log_file = Path('/home/kc-palantir/math/.claude/dynamic_learning.jsonl')
        
        if not log_file.exists():
            # No learning data yet
            sys.exit(0)
        
        # Analyze session metrics
        events = []
        with open(log_file, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        events.append(json.loads(line))
                    except:
                        pass
        
        # Filter to current session
        session_events = [e for e in events if e.get('session_id') == session_id]
        
        if not session_events:
            sys.exit(0)
        
        # Calculate metrics
        subagent_events = [e for e in session_events if e.get('event_type') == 'subagent_execution']
        
        if subagent_events:
            total_executions = len(subagent_events)
            successful_executions = len([e for e in subagent_events if e.get('success', False)])
            success_rate = successful_executions / total_executions if total_executions > 0 else 1.0
            avg_duration = sum(e.get('duration_ms', 0) for e in subagent_events) / total_executions
            
            # Create session summary
            summary = {
                "session_id": session_id,
                "total_executions": total_executions,
                "successful_executions": successful_executions,
                "success_rate": success_rate,
                "avg_duration_ms": avg_duration,
                "needs_improvement": success_rate < 0.7
            }
            
            # Save summary
            summary_file = Path(f'/home/kc-palantir/math/.claude/session_summaries/{session_id}.json')
            summary_file.parent.mkdir(parents=True, exist_ok=True)
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2)
            
            # Print summary (visible in transcript mode with Ctrl+R)
            print(f"Session Summary: {successful_executions}/{total_executions} successful ({success_rate:.1%})")
            
            # Trigger self-improvement if needed
            if success_rate < 0.7:
                output = {
                    "decision": "block",
                    "reason": f"Success rate ({success_rate:.1%}) below threshold. Triggering self-improvement analysis. Please review session metrics and consider agent improvements."
                }
                print(json.dumps(output))
                sys.exit(0)
        
        # Allow normal stop
        sys.exit(0)
        
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Non-blocking error
        print(f"WARNING: Metrics reporting failed: {e}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()

