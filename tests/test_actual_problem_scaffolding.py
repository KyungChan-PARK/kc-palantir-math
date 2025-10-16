"""
Test: Actual Problem Scaffolding

Tests scaffolding generation on the actual sample.png problem (coordinate geometry).

VERSION: 1.0.0
DATE: 2025-10-16
"""

import asyncio
import json
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.mathpix_ocr_tool import extract_math_from_image
from workflows.concept_matcher import identify_concepts
from workflows.feedback_loop_workflow import generate_scaffolding


async def test_actual_problem():
    """Test scaffolding on actual coordinate geometry problem."""
    
    print("\n" + "="*70)
    print("TEST: Actual Problem Scaffolding (Coordinate Geometry)")
    print("="*70)
    
    # Step 1: OCR
    print("\n[Step 1] OCR Extraction...")
    sample_image = str(project_root / "sample.png")
    ocr_result = extract_math_from_image(sample_image)
    
    print(f"✅ OCR Success: {ocr_result['success']}")
    print(f"   Confidence: {ocr_result['confidence']:.2%}")
    print(f"   Text: {ocr_result['text'][:100]}...")
    
    # Step 2: Concept Matching
    print("\n[Step 2] Concept Matching...")
    concepts = identify_concepts(ocr_result, top_k=5)
    
    print(f"✅ Matched {len(concepts)} concepts:")
    for i, c in enumerate(concepts, 1):
        print(f"   {i}. {c['name']} (score: {c['relevance_score']:.3f})")
    
    # Step 3: Scaffolding Generation
    print("\n[Step 3] Scaffolding Generation...")
    scaffolding = await generate_scaffolding(
        ocr_result["text"],
        concepts,
        []  # No patterns yet
    )
    
    print(f"✅ Generated {len(scaffolding['steps'])} steps:")
    for i, step in enumerate(scaffolding['steps'], 1):
        print(f"\n   Step {i}:")
        print(f"     Q: {step['question']}")
        print(f"     A: {step['expected_answer']}")
        print(f"     Hint: {step['hint']}")
        print(f"     Type: {step['cognitive_type']}")
        print(f"     Difficulty: {step['difficulty']}")
    
    # Verify it's coordinate geometry scaffolding
    assert len(scaffolding['steps']) >= 8, "Should have at least 8 steps for coordinate geometry"
    assert any("좌표" in s['question'] or "점" in s['question'] for s in scaffolding['steps']), "Should mention coordinates"
    assert any("삼각형" in s['question'] or "넓이" in s['question'] for s in scaffolding['steps']), "Should mention triangle area"
    
    print(f"\n" + "="*70)
    print("✅ TEST PASSED: Scaffolding correctly generated for coordinate geometry")
    print("="*70)
    
    return scaffolding


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    result = asyncio.run(test_actual_problem())
    
    print(f"\n\n📊 SUMMARY:")
    print(f"   Steps: {len(result['steps'])}")
    print(f"   Problem type: Coordinate geometry - triangle area")
    print(f"   Difficulty range: {min(s['difficulty'] for s in result['steps'])} - {max(s['difficulty'] for s in result['steps'])}")

