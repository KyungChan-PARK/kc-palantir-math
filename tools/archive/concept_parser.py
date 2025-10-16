"""
Concept Parser - Extract structured concepts from markdown files

Universal parser for all education levels (elementary to university)
Converts hierarchical markdown structure to JSON database format

Usage:
    from tools.concept_parser import ConceptParser

    parser = ConceptParser("middle", 1, 1, "2022_revised")
    concepts = parser.parse_file("path/to/markdown.md")
    parser.save_json(concepts, "output.json")
"""

import re
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Concept:
    """Single mathematical concept with metadata"""
    concept_id: str
    name: str
    name_en: Optional[str]
    education_level: str  # elem, middle, high, univ
    grade: int
    semester: int
    chapter: Dict[str, any]
    section: Dict[str, any]
    content: str
    prerequisites: List[str]
    difficulty: int
    curriculum: str
    tags: List[str]

    def to_dict(self) -> dict:
        return asdict(self)


class ConceptParser:
    """Universal parser for math concept extraction"""

    # Education level mapping
    LEVEL_MAP = {
        "초등": "elem",
        "중학교": "middle",
        "고등학교": "high",
        "대학": "univ"
    }

    # Chapter detection patterns
    CHAPTER_PATTERN = r'^##\s+\*\*[🔢📐📊🔄]?\s*Chapter\s+(\d+):\s*(.+?)\*\*'
    SECTION_PATTERN = r'^###\s+\*\*(\d+)\.\s*(.+?)\s*\(([^)]+)\)\*\*'
    SUBSECTION_PATTERN = r'^####\s+\*\*(\d+\.\d+)\s+(.+?)\*\*'

    # Concept patterns - supports both 3-level (1.1.1) and 4-level (1.1.1.1)
    # With or without colon separator
    CONCEPT_3LEVEL_PATTERN = r'^-\s+(\d+\.\d+\.\d+)\s+(.+?)(?::\s*(.+))?$'
    CONCEPT_4LEVEL_PATTERN = r'^\s+-\s+(\d+\.\d+\.\d+\.\d+)\s+(.+?)(?::\s*(.+))?$'

    def __init__(self, education_level: str, grade: int, semester: int, curriculum: str = "2022_revised"):
        """
        Initialize parser with metadata

        Args:
            education_level: elem, middle, high, or univ
            grade: 1-6 for elem, 1-3 for middle/high, 1-4 for univ
            semester: 1 or 2
            curriculum: curriculum identifier (e.g., "2022_revised")
        """
        self.education_level = education_level
        self.grade = grade
        self.semester = semester
        self.curriculum = curriculum

        # State tracking
        self.current_chapter = None
        self.current_section = None
        self.current_subsection = None

    def generate_concept_id(self, section_path: str) -> str:
        """Generate unique concept ID"""
        # Extract chapter number from section path
        chapter_num = section_path.split('.')[0]
        return f"{self.education_level}-{self.grade}-{self.semester}-ch{chapter_num}-{section_path}"

    def parse_file(self, filepath: str) -> List[Concept]:
        """
        Parse markdown file and extract concepts

        Args:
            filepath: Path to markdown file

        Returns:
            List of Concept objects
        """
        concepts = []

        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, 1):
            line = line.rstrip()

            # Skip empty lines and metadata
            if not line or line.startswith('***') or line.startswith('<'):
                continue

            # Try to match chapter
            chapter_match = re.match(self.CHAPTER_PATTERN, line)
            if chapter_match:
                chapter_num = int(chapter_match.group(1))
                chapter_name = chapter_match.group(2).strip()
                self.current_chapter = {
                    "number": chapter_num,
                    "name": chapter_name,
                    "name_en": self._extract_english_name(chapter_name)
                }
                continue

            # Try to match section
            section_match = re.match(self.SECTION_PATTERN, line)
            if section_match:
                section_num = section_match.group(1)
                section_name = section_match.group(2).strip()
                section_name_en = section_match.group(3).strip()

                self.current_section = {
                    "number": section_num,
                    "name": section_name,
                    "name_en": section_name_en
                }
                continue

            # Try to match subsection
            subsection_match = re.match(self.SUBSECTION_PATTERN, line)
            if subsection_match:
                subsection_num = subsection_match.group(1)
                subsection_name = subsection_match.group(2).strip()

                self.current_subsection = {
                    "number": subsection_num,
                    "name": subsection_name
                }
                continue

            # Try to match concept - 4-level first (more specific), then 3-level
            concept_match = re.match(self.CONCEPT_4LEVEL_PATTERN, line)
            is_4level = True

            if not concept_match:
                concept_match = re.match(self.CONCEPT_3LEVEL_PATTERN, line)
                is_4level = False

            if concept_match:
                concept_num = concept_match.group(1)
                concept_name = concept_match.group(2).strip()
                # Content might be None if no colon separator
                concept_content = concept_match.group(3).strip() if concept_match.group(3) else concept_name

                # Process both 3-level and 4-level concepts as actual concepts
                # Different files use different hierarchy depths
                if self.current_chapter and self.current_section:
                    concept = self._build_concept(
                        concept_num,
                        concept_name,
                        concept_content
                    )
                    concepts.append(concept)

        return concepts

    def _build_concept(self, concept_num: str, concept_name: str, concept_content: str) -> Concept:
        """Build Concept object from parsed data"""

        concept_id = self.generate_concept_id(concept_num)

        # Extract parent path
        parent_parts = concept_num.rsplit('.', 1)
        parent_path = parent_parts[0] if len(parent_parts) > 1 else concept_num

        # Determine parent name
        parent_name = self.current_subsection.get("name", "") if self.current_subsection else self.current_section.get("name", "")

        concept = Concept(
            concept_id=concept_id,
            name=concept_name,
            name_en=None,  # Will be filled by translation agent
            education_level=self.education_level,
            grade=self.grade,
            semester=self.semester,
            chapter={
                "number": self.current_chapter["number"],
                "name": self.current_chapter["name"],
                "name_en": self.current_chapter.get("name_en", "")
            },
            section={
                "path": concept_num,
                "parent": parent_path,
                "parent_name": parent_name
            },
            content=concept_content,
            prerequisites=[],  # Will be filled by dependency-mapper agent
            difficulty=self._estimate_difficulty(concept_num),
            curriculum=self.curriculum,
            tags=self._generate_tags(concept_name, concept_content)
        )

        return concept

    def _extract_english_name(self, korean_name: str) -> str:
        """Extract English name from Korean text"""
        # Common chapter name mappings
        mappings = {
            "수와 연산": "Numbers and Operations",
            "변화와 관계": "Change and Relationships",
            "도형과 측정": "Geometry and Measurement",
            "자료와 가능성": "Data and Possibility"
        }

        for kr, en in mappings.items():
            if kr in korean_name:
                return en

        return ""

    def _estimate_difficulty(self, concept_path: str) -> int:
        """Estimate difficulty based on depth and position"""
        depth = concept_path.count('.')

        # Simple heuristic: deeper = harder
        if depth <= 2:
            return 1  # Basic
        elif depth == 3:
            return 2  # Intermediate
        else:
            return 3  # Advanced

    def _generate_tags(self, name: str, content: str) -> List[str]:
        """Generate relevant tags for concept"""
        tags = []

        # Tag by concept type
        keywords = {
            "정의": "definition",
            "성질": "property",
            "정리": "theorem",
            "공식": "formula",
            "방법": "method"
        }

        for kr, en in keywords.items():
            if kr in name or kr in content:
                tags.append(en)

        # Tag by domain
        domains = {
            "소수": "prime",
            "분수": "fraction",
            "방정식": "equation",
            "함수": "function",
            "도형": "geometry",
            "확률": "probability"
        }

        for kr, en in domains.items():
            if kr in name or kr in content:
                tags.append(en)

        return tags if tags else ["general"]

    def save_json(self, concepts: List[Concept], output_path: str, indent: int = 2):
        """Save concepts to JSON file"""
        data = {
            "metadata": {
                "education_level": self.education_level,
                "grade": self.grade,
                "semester": self.semester,
                "curriculum": self.curriculum,
                "total_concepts": len(concepts)
            },
            "concepts": [c.to_dict() for c in concepts]
        }

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)

        print(f"✓ Saved {len(concepts)} concepts to {output_path}")

    def get_statistics(self, concepts: List[Concept]) -> Dict:
        """Get parsing statistics"""
        chapters = set(c.chapter["number"] for c in concepts)
        sections = set(c.section["parent"] for c in concepts)

        return {
            "total_concepts": len(concepts),
            "unique_chapters": len(chapters),
            "unique_sections": len(sections),
            "difficulty_distribution": self._count_by_difficulty(concepts),
            "tag_distribution": self._count_by_tags(concepts)
        }

    def _count_by_difficulty(self, concepts: List[Concept]) -> Dict[int, int]:
        """Count concepts by difficulty level"""
        counts = {1: 0, 2: 0, 3: 0}
        for c in concepts:
            counts[c.difficulty] = counts.get(c.difficulty, 0) + 1
        return counts

    def _count_by_tags(self, concepts: List[Concept]) -> Dict[str, int]:
        """Count concepts by tags"""
        counts = {}
        for c in concepts:
            for tag in c.tags:
                counts[tag] = counts.get(tag, 0) + 1
        return counts


def main():
    """Example usage"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python concept_parser.py <markdown_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    # Parse filename to extract metadata
    # Expected format: "중학교 1학년 1학기 수학(2022 개정교육과정) 전체 개념 완전 분해.md"
    filename = Path(input_file).stem

    # Simple parsing (can be improved)
    parser = ConceptParser("middle", 1, 1, "2022_revised")

    print(f"Parsing: {input_file}")
    concepts = parser.parse_file(input_file)

    # Save to JSON
    output_file = f"data/concepts/middle-1-1.json"
    parser.save_json(concepts, output_file)

    # Print statistics
    stats = parser.get_statistics(concepts)
    print(f"\nStatistics:")
    print(f"  Total concepts: {stats['total_concepts']}")
    print(f"  Chapters: {stats['unique_chapters']}")
    print(f"  Sections: {stats['unique_sections']}")
    print(f"  Difficulty: {stats['difficulty_distribution']}")


if __name__ == "__main__":
    main()
