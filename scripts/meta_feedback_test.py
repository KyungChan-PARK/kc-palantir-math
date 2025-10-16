"""
Test Real Meta-Cognitive Feedback Loop

This script demonstrates REAL meta-planning-analyzer feedback
by running main.py and querying via meta-query-helper.

Usage:
    uv run python scripts/test_real_meta_feedback.py
"""

import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


async def test_real_feedback_loop():
    """
    Test real meta-cognitive feedback loop via Agent SDK.
    
    Steps:
    1. Start ClaudeSDKClient
    2. Query meta-orchestrator to use meta-query-helper
    3. meta-query-helper loads planning trace
    4. meta-query-helper delegates to meta-planning-analyzer via Task
    5. Receive REAL feedback
    """
    from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
    from subagents import meta_orchestrator, meta_query_helper, meta_planning_analyzer
    
    print("="*70)
    print("🧠 Testing REAL Meta-Cognitive Feedback Loop")
    print("="*70)
    print("\nThis test:")
    print("  ✓ Uses Agent SDK (Claude Max x20)")
    print("  ✓ Queries real meta-planning-analyzer agent")
    print("  ✓ NOT simulated - actual LLM analysis")
    print("="*70)
    print()
    
    # Configure options
    options = ClaudeAgentOptions(
        model="claude-sonnet-4-5-20250929",
        permission_mode="acceptEdits",
        agents={
            "meta-orchestrator": meta_orchestrator,
            "meta-query-helper": meta_query_helper,
            "meta-planning-analyzer": meta_planning_analyzer,
        },
        allowed_tools=['Task', 'Read', 'Write', 'TodoWrite'],
    )
    
    # Start client
    async with ClaudeSDKClient(options=options) as client:
        print("✅ Client connected\n")
        
        # Query: Ask meta-orchestrator to get feedback via meta-query-helper
        query = """Please use meta-query-helper to analyze the planning trace file:
outputs/planning-traces/tool_enforcement_step3.json

meta-query-helper will load the file and query meta-planning-analyzer for REAL feedback.

Show me the complete feedback."""
        
        print(f"📤 Query: {query[:100]}...")
        print()
        
        await client.query(query)
        
        # Receive and display response
        from claude_agent_sdk import types
        
        print("📥 Receiving response...\n")
        
        async for message in client.receive_response():
            if isinstance(message, types.AssistantMessage):
                for block in message.content:
                    if isinstance(block, types.ThinkingBlock):
                        print(f"🧠 [Extended Thinking]")
                        print("─" * 70)
                        print(block.thinking[:500] + "..." if len(block.thinking) > 500 else block.thinking)
                        print("─" * 70)
                    
                    elif isinstance(block, types.TextBlock):
                        print(f"\n📝 [Response]")
                        print("─" * 70)
                        print(block.text)
                        print("─" * 70)
            
            elif isinstance(message, types.ResultMessage):
                print(f"\n✅ Complete")
                print(f"   Duration: {message.duration_ms}ms")
                print(f"   Turns: {message.num_turns}")
                break
    
    print("\n" + "="*70)
    print("✅ Real meta-cognitive feedback loop test complete!")
    print("="*70)


if __name__ == '__main__':
    asyncio.run(test_real_feedback_loop())

