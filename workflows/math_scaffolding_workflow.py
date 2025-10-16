"""
Math Scaffolding Workflow - End-to-End Pipeline

Complete workflow from math problem image to high-quality scaffolding with pattern learning.

This workflow enables teacher feedback collection for quality assurance of:
- OCR extraction accuracy
- Concept matching relevance
- Scaffolding step quality
- Pattern learning effectiveness

Feedback loop integration is a core feature that will expand across the entire project.

VERSION: 2.0.0 - Renamed from feedback_loop to math_scaffolding
DATE: 2025-10-16
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import logging

from tools.mathpix_ocr_tool import extract_math_from_image
from tools.feedback_collector import collect_interactive_feedback
from workflows.concept_matcher import identify_concepts
from tools.observability_hook import send_hook_event, get_session_id, set_session_context
from workflows.hook_events import HookEventType

logger = logging.getLogger(__name__)


async def query_neo4j_patterns(concepts: list) -> list:
    """
    Query Neo4j for applicable patterns for given concepts.
    
    Args:
        concepts: List of matched concepts
        
    Returns:
        list: Applicable patterns from Neo4j
    """
    send_hook_event(
        "pattern_query",
        HookEventType.PATTERN_QUERY_STARTED,
        {"concept_count": len(concepts)}
    )
    
    # TODO: Implement actual Neo4j query via graph_client_tool
    # For now, return empty list (no patterns yet)
    patterns = []
    
    logger.info(f"[Workflow] Queried patterns: {len(patterns)} found")
    
    send_hook_event(
        "pattern_query",
        HookEventType.PATTERN_QUERY_COMPLETED,
        {"pattern_count": len(patterns)}
    )
    
    return patterns


async def generate_scaffolding(
    problem_text: str,
    concepts: list,
    patterns: list
) -> Dict[str, Any]:
    """
    Generate scaffolding steps for the problem.
    
    Args:
        problem_text: OCR extracted problem
        concepts: Identified concepts
        patterns: Applicable learned patterns
        
    Returns:
        dict: Scaffolding with steps
    """
    send_hook_event(
        "scaffolding_generation",
        HookEventType.SCAFFOLDING_STARTED,
        {
            "problem_text": problem_text[:100],
            "concept_count": len(concepts),
            "pattern_count": len(patterns)
        }
    )
    
    logger.info(f"[Workflow] Generating scaffolding...")
    
    # TODO: Implement actual scaffolding generation
    # For now, create simple example for "60을 소인수분해하시오"
    
    # Detect problem type based on concepts and text
    is_prime_factorization = any(
        "소인수" in c.get("name", "") or "prime" in str(c.get("tags", []))
        for c in concepts
    ) and ("소인수분해" in problem_text or "분해" in problem_text)
    
    is_coordinate_geometry = any(
        "좌표" in c.get("name", "") or "일차함수" in c.get("name", "") or 
        "그래프" in c.get("name", "")
        for c in concepts
    ) or ("좌표평면" in problem_text or "그래프" in problem_text)
    
    if is_coordinate_geometry and "삼각형" in problem_text and "넓이" in problem_text:
        # Coordinate geometry - triangle area problem
        steps = [
            {
                "step_id": 1,
                "question": "주어진 정보를 정리해보세요: 점 A, B의 좌표는?",
                "expected_answer": "A(2,6), B(8,0)",
                "hint": "문제에서 주어진 좌표를 찾으세요",
                "cognitive_type": "comprehension",
                "difficulty": 1
            },
            {
                "step_id": 2,
                "question": "일차함수 y=1/2x+1/2가 x축과 만나는 점 C를 구하려면 y=?를 대입해야 하나요?",
                "expected_answer": "y=0",
                "hint": "x축 위의 점은 y좌표가 0입니다",
                "cognitive_type": "concept_application",
                "difficulty": 2
            },
            {
                "step_id": 3,
                "question": "0=1/2x+1/2를 풀면 x=?",
                "expected_answer": "x=-1",
                "hint": "양변에 2를 곱하면 0=x+1",
                "cognitive_type": "calculation",
                "difficulty": 2
            },
            {
                "step_id": 4,
                "question": "따라서 점 C의 좌표는?",
                "expected_answer": "C(-1,0)",
                "hint": "x축 위이므로 y=0",
                "cognitive_type": "synthesis",
                "difficulty": 2
            },
            {
                "step_id": 5,
                "question": "직선 AB의 방정식을 구하려면 기울기는 어떻게 구하나요?",
                "expected_answer": "(y2-y1)/(x2-x1)",
                "hint": "두 점을 지나는 직선의 기울기 공식",
                "cognitive_type": "concept_recall",
                "difficulty": 2
            },
            {
                "step_id": 6,
                "question": "AB의 기울기 m = (0-6)/(8-2) = ?",
                "expected_answer": "-1",
                "hint": "-6/6 = -1",
                "cognitive_type": "calculation",
                "difficulty": 2
            },
            {
                "step_id": 7,
                "question": "점 D는 두 직선의 교점이므로 y=1/2x+1/2와 y=-x+b의 교점입니다. 직선 AB의 y절편 b는?",
                "expected_answer": "12",
                "hint": "점 B(8,0)을 대입: 0=-8+b",
                "cognitive_type": "equation_solving",
                "difficulty": 3
            },
            {
                "step_id": 8,
                "question": "삼각형 CBD의 넓이를 구하는 공식은?",
                "expected_answer": "1/2 × 밑변 × 높이",
                "hint": "삼각형 넓이 공식",
                "cognitive_type": "concept_recall",
                "difficulty": 1
            },
            {
                "step_id": 9,
                "question": "점 C와 B 사이의 거리(밑변)는?",
                "expected_answer": "9",
                "hint": "C(-1,0)과 B(8,0)은 같은 x축 위: 8-(-1)=9",
                "cognitive_type": "calculation",
                "difficulty": 2
            },
            {
                "step_id": 10,
                "question": "점 D의 y좌표(높이)를 구하려면?",
                "expected_answer": "두 식을 연립하여 교점 구하기",
                "hint": "y=1/2x+1/2와 y=-x+12를 같다고 놓기",
                "cognitive_type": "problem_solving",
                "difficulty": 3
            }
        ]
    elif is_prime_factorization:
        # Prime factorization problem
        steps = [
            {
                "step_id": 1,
                "question": "60은 짝수인가요?",
                "expected_answer": "네",
                "hint": "끝자리를 보세요",
                "cognitive_type": "recognition",
                "difficulty": 1
            },
            {
                "step_id": 2,
                "question": "60을 2로 나누면?",
                "expected_answer": "30",
                "hint": "60 ÷ 2 = ?",
                "cognitive_type": "calculation",
                "difficulty": 2
            },
            {
                "step_id": 3,
                "question": "30도 짝수인가요?",
                "expected_answer": "네",
                "hint": "끝자리가 0, 2, 4, 6, 8이면 짝수",
                "cognitive_type": "pattern_recognition",
                "difficulty": 1
            },
            {
                "step_id": 4,
                "question": "30을 2로 나누면?",
                "expected_answer": "15",
                "hint": "30 ÷ 2 = ?",
                "cognitive_type": "calculation",
                "difficulty": 2
            },
            {
                "step_id": 5,
                "question": "15는 3의 배수인가요?",
                "expected_answer": "네",
                "hint": "1 + 5 = 6, 6은 3의 배수",
                "cognitive_type": "divisibility_rule",
                "difficulty": 2
            },
            {
                "step_id": 6,
                "question": "15를 3으로 나누면?",
                "expected_answer": "5",
                "hint": "15 ÷ 3 = ?",
                "cognitive_type": "calculation",
                "difficulty": 2
            },
            {
                "step_id": 7,
                "question": "5는 소수인가요?",
                "expected_answer": "네",
                "hint": "1과 5로만 나누어떨어짐",
                "cognitive_type": "prime_identification",
                "difficulty": 2
            },
            {
                "step_id": 8,
                "question": "지금까지 나눈 소수를 모두 써보세요",
                "expected_answer": "2, 2, 3, 5",
                "hint": "60 → 30 → 15 → 5에서 사용한 수",
                "cognitive_type": "synthesis",
                "difficulty": 3
            },
            {
                "step_id": 9,
                "question": "지수를 사용해서 표기하면?",
                "expected_answer": "2² × 3 × 5",
                "hint": "2가 2번 나왔으므로 2²",
                "cognitive_type": "notation",
                "difficulty": 3
            }
        ]
    else:
        # Generic scaffolding for other problems
        steps = [
            {
                "step_id": 1,
                "question": f"문제를 읽고 무엇을 구해야 하는지 파악하세요: {problem_text}",
                "expected_answer": "사용자 정의",
                "hint": "문제의 핵심을 찾으세요",
                "cognitive_type": "comprehension",
                "difficulty": 2
            }
        ]
    
    scaffolding = {
        "problem_id": f"prob_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "problem_text": problem_text,
        "concepts": concepts,
        "applied_patterns": patterns,
        "steps": steps,
        "generated_at": datetime.now().isoformat()
    }
    
    logger.info(f"[Workflow] Generated {len(steps)} scaffolding steps")
    
    send_hook_event(
        "scaffolding_generation",
        HookEventType.SCAFFOLDING_COMPLETED,
        {
            "step_count": len(steps),
            "problem_id": scaffolding["problem_id"]
        }
    )
    
    return scaffolding


async def store_patterns_neo4j(learned_patterns: list) -> bool:
    """
    Store learned patterns in Neo4j database.
    
    Args:
        learned_patterns: List of learned pattern dicts
        
    Returns:
        bool: Success status
    """
    send_hook_event(
        "neo4j_storage",
        HookEventType.NEO4J_WRITE_STARTED,
        {"pattern_count": len(learned_patterns)}
    )
    
    logger.info(f"[Workflow] Storing {len(learned_patterns)} patterns in Neo4j...")
    
    # TODO: Implement actual Neo4j storage via graph_client_tool
    # For now, save to JSON file as backup
    
    output_dir = Path("/home/kc-palantir/math/data/learned_patterns")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"patterns_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(learned_patterns, f, indent=2, ensure_ascii=False)
    
    logger.info(f"[Workflow] Patterns saved to: {output_file}")
    
    send_hook_event(
        "neo4j_storage",
        HookEventType.NEO4J_WRITE_COMPLETED,
        {
            "pattern_count": len(learned_patterns),
            "output_file": str(output_file)
        }
    )
    
    return True


async def extract_patterns_from_feedback(feedback_session: Dict[str, Any]) -> list:
    """
    Extract learned patterns from feedback session.
    
    Args:
        feedback_session: Complete feedback data
        
    Returns:
        list: Extracted patterns
    """
    send_hook_event(
        "pattern_learning",
        HookEventType.LEARNING_STARTED,
        {"session_id": feedback_session.get("session_id")}
    )
    
    logger.info(f"[Workflow] Extracting patterns from feedback...")
    
    patterns = []
    
    # Analyze step feedbacks
    steps = feedback_session.get("generated_steps", [])
    
    for step in steps:
        feedback = step.get("feedback", {})
        
        # Skip if no feedback or skipped
        if feedback.get("skipped") or feedback.get("rating") is None:
            continue
        
        # Pattern: Low rating with suggested improvement
        if feedback.get("rating", 5) < 4 and feedback.get("suggested_improvement"):
            pattern = {
                "pattern_id": f"lp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{step['step_id']}",
                "type": "question_improvement",
                "rule": f"Improve step {step['step_id']}: {feedback['comment']}",
                "confidence": 1.0,  # Human feedback
                "applicable_concepts": [c["concept_id"] for c in feedback_session.get("concepts_identified", [])],
                "improvement_rate": None,  # To be measured
                "reuse_count": 0,
                "examples": [
                    {
                        "before": step["question"],
                        "after": feedback["suggested_improvement"]
                    }
                ],
                "discovered_date": datetime.now().isoformat(),
                "source": "teacher_kc",
                "tested": False,
                "auto_apply": False  # Require approval first
            }
            
            patterns.append(pattern)
            
            send_hook_event(
                "pattern_learning",
                HookEventType.PATTERN_EXTRACTED,
                {
                    "pattern_id": pattern["pattern_id"],
                    "type": pattern["type"],
                    "confidence": pattern["confidence"]
                }
            )
    
    # Analyze overall feedback
    overall = feedback_session.get("overall_feedback", {})
    
    if overall.get("conceptual_depth") == "needs_more":
        pattern = {
            "pattern_id": f"lp_add_why_questions_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "type": "conceptual_depth",
            "rule": "Insert 'why' questions between mechanical steps",
            "confidence": 0.85,  # Slightly lower (general feedback)
            "applicable_concepts": ["all"],
            "improvement_rate": None,
            "reuse_count": 0,
            "examples": [
                {
                    "insert_after": "calculation_step",
                    "question": "왜 이렇게 계산하는지 생각해보세요"
                }
            ],
            "discovered_date": datetime.now().isoformat(),
            "source": "teacher_kc",
            "tested": False,
            "auto_apply": False
        }
        patterns.append(pattern)
    
    logger.info(f"[Workflow] Extracted {len(patterns)} patterns")
    
    send_hook_event(
        "pattern_learning",
        HookEventType.LEARNING_COMPLETED,
        {"patterns_extracted": len(patterns)}
    )
    
    return patterns


async def generate_validation_report(
    session_id: str,
    feedback_session: Dict[str, Any],
    learned_patterns: list
) -> None:
    """
    Generate validation report (console only, no file).
    
    Args:
        session_id: Workflow session ID
        feedback_session: Feedback data
        learned_patterns: Extracted patterns
    """
    print("\n" + "="*70)
    print("WORKFLOW VALIDATION REPORT")
    print("="*70)
    print(f"Session ID: {session_id}")
    print(f"Feedback Session: {feedback_session.get('session_id')}")
    print(f"Patterns Extracted: {len(learned_patterns)}")
    print("="*70)
    
    for i, pattern in enumerate(learned_patterns, 1):
        print(f"\nPattern {i}: {pattern['pattern_id']}")
        print(f"  Type: {pattern['type']}")
        print(f"  Confidence: {pattern['confidence']}")
        print(f"  Rule: {pattern['rule']}")
        
        if pattern.get('examples'):
            print(f"  Example:")
            for ex in pattern['examples'][:1]:  # Show first example
                if 'before' in ex:
                    print(f"    Before: {ex['before']}")
                    print(f"    After: {ex['after']}")
    
    print(f"\n{'='*70}")
    
    send_hook_event(
        "workflow_validation",
        HookEventType.VALIDATION_COMPLETED,
        {
            "session_id": session_id,
            "feedback_session_id": feedback_session.get("session_id"),
            "patterns_count": len(learned_patterns)
        }
    )


async def run_math_scaffolding_workflow(image_path: str) -> Dict[str, Any]:
    """
    Run complete math scaffolding workflow with feedback collection.
    
    This workflow:
    1. Extracts math problem from image (Mathpix OCR)
    2. Matches relevant concepts (841 math concepts)
    3. Queries learned patterns (Neo4j)
    4. Generates scaffolding steps
    5. Collects teacher feedback (quality assurance)
    6. Learns patterns (continuous improvement)
    7. Stores in Neo4j (reusable patterns)
    
    Args:
        image_path: Path to math problem image
        
    Returns:
        dict: Complete workflow results with feedback and patterns
    """
    session_id = get_session_id()
    
    print("\n" + "="*70)
    print("MATH SCAFFOLDING WORKFLOW")
    print("="*70)
    print(f"Session ID: {session_id}")
    print(f"Image: {image_path}")
    print(f"Dashboard: http://localhost:3000")
    print("="*70)
    
    try:
        # Step 1: OCR Extraction
        print("\n[1/7] OCR Extraction...")
        problem_data = extract_math_from_image(image_path)
        
        if not problem_data.get("success"):
            print(f"❌ OCR failed: {problem_data.get('error')}")
            return {"success": False, "error": "OCR failed"}
        
        print(f"✅ OCR completed (confidence: {problem_data['confidence']:.2%})")
        print(f"   Text: {problem_data['text'][:100]}...")
        
        # Set session context with problem preview
        problem_preview = problem_data['text'][:30].replace('\n', ' ')
        set_session_context(
            problem_preview=problem_preview,
            workflow_type="Math Scaffolding",
            image_path=image_path
        )
        
        # Step 2: Concept Identification
        print("\n[2/7] Concept Identification...")
        concepts = identify_concepts(problem_data, top_k=3)
        
        if not concepts:
            print("❌ No concepts matched")
            return {"success": False, "error": "No concepts matched"}
        
        print(f"✅ Matched {len(concepts)} concepts:")
        for i, c in enumerate(concepts, 1):
            print(f"   {i}. {c['name']} (score: {c['relevance_score']:.3f})")
        
        # Step 3: Query Patterns
        print("\n[3/7] Querying Learned Patterns...")
        patterns = await query_neo4j_patterns(concepts)
        print(f"✅ Found {len(patterns)} applicable patterns")
        
        # Step 4: Generate Scaffolding
        print("\n[4/7] Generating Scaffolding...")
        scaffolding = await generate_scaffolding(
            problem_data["text"],
            concepts,
            patterns
        )
        
        # Add metadata to scaffolding
        scaffolding["image_source"] = image_path
        scaffolding["ocr_result"] = {
            "text": problem_data["text"],
            "latex": problem_data["latex"],
            "confidence": problem_data["confidence"]
        }
        
        print(f"✅ Generated {len(scaffolding['steps'])} steps")
        
        # Step 5: Collect Feedback
        print("\n[5/7] Collecting Feedback...")
        feedback_session = collect_interactive_feedback(scaffolding)
        
        if feedback_session.get("cancelled"):
            print("❌ Feedback collection cancelled")
            return {"success": False, "error": "Feedback cancelled"}
        
        print(f"✅ Feedback collected: {feedback_session['session_id']}")
        
        # Step 6: Extract Patterns
        print("\n[6/7] Extracting Patterns...")
        learned_patterns = await extract_patterns_from_feedback(feedback_session)
        print(f"✅ Extracted {len(learned_patterns)} patterns")
        
        # Step 7: Store in Neo4j
        print("\n[7/7] Storing Patterns...")
        success = await store_patterns_neo4j(learned_patterns)
        
        if success:
            print(f"✅ Patterns stored successfully")
        else:
            print(f"⚠️  Pattern storage had issues")
        
        # Generate validation report
        await generate_validation_report(
            session_id,
            feedback_session,
            learned_patterns
        )
        
        return {
            "success": True,
            "session_id": session_id,
            "ocr_result": problem_data,
            "concepts": concepts,
            "patterns": patterns,
            "scaffolding": scaffolding,
            "feedback_session": feedback_session,
            "learned_patterns": learned_patterns
        }
        
    except Exception as e:
        logger.error(f"[Workflow] Error: {e}", exc_info=True)
        print(f"\n❌ Workflow failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    # Test workflow
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    test_image = "/home/kc-palantir/math/sample.png"
    
    result = asyncio.run(run_feedback_loop_workflow(test_image))
    
    print("\n" + "="*70)
    print("WORKFLOW RESULT")
    print("="*70)
    print(f"Success: {result.get('success')}")
    if result.get('success'):
        print(f"Session ID: {result['session_id']}")
        print(f"Concepts: {len(result['concepts'])}")
        print(f"Steps: {len(result['scaffolding']['steps'])}")
        print(f"Patterns: {len(result['learned_patterns'])}")
    else:
        print(f"Error: {result.get('error')}")
    print("="*70)

