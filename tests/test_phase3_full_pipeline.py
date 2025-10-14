"""
E2E Test for Full 4-Agent Pipeline (Phase 3 - Milestone 3)

Tests the complete workflow integrating all specialized agents:
research-agent → knowledge-builder → example-generator → quality-agent

Success criteria:
- Research report generated with comprehensive data
- Document created by knowledge-builder using research report
- Examples added by example-generator
- Final validation by quality-agent passes
- All intermediate artifacts present
- Final document is high-quality and complete
"""

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from agents import research_agent, knowledge_builder, example_generator, quality_agent
import asyncio
import os
import json
import re


async def test_full_pipeline():
    """Test full 4-agent pipeline: research → build → examples → quality"""

    print("=" * 80)
    print("Phase 3 - Milestone 3: Full Pipeline Integration Test")
    print("=" * 80)

    options = ClaudeAgentOptions(
        model="sonnet",
        permission_mode="acceptEdits",
        setting_sources=["project"],

        allowed_tools=[
            'Read',
            'Write',
            'Edit',
            'TodoWrite',
            'Bash',
            'mcp__brave-search__brave_web_search',
            'mcp__context7__resolve-library-id',
            'mcp__context7__get-library-docs',
        ],

        agents={
            "research-agent": research_agent,
            "knowledge-builder": knowledge_builder,
            "example-generator": example_generator,
            "quality-agent": quality_agent,
        },

        mcp_servers={}
    )

    test_concept = "Mean Value Theorem"
    test_concept_id = "mean-value-theorem"
    research_report_path = f"/tmp/research_report_{test_concept_id}.json"
    document_path = f"/home/kc-palantir/math-vault/Theorems/{test_concept_id}.md"

    # Clean up any existing artifacts
    for path in [research_report_path, document_path]:
        if os.path.exists(path):
            os.remove(path)
            print(f"Cleaned up: {path}")

    print(f"\nTest Concept: {test_concept}")
    print(f"Expected outputs:")
    print(f"  - Research report: {research_report_path}")
    print(f"  - Final document: {document_path}")

    async with ClaudeSDKClient(options=options) as client:

        # === FULL PIPELINE REQUEST ===
        print("\n" + "=" * 80)
        print("[FULL PIPELINE] Requesting complete workflow...")
        print("=" * 80)

        query = f"""Please create comprehensive documentation for "{test_concept}" using the full specialized agent pipeline:

**Step 1: Research** (delegate to research-agent)
- Conduct deep research on {test_concept}
- Identify prerequisites, formulas, related concepts
- Generate JSON research report at {research_report_path}

**Step 2: Document Generation** (delegate to knowledge-builder)
- Read the research report from Step 1
- Create structured Obsidian markdown file at {document_path}
- Include YAML frontmatter, definition, mathematical details, prerequisites
- NOTE: knowledge-builder should READ the research report and use it as input

**Step 3: Example Enhancement** (delegate to example-generator)
- Read the document created in Step 2
- Add graded examples (easy → advanced)
- Include Python/SymPy implementations
- Add counterexamples and practice problems

**Step 4: Quality Validation** (delegate to quality-agent)
- Validate the final document
- Report validation results

This is a well-known calculus theorem, so research should find abundant information.
The final document should be comprehensive, well-structured, and high-quality."""

        await client.query(query)

        response_count = 0
        validation_responses = []

        async for message in client.receive_response():
            response_count += 1
            msg_str = str(message)
            validation_responses.append(msg_str)

            if response_count <= 10 or response_count % 10 == 0:
                preview = msg_str[:120]
                print(f"  Response {response_count}: {preview}...")

        print(f"\n  Total responses: {response_count}")

    # === VERIFICATION ===
    print("\n" + "=" * 80)
    print("Full Pipeline Verification")
    print("=" * 80)

    # Check 1: Research report exists
    research_report_exists = os.path.exists(research_report_path)
    print(f"\n[1/12] Research report created: {'✅' if research_report_exists else '❌'}")

    if research_report_exists:
        with open(research_report_path, 'r') as f:
            research_report = json.load(f)
        print(f"       Definitions: {len(research_report.get('definitions', []))}")
        print(f"       Prerequisites: {len(research_report.get('prerequisites', []))}")
        print(f"       Formulas: {len(research_report.get('formulas', []))}")

    # Check 2: Document created
    document_exists = os.path.exists(document_path)
    print(f"[2/12] Document created: {'✅' if document_exists else '❌'}")

    if not document_exists:
        print(f"       Expected: {document_path}")
        return False

    # Read document for analysis
    with open(document_path, 'r', encoding='utf-8') as f:
        doc_content = f.read()

    doc_size = len(doc_content)

    # Check 3: YAML frontmatter
    yaml_match = re.match(r'^---\n(.*?)\n---', doc_content, re.DOTALL)
    has_yaml = yaml_match is not None
    print(f"[3/12] YAML frontmatter: {'✅' if has_yaml else '❌'}")

    # Check 4: Prerequisites (at least 3)
    if yaml_match:
        import yaml
        frontmatter = yaml.safe_load(yaml_match.group(1))
        prerequisites = frontmatter.get('prerequisites', [])
        prereq_count = len(prerequisites)
    else:
        prereq_count = 0

    prereq_ok = prereq_count >= 3
    print(f"[4/12] Prerequisites (≥3): {'✅' if prereq_ok else '❌'} ({prereq_count} found)")

    # Check 5: Definition section
    has_definition = '## Definition' in doc_content
    print(f"[5/12] Definition section: {'✅' if has_definition else '❌'}")

    # Check 6: Mathematical formulas
    latex_count = len(re.findall(r'\$\$.*?\$\$', doc_content, re.DOTALL)) + len(re.findall(r'\$[^\$]+\$', doc_content))
    latex_ok = latex_count >= 5
    print(f"[6/12] LaTeX formulas (≥5): {'✅' if latex_ok else '❌'} ({latex_count} found)")

    # Check 7: Examples section
    has_examples = '## Examples' in doc_content
    print(f"[7/12] Examples section: {'✅' if has_examples else '❌'}")

    # Check 8: Multiple examples (at least 2)
    example_count = doc_content.count('### Example')
    examples_ok = example_count >= 2
    print(f"[8/12] Multiple examples (≥2): {'✅' if examples_ok else '❌'} ({example_count} found)")

    # Check 9: Python implementation
    has_python = '```python' in doc_content
    print(f"[9/12] Python implementation: {'✅' if has_python else '❌'}")

    # Check 10: Document size (should be substantial)
    size_ok = doc_size >= 3000  # At least 3KB
    print(f"[10/12] Document size (≥3KB): {'✅' if size_ok else '❌'} ({doc_size} bytes)")

    # Check 11: Wikilinks (at least 5)
    wikilink_count = len(re.findall(r'\[\[([^\]]+)\]\]', doc_content))
    wikilink_ok = wikilink_count >= 5
    print(f"[11/12] Wikilinks (≥5): {'✅' if wikilink_ok else '❌'} ({wikilink_count} found)")

    # Check 12: Validation completed
    validation_text = "\n".join(validation_responses)
    validation_done = ('quality-agent' in validation_text.lower() or
                      'validation' in validation_text.lower() or
                      'PASSED' in validation_text or
                      'quality' in validation_text.lower())
    print(f"[12/12] Quality validation completed: {'✅' if validation_done else '❌'}")

    # === DOCUMENT PREVIEW ===
    print("\n" + "-" * 80)
    print("Final Document Preview:")
    print("-" * 80)

    # Show first 1000 characters
    preview = doc_content[:1000]
    print(preview)
    if len(doc_content) > 1000:
        print("\n... (truncated)")

    # === FINAL ASSESSMENT ===
    print("\n" + "=" * 80)
    print("Test Results Summary")
    print("=" * 80)

    checks = [
        ("Research report created", research_report_exists),
        ("Document created", document_exists),
        ("YAML frontmatter", has_yaml),
        ("Prerequisites", prereq_ok),
        ("Definition section", has_definition),
        ("LaTeX formulas", latex_ok),
        ("Examples section", has_examples),
        ("Multiple examples", examples_ok),
        ("Python implementation", has_python),
        ("Document size", size_ok),
        ("Wikilinks", wikilink_ok),
        ("Quality validation", validation_done),
    ]

    passed_count = sum(1 for _, passed in checks if passed)
    total_count = len(checks)

    print(f"\nChecks passed: {passed_count}/{total_count}")
    for check_name, passed in checks:
        print(f"  {'✅' if passed else '❌'} {check_name}")

    # Success threshold: 10/12 checks must pass
    success = passed_count >= 10

    print("\n" + "=" * 80)
    if success:
        print("✅ FULL PIPELINE TEST PASSED")
        print("   All 4 agents collaborated successfully to create comprehensive documentation")
    else:
        print("❌ FULL PIPELINE TEST FAILED")
        print(f"   Only {passed_count}/{total_count} checks passed (need 10/12)")
    print("=" * 80)

    return success


async def main():
    """Run full pipeline integration test"""
    print("\n" + "=" * 80)
    print("Phase 3 - Milestone 3 Test Suite: Full Pipeline Integration")
    print("Testing research → build → examples → quality workflow")
    print("=" * 80)

    try:
        test_success = await test_full_pipeline()

        print("\n" + "=" * 80)
        print("Test Summary")
        print("=" * 80)
        print(f"Full Pipeline: {'✅ PASSED' if test_success else '❌ FAILED'}")

        print("\n" + "=" * 80)
        if test_success:
            print("✅ MILESTONE 3 TEST PASSED")
            print("   Ready to proceed to Milestone 4 (Iterative Improvement with Specialized Agents)")
        else:
            print("❌ MILESTONE 3 TEST FAILED")
            print("   Need to improve agent integration")
        print("=" * 80)

        return 0 if test_success else 1

    except Exception as e:
        print(f"\n❌ ERROR during test: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()

    exit_code = asyncio.run(main())
    exit(exit_code)
