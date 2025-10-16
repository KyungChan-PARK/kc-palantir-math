"""
Graph Scaffolding Generator - Graph-specific Problem Scaffolding

Generates scaffolding for coordinate plane and graph-based problems.

VERSION: 1.0.0
DATE: 2025-10-16
"""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


def generate_graph_scaffolding(
    problem_text: str,
    graph_data: Dict[str, Any],
    concepts: List[Dict]
) -> List[Dict[str, Any]]:
    """
    Generate scaffolding steps for graph-based problems.
    
    Args:
        problem_text: OCR extracted problem text
        graph_data: Analyzed graph data (from Vision API or Mathpix)
        concepts: Matched concepts
        
    Returns:
        list: Scaffolding steps optimized for graph problems
    """
    logger.info(f"[GraphScaffolding] Generating steps for {graph_data.get('graph_type', 'unknown')}")
    
    steps = []
    graph_type = graph_data.get("graph_type", "").lower()
    
    # Step 1: Always start with information identification
    steps.append({
        "step_id": 1,
        "question": "그래프에서 주어진 정보를 정리하세요 (점의 좌표, 함수식 등)",
        "expected_answer": "문제에 제시된 모든 정보",
        "hint": "그래프와 문제 텍스트를 모두 확인하세요",
        "cognitive_type": "comprehension",
        "difficulty": 1,
        "graph_specific": True
    })
    
    # Linear function scaffolding
    if "linear" in graph_type or "일차함수" in problem_text:
        # Extract key info from graph_data
        slope = graph_data.get("slope")
        y_intercept = graph_data.get("intercepts", {}).get("y")
        
        if y_intercept is not None:
            steps.append({
                "step_id": len(steps) + 1,
                "question": "그래프가 y축과 만나는 점(y절편)은 어디인가요?",
                "expected_answer": f"y = {y_intercept}",
                "hint": "그래프에서 x=0일 때의 y 값",
                "cognitive_type": "graph_reading",
                "difficulty": 2,
                "graph_specific": True
            })
        
        if slope is not None:
            steps.append({
                "step_id": len(steps) + 1,
                "question": "그래프의 기울기는 얼마인가요?",
                "expected_answer": str(slope),
                "hint": "y의 증가량 / x의 증가량",
                "cognitive_type": "graph_analysis",
                "difficulty": 2,
                "graph_specific": True
            })
    
    # Coordinate geometry scaffolding
    if "coordinate" in graph_type or "좌표" in problem_text:
        key_points = graph_data.get("key_points", [])
        
        if key_points:
            steps.append({
                "step_id": len(steps) + 1,
                "question": f"그래프에서 중요한 점들의 좌표를 읽으세요",
                "expected_answer": str(key_points),
                "hint": "격자선을 따라 x좌표와 y좌표를 확인하세요",
                "cognitive_type": "coordinate_reading",
                "difficulty": 2,
                "graph_specific": True
            })
    
    # Triangle area (common in coordinate geometry)
    if "삼각형" in problem_text and "넓이" in problem_text:
        steps.extend([
            {
                "step_id": len(steps) + 1,
                "question": "삼각형의 세 꼭짓점의 좌표를 그래프에서 찾으세요",
                "expected_answer": "A(...), B(...), C(...)",
                "hint": "그래프에 표시된 점들을 확인하세요",
                "cognitive_type": "graph_reading",
                "difficulty": 2,
                "graph_specific": True
            },
            {
                "step_id": len(steps) + 1,
                "question": "삼각형의 밑변을 선택하고 길이를 구하세요",
                "expected_answer": "밑변 길이 계산",
                "hint": "x축이나 y축에 평행한 변을 밑변으로 선택하면 쉽습니다",
                "cognitive_type": "strategy",
                "difficulty": 3,
                "graph_specific": True
            },
            {
                "step_id": len(steps) + 1,
                "question": "선택한 밑변에 대한 높이를 구하세요",
                "expected_answer": "높이 계산",
                "hint": "밑변에 수직인 거리",
                "cognitive_type": "calculation",
                "difficulty": 2,
                "graph_specific": True
            },
            {
                "step_id": len(steps) + 1,
                "question": "넓이 = (밑변 × 높이) / 2를 계산하세요",
                "expected_answer": "최종 넓이",
                "hint": "삼각형 넓이 공식 적용",
                "cognitive_type": "calculation",
                "difficulty": 2,
                "graph_specific": True
            }
        ])
    
    # Intersection points
    if "교점" in problem_text or "만나는 점" in problem_text:
        steps.append({
            "step_id": len(steps) + 1,
            "question": "두 직선의 교점을 구하려면 어떻게 해야 하나요?",
            "expected_answer": "두 식을 연립하여 해를 구한다",
            "hint": "y = ... 과 y = ...를 같다고 놓기",
            "cognitive_type": "concept_application",
            "difficulty": 3,
            "graph_specific": True
        })
    
    # Fallback: Generic graph scaffolding
    if len(steps) == 1:  # Only initial step
        steps.extend([
            {
                "step_id": 2,
                "question": "그래프의 주요 특징을 파악하세요 (직선/곡선, 기울기, 절편 등)",
                "expected_answer": "그래프 특징 설명",
                "hint": "그래프의 모양과 위치를 관찰하세요",
                "cognitive_type": "observation",
                "difficulty": 2,
                "graph_specific": True
            },
            {
                "step_id": 3,
                "question": "문제에서 구하고자 하는 것이 무엇인가요?",
                "expected_answer": "문제의 목표",
                "hint": "문제 마지막 부분을 확인하세요",
                "cognitive_type": "comprehension",
                "difficulty": 1,
                "graph_specific": True
            }
        ])
    
    logger.info(f"[GraphScaffolding] Generated {len(steps)} graph-specific steps")
    
    return steps


if __name__ == "__main__":
    # Test graph scaffolding generator
    logging.basicConfig(level=logging.INFO)
    
    test_graph_data = {
        "graph_type": "linear_function",
        "equation": "y = 2x + 1",
        "slope": 2,
        "intercepts": {"x": -0.5, "y": 1},
        "key_points": [[0, 1], [1, 3], [2, 5]]
    }
    
    test_problem = "일차함수 y=2x+1의 그래프가 주어졌을 때, y절편과 기울기를 구하시오"
    
    steps = generate_graph_scaffolding(test_problem, test_graph_data, [])
    
    print("\n" + "="*60)
    print("Graph Scaffolding Steps:")
    print("="*60)
    for step in steps:
        print(f"\nStep {step['step_id']}:")
        print(f"  Q: {step['question']}")
        print(f"  Type: {step['cognitive_type']}")
    print("="*60)

