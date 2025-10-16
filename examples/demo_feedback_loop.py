#!/usr/bin/env python3
"""
Feedback Loop Demo - Complete Workflow Example

Demonstrates the complete feedback loop from image to pattern learning.

Usage:
    python3 examples/demo_feedback_loop.py

VERSION: 1.0.0
DATE: 2025-10-16
"""

import asyncio
import json
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from workflows.feedback_loop_workflow import run_feedback_loop_workflow
from tools.observability_hook import get_session_id


async def demo():
    """Run demo workflow with sample.png."""
    
    print("\n" + "="*70)
    print("FEEDBACK LOOP DEMO - Complete Workflow")
    print("="*70)
    print()
    print("This demo will:")
    print("  1. Extract math problem from sample.png (Mathpix OCR)")
    print("  2. Match concepts from 841 중학교 수학 개념")
    print("  3. Generate step-by-step scaffolding")
    print("  4. Collect your feedback (interactive)")
    print("  5. Learn patterns from your feedback")
    print("  6. Store patterns for reuse")
    print()
    print(f"Session ID: {get_session_id()}")
    print(f"Dashboard: http://localhost:3000")
    print()
    
    input("Press Enter to start demo (or Ctrl+C to cancel)...")
    
    # Run workflow
    sample_image = str(project_root / "sample.png")
    
    result = await run_feedback_loop_workflow(sample_image)
    
    if result.get("success"):
        print("\n" + "="*70)
        print("✅ DEMO COMPLETED SUCCESSFULLY")
        print("="*70)
        print(f"\nResults saved:")
        print(f"  - Feedback: data/feedback_sessions/{result['feedback_session']['session_id']}.json")
        print(f"  - Patterns: data/learned_patterns/patterns_*.json")
        print(f"  - OCR: data/ocr_results/ocr_*.json")
        print()
        print(f"Learned Patterns: {len(result['learned_patterns'])}")
        for i, p in enumerate(result['learned_patterns'], 1):
            print(f"  {i}. {p['type']}: {p['rule'][:60]}...")
        print()
        print(f"View in dashboard: http://localhost:3000")
        print("="*70)
    else:
        print(f"\n❌ Demo failed: {result.get('error')}")


if __name__ == "__main__":
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s:%(name)s:%(message)s'
    )
    
    try:
        asyncio.run(demo())
    except KeyboardInterrupt:
        print("\n\n❌ Demo cancelled by user")
        sys.exit(1)

