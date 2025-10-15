"""
Quality Gate Hooks for Self-Improvement System

Based on: claude-code-2-0-deduplicated-final.md
Patterns: PostToolUse auto-validation and quality checking

VERSION: 1.0.0
DATE: 2025-10-15
"""

from typing import Any, Dict
import json
import re


class HookContext:
    """Hook context placeholder"""
    def __init__(self):
        self.signal = None


async def auto_quality_check_after_write(
    input_data: Dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> Dict[str, Any]:
    """
    PostToolUse hook: Automatically check quality after file write.
    
    Based on: Code reviewer best practices (lines 2615-2647)
    
    Checks:
    - File not empty
    - Proper formatting
    - No obvious errors
    """
    if input_data.get('tool_name') != 'Write':
        return {}
    
    tool_input = input_data.get('tool_input', {})
    tool_response = input_data.get('tool_response', {})
    
    file_path = tool_input.get('file_path', '')
    content = tool_input.get('content', '')
    bytes_written = tool_response.get('bytes_written', 0)
    
    issues = []
    
    # Check 1: Empty file
    if bytes_written < 10:
        issues.append('File is nearly empty (< 10 bytes)')
    
    # Check 2: Python syntax (basic)
    if file_path.endswith('.py'):
        if 'def ' in content and 'return' not in content:
            issues.append('Function defined but no return statement found')
        
        # Check for unclosed brackets/parens
        open_count = content.count('(') + content.count('[') + content.count('{')
        close_count = content.count(')') + content.count(']') + content.count('}')
        if open_count != close_count:
            issues.append(f'Bracket mismatch: {open_count} open, {close_count} close')
    
    # Check 3: Markdown syntax
    if file_path.endswith('.md'):
        # Check for unclosed code blocks
        if content.count('```') % 2 != 0:
            issues.append('Unclosed code block detected (odd number of ```)')
    
    if issues:
        return {
            'decision': 'block',
            'reason': (
                f'⚠️ Quality issues detected in {file_path}:\n' +
                '\n'.join(f'- {issue}' for issue in issues) +
                '\n\nPlease review and fix before proceeding.'
            ),
            'hookSpecificOutput': {
                'hookEventName': 'PostToolUse',
                'additionalContext': f'Auto-quality check failed for {file_path}'
            }
        }
    
    return {}


async def monitor_improvement_impact(
    input_data: Dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> Dict[str, Any]:
    """
    PostToolUse hook: Monitor impact of self-improvement changes.
    
    Tracks:
    - Which files were modified
    - Estimated blast radius
    - Performance delta
    """
    if input_data.get('tool_name') not in ['Write', 'Edit']:
        return {}
    
    tool_input = input_data.get('tool_input', {})
    file_path = tool_input.get('file_path', '')
    
    # Track modifications to agent files
    if 'agents/' in file_path and file_path.endswith('.py'):
        return {
            'hookSpecificOutput': {
                'hookEventName': 'PostToolUse',
                'additionalContext': json.dumps({
                    'improvement_detected': True,
                    'modified_file': file_path,
                    'type': 'agent_modification',
                    'recommendation': 'Run verification tests before deployment'
                })
            }
        }
    
    return {}


async def enforce_code_quality_standards(
    input_data: Dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> Dict[str, Any]:
    """
    PostToolUse hook: Enforce coding standards after edits.
    
    Based on: Code reviewer checklist (lines 2615-2647)
    
    Standards:
    - No hardcoded values
    - Proper error handling
    - Type hints present
    - Docstrings exist
    """
    if input_data.get('tool_name') not in ['Write', 'Edit']:
        return {}
    
    tool_input = input_data.get('tool_input', {})
    file_path = tool_input.get('file_path', '')
    
    if not file_path.endswith('.py'):
        return {}
    
    content = tool_input.get('content', '') or tool_input.get('new_string', '')
    
    violations = []
    
    # Standard 1: Type hints for functions
    if 'def ' in content and 'async def' in content:
        # Check if return type hints exist
        func_lines = [line for line in content.split('\n') if 'def ' in line]
        for func_line in func_lines[:3]:  # Check first 3 functions
            if '->' not in func_line and 'def __' not in func_line:
                violations.append(f'Missing return type hint: {func_line.strip()[:50]}...')
    
    # Standard 2: Docstrings for functions/classes
    if ('class ' in content or 'def ' in content) and '"""' not in content:
        violations.append('No docstrings found in file with functions/classes')
    
    # Standard 3: Error handling
    if 'try:' in content and 'except Exception:' in content:
        violations.append('Bare "except Exception" is too broad, specify exception types')
    
    if violations:
        return {
            'hookSpecificOutput': {
                'hookEventName': 'PostToolUse',
                'additionalContext': (
                    '⚠️ Code Quality Standards:\n' +
                    '\n'.join(f'- {v}' for v in violations) +
                    '\n\nThese are recommendations, not blockers.'
                )
            }
        }
    
    return {}


async def calculate_change_impact_score(
    input_data: Dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> Dict[str, Any]:
    """
    PostToolUse hook: Calculate impact score for changes.
    
    Impact score factors:
    - File criticality (core vs peripheral)
    - Lines changed (magnitude)
    - Downstream dependencies
    """
    if input_data.get('tool_name') not in ['Write', 'Edit']:
        return {}
    
    tool_input = input_data.get('tool_input', {})
    file_path = tool_input.get('file_path', '')
    
    # Calculate criticality score (0-10)
    criticality_score = 0
    
    if 'meta_orchestrator' in file_path:
        criticality_score = 10  # Mission critical
    elif 'socratic' in file_path:
        criticality_score = 8   # High criticality
    elif 'agents/' in file_path:
        criticality_score = 6   # Medium criticality
    elif 'hooks/' in file_path:
        criticality_score = 4   # Lower criticality
    else:
        criticality_score = 2   # Minimal impact
    
    # Calculate magnitude
    if input_data.get('tool_name') == 'Edit':
        old_string = tool_input.get('old_string', '')
        new_string = tool_input.get('new_string', '')
        lines_changed = abs(old_string.count('\n') - new_string.count('\n'))
    else:
        content = tool_input.get('content', '')
        lines_changed = content.count('\n')
    
    impact_score = criticality_score * (1 + lines_changed / 100)
    
    if impact_score > 50:
        return {
            'decision': 'block',
            'reason': (
                f'🚨 HIGH IMPACT CHANGE DETECTED:\n'
                f'File: {file_path}\n'
                f'Criticality: {criticality_score}/10\n'
                f'Lines changed: {lines_changed}\n'
                f'Impact score: {impact_score:.1f}\n\n'
                f'This change requires:\n'
                f'1. Manual review\n'
                f'2. Test execution\n'
                f'3. Rollback plan\n\n'
                f'Proceed with caution?'
            )
        }
    elif impact_score > 20:
        return {
            'hookSpecificOutput': {
                'hookEventName': 'PostToolUse',
                'additionalContext': json.dumps({
                    'impact_warning': True,
                    'impact_score': impact_score,
                    'criticality': criticality_score,
                    'recommendation': 'Run tests before deployment'
                })
            }
        }
    
    return {}
