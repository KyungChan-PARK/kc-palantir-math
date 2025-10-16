"""
Observability Hook - Event Sender

Sends workflow events to observability server for real-time monitoring.

VERSION: 2.0.0 - Human-Readable Session IDs
DATE: 2025-10-16
"""

import requests
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

OBSERVABILITY_URL = "http://localhost:4000/events"
SESSION_ID = str(uuid.uuid4())  # Generated per workflow run
SESSION_NAME = None  # Human-readable session name
SESSION_CONTEXT = {}  # Additional session context


def send_hook_event(
    source_app: str,
    hook_event_type: str,
    payload: Dict[str, Any]
) -> bool:
    """
    Send hook event to observability server.
    
    Args:
        source_app: Workflow type (e.g., "math_scaffolding", "ocr_extraction")
        hook_event_type: Event type (e.g., "ocr_started", "scaffolding_completed")
        payload: Event data
        
    Returns:
        bool: True if event sent successfully, False otherwise
    """
    try:
        # Prepare event payload with session context
        event_payload = {
            "source_app": source_app,
            "session_id": SESSION_ID,
            "hook_event_type": hook_event_type,
            "payload": {
                **payload,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # Add session metadata if available
        if SESSION_NAME:
            event_payload["session_name"] = SESSION_NAME
        if SESSION_CONTEXT:
            event_payload["session_context"] = SESSION_CONTEXT
        
        response = requests.post(
            OBSERVABILITY_URL,
            json=event_payload,
            timeout=1
        )
        
        if response.status_code == 200:
            logger.debug(f"[Observability] Sent {hook_event_type} from {source_app}")
            return True
        else:
            logger.warning(f"[Observability] Failed to send event: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        # Observability server not running - don't fail workflow
        logger.debug(f"[Observability] Server not available (this is OK)")
        return False
    except Exception as e:
        # Don't fail workflow if observability is down
        logger.debug(f"[Observability] Failed to send event: {e}")
        return False


def get_session_id() -> str:
    """Get the current workflow session ID."""
    return SESSION_ID


def get_session_name() -> Optional[str]:
    """Get the human-readable session name."""
    return SESSION_NAME


def set_session_context(
    problem_preview: Optional[str] = None,
    workflow_type: Optional[str] = None,
    **kwargs
) -> None:
    """
    Set human-readable session context.
    
    Args:
        problem_preview: Short preview of the problem (e.g., "Quadratic Equation")
        workflow_type: Type of workflow (e.g., "Math Scaffolding")
        **kwargs: Additional context fields
    """
    global SESSION_NAME, SESSION_CONTEXT
    
    # Generate human-readable session name
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if problem_preview:
        # Format: "Quadratic Equation - 14:32:15"
        SESSION_NAME = f"{problem_preview} - {timestamp}"
    elif workflow_type:
        # Format: "Math Scaffolding - 14:32:15"
        SESSION_NAME = f"{workflow_type} - {timestamp}"
    else:
        # Format: "Session - 14:32:15"
        SESSION_NAME = f"Session - {timestamp}"
    
    # Store additional context
    SESSION_CONTEXT = {
        "problem_preview": problem_preview,
        "workflow_type": workflow_type,
        "timestamp": timestamp,
        **kwargs
    }
    
    logger.info(f"[Observability] Session context set: {SESSION_NAME}")


def reset_session_id(
    problem_preview: Optional[str] = None,
    workflow_type: Optional[str] = None,
    **kwargs
) -> str:
    """
    Generate a new session ID for a new workflow run.
    
    Args:
        problem_preview: Short preview of the problem
        workflow_type: Type of workflow
        **kwargs: Additional context
        
    Returns:
        str: New session ID
    """
    global SESSION_ID, SESSION_NAME, SESSION_CONTEXT
    SESSION_ID = str(uuid.uuid4())
    
    # Set session context if provided
    if problem_preview or workflow_type or kwargs:
        set_session_context(problem_preview, workflow_type, **kwargs)
    else:
        SESSION_NAME = None
        SESSION_CONTEXT = {}
    
    return SESSION_ID

