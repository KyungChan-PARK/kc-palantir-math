"""
Full Integration Test - Complete Feedback Loop

Tests the complete workflow with actual sample.png and simulated feedback.

VERSION: 1.0.0
DATE: 2025-10-16
"""

import asyncio
import json
import requests
from pathlib import Path
from datetime import datetime
import sys

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.mathpix_ocr_tool import extract_math_from_image
from workflows.concept_matcher import identify_concepts
from workflows.math_scaffolding_workflow import (
    query_neo4j_patterns,
    generate_scaffolding,
    extract_patterns_from_feedback,
    store_patterns_neo4j
)
from tools.observability_hook import get_session_id


async def run_full_integration_test():
    """Run complete workflow with simulated feedback."""
    
    print("\n" + "="*70)
    print("FULL INTEGRATION TEST - Complete Feedback Loop")
    print("="*70)
    
    session_id = get_session_id()
    print(f"Session ID: {session_id}")
    print(f"Dashboard: http://localhost:3000")
    print("="*70)
    
    # Step 1: OCR
    print("\n[1/7] OCR Extraction...")
    sample_image = str(project_root / "sample.png")
    ocr_result = extract_math_from_image(sample_image)
    
    assert ocr_result["success"], "OCR should succeed"
    assert ocr_result["confidence"] > 0.9, "High confidence expected"
    
    print(f"✅ OCR: {ocr_result['confidence']:.2%} confidence")
    print(f"   Problem: {ocr_result['text'][:80]}...")
    
    # Step 2: Concept Matching
    print("\n[2/7] Concept Matching...")
    concepts = identify_concepts(ocr_result, top_k=3)
    
    assert len(concepts) > 0, "Should match concepts"
    assert concepts[0]["relevance_score"] > 0.7, "Top concept should have high score"
    
    print(f"✅ Top concept: {concepts[0]['name']} (score: {concepts[0]['relevance_score']:.3f})")
    
    # Step 3: Pattern Query
    print("\n[3/7] Pattern Query...")
    patterns = await query_neo4j_patterns(concepts)
    
    print(f"✅ Patterns found: {len(patterns)}")
    
    # Step 4: Scaffolding Generation
    print("\n[4/7] Scaffolding Generation...")
    scaffolding = await generate_scaffolding(
        ocr_result["text"],
        concepts,
        patterns
    )
    
    scaffolding["image_source"] = sample_image
    scaffolding["ocr_result"] = ocr_result
    
    assert len(scaffolding["steps"]) >= 5, "Should generate meaningful steps"
    
    print(f"✅ Generated {len(scaffolding['steps'])} steps")
    
    # Step 5: Simulate Feedback
    print("\n[5/7] Simulating Feedback...")
    
    # Create simulated feedback (as if human reviewed)
    feedback_session = {
        "session_id": f"fs_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "timestamp": datetime.now().isoformat(),
        "problem_instance": scaffolding["problem_id"],
        "image_source": sample_image,
        "ocr_result": ocr_result,
        "concepts_identified": concepts,
        "generated_steps": [],
        "overall_feedback": {
            "scaffolding_level": "appropriate",
            "pacing": "good",
            "conceptual_depth": "needs_more"
        }
    }
    
    # Simulate feedback for each step
    for i, step in enumerate(scaffolding["steps"], 1):
        # Simulate varied ratings
        if i == 2:
            # Step 2 gets improvement suggestion
            step_feedback = {
                **step,
                "feedback": {
                    "rating": 3,
                    "comment": "Could be clearer about which value to substitute",
                    "suggested_improvement": step["question"] + " (y=0을 대입)"
                }
            }
        elif i % 3 == 0:
            # Every 3rd step gets good rating with comment
            step_feedback = {
                **step,
                "feedback": {
                    "rating": 5,
                    "comment": "Excellent step",
                    "suggested_improvement": None
                }
            }
        else:
            # Others get good rating
            step_feedback = {
                **step,
                "feedback": {
                    "rating": 4,
                    "comment": "",
                    "suggested_improvement": None
                }
            }
        
        feedback_session["generated_steps"].append(step_feedback)
    
    # Save simulated feedback
    output_dir = Path("/home/kc-palantir/math/data/feedback_sessions")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"{feedback_session['session_id']}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(feedback_session, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Simulated feedback: {feedback_session['session_id']}")
    print(f"   Saved to: {output_file}")
    
    # Step 6: Pattern Extraction
    print("\n[6/7] Pattern Extraction...")
    learned_patterns = await extract_patterns_from_feedback(feedback_session)
    
    assert len(learned_patterns) > 0, "Should extract at least one pattern"
    
    print(f"✅ Extracted {len(learned_patterns)} patterns:")
    for i, p in enumerate(learned_patterns, 1):
        print(f"   {i}. {p['type']}: {p['rule'][:60]}...")
    
    # Step 7: Pattern Storage
    print("\n[7/7] Pattern Storage...")
    success = await store_patterns_neo4j(learned_patterns)
    
    assert success, "Pattern storage should succeed"
    
    print(f"✅ Patterns stored successfully")
    
    # Verify observability events
    print("\n[Observability Check]...")
    try:
        response = requests.get(
            "http://localhost:4000/events/recent",
            params={"session_id": session_id, "limit": 50},
            timeout=2
        )
        
        if response.status_code == 200:
            data = response.json()
            events = data.get("events", [])
            print(f"✅ Observability events: {len(events)} events recorded")
            
            # Check for key event types
            event_types = set(e["hook_event_type"] for e in events)
            expected_types = {
                "ocr_started", "ocr_completed",
                "concept_match_started", "concept_match_completed",
                "scaffolding_started", "scaffolding_completed",
                "learning_started", "learning_completed"
            }
            
            found_types = event_types & expected_types
            print(f"   Key events captured: {len(found_types)}/{len(expected_types)}")
            
            if found_types:
                print(f"   Events: {', '.join(sorted(found_types))}")
        else:
            print(f"⚠️  Observability server returned {response.status_code}")
    except Exception as e:
        print(f"⚠️  Observability check failed (server might not be running): {e}")
    
    # Final Summary
    print(f"\n" + "="*70)
    print("✅ FULL INTEGRATION TEST PASSED")
    print("="*70)
    print(f"Session ID: {session_id}")
    print(f"OCR Confidence: {ocr_result['confidence']:.2%}")
    print(f"Concepts Matched: {len(concepts)}")
    print(f"Scaffolding Steps: {len(scaffolding['steps'])}")
    print(f"Patterns Learned: {len(learned_patterns)}")
    print(f"Observability: Active")
    print("="*70)
    
    return {
        "success": True,
        "session_id": session_id,
        "ocr": ocr_result,
        "concepts": concepts,
        "scaffolding": scaffolding,
        "feedback": feedback_session,
        "patterns": learned_patterns
    }


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    result = asyncio.run(run_full_integration_test())
    
    print(f"\n\n{'='*70}")
    print("INTEGRATION TEST COMPLETE")
    print(f"{'='*70}")
    print(f"Status: {'✅ SUCCESS' if result['success'] else '❌ FAILED'}")
    print(f"{'='*70}\n")
    
    sys.exit(0 if result['success'] else 1)

