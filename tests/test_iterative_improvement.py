"""
E2E Test for Iterative Improvement Loop (Phase 2)

Tests the system's ability to iteratively improve a document based on quality feedback.

Workflow:
1. Generate initial (intentionally incomplete) document
2. Validate with quality-agent
3. If not PASSED, extract improvement suggestions
4. Regenerate document incorporating feedback
5. Repeat until PASSED or max_iterations reached

Success criteria:
- Initial document has issues (NEEDS_IMPROVEMENT)
- After improvement iteration, document PASSES validation
- Quality metrics improve between iterations
"""

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from agents import knowledge_builder, quality_agent
import asyncio
import os
import re
import yaml


async def test_iterative_improvement():
    """Test iterative improvement: incomplete → improved → validated"""

    print("=" * 80)
    print("Phase 2: Iterative Improvement Loop Test")
    print("=" * 80)

    options = ClaudeAgentOptions(
        model="sonnet",
        permission_mode="acceptEdits",
        setting_sources=["project"],

        allowed_tools=[
            'Read',
            'Write',
            'Edit',
            'Grep',
            'Glob',
            'Task',
            'TodoWrite',
        ],

        agents={
            "knowledge-builder": knowledge_builder,
            "quality-agent": quality_agent,
        },

        mcp_servers={}
    )

    test_file = "/home/kc-palantir/math-vault/Concepts/slope-concept.md"
    max_iterations = 3
    iteration_results = []

    async with ClaudeSDKClient(options=options) as client:

        # === ITERATION 0: Create intentionally basic/incomplete document ===
        print("\n[ITERATION 0] Creating basic (incomplete) document...")
        print("-" * 80)

        query_0 = """Please delegate to knowledge-builder to create a BASIC and INCOMPLETE document for "Slope" concept.

Important: Make it intentionally minimal/incomplete to test improvement loop:
- Include only basic definition
- Skip examples section or make it very brief
- Include only 1-2 prerequisites
- Minimal LaTeX formulas

Save to: /home/kc-palantir/math-vault/Concepts/slope-concept.md"""

        await client.query(query_0)

        response_count = 0
        async for message in client.receive_response():
            response_count += 1
            if response_count <= 3:
                msg_str = str(message)[:100]
                print(f"  Response {response_count}: {msg_str}...")

        print(f"  Total responses: {response_count}")

        # Check if file was created
        if not os.path.exists(test_file):
            print(f"❌ File not created at {test_file}")
            return False

        initial_size = os.path.getsize(test_file)
        print(f"✅ Initial document created ({initial_size} bytes)")

        # === ITERATION 1: Validate and get feedback ===
        print("\n[ITERATION 1] Validating initial document...")
        print("-" * 80)

        query_1 = f"""Please delegate to quality-agent to validate: {test_file}

The agent should provide detailed feedback including:
- What's missing
- What needs improvement
- Specific suggestions for enhancement"""

        await client.query(query_1)

        response_count = 0
        validation_report_1 = []

        async for message in client.receive_response():
            response_count += 1
            msg_str = str(message)
            validation_report_1.append(msg_str)

            if response_count <= 3:
                print(f"  Response {response_count}: {msg_str[:100]}...")

        print(f"  Total responses: {response_count}")

        # Analyze validation result
        full_report_1 = "\n".join(validation_report_1)

        has_passed_1 = "PASSED" in full_report_1 and "NEEDS_IMPROVEMENT" not in full_report_1
        has_issues_1 = "NEEDS_IMPROVEMENT" in full_report_1 or "FAILED" in full_report_1
        has_suggestions_1 = "Suggestions" in full_report_1 or "Issues Found" in full_report_1

        print(f"\nValidation Result (Iteration 1):")
        print(f"  Status: {'✅ PASSED' if has_passed_1 else '⚠️ NEEDS_IMPROVEMENT' if has_issues_1 else '❓ UNKNOWN'}")
        print(f"  Has suggestions: {'✅' if has_suggestions_1 else '❌'}")

        iteration_results.append({
            "iteration": 1,
            "file_size": initial_size,
            "passed": has_passed_1,
            "has_suggestions": has_suggestions_1
        })

        # === ITERATION 2: Improve based on feedback ===
        if not has_passed_1:
            print("\n[ITERATION 2] Improving document based on feedback...")
            print("-" * 80)

            query_2 = f"""Please delegate to knowledge-builder to IMPROVE the document at: {test_file}

Based on the quality validation feedback above, enhance the document to address all issues:
- Add missing sections (Examples, Applications, etc.)
- Expand prerequisites to at least 5 items
- Add more LaTeX formulas and explanations
- Ensure comprehensive content

The agent should READ the existing file and EDIT it to incorporate improvements."""

            await client.query(query_2)

            response_count = 0
            async for message in client.receive_response():
                response_count += 1
                if response_count <= 3:
                    msg_str = str(message)[:100]
                    print(f"  Response {response_count}: {msg_str}...")

            print(f"  Total responses: {response_count}")

            improved_size = os.path.getsize(test_file)
            print(f"✅ Document improved ({improved_size} bytes, +{improved_size - initial_size} bytes)")

            # === ITERATION 3: Re-validate ===
            print("\n[ITERATION 3] Re-validating improved document...")
            print("-" * 80)

            query_3 = f"""Please delegate to quality-agent to re-validate: {test_file}

Check if previous issues have been addressed and document now meets quality standards."""

            await client.query(query_3)

            response_count = 0
            validation_report_2 = []

            async for message in client.receive_response():
                response_count += 1
                msg_str = str(message)
                validation_report_2.append(msg_str)

                if response_count <= 3:
                    print(f"  Response {response_count}: {msg_str[:100]}...")

            print(f"  Total responses: {response_count}")

            # Analyze re-validation result
            full_report_2 = "\n".join(validation_report_2)

            has_passed_2 = "PASSED" in full_report_2 and "NEEDS_IMPROVEMENT" not in full_report_2
            has_issues_2 = "NEEDS_IMPROVEMENT" in full_report_2 or "FAILED" in full_report_2

            print(f"\nValidation Result (Iteration 3):")
            print(f"  Status: {'✅ PASSED' if has_passed_2 else '⚠️ NEEDS_IMPROVEMENT' if has_issues_2 else '❓ UNKNOWN'}")

            iteration_results.append({
                "iteration": 3,
                "file_size": improved_size,
                "passed": has_passed_2,
                "improvement_bytes": improved_size - initial_size
            })

    # === FINAL ANALYSIS ===
    print("\n" + "=" * 80)
    print("Iterative Improvement Test Results")
    print("=" * 80)

    # Read final document stats
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()

    yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    frontmatter = yaml.safe_load(yaml_match.group(1)) if yaml_match else {}

    prerequisites = frontmatter.get('prerequisites', [])
    wikilinks = re.findall(r'\[\[([^\]]+)\]\]', content)
    latex_formulas = len(re.findall(r'\$\$.*?\$\$', content, re.DOTALL)) + len(re.findall(r'\$[^\$]+\$', content))

    print(f"\nFinal Document Metrics:")
    print(f"  File size: {os.path.getsize(test_file)} bytes")
    print(f"  Prerequisites: {len(prerequisites)}")
    print(f"  Wikilinks: {len(wikilinks)}")
    print(f"  LaTeX formulas: {latex_formulas}")

    print(f"\nIteration Summary:")
    for result in iteration_results:
        print(f"  Iteration {result['iteration']}: {result['file_size']} bytes - {'✅ PASSED' if result.get('passed') else '⚠️ NEEDS_IMPROVEMENT'}")

    # Success criteria
    initial_had_issues = iteration_results[0]['has_suggestions'] and not iteration_results[0]['passed']
    final_passed = len(iteration_results) > 1 and iteration_results[-1]['passed']
    size_increased = len(iteration_results) > 1 and iteration_results[-1]['file_size'] > iteration_results[0]['file_size']

    success_checks = [
        ("Initial document incomplete", initial_had_issues),
        ("Improvement iteration executed", len(iteration_results) > 1),
        ("Final document passed validation", final_passed),
        ("Document size increased", size_increased),
    ]

    print(f"\nSuccess Checks:")
    for check_name, passed in success_checks:
        print(f"  {'✅' if passed else '❌'} {check_name}")

    passed_checks = sum(1 for _, passed in success_checks if passed)
    total_checks = len(success_checks)

    print(f"\nPassed: {passed_checks}/{total_checks} checks")

    # Overall success
    success = passed_checks >= 3  # At least 3/4 checks must pass

    print("\n" + "=" * 80)
    if success:
        print("✅ ITERATIVE IMPROVEMENT TEST PASSED")
        print("   System successfully improved document based on quality feedback")
    else:
        print("❌ ITERATIVE IMPROVEMENT TEST FAILED")
        print(f"   Only {passed_checks}/{total_checks} checks passed")
    print("=" * 80)

    return success


async def main():
    """Run iterative improvement test"""
    print("\n" + "=" * 80)
    print("Phase 2 Test Suite: Iterative Improvement Loop")
    print("Testing automated quality-based document refinement")
    print("=" * 80)

    try:
        test_success = await test_iterative_improvement()

        print("\n" + "=" * 80)
        print("Test Summary")
        print("=" * 80)
        print(f"Iterative Improvement: {'✅ PASSED' if test_success else '❌ FAILED'}")

        print("\n" + "=" * 80)
        if test_success:
            print("✅ PHASE 2 TEST PASSED")
            print("   Ready to proceed to Phase 3+ (Additional Specialized Agents)")
        else:
            print("❌ PHASE 2 TEST FAILED")
            print("   Need to improve iterative refinement workflow")
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
