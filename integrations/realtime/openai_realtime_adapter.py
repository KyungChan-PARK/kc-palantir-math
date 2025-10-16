"""
OpenAI Realtime Adapter (skeleton)

Purpose:
- Provide a small integration surface to connect to OpenAI Realtime via
  WebSocket/WebRTC-esque client libraries (no external deps here).
- Keep responsibilities narrow: session lifecycle, event routing hooks, and
  tool-call bridging to our agent system.

NOTE: This is a skeletal adapter intended to define boundaries and integration
points. The concrete Realtime connection (auth, WS connection, media streams)
should be implemented in a higher layer or injected client.

References:
- OpenAI Realtime guide: https://platform.openai.com/docs/guides/realtime

Design:
- RealtimeSessionManager: owns session state and inbound/outbound event hooks
- ToolBridge: maps realtime function-calls to local Python callables

This file has no side effects and can be imported without network calls.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional


ToolFunc = Callable[[Dict[str, Any]], Dict[str, Any]]


@dataclass
class RealtimeConfig:
    """Configuration for a realtime session (auth and routing are external)."""

    model: str = "gpt-realtime-preview-2025-XX-XX"  # placeholder
    # Endpoint, auth, etc. provided by caller via injected client


class ToolBridge:
    """Registers and invokes local tools for model function-calls."""

    def __init__(self):
        self._tools: Dict[str, ToolFunc] = {}

    def register(self, name: str, func: ToolFunc) -> None:
        if not name or not callable(func):
            raise ValueError("Tool name and callable function are required")
        self._tools[name] = func

    def call(self, name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' is not registered")
        return self._tools[name](args or {})


class RealtimeSessionManager:
    """Thin session wrapper with event hooks.

    The actual network client (WebSocket/WebRTC) must be injected via `send`
    and `on_event` call sites.
    """

    def __init__(self, config: Optional[RealtimeConfig] = None):
        self.config = config or RealtimeConfig()
        self.tools = ToolBridge()
        self._on_event: Optional[Callable[[Dict[str, Any]], None]] = None

    def on_event(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Register a callback for inbound realtime events (delta, tool_call)."""
        self._on_event = handler

    # ------------------------------ Outbound API -----------------------------

    def send_user_text(self, text: str) -> Dict[str, Any]:
        """Prepare a model input payload for user text (caller sends over WS)."""
        return {
            "type": "input_text",
            "text": text,
            "model": self.config.model,
        }

    def send_user_audio(self, audio_bytes: bytes, mime: str = "audio/pcm") -> Dict[str, Any]:
        """Prepare a model input payload for user audio (stream chunks)."""
        return {
            "type": "input_audio",
            "mime": mime,
            "data": audio_bytes,  # caller handles base64 encoding if needed
            "model": self.config.model,
        }

    # ------------------------------ Inbound API ------------------------------

    def handle_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Route inbound realtime events. Returns tool result if applicable.

        Expected event forms (simplified):
        - {"type": "delta", "content": "partial text"}
        - {"type": "tool_call", "name": str, "arguments": {...}}
        - {"type": "final", "content": "full text"}
        """
        etype = event.get("type")
        if etype == "tool_call":
            name = event.get("name")
            args = event.get("arguments", {})
            result = self.tools.call(name, args)
            return {
                "type": "tool_result",
                "name": name,
                "result": result,
            }

        # Bubble other events to registered listener
        if self._on_event:
            self._on_event(event)
        return None


