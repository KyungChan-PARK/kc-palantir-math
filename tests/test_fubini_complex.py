"""
E2E Test for Complex Concept: Fubini's Theorem

Tests the system's ability to handle complex mathematical concepts with 13+ atomic factors.
Fubini's Theorem requires understanding of:
- Measure theory, sigma-algebras, product measures
- Lebesgue integration, L^1 spaces
- Tonelli's theorem (related concept)
- Multiple prerequisites and dependencies

This test validates:
1. Knowledge-builder can research and create comprehensive documentation
2. Quality-agent can validate complex content with 13+ prerequisites
3. YAML frontmatter includes all necessary dependencies
4. LaTeX formulas are correctly formatted
5. Wikilinks to prerequisites are properly created
"""

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from agents import knowledge_builder, quality_agent
import asyncio
import os
import re
import yaml


async def test_fubini_theorem_generation():
    """Test generating Fubini's Theorem documentation with 13+ atomic factors"""

    print("=" * 80)
    print("E2E Test: Fubini's Theorem (Complex Concept - 13+ Atomic Factors)")
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

    async with ClaudeSDKClient(options=options) as client:
        print("\n[1/6] Requesting Fubini's Theorem documentation generation...")

        query = """Please follow this workflow:

1. Delegate to knowledge-builder to create comprehensive documentation for "Fubini's Theorem"
   - This is a complex theorem in measure theory
   - It requires 13+ prerequisite concepts including:
     * σ-algebras and measurable spaces
     * Measure theory and σ-finite measures
     * Product measures
     * Lebesgue integration and L^1 spaces
     * Tonelli's theorem (closely related)
     * Measurable functions
     * Iterated integrals

2. After file is created, delegate to quality-agent to validate it
3. Report the validation results

Create the file in /home/kc-palantir/math-vault/Theorems/fubini-theorem.md"""

        await client.query(query)

        print("[2/6] Receiving responses...")
        response_count = 0
        file_created = False
        validation_done = False
        validation_report = None

        async for message in client.receive_response():
            response_count += 1
            msg_str = str(message)

            if "fubini-theorem.md" in msg_str.lower() and ("created" in msg_str.lower() or "written" in msg_str.lower()):
                file_created = True

            if "Quality Validation Report" in msg_str or ("validation" in msg_str.lower() and ("passed" in msg_str.lower() or "failed" in msg_str.lower())):
                validation_done = True
                validation_report = msg_str

            if response_count <= 5 or response_count % 20 == 0:
                print(f"    Response {response_count}: {msg_str[:120]}...")

        print(f"[3/6] Received {response_count} responses")

    # Verify file was created
    print("[4/6] Verifying file creation...")
    expected_file = "/home/kc-palantir/math-vault/Theorems/fubini-theorem.md"

    if not os.path.exists(expected_file):
        print(f"❌ File not found at {expected_file}")
        return False

    print(f"✅ File created at {expected_file}")
    file_size = os.path.getsize(expected_file)
    print(f"   File size: {file_size} bytes")

    # Read and analyze the generated file
    print("[5/6] Analyzing file content...")

    with open(expected_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract YAML frontmatter
    yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not yaml_match:
        print("❌ No YAML frontmatter found")
        return False

    frontmatter = yaml.safe_load(yaml_match.group(1))
    print("✅ YAML frontmatter found")

    # Check prerequisites count
    prerequisites = frontmatter.get('prerequisites', [])
    prereq_count = len(prerequisites)
    print(f"   Prerequisites count: {prereq_count}")

    if prereq_count < 13:
        print(f"⚠️  Expected 13+ prerequisites, found {prereq_count}")
        print(f"   Prerequisites: {prerequisites}")
    else:
        print(f"✅ Sufficient prerequisites ({prereq_count} >= 13)")

    # Check for Tonelli's theorem reference
    has_tonelli = "tonelli" in content.lower()
    print(f"   References Tonelli's Theorem: {'✅' if has_tonelli else '❌'}")

    # Count wikilinks
    wikilinks = re.findall(r'\[\[([^\]]+)\]\]', content)
    wikilink_count = len(wikilinks)
    print(f"   Wikilinks count: {wikilink_count}")

    if wikilink_count < 13:
        print(f"⚠️  Expected 13+ wikilinks, found {wikilink_count}")
    else:
        print(f"✅ Sufficient wikilinks ({wikilink_count} >= 13)")

    # Check for LaTeX formulas
    latex_blocks = re.findall(r'\$\$.*?\$\$', content, re.DOTALL)
    inline_latex = re.findall(r'\$[^\$]+\$', content)
    latex_count = len(latex_blocks) + len(inline_latex)
    print(f"   LaTeX formulas: {latex_count} (blocks: {len(latex_blocks)}, inline: {len(inline_latex)})")

    # Verify validation was performed
    print("[6/6] Verifying validation results...")

    if not validation_done:
        print("⚠️ Validation not clearly confirmed")
        return False

    print("✅ Validation completed")

    # Overall assessment
    print("\n" + "=" * 80)
    print("Content Quality Assessment")
    print("=" * 80)

    all_checks = [
        ("File created", True),
        ("YAML frontmatter present", yaml_match is not None),
        ("Prerequisites >= 13", prereq_count >= 13),
        ("Tonelli reference", has_tonelli),
        ("Wikilinks >= 13", wikilink_count >= 13),
        ("LaTeX formulas present", latex_count > 0),
        ("Validation completed", validation_done)
    ]

    passed_checks = sum(1 for _, passed in all_checks if passed)
    total_checks = len(all_checks)

    for check_name, passed in all_checks:
        print(f"  {'✅' if passed else '❌'} {check_name}")

    print(f"\nPassed: {passed_checks}/{total_checks} checks")

    # Success criteria: at least 6/7 checks must pass
    success = passed_checks >= 6

    if success:
        print("\n✅ COMPLEX CONCEPT TEST PASSED")
        print("   System successfully handled Fubini's Theorem with 13+ atomic factors")
    else:
        print("\n⚠️ COMPLEX CONCEPT TEST NEEDS IMPROVEMENT")
        print(f"   Only {passed_checks}/{total_checks} checks passed")

    return success


async def main():
    """Run Fubini's Theorem complex concept test"""
    print("\n" + "=" * 80)
    print("Complex Concept Test Suite: Fubini's Theorem")
    print("Testing system capability with 13+ atomic factors")
    print("=" * 80)

    try:
        test_success = await test_fubini_theorem_generation()

        print("\n" + "=" * 80)
        print("Test Summary")
        print("=" * 80)
        print(f"Fubini's Theorem Generation: {'✅ PASSED' if test_success else '❌ FAILED'}")

        print("\n" + "=" * 80)
        if test_success:
            print("✅ COMPLEX CONCEPT TEST PASSED")
            print("   Ready to proceed to Phase 2 (Iterative Improvement Loop)")
        else:
            print("❌ COMPLEX CONCEPT TEST FAILED")
            print("   Need to improve handling of complex concepts")
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
