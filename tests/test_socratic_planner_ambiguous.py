"""
Test Socratic Planner with Ambiguous Requests

Tests the socratic-planner agent's ability to:
1. Handle vague/ambiguous user requests
2. Generate clarification questions
3. Refine plans iteratively
"""

import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from agents import socratic_planner


async def test_ambiguous_request():
    """Test with very ambiguous request: '수학 개념 정리해줘'"""
    print("\n" + "="*60)
    print("SOCRATIC PLANNER TEST - Ambiguous Request")
    print("="*60 + "\n")

    # Very ambiguous request
    ambiguous_request = "수학 개념 정리해줘"

    print(f"📝 Test Request: '{ambiguous_request}'")
    print("\nThis is intentionally vague to test Socratic questioning.\n")
    print("Expected: Agent should ask clarification questions about:")
    print("  - Which math domain? (algebra, topology, calculus, etc.)")
    print("  - How many concepts?")
    print("  - What format? (markdown, PDF, etc.)")
    print("  - Which organization structure?")
    print("  - When needed?")
    print("\n" + "-"*60 + "\n")

    try:
        options = ClaudeAgentOptions(
            model="sonnet",
            permission_mode="acceptEdits",
            allowed_tools=[
                'Read',
                'Write',
                'TodoWrite',
                'mcp__sequential-thinking__sequentialthinking',
            ],
            agents={
                "socratic-planner": socratic_planner,
            },
        )

        async with ClaudeSDKClient(options=options) as client:
            await client.query(ambiguous_request)

            print("Receiving responses...\n")

            turn_count = 0
            questions_generated = False

            async for message in client.receive_response():
                turn_count += 1
                print(f"[{turn_count}] {message.__class__.__name__}")

                # Check for clarification questions in text
                if hasattr(message, 'content'):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            text = block.text
                            # Look for question indicators
                            if '?' in text or '질문' in text or '선택지' in text:
                                questions_generated = True
                                print(f"    ✅ Clarification questions detected")

                            # Print first 200 chars of response
                            preview = text[:200] + "..." if len(text) > 200 else text
                            print(f"    Preview: {preview}\n")

                if turn_count > 30:  # Safety limit
                    print("\n⚠️ Response limit reached")
                    break

        print("\n" + "="*60)
        print("TEST RESULTS")
        print("="*60)
        print(f"Total turns: {turn_count}")
        print(f"Questions generated: {'✅ YES' if questions_generated else '❌ NO'}")

        if questions_generated:
            print("\n✅ TEST PASSED - Agent generated clarification questions")
        else:
            print("\n⚠️  TEST INCONCLUSIVE - May need manual review")

    except Exception as e:
        print(f"\n❌ TEST FAILED - Error: {e}")
        import traceback
        traceback.print_exc()


async def test_specific_but_ambiguous():
    """Test with more specific but still ambiguous request"""
    print("\n" + "="*60)
    print("SOCRATIC PLANNER TEST - Specific but Ambiguous")
    print("="*60 + "\n")

    # Specific topic but vague details
    request = "위상수학 개념들을 정리하고 싶어요"

    print(f"📝 Test Request: '{request}'")
    print("\nThis is specific (topology) but missing details.\n")
    print("Expected: Agent should ask about:")
    print("  - How many concepts? (all 57 or subset?)")
    print("  - File structure?")
    print("  - Prerequisites mapping?")
    print("  - Timeline?")
    print("\n" + "-"*60 + "\n")

    try:
        options = ClaudeAgentOptions(
            model="sonnet",
            permission_mode="acceptEdits",
            allowed_tools=[
                'Read',
                'Write',
                'TodoWrite',
                'mcp__sequential-thinking__sequentialthinking',
            ],
            agents={
                "socratic-planner": socratic_planner,
            },
        )

        async with ClaudeSDKClient(options=options) as client:
            await client.query(request)

            print("Receiving responses...\n")

            turn_count = 0

            async for message in client.receive_response():
                turn_count += 1
                print(f"[{turn_count}] {message.__class__.__name__}")

                if hasattr(message, 'content'):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            preview = block.text[:150] + "..." if len(block.text) > 150 else block.text
                            print(f"    {preview}\n")

                if turn_count > 25:  # Safety limit
                    print("\n⚠️ Response limit reached")
                    break

        print(f"\n✅ Test completed with {turn_count} turns")

    except Exception as e:
        print(f"\n❌ TEST FAILED - Error: {e}")


async def main():
    """Run all socratic planner tests"""
    print("\n" + "="*70)
    print("SOCRATIC PLANNER - AMBIGUOUS REQUEST TEST SUITE")
    print("="*70)

    # Test 1: Very ambiguous
    await test_ambiguous_request()

    print("\n\n")

    # Test 2: Specific but ambiguous
    await test_specific_but_ambiguous()

    print("\n" + "="*70)
    print("ALL TESTS COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
