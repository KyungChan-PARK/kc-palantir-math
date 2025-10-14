"""
Automatic Concept Enrichment Tool
Enriches short math concept descriptions using contextual templates

VERSION: 1.0.0
DATE: 2025-10-14
PURPOSE: Automatically enrich 715 concepts with short content

Usage:
    python tools/auto_enrich_concepts.py --batch-size 20 --start 0
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
import argparse


class AutoEnricher:
    """Automatically enrich concept content using templates and context"""

    def __init__(self):
        self.enrichment_templates = self._build_templates()
        self.enriched_count = 0
        self.backup_created = False

    def _build_templates(self) -> Dict:
        """Build enrichment templates by concept type"""
        return {
            'definition': [
                '{name}은(는) {content}을(를) 의미한다.',
                '{name}은(는) {content}로 정의되며, 수학적으로 중요한 기초 개념이다.',
            ],
            'property': [
                '{name}의 특징은 {content}이다.',
                '{content}을(를) 만족하는 것이 {name}의 주요 성질이다.',
            ],
            'theorem': [
                '{name}은(는) {content}이 성립함을 나타낸다.',
                '정리에 따르면, {content}일 때 {name}이(가) 성립한다.',
            ],
            'formula': [
                '{name}은(는) {content}로 계산된다.',
                '{content}의 공식을 사용하여 {name}을(를) 구할 수 있다.',
            ],
            'method': [
                '{name}은(는) {content}의 방법으로 수행된다.',
                '{content}의 단계를 따라 {name}을(를) 해결한다.',
            ],
            'general': [
                '{name}은(는) {chapter_name}에서 학습하는 개념으로, {content}을(를) 다룬다.',
                '{grade}학년 {semester}학기 수학에서 배우는 {name}은(는) {content}에 관한 내용이다.',
            ]
        }

    def enrich_with_template(self, concept: Dict) -> str:
        """Generate enriched content using templates"""
        name = concept['name']
        content = concept['content']
        tags = concept.get('tags', ['general'])
        chapter_name = concept['chapter']['name']
        grade = concept['grade']
        semester = concept['semester']

        # Determine concept type from tags
        concept_type = 'general'
        for tag in tags:
            if tag in self.enrichment_templates:
                concept_type = tag
                break

        # Get appropriate template
        templates = self.enrichment_templates[concept_type]
        template = templates[0]  # Use first template for now

        # Fill template
        try:
            enriched = template.format(
                name=name,
                content=content,
                chapter_name=chapter_name,
                grade=grade,
                semester=semester
            )
            return enriched
        except:
            # Fallback to simple concatenation
            return f'{name}은(는) {content}을(를) 나타낸다.'

    def enrich_with_context(self, concept: Dict) -> str:
        """Generate contextual enrichment based on concept metadata"""
        name = concept['name']
        content = concept['content']
        chapter = concept['chapter']['name']
        section = concept['section'].get('parent_name', '')
        grade = concept['grade']

        # Pattern matching for specific concept types
        if '정의' in name or 'Definition' in name:
            return f'{name.replace(" 정의", "").replace("정의", "")}은(는) {content}로 정의된다. ' \
                   f'이는 중학교 {grade}학년 {chapter} 단원에서 학습하는 기본 개념이다.'

        elif '공식' in name or 'Formula' in name:
            return f'{content}의 공식으로 나타낸다. ' \
                   f'이 공식을 사용하여 문제를 해결할 수 있다.'

        elif '정리' in name or 'Theorem' in name:
            return f'{content}이(가) 성립한다는 정리이다. ' \
                   f'증명을 통해 이 관계식이 항상 참임을 보일 수 있다.'

        elif '성질' in name or 'Property' in name:
            return f'{content}의 특징을 가진다. ' \
                   f'이러한 성질을 이용하면 관련 문제를 더 쉽게 풀 수 있다.'

        elif '방법' in name or 'Method' in name:
            return f'{content}의 방법으로 해결한다. ' \
                   f'단계적인 접근을 통해 정확한 답을 구할 수 있다.'

        elif re.search(r'\d+', content):  # Contains numbers/formulas
            return f'{name}은(는) {content}로 계산된다. ' \
                   f'이 식을 활용하여 {section} 관련 문제를 풀 수 있다.'

        else:
            # Generic enrichment
            return f'{name}은(는) {content}에 관한 개념이다. ' \
                   f'중학교 {grade}학년 {chapter}에서 중요하게 다루어지는 내용으로, ' \
                   f'관련된 문제 해결에 필수적인 개념이다.'

    def enrich_concept(self, concept: Dict, method: str = 'context') -> Dict:
        """
        Enrich a concept's content

        Args:
            concept: Concept dictionary
            method: 'template' or 'context'

        Returns:
            Enriched concept
        """
        current_content = concept['content']

        # Skip if already enriched (>= 50 chars)
        if len(current_content) >= 50:
            return concept

        # Generate enriched content
        if method == 'template':
            enriched_content = self.enrich_with_template(concept)
        else:
            enriched_content = self.enrich_with_context(concept)

        # Update concept
        concept['content'] = enriched_content
        concept['enriched'] = True
        concept['enrichment_date'] = datetime.now().isoformat()
        concept['original_content'] = current_content

        self.enriched_count += 1

        return concept

    def process_file(self, filepath: Path, backup: bool = True, method: str = 'context') -> Dict:
        """
        Process a single JSON file

        Args:
            filepath: Path to concepts JSON file
            backup: Create backup before modifying
            method: Enrichment method

        Returns:
            Processing statistics
        """
        print(f'\nProcessing: {filepath.name}')

        # Load file
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Create backup
        if backup and not self.backup_created:
            backup_dir = filepath.parent / 'backups'
            backup_dir.mkdir(exist_ok=True)
            backup_path = backup_dir / f'{filepath.stem}_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f'  Backup created: {backup_path}')
            self.backup_created = True

        # Process concepts
        short_count = 0
        enriched_count_before = self.enriched_count

        for i, concept in enumerate(data['concepts']):
            if len(concept['content']) < 50:
                short_count += 1
                data['concepts'][i] = self.enrich_concept(concept, method=method)

        enriched_this_file = self.enriched_count - enriched_count_before

        # Save enriched file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        stats = {
            'file': filepath.name,
            'total_concepts': len(data['concepts']),
            'short_concepts': short_count,
            'enriched': enriched_this_file
        }

        print(f'  Total: {stats["total_concepts"]}, Short: {stats["short_concepts"]}, Enriched: {stats["enriched"]}')

        return stats

    def process_all_files(self, data_dir: Path, method: str = 'context') -> List[Dict]:
        """Process all middle school concept files"""
        files = sorted(data_dir.glob('middle-*.json'))

        print(f'Found {len(files)} files to process')

        all_stats = []
        for filepath in files:
            stats = self.process_file(filepath, backup=True, method=method)
            all_stats.append(stats)

        return all_stats


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(description='Auto-enrich concept content')
    parser.add_argument('--method', choices=['template', 'context'], default='context',
                        help='Enrichment method (default: context)')
    parser.add_argument('--data-dir', type=str, default='data/concepts',
                        help='Directory containing concept JSON files')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be done without modifying files')

    args = parser.parse_args()

    data_dir = Path(args.data_dir)

    if not data_dir.exists():
        print(f'Error: Data directory not found: {data_dir}')
        return

    enricher = AutoEnricher()

    if args.dry_run:
        print('DRY RUN - No files will be modified')
        # Just show statistics
        for filepath in sorted(data_dir.glob('middle-*.json')):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            short = sum(1 for c in data['concepts'] if len(c['content']) < 50)
            print(f'{filepath.name}: {len(data["concepts"])} concepts, {short} short')
    else:
        print(f'Starting auto-enrichment using {args.method} method...\n')
        stats = enricher.process_all_files(data_dir, method=args.method)

        print(f'\n=== ENRICHMENT COMPLETE ===')
        print(f'Total enriched: {enricher.enriched_count} concepts')
        print(f'\nPer-file statistics:')
        for s in stats:
            print(f'  {s["file"]}: {s["enriched"]}/{s["short_concepts"]} enriched')


if __name__ == '__main__':
    main()
