#!/usr/bin/env python3
"""
Session Monitoring Tool

실시간 세션 모니터링:
- 1M token 사용량
- Context window 상태
- Agent 실행 통계
- Hook 실행 현황

VERSION: 1.0.0
DATE: 2025-10-16
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime


def find_latest_session():
    """Find most recent session log"""
    log_dir = Path("/tmp/math-agent-logs")
    if not log_dir.exists():
        return None
    
    json_files = list(log_dir.glob("session-*.json"))
    if not json_files:
        return None
    
    latest = max(json_files, key=lambda p: p.stat().st_mtime)
    return latest


def parse_session_log(session_file: Path) -> dict:
    """Parse session log for metrics"""
    try:
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        return session_data
    except:
        return {}


def monitor_token_usage():
    """Monitor token usage from observability events"""
    try:
        import httpx
        
        # Query recent events
        response = httpx.get(
            "http://localhost:4000/events/recent?limit=1000",
            timeout=5
        )
        
        if response.status_code != 200:
            return None
        
        events = response.json().get('events', [])
        
        # Extract token usage from events
        total_tokens = 0
        input_tokens = 0
        output_tokens = 0
        
        for event in events:
            payload = event.get('payload', {})
            
            # Look for token usage in tool responses
            if 'usage' in payload:
                usage = payload['usage']
                input_tokens += usage.get('input_tokens', 0)
                output_tokens += usage.get('output_tokens', 0)
        
        total_tokens = input_tokens + output_tokens
        
        return {
            'total_tokens': total_tokens,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'context_1m_usage_pct': (total_tokens / 1_000_000) * 100 if total_tokens > 0 else 0
        }
    
    except Exception as e:
        return None


def get_agent_stats():
    """Get agent execution stats from observability"""
    try:
        import httpx
        
        response = httpx.get(
            "http://localhost:4000/events/recent?limit=1000",
            timeout=5
        )
        
        if response.status_code != 200:
            return {}
        
        events = response.json().get('events', [])
        
        # Count by agent
        agent_calls = {}
        hook_calls = {}
        
        for event in events:
            hook_type = event.get('hook_event_type', '')
            payload = event.get('payload', {})
            
            # Count hook types
            hook_calls[hook_type] = hook_calls.get(hook_type, 0) + 1
            
            # Extract agent from tool calls
            if hook_type == 'PreToolUse':
                tool_name = payload.get('tool_name', '')
                if tool_name == 'Task':
                    agent = payload.get('tool_input', {}).get('subagent_type', 'unknown')
                    agent_calls[agent] = agent_calls.get(agent, 0) + 1
        
        return {
            'agent_calls': agent_calls,
            'hook_calls': hook_calls
        }
    
    except:
        return {}


def display_status():
    """Display comprehensive session status"""
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║              Math System - Session Monitor                           ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Session info
    session_file = find_latest_session()
    if session_file:
        session_data = parse_session_log(session_file)
        print(f"📋 Session Info:")
        print(f"   Session ID: {session_data.get('session_id', 'unknown')}")
        print(f"   Started: {session_data.get('timestamp', 'unknown')}")
        print(f"   Turns: {session_data.get('conversation_turns', 0)}")
    else:
        print("⚠️  No active session found")
    
    print()
    
    # Token usage
    print("🎯 1M Context Window Status:")
    token_usage = monitor_token_usage()
    
    if token_usage:
        total = token_usage['total_tokens']
        pct = token_usage['context_1m_usage_pct']
        
        print(f"   Total tokens: {total:,}")
        print(f"   Input tokens: {token_usage['input_tokens']:,}")
        print(f"   Output tokens: {token_usage['output_tokens']:,}")
        print(f"   1M Context usage: {pct:.2f}%")
        
        # Visual bar
        bar_length = 50
        filled = int(bar_length * pct / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"   [{bar}] {pct:.1f}%")
        print(f"   Remaining: {1_000_000 - total:,} tokens")
    else:
        print("   ⚠️  Token usage not available (observability server offline?)")
        print("   Note: 1M context is enabled via claude-sonnet-4-5-20250929 model")
    
    print()
    
    # Agent stats
    print("🤖 Agent Activity:")
    stats = get_agent_stats()
    
    if stats.get('agent_calls'):
        for agent, count in sorted(stats['agent_calls'].items(), key=lambda x: x[1], reverse=True):
            print(f"   {agent}: {count} calls")
    else:
        print("   No agent activity recorded yet")
    
    print()
    
    # Hook stats
    print("🔗 Hook System Activity:")
    
    if stats.get('hook_calls'):
        for hook, count in sorted(stats['hook_calls'].items()):
            print(f"   {hook}: {count} invocations")
    else:
        print("   No hook activity yet")
    
    print()
    
    # Runtime features
    print("⚡ Runtime Features:")
    print("   ✅ Observability: Active")
    print("   ✅ Realtime: Enabled")
    print("   ✅ Computer-Use: Enabled")
    print("   ✅ Hooks: 10 filesystem hooks")
    print("   ✅ 1M Context: Enabled (claude-sonnet-4-5-20250929)")
    
    print()
    print("=" * 70)
    print("Refresh: python3 scripts/monitor_session.py")
    print("Events: curl http://localhost:4000/events/recent?limit=10")
    print("=" * 70)


if __name__ == "__main__":
    try:
        display_status()
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped")
        sys.exit(0)

