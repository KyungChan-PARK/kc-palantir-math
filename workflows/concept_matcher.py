"""
Concept Matcher - Match Problem Text to Concepts

Identifies relevant mathematical concepts from problem text using keyword matching.

VERSION: 1.0.0
DATE: 2025-10-16
"""

import json
from pathlib import Path
from typing import List, Dict, Any
import logging

from tools.observability_hook import send_hook_event
from workflows.hook_events import HookEventType

logger = logging.getLogger(__name__)

CONCEPTS_DIR = Path("/home/kc-palantir/math/data/concepts")


def load_all_concepts() -> List[Dict[str, Any]]:
    """
    Load all concept definitions from JSON files.
    
    Returns:
        list: All concepts from middle-1-1 through middle-3-2
    """
    all_concepts = []
    
    concept_files = [
        "middle-1-1.json",
        "middle-1-2.json",
        "middle-2-1.json",
        "middle-2-2.json",
        "middle-3-1.json",
        "middle-3-2.json"
    ]
    
    for filename in concept_files:
        filepath = CONCEPTS_DIR / filename
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    concepts = data.get("concepts", [])
                    all_concepts.extend(concepts)
                    logger.debug(f"[ConceptMatcher] Loaded {len(concepts)} concepts from {filename}")
            except Exception as e:
                logger.error(f"[ConceptMatcher] Failed to load {filename}: {e}")
    
    logger.info(f"[ConceptMatcher] Total concepts loaded: {len(all_concepts)}")
    return all_concepts


def calculate_relevance_score(problem_text: str, concept: Dict[str, Any]) -> float:
    """
    Calculate relevance score between problem text and concept.
    
    Simple keyword-based matching for now.
    
    Args:
        problem_text: OCR extracted problem text
        concept: Concept data from JSON
        
    Returns:
        float: Relevance score (0.0 - 1.0)
    """
    score = 0.0
    problem_lower = problem_text.lower()
    
    # Check concept name
    concept_name = concept.get("name", "").lower()
    if concept_name in problem_lower:
        score += 0.5
    
    # Check keywords in concept name
    name_keywords = concept_name.split()
    for keyword in name_keywords:
        if len(keyword) > 1 and keyword in problem_lower:
            score += 0.1
    
    # Check tags
    tags = concept.get("tags", [])
    for tag in tags:
        if tag.lower() in problem_lower:
            score += 0.15
    
    # Check content
    content = concept.get("content", "").lower()
    content_keywords = set(content.split())
    problem_keywords = set(problem_lower.split())
    common_keywords = content_keywords & problem_keywords
    
    if common_keywords:
        score += 0.2 * (len(common_keywords) / len(problem_keywords))
    
    # Specific keyword matching
    keyword_map = {
        "소인수분해": ["소인수", "분해하시오", "소수의 곱"],
        "방정식": ["방정식", "해를 구하시오", "풀이"],
        "일차함수": ["일차함수", "그래프", "기울기", "y절편", "좌표평면"],
        "좌표": ["좌표", "점", "좌표평면", "\\(", "\\mathrm"],
        "도형": ["삼각형", "사각형", "원", "넓이", "둘레"],
        "확률": ["확률", "경우의 수"],
    }
    
    for concept_keyword, related_keywords in keyword_map.items():
        if concept_keyword in concept_name:
            for kw in related_keywords:
                if kw in problem_lower:
                    score += 0.2  # Increased weight for keyword matches
    
    # Cap at 1.0
    return min(score, 1.0)


def identify_concepts(problem_data: Dict[str, Any], top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Identify top-k most relevant concepts for the problem.
    
    Args:
        problem_data: OCR result with text and latex
        top_k: Number of top concepts to return
        
    Returns:
        list: Top-k concepts with relevance scores
    """
    send_hook_event(
        "concept_matcher",
        HookEventType.CONCEPT_MATCH_STARTED,
        {
            "text_preview": problem_data.get("text", "")[:100],
            "top_k": top_k
        }
    )
    
    logger.info(f"[ConceptMatcher] Identifying concepts for problem...")
    
    problem_text = problem_data.get("text", "") + " " + problem_data.get("latex", "")
    
    # Load all concepts
    all_concepts = load_all_concepts()
    
    # Calculate relevance scores
    scored_concepts = []
    for concept in all_concepts:
        score = calculate_relevance_score(problem_text, concept)
        if score > 0.1:  # Only include if some relevance
            scored_concepts.append({
                "concept_id": concept.get("concept_id"),
                "name": concept.get("name"),
                "content": concept.get("content"),
                "grade": concept.get("grade"),
                "semester": concept.get("semester"),
                "chapter": concept.get("chapter", {}).get("name"),
                "tags": concept.get("tags", []),
                "relevance_score": score
            })
    
    # Sort by score and get top-k
    scored_concepts.sort(key=lambda x: x["relevance_score"], reverse=True)
    top_concepts = scored_concepts[:top_k]
    
    logger.info(f"[ConceptMatcher] Top {len(top_concepts)} concepts identified:")
    for i, concept in enumerate(top_concepts, 1):
        logger.info(f"  {i}. {concept['name']} (score: {concept['relevance_score']:.3f})")
    
    send_hook_event(
        "concept_matcher",
        HookEventType.CONCEPT_MATCH_COMPLETED,
        {
            "concepts_found": len(top_concepts),
            "top_concept": top_concepts[0]["concept_id"] if top_concepts else None,
            "top_score": top_concepts[0]["relevance_score"] if top_concepts else 0
        }
    )
    
    return top_concepts


if __name__ == "__main__":
    # Test concept matcher
    logging.basicConfig(level=logging.INFO)
    
    test_problem = {
        "text": "60을 소인수분해하시오",
        "latex": "60 = 2^2 \\times 3 \\times 5"
    }
    
    concepts = identify_concepts(test_problem, top_k=5)
    
    print("\n" + "="*60)
    print("Top Matched Concepts:")
    print("="*60)
    for i, concept in enumerate(concepts, 1):
        print(f"\n{i}. {concept['name']} ({concept['concept_id']})")
        print(f"   Score: {concept['relevance_score']:.3f}")
        print(f"   Chapter: {concept['chapter']}")
        print(f"   Tags: {', '.join(concept['tags'])}")
    print("="*60)

