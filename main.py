"""
Math Education Agent System - Main Entry Point

Based on Kenny Liao's Claude Agent SDK pattern
References: /home/kc-palantir/claude-agent-sdk-intro/6_subagents.py

Architecture:
- User → Meta-Orchestrator (main agent)
- Meta-Orchestrator → 6 Specialized Subagents
- Subagents: knowledge-builder, quality-agent, research-agent,
             example-generator, dependency-mapper, socratic-planner

VERSION: 2.0.0 - Integrated infrastructure modules
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
from agents.structured_logger import StructuredLogger, set_trace_id
from agents.performance_monitor import PerformanceMonitor
from agents.context_manager import ContextManager
from agents.error_handler import ErrorTracker

import asyncio
import uuid
import time
import logging


async def main():
    # Initialize infrastructure
    print("=" * 80)
    print("Math Education Multi-Agent System v2.0")
    print("=" * 80)
    print("\n[Infrastructure] Initializing logging and monitoring...\n")

    # Setup structured logger
    from datetime import datetime
    logger = StructuredLogger(
        log_dir="/tmp/math-agent-logs",
        trace_id=f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    )
    logger.system_event("system_start", "Math agent system starting")

    # Setup performance monitor
    performance_monitor = PerformanceMonitor()

    # Setup error tracker
    error_tracker = ErrorTracker(max_retries=3)

    print("✅ Infrastructure initialized")
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
        # Initialize context manager with memory tool function
        def memory_tool_func(tool_name: str, **params):
            """Wrapper for memory-keeper MCP tool calls"""
            # This will be called by context_manager
            # In SDK, we can't directly call MCP tools from Python
            # So we log the intent and return empty result
            logger.system_event("memory_tool_call", f"Tool: {tool_name}", metadata=params)
            return {"items": []}

        context_manager = ContextManager(memory_tool_func)

        # Main conversation loop
        while True:
            # Get user input
            try:
                user_input = input("\n\033[1;34mYou:\033[0m ")
            except (EOFError, KeyboardInterrupt):
                print("\n\nExiting...")
                logger.system_event("system_shutdown", "User interrupted")
                break

            if user_input.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                logger.system_event("system_shutdown", "User exit")
                performance_monitor.print_summary()
                break

            if not user_input.strip():
                continue

            # Generate trace_id for this query
            query_trace_id = str(uuid.uuid4())[:8]
            set_trace_id(query_trace_id)

            # Log query start
            logger.system_event(
                "user_query_start",
                f"Processing query (trace_id: {query_trace_id})",
                metadata={"query": user_input}
            )

            # Start timing
            query_start_time = time.time()
            query_success = False

            try:
                # Send query to main agent
                await client.query(user_input)

                # Receive and display responses
                async for message in client.receive_response():
                    # Simple message display
                    # For production, use cli_tools.py from Kenny Liao's pattern
                    print(f"\n{message}")

                query_success = True

            except Exception as e:
                logger.error(
                    "meta-orchestrator",
                    type(e).__name__,
                    str(e),
                    metadata={"query": user_input}
                )
                print(f"\n❌ Error: {e}")

                # Record error in tracker
                error_tracker.record_error(
                    agent_name="meta-orchestrator",
                    task_id=query_trace_id,
                    error=e,
                    context={"query": user_input}
                )

            finally:
                # Record performance
                query_duration_ms = (time.time() - query_start_time) * 1000
                performance_monitor.record_execution(
                    agent_name="meta-orchestrator",
                    duration_ms=query_duration_ms,
                    success=query_success
                )

                # Log query completion
                logger.system_event(
                    "user_query_complete",
                    f"Query completed (trace_id: {query_trace_id})",
                    metadata={
                        "duration_ms": query_duration_ms,
                        "success": query_success
                    }
                )


if __name__ == "__main__":
    # Enable nested async (required for some environments)
    import nest_asyncio
    nest_asyncio.apply()

    # Run the main loop
    asyncio.run(main())
