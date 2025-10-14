"""
Test Relationship Definer on 20 Sample Concepts

PURPOSE: Validate relationship classification quality before running on full 841 concepts
TESTS:
- Confidence score distribution
- Reasoning trace quality
- Uncertainty measurement
- Alternative classifications
- OntoClean validation
"""

import json
import os
from pathlib import Path
from agents.relationship_definer import RelationshipDefiner

def select_diverse_sample(concepts, sample_size=20):
    """
    Select diverse sample from concepts.

    Strategy:
    - Take first 10 (basic concepts: prime, composite, exponents)
    - Take every 5th from remaining (spread across chapters)
    - Include concepts with different difficulty levels
    """

    # First 10 concepts (basic)
    sample = concepts[:10]

    # Every 5th concept from remaining
    remaining = concepts[10:]
    for i in range(0, len(remaining), 5):
        if len(sample) >= sample_size:
            break
        sample.append(remaining[i])

    return sample[:sample_size]

def analyze_test_results(relationships):
    """Analyze quality of relationship classifications"""

    if not relationships:
        print("⚠️ No relationships found")
        return

    print("\n" + "="*60)
    print("TEST RESULTS ANALYSIS")
    print("="*60)

    # 1. Confidence distribution
    confidences = [r['relationship']['confidence'] for r in relationships]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0

    print(f"\n📊 Confidence Scores:")
    print(f"  Total relationships: {len(relationships)}")
    print(f"  Average confidence: {avg_confidence:.3f}")
    print(f"  Min confidence: {min(confidences):.3f}")
    print(f"  Max confidence: {max(confidences):.3f}")
    print(f"  High confidence (≥0.90): {sum(1 for c in confidences if c >= 0.90)}")
    print(f"  Medium confidence (0.70-0.89): {sum(1 for c in confidences if 0.70 <= c < 0.90)}")

    # 2. Relationship type distribution
    from collections import Counter
    types = [r['relationship']['type'] for r in relationships]
    type_counts = Counter(types)

    print(f"\n🔗 Relationship Types:")
    for rel_type, count in type_counts.most_common():
        percentage = (count / len(relationships)) * 100
        print(f"  {rel_type}: {count} ({percentage:.1f}%)")

    # 3. Uncertainty analysis
    uncertainties = [r['relationship'].get('uncertainty_breakdown', {}) for r in relationships]
    has_uncertainty = sum(1 for u in uncertainties if u)

    print(f"\n🎲 Uncertainty Measurement:")
    print(f"  Relationships with uncertainty data: {has_uncertainty}/{len(relationships)}")

    if has_uncertainty > 0:
        epistemic_avg = sum(u.get('epistemic', 0) for u in uncertainties) / has_uncertainty
        aleatoric_avg = sum(u.get('aleatoric', 0) for u in uncertainties) / has_uncertainty
        model_avg = sum(u.get('model_indecision', 0) for u in uncertainties) / has_uncertainty

        print(f"  Average epistemic: {epistemic_avg:.3f}")
        print(f"  Average aleatoric: {aleatoric_avg:.3f}")
        print(f"  Average model_indecision: {model_avg:.3f}")

    # 4. Reasoning trace quality
    has_reasoning = sum(1 for r in relationships if 'reasoning_trace' in r['relationship'])

    print(f"\n🧠 Reasoning Traces:")
    print(f"  Relationships with reasoning: {has_reasoning}/{len(relationships)}")

    if has_reasoning > 0:
        avg_steps = sum(len(r['relationship'].get('reasoning_trace', [])) for r in relationships) / has_reasoning
        print(f"  Average reasoning steps: {avg_steps:.1f}")

    # 5. Alternative classifications
    has_alternatives = sum(1 for r in relationships if 'alternative_classifications' in r['relationship'])

    print(f"\n🔄 Alternative Classifications:")
    print(f"  Relationships with alternatives: {has_alternatives}/{len(relationships)}")

    # 6. Validation results
    has_validation = sum(1 for r in relationships if 'validation' in r['relationship'])

    print(f"\n✅ OntoClean Validation:")
    print(f"  Relationships with validation: {has_validation}/{len(relationships)}")

    # 7. Sample detailed output
    print(f"\n📋 Sample Relationship (First):")
    if relationships:
        sample = relationships[0]
        print(f"  Source: {sample['source_name']}")
        print(f"  Target: {sample['target_name']}")
        print(f"  Type: {sample['relationship']['type']}")
        print(f"  Confidence: {sample['relationship']['confidence']:.3f}")
        print(f"  Reason: {sample['relationship']['reason'][:100]}...")

def main():
    print("="*60)
    print("RELATIONSHIP DEFINER - 20 SAMPLE TEST")
    print("="*60)

    # Load concepts
    data_path = Path(__file__).parent / "data" / "concepts" / "middle-1-1.json"

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_concepts = data['concepts']

    print(f"\n📚 Loaded {len(all_concepts)} concepts from middle-1-1.json")

    # Select 20 diverse samples
    sample_concepts = select_diverse_sample(all_concepts, sample_size=20)

    print(f"\n✅ Selected {len(sample_concepts)} sample concepts:")
    for i, concept in enumerate(sample_concepts, 1):
        print(f"  {i}. {concept['concept_id']}: {concept['name']} (difficulty: {concept['difficulty']})")

    # Initialize RelationshipDefiner
    print(f"\n🤖 Initializing Relationship Definer (Claude Opus 4)...")

    try:
        agent = RelationshipDefiner()
        print("✅ Agent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        print("\nℹ️ Make sure ANTHROPIC_API_KEY is set:")
        print("   export ANTHROPIC_API_KEY='your-key-here'")
        return

    # Test on FIRST concept only (to save API costs during testing)
    test_concept = sample_concepts[0]

    print(f"\n🧪 Testing on: {test_concept['concept_id']} - {test_concept['name']}")
    print(f"   Analyzing against {len(sample_concepts)} sample concepts...")

    try:
        relationships = agent.analyze_concept_relationships(
            source_concept=test_concept,
            all_concepts=sample_concepts,  # Use sample subset for faster testing
            max_relationships=10
        )

        print(f"\n✅ Analysis complete! Found {len(relationships)} relationships")

        # Save results
        output_dir = Path(__file__).parent / "outputs" / "relationship-test"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"test_sample_{test_concept['concept_id']}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "test_concept": test_concept,
                "sample_size": len(sample_concepts),
                "relationships_found": len(relationships),
                "relationships": relationships
            }, f, ensure_ascii=False, indent=2)

        print(f"\n💾 Results saved to: {output_file}")

        # Analyze results
        analyze_test_results(relationships)

        print("\n" + "="*60)
        print("✅ TEST COMPLETE")
        print("="*60)
        print("\nNext steps:")
        print("1. Review results in outputs/relationship-test/")
        print("2. Check confidence scores and reasoning quality")
        print("3. If satisfactory, run on all 20 samples")
        print("4. Then run on full 841 concepts")

    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
