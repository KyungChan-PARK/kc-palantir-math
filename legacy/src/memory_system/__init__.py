"""
Memory System for Palantir Math Education Project

Provides persistent memory across Claude sessions with automatic
integration with sequential-thinking MCP tool.

Includes Context Editing and Enhanced Stop Reasons handling for Sonnet 4.5.
"""

from .memory_handler import MemoryHandler, get_memory_handler
from .thinking_memory_integration import (
    ThinkingMemoryIntegration,
    get_thinking_integration,
    think_and_remember
)
from .context_manager import (
    ContextManager,
    get_context_manager,
    StopReason
)

__all__ = [
    'MemoryHandler',
    'get_memory_handler',
    'ThinkingMemoryIntegration',
    'get_thinking_integration',
    'think_and_remember',
    'ContextManager',
    'get_context_manager',
    'StopReason'
]

__version__ = '1.0.0'
