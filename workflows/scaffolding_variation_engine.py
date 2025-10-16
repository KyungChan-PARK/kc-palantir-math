"""
Scaffolding Variation Engine - Dimension Assignment & Directive Generation

Generates unique variation directives for parallel scaffolding generation.
Each directive specifies a distinct pedagogical approach.

VERSION: 1.0.0
DATE: 2025-10-16
"""

from typing import Dict, List, Any
from dataclasses import dataclass
import random


# ============================================================================
# Variation Dimensions
# ============================================================================

@dataclass
class VariationDimension:
    """Definition of a scaffolding variation dimension."""
    name: str
    description: str
    instructions: List[str]
    cognitive_focus: str
    difficulty_modifier: float  # 0.8-1.2 (easier to harder)


VARIATION_DIMENSIONS = {
    "socratic_depth": VariationDimension(
        name="Socratic Depth",
        description="Maximize Socratic questioning with minimal direct instruction",
        instructions=[
            "Frame every step as a discovery question, not a directive",
            "Use 'What happens if...?' and 'Why do you think...?' phrasing",
            "Guide student to discover patterns through questions",
            "Minimize hints - let questions lead to insights",
            "Encourage hypothesis testing: 'Try it and see'",
        ],
        cognitive_focus="discovery_learning",
        difficulty_modifier=1.1  # Slightly harder (less guidance)
    ),
    
    "visual_emphasis": VariationDimension(
        name="Visual Emphasis",
        description="Emphasize geometric and graphical thinking",
        instructions=[
            "Reference visual models in every step (diagrams, graphs, number lines)",
            "Use spatial language: 'Draw', 'Visualize', 'Picture'",
            "Connect algebraic steps to geometric interpretations",
            "Include diagram descriptions in questions",
            "Leverage visual patterns and symmetries",
        ],
        cognitive_focus="visual_spatial_reasoning",
        difficulty_modifier=0.9  # Easier (visual aids help)
    ),
    
    "algebraic_rigor": VariationDimension(
        name="Algebraic Rigor",
        description="Focus on symbolic manipulation and formal notation",
        instructions=[
            "Emphasize equation transformations and symbolic operations",
            "Use precise mathematical notation in every step",
            "Build algebraic reasoning skills explicitly",
            "Include formal proof steps where appropriate",
            "Focus on general formulas before specific examples",
        ],
        cognitive_focus="symbolic_reasoning",
        difficulty_modifier=1.15  # Harder (more abstract)
    ),
    
    "metacognitive": VariationDimension(
        name="Metacognitive",
        description="Add 'why' questions and strategy awareness",
        instructions=[
            "Include 'why' questions after each major step",
            "Prompt strategy selection: 'What approach would work here?'",
            "Encourage reflection: 'What did you learn from this step?'",
            "Highlight common mistakes and how to avoid them",
            "Ask students to explain their reasoning process",
        ],
        cognitive_focus="metacognition_strategy",
        difficulty_modifier=1.0  # Neutral (adds depth, not difficulty)
    ),
    
    "minimal_hints": VariationDimension(
        name="Minimal Hints (Challenge Mode)",
        description="Sparse guidance for advanced students",
        instructions=[
            "Provide minimal hints - only when absolutely necessary",
            "Questions should be self-contained and clear",
            "Trust student ability to work through challenges",
            "Hints should point to resources, not solutions",
            "Emphasize independent problem-solving",
        ],
        cognitive_focus="independence_challenge",
        difficulty_modifier=1.2  # Harder (less support)
    ),
    
    "conceptual_bridges": VariationDimension(
        name="Conceptual Bridges",
        description="Explicit connections to related concepts",
        instructions=[
            "Connect each step to broader mathematical concepts",
            "Reference prerequisite concepts explicitly",
            "Show how this problem relates to other areas",
            "Build conceptual networks, not isolated skills",
            "Include 'This connects to...' statements",
        ],
        cognitive_focus="conceptual_connections",
        difficulty_modifier=1.05  # Slightly harder (more abstract)
    ),
    
    "real_world": VariationDimension(
        name="Real-World Application",
        description="Ground scaffolding in practical contexts",
        instructions=[
            "Frame problem in real-world scenario",
            "Use practical examples in each step",
            "Show relevance to everyday situations",
            "Include application context in questions",
            "Connect to student experiences and interests",
        ],
        cognitive_focus="applied_reasoning",
        difficulty_modifier=0.95  # Easier (concrete contexts)
    ),
}


# ============================================================================
# Variation Assignment
# ============================================================================

class VariationEngine:
    """Assigns variation dimensions to parallel agents."""
    
    def __init__(self):
        self.used_dimensions: List[str] = []
        self.dimension_performance: Dict[str, float] = {}  # dimension → avg rating
    
    def assign_dimensions(
        self,
        count: int,
        existing_variations: List[Dict[str, Any]] = None,
        prefer_high_rated: bool = False
    ) -> List[VariationDimension]:
        """
        Assign unique variation dimensions for parallel generation.
        
        Args:
            count: Number of variations to generate
            existing_variations: Already generated variations to avoid duplicates
            prefer_high_rated: Prioritize dimensions with high historical ratings
            
        Returns:
            list: VariationDimension objects for each agent
        """
        # Identify already-used dimensions
        used_dims = set()
        if existing_variations:
            for var in existing_variations:
                dim_name = var.get("variation_dimension")
                if dim_name:
                    used_dims.add(dim_name)
        
        # Available dimensions
        available = [
            dim for name, dim in VARIATION_DIMENSIONS.items()
            if name not in used_dims
        ]
        
        # If prefer_high_rated, sort by performance
        if prefer_high_rated and self.dimension_performance:
            available.sort(
                key=lambda d: self.dimension_performance.get(d.name, 0),
                reverse=True
            )
        
        # If we need more than available, allow reuse with combinations
        if count > len(available):
            # Create combined dimensions
            available.extend(self._create_combined_dimensions(count - len(available)))
        
        # Assign first N dimensions
        return available[:count]
    
    def _create_combined_dimensions(self, count: int) -> List[VariationDimension]:
        """Create combined dimension variations."""
        combinations = [
            ("socratic_depth", "visual_emphasis", "Socratic + Visual: Question-based discovery with visual models"),
            ("algebraic_rigor", "metacognitive", "Algebraic + Metacognitive: Symbolic reasoning with strategy awareness"),
            ("visual_emphasis", "real_world", "Visual + Real-world: Graphical thinking in practical contexts"),
            ("socratic_depth", "conceptual_bridges", "Socratic + Conceptual: Discovery learning with cross-concept connections"),
            ("minimal_hints", "metacognitive", "Challenge + Metacognitive: Independent solving with strategy reflection"),
        ]
        
        combined_dims = []
        for i, (dim1_name, dim2_name, description) in enumerate(combinations[:count]):
            dim1 = VARIATION_DIMENSIONS[dim1_name]
            dim2 = VARIATION_DIMENSIONS[dim2_name]
            
            combined = VariationDimension(
                name=f"{dim1.name} + {dim2.name}",
                description=description,
                instructions=dim1.instructions[:3] + dim2.instructions[:3],
                cognitive_focus=f"{dim1.cognitive_focus}+{dim2.cognitive_focus}",
                difficulty_modifier=(dim1.difficulty_modifier + dim2.difficulty_modifier) / 2
            )
            combined_dims.append(combined)
        
        return combined_dims
    
    def record_dimension_performance(self, dimension_name: str, rating: float):
        """Record performance of a dimension for future prioritization."""
        if dimension_name not in self.dimension_performance:
            self.dimension_performance[dimension_name] = rating
        else:
            # Running average
            current = self.dimension_performance[dimension_name]
            self.dimension_performance[dimension_name] = (current + rating) / 2
    
    def get_top_dimensions(self, n: int = 5) -> List[str]:
        """Get top N performing dimensions based on historical ratings."""
        if not self.dimension_performance:
            # Default order if no history
            return list(VARIATION_DIMENSIONS.keys())[:n]
        
        sorted_dims = sorted(
            self.dimension_performance.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [name for name, _ in sorted_dims[:n]]


# ============================================================================
# Directive Generation
# ============================================================================

def generate_variation_directive(
    dimension: VariationDimension,
    iteration_number: int,
    shared_context: Dict[str, Any],
    existing_variations: List[str]
) -> str:
    """
    Generate complete directive for a sub-agent.
    
    Args:
        dimension: Assigned variation dimension
        iteration_number: Iteration/variation number
        shared_context: Problem data, concepts, patterns
        existing_variations: List of already-generated variation summaries
        
    Returns:
        str: Complete prompt for sub-agent
    """
    problem_text = shared_context.get("problem_text", "")
    concepts = shared_context.get("concepts", [])
    patterns = shared_context.get("existing_patterns", [])
    
    concept_names = [c.get("name", "") for c in concepts]
    
    # Build instructions list
    instructions_text = "\n".join([f"  - {inst}" for inst in dimension.instructions])
    
    # Build existing variations summary
    existing_text = ""
    if existing_variations:
        existing_text = "\n\nEXISTING VARIATIONS (avoid duplicating these approaches):\n"
        for i, var_summary in enumerate(existing_variations, 1):
            existing_text += f"{i}. {var_summary}\n"
    
    directive = f"""
TASK: Generate scaffolding variation {iteration_number} for math problem

PROBLEM CONTEXT:
- Problem: {problem_text}
- Matched Concepts: {', '.join(concept_names)}
- Available Patterns: {len(patterns)} patterns from Neo4j

YOUR UNIQUE VARIATION DIMENSION: {dimension.name}

DIMENSION DESCRIPTION:
{dimension.description}

SPECIFIC INSTRUCTIONS FOR THIS DIMENSION:
{instructions_text}

COGNITIVE FOCUS: {dimension.cognitive_focus}
DIFFICULTY MODIFIER: {dimension.difficulty_modifier:.2f}x
{existing_text}

REQUIREMENTS:
1. Generate 6-12 progressive sub-problem steps
2. Each step MUST be a measurable problem with expected answer
3. Embody your assigned variation dimension throughout ALL steps
4. Ensure genuine pedagogical uniqueness (not just wording changes)
5. Follow JSON schema from specification exactly
6. Include validation rules for each step

OUTPUT FORMAT:
```json
{{
  "problem_id": "prob_{iteration_number}",
  "variation_dimension": "{dimension.name.lower().replace(' ', '_')}",
  "steps": [
    {{
      "step_id": 1,
      "question": "Your question here",
      "expected_answer": "Expected answer",
      "hint": "Guiding hint",
      "cognitive_type": "comprehension|concept_application|calculation|synthesis|...",
      "difficulty": 1-5
    }}
  ],
  "metadata": {{
    "pedagogy_style": "Style based on your dimension",
    "total_steps": 8,
    "variation_iteration": {iteration_number}
  }}
}}
```

DELIVERABLE: Complete scaffolding as JSON following specification.

Your variation must be PEDAGOGICALLY UNIQUE. Focus on HOW you teach, not just WHAT steps to include.
"""
    
    return directive


# ============================================================================
# Uniqueness Validation
# ============================================================================

def calculate_variation_similarity(var1: Dict, var2: Dict) -> float:
    """
    Calculate similarity between two variations.
    
    Returns:
        float: Similarity score (0.0 = completely different, 1.0 = identical)
    """
    # Compare step sequences
    steps1 = var1.get("steps", [])
    steps2 = var2.get("steps", [])
    
    if not steps1 or not steps2:
        return 0.0
    
    # Compare questions
    questions1 = set(s.get("question", "") for s in steps1)
    questions2 = set(s.get("question", "") for s in steps2)
    
    # Jaccard similarity on question keywords
    words1 = set()
    words2 = set()
    
    for q in questions1:
        words1.update(q.lower().split())
    for q in questions2:
        words2.update(q.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    
    jaccard = intersection / union if union > 0 else 0.0
    
    # Consider step count similarity
    step_count_diff = abs(len(steps1) - len(steps2)) / max(len(steps1), len(steps2))
    step_count_similarity = 1.0 - step_count_diff
    
    # Weighted average
    overall_similarity = (jaccard * 0.7) + (step_count_similarity * 0.3)
    
    return overall_similarity


def validate_uniqueness(
    new_variation: Dict,
    existing_variations: List[Dict],
    threshold: float = 0.8
) -> bool:
    """
    Validate that new variation is sufficiently unique.
    
    Args:
        new_variation: Newly generated variation
        existing_variations: All existing variations
        threshold: Maximum allowed similarity (default 0.8)
        
    Returns:
        bool: True if unique enough, False if too similar
    """
    for existing in existing_variations:
        similarity = calculate_variation_similarity(new_variation, existing)
        if similarity >= threshold:
            return False
    
    return True


# ============================================================================
# Variation Summarization
# ============================================================================

def summarize_variation(variation: Dict) -> str:
    """
    Create brief summary of variation for context sharing.
    
    Args:
        variation: Complete variation data
        
    Returns:
        str: One-line summary
    """
    dimension = variation.get("variation_dimension", "unknown")
    step_count = len(variation.get("steps", []))
    pedagogy = variation.get("metadata", {}).get("pedagogy_style", "standard")
    
    return f"{dimension} ({step_count} steps, {pedagogy} pedagogy)"

