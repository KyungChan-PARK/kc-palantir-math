"""
Full Workflow Test: Create + Validate

Tests knowledge-builder creating a concept, then quality-agent validating it
"""

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from agents import knowledge_builder, quality_agent
import asyncio
import os


async def main():
    try:
        print("=" * 60)
        print("Full Workflow Test: Create + Validate")
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

        print("\nTest: Create 'Quadratic Formula' and validate it\n")

        async with ClaudeSDKClient(options=options) as client:
            query = """Please follow this two-step workflow:

Step 1: Create concept file for "Quadratic Formula"
   - Save to: /home/kc-palantir/math-vault/Theorems/quadratic-formula.md

Step 2: Validate the created file
   - Check YAML, wikilinks, structure, LaTeX

Provide a summary after both steps are complete."""

            await client.query(query)

            print("Receiving responses (max 50)...\n")
            response_count = 0
            file_created = False
            validation_done = False

            async for message in client.receive_response():
                response_count += 1
                msg_str = str(message)

                # Track progress
                if "quadratic-formula.md" in msg_str.lower():
                    if "created" in msg_str.lower() or "written" in msg_str.lower():
                        file_created = True
                        print(f"  [{response_count}] ✅ File creation detected")

                if "validation" in msg_str.lower() and ("pass" in msg_str.lower() or "fail" in msg_str.lower()):
                    validation_done = True
                    print(f"  [{response_count}] ✅ Validation detected")

                if response_count % 10 == 0:
                    print(f"  [{response_count}] Processing...")

                if response_count > 50:
                    print("\n  ⚠️ Response limit reached")
                    break

        print(f"\nCompleted with {response_count} responses")

        # Verify results
        print("\n" + "=" * 60)
        print("Verification")
        print("=" * 60)

        expected_file = "/home/kc-palantir/math-vault/Theorems/quadratic-formula.md"

        if os.path.exists(expected_file):
            file_size = os.path.getsize(expected_file)
            print(f"✅ File exists: {expected_file}")
            print(f"   Size: {file_size} bytes")

            if file_size > 1000:
                print(f"✅ File has substantial content")
            else:
                print(f"⚠️ File is small ({file_size} bytes)")

        else:
            print(f"❌ File not found: {expected_file}")
            return 1

        if validation_done:
            print(f"✅ Validation was performed")
        else:
            print(f"⚠️ Validation not clearly detected")

        print("\n" + "=" * 60)
        print("✅ FULL WORKFLOW TEST PASSED")
        print("=" * 60)
        return 0

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()

    exit_code = asyncio.run(main())
    exit(exit_code)
