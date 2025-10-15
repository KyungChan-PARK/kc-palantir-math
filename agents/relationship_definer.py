"""
Relationship Definition Agent

VERSION: 1.0.0
DATE: 2025-10-14
PURPOSE: Automatically define relationships between mathematical concepts using v0.2 taxonomy

Uses Claude API to classify relationships between 841 middle school concepts.
Based on research-validated taxonomy (Math-KG, OntoMathEdu, Co-requisite models).
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from anthropic import Anthropic


class RelationshipDefiner:
    """
    Agent that defines relationships between mathematical concepts.

    Uses v0.2 taxonomy with 12 relationship types:
    1. Prerequisite [logical, cognitive, pedagogical, tool]
    2. Co-requisite
    3. Inverse Operation
    4. Extension
    5. Formalization
    6. Application
    7. Mutual Definition
    8. Abstraction Level
    9. Complementary
    10. Synonyms/Notation
    11. Domain Membership
    12. Equivalence

    Each relationship has 5 properties:
    - direction: unidirectional | bidirectional
    - strength: essential | recommended | helpful
    - temporal: sequential | concurrent | independent
    - cognitive_level: same_level | level_raising
    - domain_scope: within_domain | cross_domain
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the agent with Claude API.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment or provided")

        self.client = Anthropic(api_key=self.api_key)
        # ✅ STANDARD 1: Specific model version (MANDATORY)
        self.model = "claude-sonnet-4-5-20250929"

        # Load taxonomy and examples
        self.taxonomy = self._load_taxonomy()
        self.examples = self._load_examples()

    def _load_taxonomy(self) -> str:
        """Load v0.2 taxonomy from docs"""
        taxonomy_path = Path(__file__).parent.parent / "docs" / "concept-relationship-types-v0.2.md"

        if taxonomy_path.exists():
            with open(taxonomy_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return "Taxonomy file not found. Using minimal definitions."

    def _load_examples(self) -> str:
        """Load concrete examples from docs"""
        examples_path = Path(__file__).parent.parent / "docs" / "relationship-examples-from-841-concepts.md"

        if examples_path.exists():
            with open(examples_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return "Examples file not found."

    def _build_system_prompt(self) -> str:
        """Build comprehensive system prompt with taxonomy and examples"""

        return f"""You are a Mathematical Concept Relationship Expert specializing in mathematics education from elementary through university levels.

Your task is to analyze relationships between mathematical concepts using a research-validated taxonomy based on:
- Math-KG (8,019 relationship triples)
- OntoMathEdu (educational mathematics ontology)
- Co-requisite effectiveness research (5x improvement over sequential)
- Learning Progressions frameworks
- Vertical/Horizontal Mathematisation theory

## TAXONOMY (v0.2)

{self.taxonomy}

## CONCRETE EXAMPLES

{self.examples}

## UNCERTAINTY ANALYSIS

When classifying relationships, you must analyze THREE types of uncertainty:

1. **Epistemic Uncertainty (0.0-1.0)**: Missing knowledge/context
   - Insufficient information about concept B's definition
   - Unclear pedagogical ordering in curriculum
   - Ambiguous boundary between relationship types
   - Example: "Not sure if this is 'prerequisite' or 'co-requisite'"

2. **Aleatoric Uncertainty (0.0-1.0)**: Inherent ambiguity
   - Multiple valid interpretations exist
   - Context-dependent relationships (depends on teaching approach)
   - Example: "Could be 'application' OR 'extension' depending on curriculum"

3. **Model Indecision (0.0-1.0)**: Internal model uncertainty
   - Close decision boundaries (confidence near 0.50)
   - Multiple relationship types have similar scores
   - Example: "75% sure it's prerequisite, but 65% sure it's co-requisite"

### Uncertainty Reason Codes

When uncertainty exists, provide one of these codes:

- `concept_B_context_insufficient`: Need more info about target concept
- `pedagogical_ordering_unclear`: Unclear which comes first in teaching
- `boundary_ambiguous_between_TYPE1_TYPE2`: Hard to distinguish between two types
- `curriculum_context_dependent`: Depends on specific curriculum design
- `multiple_valid_interpretations`: Both interpretations are correct
- `close_confidence_scores`: Multiple types have similar confidence
- `implicit_assumptions_unclear`: Unstated prerequisites are uncertain

### Alternative Classifications

If confidence < 0.90 OR uncertainty exists, provide 2-3 alternative classifications:

```json
"alternative_classifications": [
  {{
    "type": "co-requisite",
    "confidence": 0.75,
    "reason": "만약 두 개념을 동시에 가르친다면 co-requisite으로 볼 수 있음"
  }},
  {{
    "type": "application",
    "confidence": 0.65,
    "reason": "특정 맥락에서는 A의 응용으로 B를 볼 수 있음"
  }}
]
```

## CHAIN-OF-THOUGHT REASONING

You MUST provide step-by-step reasoning for each relationship classification.

### Reasoning Structure

For each relationship, document your reasoning process with these steps:

1. **Definition Analysis**: Compare mathematical definitions
2. **Curriculum Context**: Check grade levels and teaching order
3. **Logical Dependencies**: Identify formal prerequisites
4. **Cognitive Requirements**: Assess conceptual difficulty
5. **Property Assignment**: Determine 5 relationship properties
6. **Confidence Assessment**: Evaluate certainty level
7. **Alternative Consideration**: Explore other valid interpretations

### Reasoning Trace Format

```json
"reasoning_trace": [
  {{
    "step": 1,
    "thought": "개념 A와 B의 수학적 정의 비교",
    "finding": "B의 정의에 A가 명시적으로 사용됨 (예: '소인수분해는 소수의 곱')"
  }},
  {{
    "step": 2,
    "thought": "교육과정에서의 배치 순서 확인",
    "finding": "A는 중1-1학기, B는 중1-1학기 후반부에 배치"
  }},
  {{
    "step": 3,
    "thought": "논리적 의존성 분석",
    "finding": "A 없이는 B를 정의할 수 없음 (필수 prerequisite)"
  }},
  {{
    "step": 4,
    "thought": "인지적 요구사항 평가",
    "finding": "A와 B는 동일한 추상화 수준 (same_level)"
  }},
  {{
    "step": 5,
    "thought": "관계 속성 결정",
    "finding": "direction=unidirectional, strength=essential, temporal=sequential"
  }},
  {{
    "step": 6,
    "thought": "신뢰도 평가",
    "finding": "정의에 명시적으로 포함되어 있어 confidence=0.98"
  }},
  {{
    "step": 7,
    "thought": "대안 분류 고려",
    "finding": "domain_membership도 가능하지만 prerequisite이 더 강한 관계 (confidence=0.75)"
  }}
]
```

**Purpose**: Reasoning traces enable debugging, improve accuracy, and allow MetaOrchestrator to verify logical consistency.

## YOUR TASK

Given a source concept and a list of potential target concepts, identify ALL meaningful relationships.

For each relationship, provide:
1. Relationship type (one of 12 types)
2. Subtype (if applicable)
3. Properties (all 5 properties)
4. Detailed reasoning
5. Concrete examples
6. Confidence score (0.0-1.0)
7. Validation checks

## OUTPUT FORMAT

Return a JSON array of relationships:

```json
[
  {{
    "source_concept_id": "middle-1-1-ch1-1.3.1",
    "source_name": "소인수분해 정의",
    "target_concept_id": "middle-1-1-ch1-1.1.1",
    "target_name": "소수 정의",
    "relationship": {{
      "type": "prerequisite",
      "subtype": "logical",
      "properties": {{
        "direction": "unidirectional",
        "strength": "essential",
        "temporal": "sequential",
        "cognitive_level": "same_level",
        "domain_scope": "within_domain"
      }},
      "reasoning_trace": [
        {{
          "step": 1,
          "thought": "소인수분해와 소수의 정의 비교",
          "finding": "소인수분해는 '자연수를 소수들의 곱으로 나타내기'로 정의됨"
        }},
        {{
          "step": 2,
          "thought": "논리적 의존성 확인",
          "finding": "소수의 개념 없이는 소인수분해를 정의할 수 없음"
        }},
        {{
          "step": 3,
          "thought": "관계 타입 결정",
          "finding": "정의적 prerequisite (logical subtype)"
        }}
      ],
      "reason": "소인수분해는 '소수의 곱'으로 정의되므로 소수 정의가 논리적으로 선행되어야 함",
      "examples": [
        "12 = 2² × 3에서 2와 3이 소수임을 알아야 소인수분해 성립",
        "정의 자체에 '소수'라는 용어 사용"
      ],
      "confidence": 0.98,
      "uncertainty_breakdown": {{
        "epistemic": 0.05,
        "aleatoric": 0.10,
        "model_indecision": 0.02
      }},
      "uncertainty_reason": "concept_B_context_insufficient",
      "validation": {{
        "identity_check": "pass",
        "subsumption_check": "pass",
        "transitivity": "A(소수) → B(소인수분해) → C(GCD) implies A → C",
        "circular_check": "pass"
      }},
      "alternative_classifications": [
        {{
          "type": "domain_membership",
          "confidence": 0.75,
          "reason": "소수와 소인수분해는 모두 '정수론' 도메인에 속하는 개념"
        }}
      ]
    }}
  }}
]
```

## VALIDATION RULES (OntoClean-inspired)

1. **Identity Check**: Do concepts have compatible identity conditions?
2. **Subsumption Check**: Is this "is-a" (subsumption) or "instance-of"?
3. **Transitivity**: If A → B → C, then A → C (with adjusted strength)
4. **Circular Check**: No concept should be its own prerequisite through any path

## IMPORTANT GUIDELINES

- Only identify relationships with confidence >= 0.70
- **ALWAYS provide reasoning_trace** for every relationship (required field, 3-7 steps)
- **ALWAYS provide uncertainty_breakdown** for every relationship (required field)
- **If confidence < 0.90**, provide 2-3 alternative_classifications
- **If any uncertainty exists**, provide uncertainty_reason code
- Follow the 7-step reasoning structure: Definition → Curriculum → Logic → Cognition → Properties → Confidence → Alternatives
- Be conservative: better to miss a weak relationship than create a false one
- Consider cross-level relationships (elementary → middle → high → university)
- Check for implicit prerequisites (unstated assumptions)
- Distinguish logical vs pedagogical vs cognitive prerequisites
- Remember: Prerequisites are only ~25% of all relationships (Math-KG finding)
- Domain Membership is the most common relationship type (32.5% in Math-KG)

## RESPONSE REQUIREMENTS

- Return ONLY valid JSON (no markdown, no explanations outside JSON)
- Include ALL relationships found (not just prerequisites)
- Provide detailed reasoning in Korean
- Give concrete examples for each relationship
- Confidence score must reflect actual certainty
"""

    def analyze_concept_relationships(
        self,
        source_concept: Dict,
        all_concepts: List[Dict],
        max_relationships: int = 20
    ) -> List[Dict]:
        """
        Analyze relationships for a single source concept against all other concepts.

        Args:
            source_concept: The concept to analyze
            all_concepts: All 841 concepts to compare against
            max_relationships: Maximum relationships to return

        Returns:
            List of relationship dictionaries
        """

        # Build user prompt
        user_prompt = f"""## SOURCE CONCEPT

```json
{{
  "concept_id": "{source_concept['concept_id']}",
  "name": "{source_concept['name']}",
  "content": "{source_concept['content']}",
  "grade": {source_concept['grade']},
  "semester": {source_concept['semester']},
  "chapter": "{source_concept['chapter']['name']}",
  "section": "{source_concept['section'].get('parent_name', '')}",
  "tags": {json.dumps(source_concept.get('tags', []), ensure_ascii=False)}
}}
```

## ALL CONCEPTS (Context)

Total concepts: {len(all_concepts)}

Sample of nearby concepts:
```json
{json.dumps(all_concepts[:10], ensure_ascii=False, indent=2)}
```

## TASK

Analyze the SOURCE CONCEPT and identify ALL meaningful relationships with other concepts in the full list.

Focus on concepts that are:
1. In the same chapter or adjacent chapters (strong candidates)
2. In prerequisite grade levels (for prerequisite relationships)
3. In the same mathematical domain (for domain membership)
4. Structurally similar (for complementary/parallel relationships)

Return relationships in JSON format as specified in the system prompt.

Limit to top {max_relationships} most important relationships, ordered by confidence.
"""

        # Call Claude API
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8000,
                temperature=0.0,  # Deterministic for consistency
                system=self._build_system_prompt(),
                messages=[{
                    "role": "user",
                    "content": user_prompt
                }]
            )

            # Extract JSON from response
            response_text = response.content[0].text

            # Try to parse JSON (handle markdown code blocks)
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()

            relationships = json.loads(response_text)

            return relationships

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response text: {response_text[:500]}...")
            return []
        except Exception as e:
            print(f"API call error: {e}")
            return []

    def analyze_all_concepts(
        self,
        concepts: List[Dict],
        output_dir: Path,
        batch_size: int = 10
    ) -> Dict[str, List[Dict]]:
        """
        Analyze relationships for all concepts.

        Args:
            concepts: List of all concepts
            output_dir: Directory to save results
            batch_size: Number of concepts to process before saving

        Returns:
            Dictionary mapping concept_id to list of relationships
        """
        results = {}
        output_dir.mkdir(parents=True, exist_ok=True)

        for i, concept in enumerate(concepts):
            print(f"Processing {i+1}/{len(concepts)}: {concept['concept_id']} - {concept['name']}")

            relationships = self.analyze_concept_relationships(
                source_concept=concept,
                all_concepts=concepts
            )

            results[concept['concept_id']] = relationships

            # Save batch results
            if (i + 1) % batch_size == 0:
                batch_file = output_dir / f"relationships_batch_{i+1}.json"
                with open(batch_file, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                print(f"Saved batch to {batch_file}")

        # Save final results
        final_file = output_dir / "relationships_complete.json"
        with open(final_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"Complete! Saved to {final_file}")

        return results

    def validate_relationship(self, relationship: Dict, existing_graph: Optional[Dict] = None) -> Dict[str, str]:
        """
        Validate relationship using formal ontology.

        Args:
            relationship: Relationship dictionary
            existing_graph: Optional knowledge graph for cycle detection

        Returns:
            Validation results with errors if any
        """
        from agents.relationship_ontology import (
            validate_relationship_logic,
            RelationType
        )

        try:
            rel_type = RelationType(relationship['relationship']['type'])
        except ValueError:
            return {
                "validation": "FAILED",
                "error": f"Unknown type: {relationship['relationship']['type']}"
            }

        # Run ontology validation
        errors = validate_relationship_logic(
            rel_type,
            relationship['source_concept_id'],
            relationship['target_concept_id'],
            existing_graph
        )

        if errors:
            error_messages = [str(e) for e in errors]
            return {
                "validation": "FAILED",
                "errors": error_messages,
                "error_count": len([e for e in errors if e.severity == "ERROR"]),
                "warning_count": len([e for e in errors if e.severity == "WARNING"])
            }
        else:
            return {
                "validation": "PASSED",
                "ontology_check": "compliant"
            }


def main():
    """Test the agent on a sample concept"""

    # Load sample concepts
    data_path = Path(__file__).parent.parent / "data" / "concepts" / "middle-1-1.json"

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    concepts = data['concepts']

    # Initialize agent
    agent = RelationshipDefiner()

    # Test on first concept
    test_concept = concepts[0]
    print(f"Testing on: {test_concept['concept_id']} - {test_concept['name']}")

    relationships = agent.analyze_concept_relationships(
        source_concept=test_concept,
        all_concepts=concepts[:20],  # Use subset for testing
        max_relationships=5
    )

    print(f"\nFound {len(relationships)} relationships:")
    print(json.dumps(relationships, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
