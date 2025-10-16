#!/usr/bin/env python3
"""
Observability Event Sender - Hook Utility

Sends Claude Code hook events to observability server.
Based on: disler/claude-code-hooks-multi-agent-observability

USAGE: Called by other hook scripts
  echo '{"event_type":"PreToolUse", ...}' | python3 send_event.py

VERSION: 1.0.0
DATE: 2025-10-16
"""

import json
import sys
import os

def send_event(event_data: dict) -> bool:
    """
    Send event to observability server.
    
    Fire-and-forget - failures are logged but don't block execution.
    
    Args:
        event_data: Event payload with hook-specific fields
    
    Returns:
        True if sent successfully, False otherwise
    """
    try:
        import httpx
        
        # Get server URL from environment or use default
        server_url = os.getenv("OBS_EVENTS_URL", "http://localhost:4000/events")
        
        # Extract session info from stdin data
        session_id = event_data.get('session_id', 'unknown')
        hook_type = event_data.get('hook_event_name', 'Unknown')
        
        # Build payload matching disler schema
        payload = {
            "source_app": "math-system",
            "session_id": session_id,
            "hook_event_type": hook_type,
            "payload": event_data
        }
        
        # Send with timeout (non-blocking)
        with httpx.Client(timeout=1.0) as client:
            response = client.post(server_url, json=payload)
            
            if 200 <= response.status_code < 300:
                print(f"✓ Event sent: {hook_type}", file=sys.stderr)
                return True
            else:
                print(f"⚠ Event send failed: HTTP {response.status_code}", file=sys.stderr)
                return False
                
    except ImportError:
        print("⚠ httpx not available - install with: pip install httpx", file=sys.stderr)
        return False
        
    except Exception as e:
        print(f"⚠ Event send error: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    # Read event data from stdin
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Send event (fire-and-forget)
    send_event(input_data)
    
    # Always exit successfully - don't block on observability failures
    sys.exit(0)

