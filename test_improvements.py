"""
Test script to verify human-readable session names and workflow type improvements.
"""

import asyncio
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from tools.observability_hook import (
    send_hook_event, 
    reset_session_id, 
    set_session_context,
    get_session_name
)
from workflows.hook_events import HookEventType


def test_session_naming():
    """Test human-readable session names."""
    print("\n" + "="*70)
    print("TESTING SESSION NAMING IMPROVEMENTS")
    print("="*70)
    
    # Test 1: Problem-based session name
    print("\n[Test 1] Creating session with problem preview...")
    reset_session_id(
        problem_preview="Solve quadratic equation x²+5x+6=0",
        workflow_type="Math Scaffolding",
        difficulty="medium"
    )
    
    session_name = get_session_name()
    print(f"✅ Session name: {session_name}")
    
    # Send some events with specific workflow types
    print("\n[Test 2] Sending events with specific workflow types...")
    
    send_hook_event(
        "ocr_extraction",
        HookEventType.OCR_STARTED,
        {"image_path": "/test/problem.png"}
    )
    time.sleep(0.2)
    
    send_hook_event(
        "ocr_extraction",
        HookEventType.OCR_COMPLETED,
        {"text": "Solve quadratic equation", "confidence": 0.95}
    )
    time.sleep(0.2)
    
    send_hook_event(
        "concept_matching",
        HookEventType.CONCEPT_MATCH_STARTED,
        {"text_length": 25}
    )
    time.sleep(0.2)
    
    send_hook_event(
        "concept_matching",
        HookEventType.CONCEPT_MATCH_COMPLETED,
        {"matched_concepts": ["Quadratic Equations", "Factoring"]}
    )
    time.sleep(0.2)
    
    send_hook_event(
        "pattern_query",
        HookEventType.PATTERN_QUERY_STARTED,
        {"concept_count": 2}
    )
    time.sleep(0.2)
    
    send_hook_event(
        "pattern_query",
        HookEventType.PATTERN_QUERY_COMPLETED,
        {"pattern_count": 3}
    )
    time.sleep(0.2)
    
    send_hook_event(
        "scaffolding_generation",
        HookEventType.SCAFFOLDING_STARTED,
        {"problem_type": "quadratic"}
    )
    time.sleep(0.2)
    
    send_hook_event(
        "scaffolding_generation",
        HookEventType.SCAFFOLDING_COMPLETED,
        {"step_count": 8}
    )
    time.sleep(0.2)
    
    print("✅ Sent 8 events with specific workflow types")
    
    # Test 3: Another session with different problem
    print("\n[Test 3] Creating second session...")
    reset_session_id(
        problem_preview="Find area of triangle ABC",
        workflow_type="Geometry Scaffolding"
    )
    
    session_name = get_session_name()
    print(f"✅ Session name: {session_name}")
    
    send_hook_event(
        "pattern_learning",
        HookEventType.LEARNING_STARTED,
        {"feedback_count": 5}
    )
    time.sleep(0.2)
    
    send_hook_event(
        "pattern_learning",
        HookEventType.PATTERN_EXTRACTED,
        {"pattern_type": "hint_improvement"}
    )
    time.sleep(0.2)
    
    send_hook_event(
        "pattern_learning",
        HookEventType.LEARNING_COMPLETED,
        {"patterns_extracted": 3}
    )
    time.sleep(0.2)
    
    send_hook_event(
        "neo4j_storage",
        HookEventType.NEO4J_WRITE_STARTED,
        {"pattern_count": 3}
    )
    time.sleep(0.2)
    
    send_hook_event(
        "neo4j_storage",
        HookEventType.NEO4J_WRITE_COMPLETED,
        {"success": True}
    )
    time.sleep(0.2)
    
    print("✅ Sent 5 more events")
    
    print("\n" + "="*70)
    print("✅ TEST COMPLETED")
    print("="*70)
    print("\n📊 Open dashboard at: http://localhost:5173")
    print("\nExpected improvements:")
    print("  1. Session IDs show as: 'Problem preview - HH:MM:SS'")
    print("  2. Source apps are specific: ocr_extraction, concept_matching, etc.")
    print("  3. Session dropdown shows human-readable names")
    print("="*70)


if __name__ == "__main__":
    test_session_naming()

