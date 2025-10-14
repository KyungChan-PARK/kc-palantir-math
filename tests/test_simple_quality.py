"""
Simple Quality Agent Test

Tests just the quality agent validation of existing file
"""

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from agents import quality_agent
import asyncio


async def main():
    try:
        print("=" * 60)
        print("Simple Quality Agent Test")
        print("=" * 60)

        options = ClaudeAgentOptions(
            model="sonnet",
            permission_mode="acceptEdits",
            setting_sources=["project"],

            allowed_tools=[
                'Read',
                'Grep',
                'Glob',
                'Task',
                'TodoWrite',
            ],

            agents={
                "quality-agent": quality_agent,
            },

            mcp_servers={}
        )

        print("\nValidating: /home/kc-palantir/math-vault/Theorems/pythagorean-theorem.md")

        async with ClaudeSDKClient(options=options) as client:
            query = """Validate the file at /home/kc-palantir/math-vault/Theorems/pythagorean-theorem.md

Check:
1. YAML frontmatter is valid
2. Wikilinks are properly formatted
3. Content structure is complete
4. LaTeX formulas are present

Provide a brief validation report."""

            await client.query(query)

            print("\nReceiving responses...\n")
            response_count = 0

            async for message in client.receive_response():
                response_count += 1
                print(f"[{response_count}] {str(message)[:200]}...")

                if response_count > 30:  # Safety limit
                    print("\n⚠️ Response limit reached")
                    break

        print(f"\n✅ Test completed ({response_count} responses)")
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
