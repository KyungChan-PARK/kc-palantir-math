"""
Feedback Collector - Interactive CLI Feedback Collection

Collects human feedback on scaffolding steps via interactive CLI.

VERSION: 1.0.0
DATE: 2025-10-16
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import logging

from tools.observability_hook import send_hook_event
from workflows.hook_events import HookEventType

logger = logging.getLogger(__name__)


def collect_step_feedback(step: Dict[str, Any], step_number: int) -> Dict[str, Any]:
    """
    Collect feedback for a single scaffolding step.
    
    Args:
        step: Step data (question, expected_answer, etc.)
        step_number: Step number (1-indexed)
        
    Returns:
        dict: Feedback data with rating, comment, suggested_improvement
    """
    print(f"\n{'='*70}")
    print(f"Step {step_number}: {step.get('question', 'N/A')}")
    print(f"{'='*70}")
    
    if 'expected_answer' in step:
        print(f"Expected answer: {step['expected_answer']}")
    if 'hint' in step:
        print(f"Hint: {step['hint']}")
    
    # Collect rating
    while True:
        try:
            rating_input = input("\nRate this step (1-5, or 's' to skip): ").strip()
            if rating_input.lower() == 's':
                return {
                    "rating": None,
                    "comment": "",
                    "suggested_improvement": None,
                    "skipped": True
                }
            
            rating = int(rating_input)
            if 1 <= rating <= 5:
                break
            else:
                print("Please enter a number between 1 and 5")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5")
    
    # Collect comment
    comment = input("Comment (optional, press Enter to skip): ").strip()
    
    # Collect suggested improvement if rating < 4
    suggested_improvement = None
    if rating < 4:
        suggested_improvement = input("Suggested improvement (optional): ").strip()
        if not suggested_improvement:
            suggested_improvement = None
    
    feedback = {
        "rating": rating,
        "comment": comment if comment else "",
        "suggested_improvement": suggested_improvement,
        "skipped": False
    }
    
    # Send hook event
    send_hook_event(
        "feedback_collector",
        HookEventType.FEEDBACK_STEP_COLLECTED,
        {
            "step_number": step_number,
            "rating": rating,
            "has_comment": bool(comment),
            "has_improvement": bool(suggested_improvement)
        }
    )
    
    return feedback


def collect_overall_feedback(problem: Dict[str, Any]) -> Dict[str, Any]:
    """
    Collect overall feedback on the scaffolding.
    
    Args:
        problem: Complete problem data with all steps
        
    Returns:
        dict: Overall feedback
    """
    print(f"\n{'='*70}")
    print("Overall Feedback")
    print(f"{'='*70}")
    
    # Scaffolding level
    print("\nScaffolding level:")
    print("  1. Too simple (needs more steps)")
    print("  2. Appropriate")
    print("  3. Too detailed (too many steps)")
    
    while True:
        try:
            level_input = input("Select (1-3): ").strip()
            level = int(level_input)
            if 1 <= level <= 3:
                break
        except ValueError:
            pass
        print("Please enter 1, 2, or 3")
    
    level_map = {1: "too_simple", 2: "appropriate", 3: "too_detailed"}
    scaffolding_level = level_map[level]
    
    # Pacing
    print("\nPacing:")
    print("  1. Too fast")
    print("  2. Good")
    print("  3. Too slow")
    
    while True:
        try:
            pacing_input = input("Select (1-3): ").strip()
            pacing = int(pacing_input)
            if 1 <= pacing <= 3:
                break
        except ValueError:
            pass
        print("Please enter 1, 2, or 3")
    
    pacing_map = {1: "too_fast", 2: "good", 3: "too_slow"}
    pacing_value = pacing_map[pacing]
    
    # Conceptual depth
    print("\nConceptual depth:")
    print("  1. Needs more 'why' questions")
    print("  2. Good balance")
    print("  3. Too theoretical")
    
    while True:
        try:
            depth_input = input("Select (1-3): ").strip()
            depth = int(depth_input)
            if 1 <= depth <= 3:
                break
        except ValueError:
            pass
        print("Please enter 1, 2, or 3")
    
    depth_map = {1: "needs_more", 2: "good", 3: "too_theoretical"}
    conceptual_depth = depth_map[depth]
    
    # Additional suggestions
    suggestions = input("\nAdditional suggestions (optional): ").strip()
    
    return {
        "scaffolding_level": scaffolding_level,
        "pacing": pacing_value,
        "conceptual_depth": conceptual_depth,
        "suggestions": suggestions if suggestions else ""
    }


def collect_interactive_feedback(scaffolding: Dict[str, Any]) -> Dict[str, Any]:
    """
    Collect complete feedback session interactively.
    
    Args:
        scaffolding: Complete scaffolding data with all steps
        
    Returns:
        dict: Complete feedback session
    """
    send_hook_event(
        "feedback_collector",
        HookEventType.FEEDBACK_STARTED,
        {
            "step_count": len(scaffolding.get("steps", [])),
            "problem_id": scaffolding.get("problem_id", "unknown")
        }
    )
    
    print("\n" + "="*70)
    print("FEEDBACK COLLECTION SESSION")
    print("="*70)
    print(f"Problem: {scaffolding.get('problem_text', 'N/A')}")
    print(f"Total steps: {len(scaffolding.get('steps', []))}")
    print("\nYou will rate each step. Press Ctrl+C to cancel anytime.")
    print("="*70)
    
    # Collect feedback for each step
    step_feedbacks = []
    steps = scaffolding.get("steps", [])
    
    try:
        for i, step in enumerate(steps, 1):
            feedback = collect_step_feedback(step, i)
            
            # Update step with feedback
            step_with_feedback = {**step, "feedback": feedback}
            step_feedbacks.append(step_with_feedback)
            
            # Show progress
            print(f"\n[Progress: {i}/{len(steps)}]")
        
        # Collect overall feedback
        overall = collect_overall_feedback(scaffolding)
        
        # Generate session ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_id = f"fs_{timestamp}"
        
        # Compile complete feedback session
        feedback_session = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "problem_instance": scaffolding.get("problem_id", "unknown"),
            "image_source": scaffolding.get("image_source", "unknown"),
            "ocr_result": scaffolding.get("ocr_result", {}),
            "concepts_identified": scaffolding.get("concepts", []),
            "generated_steps": step_feedbacks,
            "overall_feedback": overall,
            "extracted_patterns": []  # Will be filled by feedback-learning-agent
        }
        
        # Save to file
        output_dir = Path("/home/kc-palantir/math/data/feedback_sessions")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"{session_id}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(feedback_session, f, indent=2, ensure_ascii=False)
        
        logger.info(f"[Feedback] Session saved: {output_file}")
        
        # Send completion hook
        send_hook_event(
            "feedback_collector",
            HookEventType.FEEDBACK_COMPLETED,
            {
                "session_id": session_id,
                "steps_rated": len(step_feedbacks),
                "avg_rating": sum(s["feedback"]["rating"] for s in step_feedbacks if s["feedback"]["rating"]) / len([s for s in step_feedbacks if s["feedback"]["rating"]]) if step_feedbacks else 0,
                "output_file": str(output_file)
            }
        )
        
        print(f"\n{'='*70}")
        print(f"✅ Feedback session saved: {session_id}")
        print(f"   File: {output_file}")
        print(f"{'='*70}")
        
        return feedback_session
        
    except KeyboardInterrupt:
        print("\n\n❌ Feedback collection cancelled by user")
        return {
            "session_id": f"cancelled_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "cancelled": True,
            "partial_feedback": step_feedbacks
        }


if __name__ == "__main__":
    # Test feedback collector
    logging.basicConfig(level=logging.INFO)
    
    test_scaffolding = {
        "problem_id": "test_001",
        "problem_text": "60을 소인수분해하시오",
        "steps": [
            {
                "step_id": 1,
                "question": "60은 짝수인가요?",
                "expected_answer": "네",
                "hint": "끝자리를 보세요"
            },
            {
                "step_id": 2,
                "question": "60을 2로 나누면?",
                "expected_answer": "30",
                "hint": "60 ÷ 2 = ?"
            }
        ]
    }
    
    result = collect_interactive_feedback(test_scaffolding)
    print(f"\n\nCollected feedback:\n{json.dumps(result, indent=2, ensure_ascii=False)}")

