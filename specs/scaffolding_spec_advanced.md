# Advanced Math Scaffolding Specification v2.0

## Core Challenge
Generate sophisticated, multi-modal scaffolding that adapts to student performance clusters and integrates cross-concept synthesis.

## Advanced Variation Dimensions

### Wave 2+ Enhancements

#### Multi-Modal Integration
Combine multiple representation systems:
- **Symbolic**: Algebraic notation, equations
- **Visual**: Diagrams, graphs, geometric models  
- **Verbal**: Natural language explanations
- **Numeric**: Concrete examples, patterns

Example: "Draw the number line (visual) showing 60 ÷ 2 = 30 (symbolic) which means half of 60 (verbal) is 30 (numeric)"

#### Adaptive Difficulty Branching
Based on student's PerformanceCluster:
- **High-performing**: Skip basic steps, add extension problems
- **Average**: Standard progression with moderate hints
- **Struggling**: More granular steps, stronger scaffolding

#### Cross-Concept Synthesis
Explicit connections between concepts:
- "소인수분해는 어떻게 최대공약수와 연결되나요?"
- "좌표평면의 넓이 구하기는 어떤 대수적 공식과 같나요?"
- Integration of 2-3 concepts per scaffolding

#### Metacognitive Sophistication
Advanced strategy awareness:
- "이 문제를 푸는 여러 방법 중 어떤 것이 가장 효율적일까요?"
- "막혔을 때 어떤 전략을 사용할 수 있을까요?"
- "이 단계에서 실수하기 쉬운 부분은 무엇일까요?"

### Progressive Sophistication Strategy

**Wave 1**: Basic variation dimensions (single focus)
- Socratic OR Visual OR Algebraic

**Wave 2**: Multi-dimensional combinations (dual focus)
- Socratic + Visual
- Algebraic + Metacognitive  
- Minimal Hints + Conceptual Bridges

**Wave 3**: Adaptive + Multi-modal (triple focus)
- Performance-adaptive + Multi-modal + Cross-concept
- Socratic + Visual + Real-world

**Wave N**: Revolutionary pedagogies
- Game-based scaffolding
- Peer teaching simulation
- Error-driven learning (intentional mistakes)

## Enhanced Quality Criteria

### Cognitive Depth (Target: >9.0/10)
- Multiple representation systems per problem
- Explicit strategy instruction
- Connection to broader mathematical ideas
- Transfer potential to other domains

### Pedagogical Innovation (Target: >8.5/10)
- Novel teaching approaches
- Student agency and choice
- Formative assessment integration
- Growth mindset reinforcement

### Adaptability (Target: >8.0/10)
- Performance cluster differentiation
- Branching paths for different student responses
- Dynamic hint revelation based on struggles

## Advanced Output Format

```json
{
  "problem_id": "prob_advanced_001",
  "variation_dimension": "multi_modal_adaptive",
  "performance_cluster": "high | average | struggling",
  "steps": [...],
  "branching_paths": {
    "step_3_correct": [4, 5, 6],
    "step_3_incorrect": [4a, 4b, 5]
  },
  "multi_modal_components": {
    "visual_aids": ["diagram_url_1", "graph_url_2"],
    "symbolic_forms": ["latex_1", "latex_2"],
    "verbal_explanations": ["text_1", "text_2"]
  },
  "cross_concept_links": [
    {"from_step": 5, "to_concept": "최대공약수", "relationship": "prerequisite"},
    {"from_step": 7, "to_concept": "약수", "relationship": "application"}
  ],
  "metacognitive_prompts": [
    {"after_step": 3, "prompt": "여기까지의 전략을 설명해보세요"},
    {"after_step": 6, "prompt": "다른 방법은 없을까요?"}
  ]
}
```

## Meta-Pattern Extraction

When analyzing 5+ variations, extract meta-patterns:

### Pattern Types
- **Structural Patterns**: Common step sequences across variations
- **Pedagogical Patterns**: Effective teaching strategies identified
- **Difficulty Patterns**: Optimal difficulty progressions
- **Hint Patterns**: Most effective hint formulations
- **Engagement Patterns**: Which variations students prefer

### Meta-Pattern Format
```json
{
  "meta_pattern_id": "mp_optimal_prime_factorization_flow",
  "extracted_from": ["variation_1", "variation_3", "variation_7"],
  "pattern_type": "structural",
  "description": "Across 3 high-rated variations, the pattern of (even check → divide by 2 → repeat → prime check) scored 4.5+ average",
  "applicability": "All prime factorization problems",
  "effectiveness_evidence": {
    "avg_teacher_rating": 4.7,
    "avg_student_completion": 0.92,
    "avg_time_per_step": 45
  },
  "recommended_for_clusters": ["average", "high"]
}
```

## Specification Evolution Protocol

After each wave, evolve the specification:

1. **Analyze Feedback**: Which dimensions rated highest
2. **Identify Gaps**: What wasn't covered well
3. **Synthesize Insights**: Meta-patterns from variations
4. **Update Spec**: Add new quality criteria, refine dimensions
5. **Progressive Complexity**: Next wave tackles harder dimensions

Example evolution:
```
Wave 1 Spec → Basic variations (7 dimensions)
  ↓ Feedback: Visual emphasis rated 4.8/5.0
Wave 2 Spec → Visual + X combinations prioritized
  ↓ Feedback: Visual + Metacognitive = 4.9/5.0
Wave 3 Spec → Visual + Metacognitive + Multi-modal
```

Generate increasingly sophisticated scaffolding through specification-driven evolution.

