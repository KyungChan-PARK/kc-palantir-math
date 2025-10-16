# Math Scaffolding Specification v1.0

## Core Challenge
Generate high-quality scaffolding for math problems that guides students through progressive sub-problems, ensuring conceptual understanding rather than mechanical calculation.

## Output Requirements

**File Naming**: `scaffolding_[problem_id]_v[iteration].json`

**Content Structure**: Scaffolding with progressive steps
```json
{
  "problem_id": "prob_YYYYMMDD_HHMMSS",
  "problem_text": "Original problem text",
  "variation_dimension": "socratic_depth | visual_emphasis | algebraic_rigor | ...",
  "concepts": ["Matched concepts"],
  "steps": [
    {
      "step_id": 1,
      "question": "Progressive sub-problem question",
      "expected_answer": "Expected student answer",
      "hint": "Guiding hint (not solution)",
      "cognitive_type": "comprehension | concept_application | calculation | synthesis | ...",
      "difficulty": 1-5,
      "validation_rule": "How to validate answer"
    }
  ],
  "metadata": {
    "total_steps": 8,
    "difficulty_curve": "gradual | steep | adaptive",
    "pedagogy_style": "socratic | direct | discovery",
    "generated_at": "ISO timestamp"
  }
}
```

## Variation Dimensions

Each scaffolding iteration must embody a distinctive pedagogical approach:

### Dimension Categories
- **Socratic Depth**: Maximize questioning, minimal direct instruction, student discovery
- **Visual Emphasis**: Geometric reasoning, diagrams, spatial thinking primacy
- **Algebraic Rigor**: Symbolic manipulation focus, formal notation, equation solving
- **Metacognitive**: "Why" questions, reflection prompts, strategy awareness
- **Minimal Hints**: Challenge mode with sparse guidance, student independence
- **Conceptual Bridges**: Explicit connections to related concepts, cross-domain links
- **Real-World Context**: Application scenarios, practical examples, relevance

### Dimension Implementation
- **Step Progression**: How difficulty increases across steps
- **Question Phrasing**: Language style (Socratic vs direct vs exploratory)
- **Hint Strategy**: When/how hints are provided
- **Cognitive Mix**: Balance of comprehension, application, synthesis, evaluation
- **Validation**: How student understanding is checked

## Quality Criteria

### Scaffolding Effectiveness (Target: >8.0/10)
- **Cognitive Progression**: Each step builds on previous (no jumps)
- **Difficulty Curve**: Gradual increase, no sudden spikes
- **Hint Quality**: Guides without solving, appropriate difficulty
- **Completeness**: Covers all sub-skills needed for target problem
- **Clarity**: Questions are unambiguous and grade-appropriate

### Uniqueness Requirements (Target: >0.8 similarity score)
- **Step Sequence**: Different ordering or grouping of sub-problems
- **Question Phrasing**: Distinct wording even for similar cognitive goals
- **Pedagogical Approach**: Unique teaching strategy per variation
- **Cognitive Focus**: Different emphasis (visual vs algebraic vs metacognitive)

### Specification Compliance (Target: 100%)
- **JSON Schema**: Valid structure, all required fields present
- **Step Count**: 6-12 steps (optimal range for middle school)
- **Difficulty Range**: Steps span 1-5 difficulty scale appropriately
- **Cognitive Coverage**: Multiple cognitive types represented
- **Hint Appropriateness**: Hints don't reveal answers directly

## Enhancement Principles

### Progressive Sub-Problems
- Each step is a **measurable problem**, not just a hint
- Students can succeed/fail at each step independently
- Clear expected answers enable automated validation
- Cognitive type classification enables learning analytics

### Adaptive Difficulty
- First steps: Low difficulty (1-2), build confidence
- Middle steps: Moderate difficulty (2-3), core work
- Final steps: Higher difficulty (3-5), synthesis and extension

### Metacognitive Integration
- Include "why" questions at key transitions
- Prompt strategy awareness ("What approach would work here?")
- Encourage reflection on learning process

## Success Metrics

### Teacher Rating (Collected via Feedback)
- Overall scaffolding quality: 1-5 scale
- Individual step quality: 1-5 scale
- Suggested improvements: Free text
- **Target**: Average rating ≥ 4.0/5.0

### Student Performance (Measured)
- Step completion rate: % of students completing each step
- Time per step: Average seconds to solve
- Mistake count: Attempts before correct answer
- **Target**: >80% completion rate per step

### Pattern Reusability
- Pattern applicability: How many problems can use this pattern
- Pattern effectiveness: Improvement when pattern applied
- **Target**: ≥3 problems per pattern, ≥20% improvement

## Variation Strategy

For N iterations, assign variation dimensions cyclically:
1. **Socratic Depth** - Question-based discovery
2. **Visual Emphasis** - Geometric/graphical thinking
3. **Algebraic Rigor** - Symbolic manipulation
4. **Metacognitive** - Strategy and reflection
5. **Minimal Hints** - Challenge mode
6. **Conceptual Bridges** - Cross-concept connections
7. **Real-World** - Application context

## Example Variations

### Problem: "60을 소인수분해하시오"

**Variation 1 (Socratic)**:
```
Step 1: "60은 어떤 종류의 수인가요? (짝수? 홀수?)"
Step 2: "짝수라면 어떤 소수로 나눌 수 있을까요?"
Step 3: "왜 가장 작은 소수부터 나누는 것이 좋을까요?"
...
```

**Variation 2 (Visual)**:
```
Step 1: "60을 작은 블록들로 나누어 봅시다. 2개씩 나누면?"
Step 2: "30개 블록이 남았네요. 또 2개씩 나누면?"
Step 3: "이제 15개. 그림으로 그려보면 어떤 모양일까요?"
...
```

**Variation 3 (Algebraic)**:
```
Step 1: "60 = 2 × ? 를 만족하는 ?는?"
Step 2: "60 = 2 × 30 = 2 × 2 × ? 다음은?"
Step 3: "지수 표기법으로 나타내면?"
...
```

Generate unique, effective, specification-compliant scaffolding variations.

