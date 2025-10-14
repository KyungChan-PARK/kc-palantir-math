"""
Content Enricher - Enrich short concept descriptions with detailed explanations

VERSION: 1.0.0
DATE: 2025-10-14
PURPOSE: Improve 85% of concepts with short content (<20 chars)

Usage:
    from tools.content_enricher import ContentEnricher

    enricher = ContentEnricher()
    enriched = enricher.enrich_concept(concept_data)
"""

import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime


class ContentEnricher:
    """Enrich mathematical concept descriptions based on context"""

    def __init__(self):
        self.enrichment_count = 0
        self.enrichment_log = []

    def enrich_concept(self, concept: Dict) -> Dict:
        """
        Enrich a single concept with detailed explanation

        Args:
            concept: Concept dictionary with metadata

        Returns:
            Enriched concept dictionary
        """
        # Manual enrichment mappings based on concept analysis
        enrichments = self._get_enrichment_mapping()

        concept_id = concept['concept_id']
        name = concept['name']
        current_content = concept['content']

        # Check if already enriched (content > 50 chars is considered good)
        if len(current_content) >= 50:
            return concept

        # Try to find enrichment
        enriched_content = enrichments.get(concept_id)

        if enriched_content:
            concept['content'] = enriched_content
            self.enrichment_count += 1
            self.enrichment_log.append({
                'concept_id': concept_id,
                'name': name,
                'original_length': len(current_content),
                'enriched_length': len(enriched_content),
                'timestamp': datetime.now().isoformat()
            })

        return concept

    def _get_enrichment_mapping(self) -> Dict[str, str]:
        """Sample enrichment mappings - to be extended"""
        return {
            # Sample 1: 그래프를 이용한 연립방정식 풀이
            'middle-2-1-ch6-6.2.3':
                '두 일차방정식을 각각 그래프로 나타내어, 두 직선의 교점의 좌표를 구함으로써 연립방정식의 해를 찾는 방법. '
                '교점이 존재하면 해가 하나, 평행하면 해가 없고, 일치하면 무수히 많은 해가 존재한다.',

            # Sample 2: 농도와 혼합 문제
            'middle-1-1-ch4-4.3.4':
                '서로 다른 농도의 용액을 섞을 때, 용질의 양과 용액의 양을 방정식으로 나타내어 푸는 문제. '
                '(농도) = (용질의 양)/(용액의 양) × 100 공식을 활용하며, 혼합 전후의 용질 양이 보존됨을 이용한다.',

            # Sample 3: 최소공배수 정의
            'middle-1-1-ch1-1.5.2':
                '두 개 이상의 자연수의 공통된 배수 중에서 가장 작은 양의 정수. '
                '예를 들어, 4와 6의 최소공배수는 12이다. 소인수분해를 이용하여 구할 수 있으며, '
                '각 소인수의 최대 지수를 선택하여 곱한다.',

            # Sample 4: 정n각형의 한 외각
            'middle-1-2-ch2-2.2.3.2':
                '정n각형의 한 꼭짓점에서의 외각의 크기는 360° ÷ n으로 계산된다. '
                '이는 정다각형의 모든 외각의 합이 항상 360°이며, n개의 외각이 모두 같기 때문이다. '
                '예: 정육각형(n=6)의 한 외각은 60°이다.',

            # Sample 5: SAS 합동
            'middle-1-2-ch1-1.6.2.2':
                '두 삼각형에서 두 변의 길이와 그 끼인각의 크기가 각각 같으면 두 삼각형은 합동이다. '
                'Side-Angle-Side 조건으로, 삼각형의 합동을 증명하는 기본 조건 중 하나이다. '
                '예: AB=DE, AC=DF, ∠A=∠D이면 △ABC ≡ △DEF'
        }

    def get_statistics(self) -> Dict:
        """Get enrichment statistics"""
        if not self.enrichment_log:
            return {
                'total_enriched': 0,
                'avg_original_length': 0,
                'avg_enriched_length': 0,
                'improvement_ratio': 0
            }

        total = len(self.enrichment_log)
        avg_original = sum(log['original_length'] for log in self.enrichment_log) / total
        avg_enriched = sum(log['enriched_length'] for log in self.enrichment_log) / total

        return {
            'total_enriched': total,
            'avg_original_length': avg_original,
            'avg_enriched_length': avg_enriched,
            'improvement_ratio': avg_enriched / avg_original if avg_original > 0 else 0
        }


def main():
    """Test enrichment on sample concepts"""
    enricher = ContentEnricher()

    # Test on middle-1-1
    test_file = Path('data/concepts/middle-1-1.json')

    if not test_file.exists():
        print(f"Test file not found: {test_file}")
        return

    with open(test_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Testing enrichment on {len(data['concepts'])} concepts...")

    enriched_concepts = []
    for concept in data['concepts']:
        enriched = enricher.enrich_concept(concept)
        enriched_concepts.append(enriched)

    stats = enricher.get_statistics()
    print(f"\nEnrichment Statistics:")
    print(f"  Total enriched: {stats['total_enriched']}")
    print(f"  Avg original length: {stats['avg_original_length']:.1f} chars")
    print(f"  Avg enriched length: {stats['avg_enriched_length']:.1f} chars")
    print(f"  Improvement ratio: {stats['improvement_ratio']:.1f}x")


if __name__ == '__main__':
    main()
