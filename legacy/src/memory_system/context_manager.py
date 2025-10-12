#!/usr/bin/env python3
"""
Context Manager for Sonnet 4.5
Handles Context Editing and Enhanced Stop Reasons
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum

from .memory_handler import get_memory_handler
from .thinking_memory_integration import get_thinking_integration


class StopReason(Enum):
    """Enhanced Stop Reasons for Sonnet 4.5"""
    END_TURN = "end_turn"              # Natural completion
    MAX_TOKENS = "max_tokens"          # Reached max_tokens limit
    STOP_SEQUENCE = "stop_sequence"    # Hit a stop sequence
    TOOL_USE = "tool_use"              # Stopped to use a tool
    CONTENT_FILTERED = "content_filtered"  # Content policy violation


class ContextManager:
    """
    Manages context editing and stop reasons for Sonnet 4.5
    Ensures seamless recovery after context compacting
    """

    def __init__(self):
        self.memory = get_memory_handler()
        self.thinking = get_thinking_integration()
        self.token_warning_threshold = 140000
        self.token_edit_threshold = 150000
        self.keep_recent_tool_uses = 5

    def check_token_usage(self, current_tokens: int) -> Dict[str, Any]:
        """
        Check current token usage and trigger appropriate actions

        Args:
            current_tokens: Current conversation token count

        Returns:
            Action recommendation dictionary
        """
        if current_tokens >= self.token_edit_threshold:
            return {
                "status": "critical",
                "action": "save_and_compact",
                "message": f"Token limit reached ({current_tokens}/{self.token_edit_threshold})",
                "immediate": True
            }
        elif current_tokens >= self.token_warning_threshold:
            return {
                "status": "warning",
                "action": "checkpoint",
                "message": f"Approaching token limit ({current_tokens}/{self.token_edit_threshold})",
                "immediate": False
            }
        else:
            return {
                "status": "ok",
                "action": "continue",
                "tokens_remaining": self.token_edit_threshold - current_tokens
            }

    def create_pre_compact_checkpoint(
        self,
        current_state: Dict[str, Any],
        tool_results_to_preserve: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create comprehensive checkpoint before context compacting

        Args:
            current_state: Current work state
            tool_results_to_preserve: Important tool results to save

        Returns:
            Status dictionary
        """
        timestamp = datetime.now()

        # 1. Save thinking log summary
        thinking_summary = self.thinking.generate_summary()

        # 2. Extract key information from tool results
        preserved_tools = []
        for tool_result in tool_results_to_preserve[-self.keep_recent_tool_uses:]:
            preserved_tools.append({
                "tool": tool_result.get('tool_name'),
                "timestamp": tool_result.get('timestamp'),
                "summary": tool_result.get('summary', '')[:500],  # First 500 chars
                "key_data": tool_result.get('important_data', {})
            })

        # 3. Create comprehensive checkpoint
        checkpoint = {
            "checkpoint_name": f"pre-compact-{timestamp.strftime('%Y%m%d-%H%M%S')}",
            "timestamp": timestamp.isoformat(),
            "trigger": "context_editing",
            "current_state": current_state,
            "thinking_summary": thinking_summary,
            "preserved_tool_results": preserved_tools,
            "recovery_instructions": self._generate_recovery_instructions(current_state)
        }

        # 4. Save to memory
        checkpoint_path = f"phase-progress/pre-compact-{timestamp.strftime('%Y%m%d-%H%M%S')}.json"
        result = self.memory.create(
            checkpoint_path,
            json.dumps(checkpoint, indent=2, ensure_ascii=False)
        )

        # 5. Update current state pointer
        if result['status'] == 'success':
            self.memory.create(
                "phase-progress/current-state.json",
                json.dumps(checkpoint, indent=2, ensure_ascii=False)
            )

        return result

    def recover_from_compact(self) -> Optional[Dict[str, Any]]:
        """
        Recover state after context compacting

        Returns:
            Recovered state dictionary or None
        """
        # Try to load latest checkpoint
        result = self.memory.view("phase-progress/current-state.json")

        if result['status'] != 'success':
            return None

        try:
            checkpoint = json.loads(result['content'])

            # Log recovery
            self.memory.create(
                f"phase-progress/recovery-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log",
                f"Recovered from: {checkpoint['checkpoint_name']}\n"
                f"Original timestamp: {checkpoint['timestamp']}\n"
                f"Recovery timestamp: {datetime.now().isoformat()}\n"
            )

            return checkpoint

        except json.JSONDecodeError:
            return None

    def handle_stop_reason(
        self,
        stop_reason: str,
        stop_sequence: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle enhanced stop reasons from Sonnet 4.5

        Args:
            stop_reason: The stop reason from API response
            stop_sequence: The actual stop sequence if applicable
            context: Additional context about the stop

        Returns:
            Handling instructions dictionary
        """
        try:
            reason_enum = StopReason(stop_reason)
        except ValueError:
            reason_enum = StopReason.END_TURN

        handlers = {
            StopReason.END_TURN: self._handle_end_turn,
            StopReason.MAX_TOKENS: self._handle_max_tokens,
            StopReason.STOP_SEQUENCE: self._handle_stop_sequence,
            StopReason.TOOL_USE: self._handle_tool_use,
            StopReason.CONTENT_FILTERED: self._handle_content_filtered
        }

        handler = handlers.get(reason_enum, self._handle_unknown)
        return handler(stop_sequence, context)

    def _handle_end_turn(self, stop_sequence: Optional[str], context: Optional[Dict]) -> Dict[str, Any]:
        """Handle natural completion"""
        return {
            "status": "completed",
            "action": "continue_if_needed",
            "message": "Task completed naturally",
            "create_checkpoint": True
        }

    def _handle_max_tokens(self, stop_sequence: Optional[str], context: Optional[Dict]) -> Dict[str, Any]:
        """Handle max tokens reached"""
        return {
            "status": "truncated",
            "action": "save_and_continue",
            "message": "Response truncated due to max_tokens limit",
            "create_checkpoint": True,
            "continue_in_next_turn": True
        }

    def _handle_stop_sequence(self, stop_sequence: Optional[str], context: Optional[Dict]) -> Dict[str, Any]:
        """Handle stop sequence hit"""
        return {
            "status": "stopped",
            "action": "checkpoint",
            "message": f"Hit stop sequence: {stop_sequence}",
            "stop_sequence": stop_sequence,
            "create_checkpoint": True
        }

    def _handle_tool_use(self, stop_sequence: Optional[str], context: Optional[Dict]) -> Dict[str, Any]:
        """Handle tool use stop"""
        return {
            "status": "tool_pending",
            "action": "execute_tool",
            "message": "Stopped to execute tool",
            "create_checkpoint": False
        }

    def _handle_content_filtered(self, stop_sequence: Optional[str], context: Optional[Dict]) -> Dict[str, Any]:
        """Handle content policy violation"""
        return {
            "status": "filtered",
            "action": "review_and_modify",
            "message": "Content filtered due to policy violation",
            "create_checkpoint": False,
            "requires_user_review": True
        }

    def _handle_unknown(self, stop_sequence: Optional[str], context: Optional[Dict]) -> Dict[str, Any]:
        """Handle unknown stop reason"""
        return {
            "status": "unknown",
            "action": "checkpoint_and_alert",
            "message": f"Unknown stop reason",
            "create_checkpoint": True
        }

    def _generate_recovery_instructions(self, state: Dict[str, Any]) -> str:
        """Generate human-readable recovery instructions"""
        phase = state.get('phase', 'Unknown')
        next_tasks = state.get('next_tasks', [])

        instructions = f"""
RECOVERY INSTRUCTIONS:
=====================

Phase: {phase}

Next Tasks:
"""
        for i, task in enumerate(next_tasks[:5], 1):
            instructions += f"{i}. {task}\n"

        instructions += f"""
To Resume:
1. Check this checkpoint data
2. Review thinking_summary for context
3. Load preserved_tool_results if needed
4. Continue with next_tasks

Memory locations:
- Thinking logs: .claude/memories/thinking-logs/
- Phase progress: .claude/memories/phase-progress/
- Ontology changes: .claude/memories/ontology-evolution/
"""
        return instructions

    def get_context_editing_config(self) -> Dict[str, Any]:
        """
        Get context editing configuration for API

        Returns:
            Configuration dictionary for Anthropic API
        """
        return {
            "betas": ["context-management-2025-06-27"],
            "context_management": {
                "edits": [
                    {
                        "type": "clear_tool_uses_20250919",
                        "trigger": {
                            "type": "input_tokens",
                            "value": self.token_edit_threshold
                        },
                        "keep": {
                            "type": "tool_uses",
                            "value": self.keep_recent_tool_uses
                        },
                        "exclude_tools": ["memory"]
                    }
                ]
            }
        }


# Global instance
_context_manager = None


def get_context_manager() -> ContextManager:
    """Get or create global context manager instance"""
    global _context_manager
    if _context_manager is None:
        _context_manager = ContextManager()
    return _context_manager


if __name__ == "__main__":
    # Test the context manager
    manager = get_context_manager()

    # Test token checking
    print("Testing token usage checks:\n")

    for tokens in [50000, 140000, 150000]:
        result = manager.check_token_usage(tokens)
        print(f"Tokens: {tokens:,}")
        print(f"Status: {result['status']}")
        print(f"Action: {result['action']}")
        print(f"Message: {result['message']}")
        print()

    # Test stop reason handling
    print("\nTesting stop reason handling:\n")

    stop_reasons = [
        ("end_turn", None),
        ("max_tokens", None),
        ("stop_sequence", "STOP"),
        ("tool_use", None)
    ]

    for reason, sequence in stop_reasons:
        result = manager.handle_stop_reason(reason, sequence)
        print(f"Stop Reason: {reason}")
        print(f"Status: {result['status']}")
        print(f"Action: {result['action']}")
        print(f"Message: {result['message']}")
        print()

    # Test context editing config
    print("\nContext Editing Configuration:")
    print(json.dumps(manager.get_context_editing_config(), indent=2))
