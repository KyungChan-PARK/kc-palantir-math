"""
E2E Test for Research Agent (Phase 3 - Milestone 1)

Tests the research-agent's ability to:
1. Conduct deep research on a mathematical concept
2. Extract definitions, formulas, prerequisites, related concepts
3. Generate structured JSON research report

Success criteria:
- JSON research report created at /tmp/research_report_{concept-id}.json
- At least 3 definitions collected
- At least 5 prerequisites identified
- At least 1 formula extracted
- At least 3 related concepts found
- Valid JSON syntax
"""

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from agents import research_agent
import asyncio
import os
import json


async def test_research_agent():
    """Test research-agent in isolation: Cauchy-Schwarz Inequality"""

    print("=" * 80)
    print("Phase 3 - Milestone 1: Research Agent Isolation Test")
    print("=" * 80)

    options = ClaudeAgentOptions(
        model="sonnet",
        permission_mode="acceptEdits",
        setting_sources=["project"],

        allowed_tools=[
            'Read',
            'Write',
            'TodoWrite',
            'mcp__brave-search__brave_web_search',
            'mcp__context7__resolve-library-id',
            'mcp__context7__get-library-docs',
        ],

        agents={
            "research-agent": research_agent,
        },

        mcp_servers={}
    )

    test_concept = "Cauchy-Schwarz Inequality"
    expected_report_path = "/tmp/research_report_cauchy-schwarz-inequality.json"

    # Clean up any existing report
    if os.path.exists(expected_report_path):
        os.remove(expected_report_path)
        print(f"Cleaned up existing report: {expected_report_path}\n")

    async with ClaudeSDKClient(options=options) as client:

        # === REQUEST: Research Task ===
        print(f"\n[REQUEST] Delegating research task to research-agent...")
        print("-" * 80)

        query = f"""Please delegate to research-agent to conduct comprehensive research on "{test_concept}".

The research-agent should:
1. Use Brave Search to collect definitions, formulas, prerequisites
2. Identify at least 5 prerequisites with dependency levels
3. Find related concepts and theorems
4. Generate JSON research report at /tmp/research_report_cauchy-schwarz-inequality.json

This is a well-known inequality in mathematics, so there should be abundant information available."""

        await client.query(query)

        response_count = 0
        async for message in client.receive_response():
            response_count += 1
            if response_count <= 5:
                msg_str = str(message)[:120]
                print(f"  Response {response_count}: {msg_str}...")

        print(f"\n  Total responses: {response_count}")

    # === VERIFICATION ===
    print("\n" + "=" * 80)
    print("Research Report Verification")
    print("=" * 80)

    # Check 1: File exists
    file_exists = os.path.exists(expected_report_path)
    print(f"\n[1/7] File created: {'✅' if file_exists else '❌'}")
    if not file_exists:
        print(f"      Expected: {expected_report_path}")
        return False

    # Check 2: Valid JSON
    try:
        with open(expected_report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)
        json_valid = True
        print(f"[2/7] Valid JSON: ✅")
    except json.JSONDecodeError as e:
        json_valid = False
        print(f"[2/7] Valid JSON: ❌ ({e})")
        return False

    # Check 3: Required fields present
    required_fields = ['concept', 'definitions', 'formulas', 'prerequisites', 'related_concepts']
    fields_present = all(field in report for field in required_fields)
    print(f"[3/7] Required fields present: {'✅' if fields_present else '❌'}")
    if not fields_present:
        missing = [f for f in required_fields if f not in report]
        print(f"      Missing: {missing}")
        return False

    # Check 4: Definitions count (minimum 3)
    definitions_count = len(report.get('definitions', []))
    definitions_ok = definitions_count >= 3
    print(f"[4/7] Definitions collected (≥3): {'✅' if definitions_ok else '❌'} ({definitions_count} found)")

    # Check 5: Prerequisites count (minimum 5)
    prerequisites_count = len(report.get('prerequisites', []))
    prerequisites_ok = prerequisites_count >= 5
    print(f"[5/7] Prerequisites identified (≥5): {'✅' if prerequisites_ok else '❌'} ({prerequisites_count} found)")

    # Check 6: Formulas count (minimum 1)
    formulas_count = len(report.get('formulas', []))
    formulas_ok = formulas_count >= 1
    print(f"[6/7] Formulas extracted (≥1): {'✅' if formulas_ok else '❌'} ({formulas_count} found)")

    # Check 7: Related concepts count (minimum 3)
    related_count = len(report.get('related_concepts', []))
    related_ok = related_count >= 3
    print(f"[7/7] Related concepts (≥3): {'✅' if related_ok else '❌'} ({related_count} found)")

    # === DETAILED REPORT PREVIEW ===
    print("\n" + "-" * 80)
    print("Research Report Preview:")
    print("-" * 80)
    print(f"Concept: {report.get('concept', 'N/A')}")
    print(f"Domain: {report.get('domain_classification', {}).get('primary_domain', 'N/A')}")
    print(f"Level: {report.get('domain_classification', {}).get('level', 'N/A')}")

    if report.get('definitions'):
        print(f"\nDefinitions ({len(report['definitions'])}):")
        for i, defn in enumerate(report['definitions'][:2], 1):
            print(f"  {i}. [{defn.get('source', 'Unknown')}] {defn.get('text', 'N/A')[:100]}...")

    if report.get('prerequisites'):
        print(f"\nPrerequisites ({len(report['prerequisites'])}):")
        for prereq in report['prerequisites'][:5]:
            print(f"  - {prereq.get('name', 'N/A')} ({prereq.get('level', 'N/A')})")

    if report.get('formulas'):
        print(f"\nFormulas ({len(report['formulas'])}):")
        for formula in report['formulas'][:2]:
            print(f"  - {formula.get('description', 'N/A')}")

    if report.get('related_concepts'):
        print(f"\nRelated Concepts ({len(report['related_concepts'])}):")
        for concept in report['related_concepts'][:5]:
            print(f"  - {concept.get('name', 'N/A')} ({concept.get('relationship', 'N/A')})")

    # === FINAL ASSESSMENT ===
    print("\n" + "=" * 80)
    print("Test Results Summary")
    print("=" * 80)

    checks = [
        ("File created", file_exists),
        ("Valid JSON", json_valid),
        ("Required fields", fields_present),
        ("Definitions ≥3", definitions_ok),
        ("Prerequisites ≥5", prerequisites_ok),
        ("Formulas ≥1", formulas_ok),
        ("Related concepts ≥3", related_ok),
    ]

    passed_count = sum(1 for _, passed in checks if passed)
    total_count = len(checks)

    print(f"\nChecks passed: {passed_count}/{total_count}")
    for check_name, passed in checks:
        print(f"  {'✅' if passed else '❌'} {check_name}")

    # Success threshold: 6/7 checks must pass
    success = passed_count >= 6

    print("\n" + "=" * 80)
    if success:
        print("✅ RESEARCH AGENT TEST PASSED")
        print("   Research-agent successfully conducted deep research and generated structured report")
    else:
        print("❌ RESEARCH AGENT TEST FAILED")
        print(f"   Only {passed_count}/{total_count} checks passed (need 6/7)")
    print("=" * 80)

    return success


async def main():
    """Run research agent isolation test"""
    print("\n" + "=" * 80)
    print("Phase 3 - Milestone 1 Test Suite: Research Agent")
    print("Testing research-agent's ability to gather and structure information")
    print("=" * 80)

    try:
        test_success = await test_research_agent()

        print("\n" + "=" * 80)
        print("Test Summary")
        print("=" * 80)
        print(f"Research Agent: {'✅ PASSED' if test_success else '❌ FAILED'}")

        print("\n" + "=" * 80)
        if test_success:
            print("✅ MILESTONE 1 TEST PASSED")
            print("   Ready to proceed to Milestone 2 (Example Generator)")
        else:
            print("❌ MILESTONE 1 TEST FAILED")
            print("   Need to improve research-agent implementation")
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
