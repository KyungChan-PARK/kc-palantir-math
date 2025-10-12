#!/usr/bin/env python3
"""
Anthropic API Wrapper with Context Editing and Enhanced Stop Reasons
Fully integrated with memory system for Sonnet 4.5
"""

import os
from typing import Dict, Any, List, Optional, Iterator
from anthropic import Anthropic, AnthropicBedrock, AnthropicVertex
from anthropic.types import Message, MessageStreamEvent

from .context_manager import get_context_manager
from .thinking_memory_integration import get_thinking_integration


class PalantirAPIWrapper:
    """
    Wrapper around Anthropic API with full Sonnet 4.5 features:
    - Context Editing
    - Enhanced Stop Reasons
    - Memory Tool integration
    - Automatic checkpoint management
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-5-20250929",
        use_bedrock: bool = False,
        use_vertex: bool = False
    ):
        """
        Initialize API wrapper

        Args:
            api_key: Anthropic API key (reads from ANTHROPIC_API_KEY env if not provided)
            model: Model identifier
            use_bedrock: Use AWS Bedrock instead of direct API
            use_vertex: Use Google Vertex AI instead of direct API
        """
        # Initialize client
        if use_bedrock:
            self.client = AnthropicBedrock()
        elif use_vertex:
            self.client = AnthropicVertex()
        else:
            self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

        self.model = model
        self.context_manager = get_context_manager()
        self.thinking_integration = get_thinking_integration()

        # Token tracking
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def create_message(
        self,
        messages: List[Dict[str, Any]],
        max_tokens: int = 4096,
        system: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        enable_context_editing: bool = True,
        enable_memory_tool: bool = True,
        **kwargs
    ) -> Message:
        """
        Create a message with full Sonnet 4.5 features

        Args:
            messages: Conversation messages
            max_tokens: Maximum tokens to generate
            system: System prompt
            tools: Tool definitions
            enable_context_editing: Enable automatic context editing
            enable_memory_tool: Add memory tool automatically
            **kwargs: Additional arguments to pass to API

        Returns:
            Message response
        """
        # Check token usage before making request
        token_check = self.context_manager.check_token_usage(self.total_input_tokens)

        if token_check['status'] == 'critical':
            print(f"⚠️  {token_check['message']}")
            print("💾 Creating checkpoint before proceeding...")

            # Create checkpoint
            self._create_emergency_checkpoint(messages)

        elif token_check['status'] == 'warning':
            print(f"⚡ {token_check['message']}")

        # Prepare tools
        if tools is None:
            tools = []

        # Add memory tool if enabled
        if enable_memory_tool:
            memory_tool = {
                "type": "memory_20250818",
                "name": "memory"
            }
            if memory_tool not in tools:
                tools.append(memory_tool)

        # Prepare request parameters
        request_params = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "tools": tools if tools else None,
            **kwargs
        }

        if system:
            request_params["system"] = system

        # Add context editing configuration
        if enable_context_editing:
            context_config = self.context_manager.get_context_editing_config()
            request_params["betas"] = context_config["betas"]
            request_params["context_management"] = context_config["context_management"]

        # Make API request
        response = self.client.beta.messages.create(**request_params) if enable_context_editing else self.client.messages.create(**request_params)

        # Update token tracking
        self.total_input_tokens += response.usage.input_tokens
        self.total_output_tokens += response.usage.output_tokens

        # Handle stop reason
        self._handle_stop_reason(response)

        return response

    def create_message_stream(
        self,
        messages: List[Dict[str, Any]],
        max_tokens: int = 4096,
        system: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        enable_context_editing: bool = True,
        enable_memory_tool: bool = True,
        **kwargs
    ) -> Iterator[MessageStreamEvent]:
        """
        Create a streaming message with full Sonnet 4.5 features

        Args:
            messages: Conversation messages
            max_tokens: Maximum tokens to generate
            system: System prompt
            tools: Tool definitions
            enable_context_editing: Enable automatic context editing
            enable_memory_tool: Add memory tool automatically
            **kwargs: Additional arguments to pass to API

        Yields:
            Stream events
        """
        # Prepare tools
        if tools is None:
            tools = []

        # Add memory tool if enabled
        if enable_memory_tool:
            memory_tool = {
                "type": "memory_20250818",
                "name": "memory"
            }
            if memory_tool not in tools:
                tools.append(memory_tool)

        # Prepare request parameters
        request_params = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "tools": tools if tools else None,
            **kwargs
        }

        if system:
            request_params["system"] = system

        # Add context editing configuration
        if enable_context_editing:
            context_config = self.context_manager.get_context_editing_config()
            request_params["betas"] = context_config["betas"]
            request_params["context_management"] = context_config["context_management"]

        # Make streaming API request
        with self.client.beta.messages.stream(**request_params) if enable_context_editing else self.client.messages.stream(**request_params) as stream:
            for event in stream:
                yield event

            # Get final message
            final_message = stream.get_final_message()

            # Update token tracking
            self.total_input_tokens += final_message.usage.input_tokens
            self.total_output_tokens += final_message.usage.output_tokens

            # Handle stop reason
            self._handle_stop_reason(final_message)

    def _handle_stop_reason(self, response: Message) -> None:
        """Handle enhanced stop reasons from response"""
        stop_reason = response.stop_reason

        # Get stop sequence if present
        stop_sequence = getattr(response, 'stop_sequence', None)

        # Handle through context manager
        result = self.context_manager.handle_stop_reason(
            stop_reason,
            stop_sequence=stop_sequence
        )

        # Create checkpoint if needed
        if result.get('create_checkpoint'):
            print(f"📌 Stop reason: {stop_reason} - Creating checkpoint...")
            self._create_checkpoint(f"stop-{stop_reason}")

        # Alert user if needed
        if result.get('requires_user_review'):
            print(f"⚠️  {result['message']} - User review required")

        # Handle continuation
        if result.get('continue_in_next_turn'):
            print(f"➡️  {result['message']} - Continuing in next turn...")

    def _create_checkpoint(self, reason: str) -> None:
        """Create a checkpoint"""
        from datetime import datetime

        checkpoint_data = {
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens
        }

        self.thinking_integration.create_recovery_checkpoint(
            checkpoint_name=f"{reason}-{datetime.now().strftime('%H%M%S')}",
            state=checkpoint_data
        )

    def _create_emergency_checkpoint(self, messages: List[Dict[str, Any]]) -> None:
        """Create emergency checkpoint before token limit"""
        from datetime import datetime

        # Extract last few messages as context
        recent_context = messages[-3:] if len(messages) >= 3 else messages

        checkpoint_data = {
            "reason": "emergency_token_limit",
            "timestamp": datetime.now().isoformat(),
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
            "recent_context": recent_context
        }

        self.context_manager.create_pre_compact_checkpoint(
            current_state=checkpoint_data,
            tool_results_to_preserve=[]
        )

    def get_token_usage(self) -> Dict[str, int]:
        """Get current token usage"""
        return {
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "remaining_before_warning": max(0, 140000 - self.total_input_tokens),
            "remaining_before_edit": max(0, 150000 - self.total_input_tokens)
        }

    def reset_token_tracking(self) -> None:
        """Reset token tracking (call after context edit)"""
        print(f"♻️  Context edited. Token tracking reset.")
        print(f"📊 Previous session: {self.total_input_tokens:,} input + {self.total_output_tokens:,} output")

        self.total_input_tokens = 0
        self.total_output_tokens = 0


def create_palantir_client(
    model: str = "claude-sonnet-4-5-20250929",
    **kwargs
) -> PalantirAPIWrapper:
    """
    Factory function to create Palantir API wrapper

    Args:
        model: Model identifier
        **kwargs: Additional arguments for PalantirAPIWrapper

    Returns:
        Configured API wrapper instance
    """
    return PalantirAPIWrapper(model=model, **kwargs)


if __name__ == "__main__":
    # Test the API wrapper
    print("Testing Palantir API Wrapper\n")

    # Create client
    client = create_palantir_client()

    # Simple test message
    messages = [
        {
            "role": "user",
            "content": "Explain the Fubini theorem in one sentence."
        }
    ]

    print("Sending test message...")

    try:
        response = client.create_message(
            messages=messages,
            max_tokens=1024,
            enable_context_editing=True,
            enable_memory_tool=True
        )

        print(f"\n✅ Response received")
        print(f"📊 Stop reason: {response.stop_reason}")
        print(f"💬 Content: {response.content[0].text[:200]}...")

        # Check token usage
        usage = client.get_token_usage()
        print(f"\n📈 Token Usage:")
        print(f"   Input: {usage['input_tokens']:,}")
        print(f"   Output: {usage['output_tokens']:,}")
        print(f"   Total: {usage['total_tokens']:,}")
        print(f"   Remaining: {usage['remaining_before_warning']:,}")

    except Exception as e:
        print(f"❌ Error: {e}")
