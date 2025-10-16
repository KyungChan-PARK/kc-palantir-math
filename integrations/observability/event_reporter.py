"""
Observability Event Reporter

Lightweight client to send Claude Code-style hook events to an external
observability server (e.g., disler/claude-code-hooks-multi-agent-observability).

This module intentionally has no extra dependencies beyond `httpx` which is
already part of this project. It provides a small, typed surface for posting
events and convenience helpers for common hook types.

References:
- Repo: https://github.com/disler/claude-code-hooks-multi-agent-observability
- Server endpoint (default): POST http://localhost:4000/events

Usage:
    reporter = EventReporter(source_app="math-system")
    reporter.session_start(session_id="sess-123", payload={"user": "kc"})
    reporter.pre_tool_use("sess-123", tool_name="Read", tool_input={"path": "README.md"})
    reporter.post_tool_use("sess-123", tool_name="Read", result={"bytes": 3245})
    reporter.session_end("sess-123", reason="completed")

Schema (aligned with the GitHub repo):
{
  "source_app": "str",
  "session_id": "str",
  "hook_event_type": "PreToolUse|PostToolUse|Notification|Stop|SubagentStop|PreCompact|UserPromptSubmit|SessionStart|SessionEnd",
  "payload": {"any": "json"}
}
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional
import os

import httpx


class HookEventType(str, Enum):
    """Supported hook event types (kept in sync with the observability server)."""

    PRE_TOOL_USE = "PreToolUse"
    POST_TOOL_USE = "PostToolUse"
    NOTIFICATION = "Notification"
    STOP = "Stop"
    SUBAGENT_STOP = "SubagentStop"
    PRE_COMPACT = "PreCompact"
    USER_PROMPT_SUBMIT = "UserPromptSubmit"
    SESSION_START = "SessionStart"
    SESSION_END = "SessionEnd"


@dataclass
class ObservabilityEvent:
    """Event payload envelope sent to the observability server."""

    source_app: str
    session_id: str
    hook_event_type: HookEventType
    payload: Dict[str, Any]


class EventReporter:
    """HTTP client for posting observability events.

    The server base URL can be configured via the OBS_EVENTS_URL environment
    variable. Defaults to http://localhost:4000/events
    """

    def __init__(
        self,
        source_app: str,
        base_url: Optional[str] = None,
        timeout_s: float = 5.0
    ):
        self.source_app = source_app
        self.base_url = base_url or os.getenv("OBS_EVENTS_URL", "http://localhost:4000/events")
        self.timeout_s = timeout_s

    def _post(self, event: ObservabilityEvent) -> bool:
        """Post event to the server. Returns True on 2xx, False otherwise."""
        try:
            with httpx.Client(timeout=self.timeout_s) as client:
                resp = client.post(self.base_url, json={
                    "source_app": event.source_app,
                    "session_id": event.session_id,
                    "hook_event_type": event.hook_event_type.value,
                    "payload": event.payload,
                })
                return 200 <= resp.status_code < 300
        except Exception:
            return False

    # -------------------------- Convenience helpers -------------------------

    def send(self, session_id: str, event_type: HookEventType, payload: Dict[str, Any]) -> bool:
        return self._post(ObservabilityEvent(
            source_app=self.source_app,
            session_id=session_id,
            hook_event_type=event_type,
            payload=payload,
        ))

    def session_start(self, session_id: str, payload: Optional[Dict[str, Any]] = None) -> bool:
        return self.send(session_id, HookEventType.SESSION_START, payload or {})

    def session_end(self, session_id: str, reason: str, payload: Optional[Dict[str, Any]] = None) -> bool:
        data = {"reason": reason}
        if payload:
            data.update(payload)
        return self.send(session_id, HookEventType.SESSION_END, data)

    def pre_tool_use(self, session_id: str, tool_name: str, tool_input: Optional[Dict[str, Any]] = None) -> bool:
        return self.send(session_id, HookEventType.PRE_TOOL_USE, {
            "tool_name": tool_name,
            "tool_input": tool_input or {},
        })

    def post_tool_use(self, session_id: str, tool_name: str, result: Optional[Dict[str, Any]] = None, success: Optional[bool] = None) -> bool:
        payload: Dict[str, Any] = {"tool_name": tool_name}
        if result is not None:
            payload["result"] = result
        if success is not None:
            payload["success"] = success
        return self.send(session_id, HookEventType.POST_TOOL_USE, payload)

    def notification(self, session_id: str, message: str, level: str = "info", extra: Optional[Dict[str, Any]] = None) -> bool:
        payload = {"message": message, "level": level}
        if extra:
            payload.update(extra)
        return self.send(session_id, HookEventType.NOTIFICATION, payload)

    def stop(self, session_id: str, summary: str, chat_transcript: Optional[str] = None) -> bool:
        payload: Dict[str, Any] = {"summary": summary}
        if chat_transcript:
            payload["chat_transcript"] = chat_transcript
        return self.send(session_id, HookEventType.STOP, payload)

    def subagent_stop(self, session_id: str, agent_name: str, details: Optional[Dict[str, Any]] = None) -> bool:
        payload = {"agent_name": agent_name}
        if details:
            payload.update(details)
        return self.send(session_id, HookEventType.SUBAGENT_STOP, payload)

    def pre_compact(self, session_id: str, strategy: str, stats: Optional[Dict[str, Any]] = None) -> bool:
        payload = {"strategy": strategy}
        if stats:
            payload.update(stats)
        return self.send(session_id, HookEventType.PRE_COMPACT, payload)

    def user_prompt_submit(self, session_id: str, prompt_preview: str, length: Optional[int] = None) -> bool:
        payload: Dict[str, Any] = {"prompt": prompt_preview}
        if length is not None:
            payload["length"] = length
        return self.send(session_id, HookEventType.USER_PROMPT_SUBMIT, payload)


