"""
E2E Test for Math Education Agent System

Tests the full workflow:
1. Create ClaudeSDKClient with knowledge-builder agent
2. Send query to build a math concept
3. Verify Obsidian file is created in math-vault/
"""

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from agents import knowledge_builder
import asyncio
import os


async def test_pythagorean_theorem():
    """Test creating Pythagorean Theorem concept file"""

    print("=" * 60)
    print("E2E Test: Building Pythagorean Theorem Concept")
    print("=" * 60)

    # Configure agent options (same as main.py)
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
            'Task',      # Required for subagents!
            'TodoWrite',
        ],

        agents={
            "knowledge-builder": knowledge_builder,
        },

        mcp_servers={}
    )

    # Create client and send query
    async with ClaudeSDKClient(options=options) as client:
        print("\n[1/4] Sending query to knowledge-builder agent...")

        query = """Please delegate to the knowledge-builder subagent to build the concept "Pythagorean Theorem" and create an Obsidian markdown file in the math-vault directory."""

        await client.query(query)

        print("[2/4] Receiving responses...")
        response_count = 0

        async for message in client.receive_response():
            response_count += 1
            print(f"    Response {response_count}: {str(message)[:200]}...")

        print(f"[3/4] Received {response_count} responses")

    # Verify file was created
    print("[4/4] Verifying file creation...")
    expected_file = "/home/kc-palantir/math-vault/Theorems/pythagorean-theorem.md"

    if os.path.exists(expected_file):
        print(f"✅ SUCCESS: File created at {expected_file}")

        # Check file size
        file_size = os.path.getsize(expected_file)
        print(f"   File size: {file_size} bytes")

        # Preview first 30 lines
        with open(expected_file, 'r') as f:
            lines = f.readlines()[:30]
            print(f"\n   Preview (first 30 lines):")
            print("   " + "-" * 50)
            for line in lines:
                print(f"   {line.rstrip()}")
            print("   " + "-" * 50)

        return True
    else:
        print(f"❌ FAILURE: File not found at {expected_file}")
        print(f"\n   Checking math-vault contents:")
        for root, dirs, files in os.walk("/home/kc-palantir/math-vault"):
            level = root.replace("/home/kc-palantir/math-vault", '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f'{subindent}{file}')

        return False


async def main():
    """Run all e2e tests"""
    try:
        success = await test_pythagorean_theorem()

        print("\n" + "=" * 60)
        if success:
            print("✅ E2E TEST PASSED")
        else:
            print("❌ E2E TEST FAILED")
        print("=" * 60)

        return 0 if success else 1

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
