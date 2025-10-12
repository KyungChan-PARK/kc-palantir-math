"""
Math Education Agent System - Main Entry Point

Based on Kenny Liao's Claude Agent SDK pattern
References: /home/kc-palantir/claude-agent-sdk-intro/6_subagents.py

Architecture:
- User → Meta-Orchestrator (main agent)
- Meta-Orchestrator → 6 Specialized Subagents
- Subagents: knowledge-builder, quality-agent, research-agent,
             example-generator, dependency-mapper, socratic-planner
"""

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from agents import (
    meta_orchestrator,
    knowledge_builder,
    quality_agent,
    research_agent,
    example_generator,
    dependency_mapper,
    socratic_planner,
)
import asyncio


async def main():
    print("=" * 80)
    print("Math Education Multi-Agent System")
    print("=" * 80)
    print("\nMain Agent: Meta-Orchestrator")
    print("Subagents: 6 specialized agents")
    print("  - knowledge-builder: Create Obsidian markdown files")
    print("  - quality-agent: Validate file quality")
    print("  - research-agent: Deep concept research")
    print("  - example-generator: Generate mathematical examples")
    print("  - dependency-mapper: Map prerequisite dependencies")
    print("  - socratic-planner: Clarify user requirements")
    print("\nType 'exit' to quit\n")

    # Configure agent options
    options = ClaudeAgentOptions(
        model="sonnet",
        permission_mode="acceptEdits",
        setting_sources=["project"],

        # Main agent tools (Meta-Orchestrator)
        # CRITICAL: 'Task' is required for subagent delegation!
        allowed_tools=[
            'Task',      # ⚠️ Required for subagents!
            'Read',
            'Write',
            'Edit',
            'Grep',
            'Glob',
            'TodoWrite',
            'mcp__sequential-thinking__sequentialthinking',
            # Memory management (scalable.pdf p3: orchestrator needs context persistence)
            'mcp__memory-keeper__context_save',
            'mcp__memory-keeper__context_get',
            'mcp__memory-keeper__context_search',
        ],

        # All subagent definitions (6 agents)
        agents={
            "meta-orchestrator": meta_orchestrator,
            "knowledge-builder": knowledge_builder,
            "quality-agent": quality_agent,
            "research-agent": research_agent,
            "example-generator": example_generator,
            "dependency-mapper": dependency_mapper,
            "socratic-planner": socratic_planner,
        },

        # MCP servers
        # Note: Assumes brave-search, context7, memory-keeper, sequential-thinking
        # are already installed globally via claude mcp
        mcp_servers={}
    )

    # Create client and start conversation loop
    async with ClaudeSDKClient(options=options) as client:
        while True:
            # Get user input
            try:
                user_input = input("\n\033[1;34mYou:\033[0m ")
            except (EOFError, KeyboardInterrupt):
                print("\n\nExiting...")
                break

            if user_input.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break

            if not user_input.strip():
                continue

            # Send query to main agent
            await client.query(user_input)

            # Receive and display responses
            async for message in client.receive_response():
                # Simple message display
                # For production, use cli_tools.py from Kenny Liao's pattern
                print(f"\n{message}")


if __name__ == "__main__":
    # Enable nested async (required for some environments)
    import nest_asyncio
    nest_asyncio.apply()

    # Run the main loop
    asyncio.run(main())
