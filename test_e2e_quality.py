"""
E2E Test for Quality Agent

Tests the full workflow with quality validation:
1. Create ClaudeSDKClient with both agents
2. Generate a concept file (knowledge-builder)
3. Validate the file (quality-agent)
4. Verify validation report is created
"""

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from agents import knowledge_builder, quality_agent
import asyncio
import os
import re


async def test_quality_validation_existing_file():
    """Test validating existing Pythagorean Theorem file"""

    print("=" * 60)
    print("E2E Test: Quality Agent - Existing File Validation")
    print("=" * 60)

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
        print("\n[1/4] Sending validation request to quality-agent...")

        query = """Please delegate to the quality-agent subagent to validate the file at:
/home/kc-palantir/math-vault/Theorems/pythagorean-theorem.md

The agent should check YAML frontmatter, wikilinks, content structure, LaTeX formulas, and basic mathematical accuracy."""

        await client.query(query)

        print("[2/4] Receiving responses...")
        response_count = 0
        validation_report = None

        async for message in client.receive_response():
            response_count += 1
            msg_str = str(message)

            # Extract validation report if present
            if "Quality Validation Report" in msg_str or "PASSED" in msg_str or "FAILED" in msg_str:
                validation_report = msg_str

            if response_count <= 5 or response_count % 10 == 0:
                print(f"    Response {response_count}: {msg_str[:150]}...")

        print(f"[3/4] Received {response_count} responses")

    # Verify validation completed
    print("[4/4] Verifying validation results...")

    if validation_report:
        print(f"✅ Validation report generated")

        # Check for key validation elements
        has_yaml_check = "YAML" in validation_report or "frontmatter" in validation_report
        has_wikilinks_check = "wikilink" in validation_report.lower()
        has_assessment = "PASS" in validation_report or "FAIL" in validation_report

        print(f"   Contains YAML check: {'✅' if has_yaml_check else '❌'}")
        print(f"   Contains wikilinks check: {'✅' if has_wikilinks_check else '❌'}")
        print(f"   Contains assessment: {'✅' if has_assessment else '❌'}")

        if has_yaml_check and has_wikilinks_check and has_assessment:
            print("\n✅ Quality validation successful")
            return True
        else:
            print("\n⚠️ Validation incomplete - missing some checks")
            return False
    else:
        print("❌ No validation report found in responses")
        return False


async def test_full_workflow_with_validation():
    """Test full workflow: create concept + validate"""

    print("\n" + "=" * 60)
    print("E2E Test: Full Workflow (Create + Validate)")
    print("=" * 60)

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
        print("\n[1/5] Creating test concept: Distance Formula...")

        query = """Please follow this workflow:

1. Delegate to knowledge-builder to create concept file for "Distance Formula"
2. After file is created, delegate to quality-agent to validate it
3. Report the validation results

Create the file in /home/kc-palantir/math-vault/Theorems/distance-formula.md"""

        await client.query(query)

        print("[2/5] Receiving responses...")
        response_count = 0
        file_created = False
        validation_done = False

        async for message in client.receive_response():
            response_count += 1
            msg_str = str(message)

            if "distance-formula.md" in msg_str.lower() and ("created" in msg_str.lower() or "written" in msg_str.lower()):
                file_created = True

            if "Quality Validation Report" in msg_str or ("validation" in msg_str.lower() and ("passed" in msg_str.lower() or "failed" in msg_str.lower())):
                validation_done = True

            if response_count <= 5 or response_count % 10 == 0:
                print(f"    Response {response_count}: {msg_str[:150]}...")

        print(f"[3/5] Received {response_count} responses")

    # Verify file was created
    print("[4/5] Verifying file creation...")
    expected_file = "/home/kc-palantir/math-vault/Theorems/distance-formula.md"

    if os.path.exists(expected_file):
        print(f"✅ File created at {expected_file}")
        file_size = os.path.getsize(expected_file)
        print(f"   File size: {file_size} bytes")
    else:
        print(f"❌ File not found at {expected_file}")
        return False

    # Verify validation was performed
    print("[5/5] Verifying validation was performed...")

    if validation_done:
        print("✅ Validation completed")
        return True
    else:
        print("⚠️ Validation not clearly confirmed")
        return False


async def main():
    """Run all e2e quality tests"""
    print("\n" + "=" * 60)
    print("Quality Agent E2E Test Suite")
    print("=" * 60)

    try:
        # Test 1: Validate existing file
        test1_success = await test_quality_validation_existing_file()

        # Test 2: Full workflow
        test2_success = await test_full_workflow_with_validation()

        # Summary
        print("\n" + "=" * 60)
        print("Test Summary")
        print("=" * 60)
        print(f"Test 1 (Existing File Validation): {'✅ PASSED' if test1_success else '❌ FAILED'}")
        print(f"Test 2 (Full Workflow): {'✅ PASSED' if test2_success else '❌ FAILED'}")

        all_passed = test1_success and test2_success

        print("\n" + "=" * 60)
        if all_passed:
            print("✅ ALL E2E QUALITY TESTS PASSED")
        else:
            print("❌ SOME E2E QUALITY TESTS FAILED")
        print("=" * 60)

        return 0 if all_passed else 1

    except Exception as e:
        print(f"\n❌ ERROR during tests: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()

    exit_code = asyncio.run(main())
    exit(exit_code)
