"""
Batch Parser for Middle School Math Concepts
Processes all 6 middle school files (grades 1-3, semesters 1-2)

Usage:
    python3 tools/batch_parse_middle_school.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.concept_parser import ConceptParser


# Middle school file definitions
MIDDLE_SCHOOL_FILES = [
    {
        "filename": "중학교 1학년 1학기 수학(2022 개정교육과정) 전체 개념 완전 분해.md",
        "grade": 1,
        "semester": 1,
        "output": "middle-1-1.json"
    },
    {
        "filename": "중학교 1학년 2학기 수학(2022 개정교육과정) 전체 개념 완전 분해.md",
        "grade": 1,
        "semester": 2,
        "output": "middle-1-2.json"
    },
    {
        "filename": "중학교 2학년 1학기 수학(2022 개정교육과정) 전체 개념 완전 분해.md",
        "grade": 2,
        "semester": 1,
        "output": "middle-2-1.json"
    },
    {
        "filename": "중학교 2학년 2학기 수학(2022 개정교육과정) 전체 개념 완전 분해.md",
        "grade": 2,
        "semester": 2,
        "output": "middle-2-2.json"
    },
    {
        "filename": "중학교 3학년 1학기 수학(2022 개정교육과정) 전체 개념 완전 분해.md",
        "grade": 3,
        "semester": 1,
        "output": "middle-3-1.json"
    },
    {
        "filename": "중학교 3학년 2학기 수학(2022 개정교육과정) 전체 개념 완전 분해.md",
        "grade": 3,
        "semester": 2,
        "output": "middle-3-2.json"
    }
]


def main():
    """Batch parse all middle school files"""

    base_dir = Path(__file__).parent.parent
    input_dir = base_dir / "math-concepts-mapping-prep"
    output_dir = base_dir / "data" / "concepts"

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("BATCH PARSING: Middle School Math (2022 Revised Curriculum)")
    print("=" * 80)
    print()

    total_concepts = 0
    results = []

    for file_def in MIDDLE_SCHOOL_FILES:
        filename = file_def["filename"]
        grade = file_def["grade"]
        semester = file_def["semester"]
        output_filename = file_def["output"]

        input_path = input_dir / filename
        output_path = output_dir / output_filename

        if not input_path.exists():
            print(f"⚠️  SKIP: {filename} not found")
            continue

        print(f"📄 Processing: Grade {grade} Semester {semester}")
        print(f"   Input: {filename}")

        # Create parser
        parser = ConceptParser("middle", grade, semester, "2022_revised")

        # Parse file
        try:
            concepts = parser.parse_file(str(input_path))

            # Save to JSON
            parser.save_json(concepts, str(output_path))

            # Get statistics
            stats = parser.get_statistics(concepts)

            print(f"   ✓ Extracted: {len(concepts)} concepts")
            print(f"   ✓ Chapters: {stats['unique_chapters']}")
            print(f"   ✓ Sections: {stats['unique_sections']}")
            print(f"   ✓ Output: {output_filename}")
            print()

            total_concepts += len(concepts)

            results.append({
                "grade": grade,
                "semester": semester,
                "concepts": len(concepts),
                "chapters": stats['unique_chapters'],
                "sections": stats['unique_sections'],
                "output": output_filename
            })

        except Exception as e:
            print(f"   ✗ ERROR: {e}")
            print()
            continue

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Files processed: {len(results)}/{len(MIDDLE_SCHOOL_FILES)}")
    print(f"Total concepts: {total_concepts}")
    print()

    print("Breakdown by grade:")
    for result in results:
        print(f"  Middle {result['grade']}-{result['semester']}: {result['concepts']} concepts, "
              f"{result['chapters']} chapters, {result['sections']} sections")

    print()
    print(f"✓ All JSON files saved to: {output_dir}")
    print()

    return results


if __name__ == "__main__":
    results = main()
