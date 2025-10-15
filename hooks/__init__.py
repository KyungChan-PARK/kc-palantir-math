"""
Hooks Package for Enhanced Meta-Orchestrator

Provides hook functions for:
- SDK validation (PreToolUse)
- Quality gates (PostToolUse)
- Self-improvement (Stop, SubagentStop)
- Ambiguity detection (UserPromptSubmit)

Based on: claude-code-2-0-deduplicated-final.md
"""

from hooks.validation_hooks import (
    validate_sdk_parameters,
    check_agent_exists,
    verify_parallel_execution_possible,
    validate_file_operation,
)

from hooks.quality_hooks import (
    auto_quality_check_after_write,
    monitor_improvement_impact,
    enforce_code_quality_standards,
    calculate_change_impact_score,
)

from hooks.learning_hooks import (
    auto_trigger_improvement,
    learn_from_questions,
    detect_ambiguity_before_execution,
    inject_historical_context,
    track_session_learning,
)

__all__ = [
    # Validation hooks (PreToolUse)
    'validate_sdk_parameters',
    'check_agent_exists',
    'verify_parallel_execution_possible',
    'validate_file_operation',
    
    # Quality hooks (PostToolUse)
    'auto_quality_check_after_write',
    'monitor_improvement_impact',
    'enforce_code_quality_standards',
    'calculate_change_impact_score',
    
    # Learning hooks (Stop, UserPromptSubmit, SessionEnd)
    'auto_trigger_improvement',
    'learn_from_questions',
    'detect_ambiguity_before_execution',
    'inject_historical_context',
    'track_session_learning',
]

