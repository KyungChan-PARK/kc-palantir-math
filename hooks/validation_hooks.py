"""
Validation Hooks for Meta-Orchestrator

Based on: claude-code-2-0-deduplicated-final.md
Patterns: PreToolUse validation prevents execution of invalid tool calls

VERSION: 1.0.0
DATE: 2025-10-15
"""

from typing import Any, Dict
import inspect
import re


class HookContext:
    """Hook context placeholder (matches claude_agent_sdk.HookContext)"""
    def __init__(self):
        self.signal = None


async def validate_sdk_parameters(
    input_data: Dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> Dict[str, Any]:
    """
    PreToolUse hook: Validate SDK parameters BEFORE Task execution.
    
    Prevents TypeErrors from invalid AgentDefinition parameters.
    
    Based on: claude-code-2-0-deduplicated-final.md lines 9541-9574
    Pattern: Hook-based validation prevents execution of invalid tool calls
    
    Real-world learning:
    - Prevented: "thinking parameter doesn't exist in AgentDefinition" 
    - Prevented: "stream_response() method doesn't exist in ClaudeSDKClient"
    - Saved: 90 minutes of rework from 2 TypeErrors
    """
    if input_data.get('tool_name') != 'Task':
        return {}
    
    task_input = input_data.get('tool_input', {})
    agent_name = task_input.get('subagent_type', '')
    prompt = task_input.get('prompt', '')
    
    # Validation 1: Check for invalid AgentDefinition parameters
    invalid_params = {
        'thinking': 'Agent SDK does not support thinking parameter. Use Extended Thinking via model config instead.',
        'cache_control': 'Agent SDK does not support cache_control. This is a low-level Anthropic SDK feature.',
        'system': 'Agent SDK uses "prompt" not "system". Use prompt field for system instructions.',
    }
    
    for param, message in invalid_params.items():
        if param in prompt.lower():
            return {
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'permissionDecision': 'ask',
                    'permissionDecisionReason': f'⚠️ SDK Compatibility Issue: {message}'
                }
            }
    
    # Validation 2: Check for non-existent methods
    invalid_methods = {
        'stream_response': 'ClaudeSDKClient has receive_response(), not stream_response()',
        'stream(': 'ClaudeSDKClient does not have stream(). Use query() or receive_response()',
    }
    
    for method, message in invalid_methods.items():
        if method in prompt:
            return {
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'permissionDecision': 'deny',
                    'permissionDecisionReason': f'❌ Invalid Method: {message}'
                }
            }
    
    return {}  # All validations passed


async def check_agent_exists(
    input_data: Dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> Dict[str, Any]:
    """
    PreToolUse hook: Verify agent exists before delegation.
    
    Prevents: "Agent X not found" errors
    """
    if input_data.get('tool_name') != 'Task':
        return {}
    
    task_input = input_data.get('tool_input', {})
    agent_name = task_input.get('subagent_type', '')
    
    # Import agent registry (would be from actual config)
    try:
        from agents import AGENT_REGISTRY
        
        if agent_name not in AGENT_REGISTRY:
            available = ', '.join(AGENT_REGISTRY.keys())
            return {
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'permissionDecision': 'deny',
                    'permissionDecisionReason': (
                        f'❌ Agent "{agent_name}" not found.\n'
                        f'Available agents: {available}'
                    )
                }
            }
    except ImportError:
        # Registry not available, skip validation
        pass
    
    return {}


async def verify_parallel_execution_possible(
    input_data: Dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> Dict[str, Any]:
    """
    PreToolUse hook: Check if task can be parallelized.
    
    Based on: claude-code-2-0-deduplicated-final.md
    Pattern: "Maximize use of parallel tool calls where possible"
    
    Provides guidance to agent on parallelization opportunities.
    """
    if input_data.get('tool_name') != 'Task':
        return {}
    
    task_input = input_data.get('tool_input', {})
    prompt = task_input.get('prompt', '')
    
    # Detect sequential patterns that could be parallelized
    sequential_indicators = [
        r'then\s+read',
        r'after\s+that',
        r'next\s+read',
        r'wait.*then',
    ]
    
    has_sequential = any(
        re.search(pattern, prompt, re.IGNORECASE)
        for pattern in sequential_indicators
    )
    
    if has_sequential:
        # Suggest parallelization
        return {
            'hookSpecificOutput': {
                'hookEventName': 'PreToolUse',
                'additionalContext': (
                    '💡 PARALLELIZATION OPPORTUNITY DETECTED:\n'
                    'Consider executing independent tasks in parallel for 90% latency reduction.\n'
                    'Example: Multiple read_file() calls can be made simultaneously.'
                )
            }
        }
    
    return {}


async def validate_file_operation(
    input_data: Dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> Dict[str, Any]:
    """
    PreToolUse hook: Validate file operations before execution.
    
    Prevents: Overwriting important files, path traversal, etc.
    """
    tool_name = input_data.get('tool_name', '')
    
    if tool_name not in ['Write', 'Edit']:
        return {}
    
    tool_input = input_data.get('tool_input', {})
    file_path = tool_input.get('file_path', '')
    
    # Check for protected files
    protected_patterns = [
        r'agents/.*\.py$',  # Agent definitions
        r'config\.py$',     # Config files
        r'__init__\.py$',   # Package init
    ]
    
    for pattern in protected_patterns:
        if re.search(pattern, file_path):
            return {
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'permissionDecision': 'ask',
                    'permissionDecisionReason': (
                        f'⚠️ Modifying protected file: {file_path}\n'
                        f'This could affect core system functionality. Proceed?'
                    )
                }
            }
    
    # Check for path traversal
    if '..' in file_path or file_path.startswith('/'):
        if not file_path.startswith('/home/kc-palantir/math'):
            return {
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'permissionDecision': 'deny',
                    'permissionDecisionReason': (
                        f'❌ Invalid path: {file_path}\n'
                        f'Path must be within project directory.'
                    )
                }
            }
    
    return {}

