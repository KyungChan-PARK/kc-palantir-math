"""
Feedback Loop Workflow - Compatibility Alias

This module provides backward compatibility by re-exporting the renamed
math_scaffolding_workflow module as feedback_loop_workflow.

VERSION: 1.0.0
DATE: 2025-10-16
"""

from workflows.math_scaffolding_workflow import (
    run_math_scaffolding_workflow as run_feedback_loop_workflow,
    query_neo4j_patterns,
    generate_scaffolding,
    store_patterns_neo4j,
    extract_patterns_from_feedback,
    generate_validation_report
)

__all__ = [
    'run_feedback_loop_workflow',
    'query_neo4j_patterns',
    'generate_scaffolding',
    'store_patterns_neo4j',
    'extract_patterns_from_feedback',
    'generate_validation_report'
]

