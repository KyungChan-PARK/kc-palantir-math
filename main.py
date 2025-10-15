"""
Math Education Agent System - Main Entry Point

Based on Kenny Liao's Claude Agent SDK pattern
References: /home/kc-palantir/claude-agent-sdk-intro/6_subagents.py

Architecture:
- User → Meta-Orchestrator (main agent)
- Meta-Orchestrator → 6 Specialized Subagents
- Subagents: knowledge-builder, quality-agent, research-agent,
             example-generator, dependency-mapper, socratic-planner

VERSION: 2.2.0 - Real LLM Integration + Hook System + Semantic Layer
"""

import os
import sys
from dotenv import load_dotenv
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from agents import (
    meta_orchestrator,
    knowledge_builder,
    quality_agent,
    research_agent,
    example_generator,
    dependency_mapper,
    self_improver_agent,
    socratic_requirements_agent,  # NEW: Replaces socratic-planner and socratic-mediator
)
from agents.meta_planning_analyzer import meta_planning_analyzer
from agents.meta_query_helper import meta_query_helper
from agents.agent_registry import AgentRegistry
from agents.structured_logger import StructuredLogger, set_trace_id
from agents.performance_monitor import PerformanceMonitor
from agents.context_manager import ContextManager
from agents.error_handler import ErrorTracker

# Hook integration (v2.2.0)
try:
    from hooks.hook_integrator import (
        get_default_meta_orchestrator_hooks,
        get_default_socratic_agent_hooks
    )
    HOOKS_AVAILABLE = True
except ImportError:
    HOOKS_AVAILABLE = False
    
    def get_default_meta_orchestrator_hooks():
        return {}
    def get_default_socratic_agent_hooks():
        return {}

import asyncio
import uuid
import time
import logging


async def main():
    # Load environment variables from .env file
    load_dotenv()

    # Check for API key (optional for Claude Code users)
    api_key = os.getenv("ANTHROPIC_API_KEY")

    # Initialize infrastructure
    print("=" * 80)
    print("Math Education Multi-Agent System v2.1")
    print("=" * 80)
    print("\n[Infrastructure] Initializing logging and monitoring...")

    if api_key:
        print(f"[Auth] Anthropic API Key: {'*' * 8}{api_key[-4:]} ✓")
    else:
        print("[Auth] Using Claude Code authentication (API key not required) ✓")
        print("       Note: If you need API-based access, create .env with ANTHROPIC_API_KEY")
    print()

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
    
    # Dynamic agent discovery
    print("\n[Agent Discovery] Scanning agents directory...")
    from pathlib import Path
    registry = AgentRegistry(Path(__file__).parent / "agents")
    discovered_agents = registry.discover_agents()
    
    # Visual status display
    print("Agent Feature Status:")
    print("─" * 70)
    for name in sorted(discovered_agents.keys()):
        meta = registry.get_agent_capabilities(name)
        thinking_icon = "🧠" if meta.get("has_extended_thinking") else "  "
        cache_icon = "💾" if meta.get("has_prompt_caching") else "  "
        budget = f"{meta.get('thinking_budget', 0)/1000:.0f}k" if meta.get('thinking_budget') else "-"
        print(f"  {thinking_icon}{cache_icon} {name:<30} Budget: {budget}")
    
    print("─" * 70)
    print(f"Total: {len(discovered_agents)} agents")
    print(f"Extended Thinking: {len(registry.get_agents_with_extended_thinking())} agents")
    print(f"Prompt Caching: {len(registry.get_agents_with_caching())} agents")
    
    # Hook system status
    if HOOKS_AVAILABLE:
        print("\n🔗 Hook System Active:")
        print("──────────────────────────────────────────────────────────────────────")
        print("  ✅ PreToolUse: SDK validation, agent checks, parallel detection")
        print("  ✅ PostToolUse: Quality gates, metrics logging, impact analysis")
        print("  ✅ Stop: Auto-improvement trigger (success_rate < 70%)")
        print("  ✅ UserPromptSubmit: Ambiguity detection (>30% triggers Socratic)")
        print("──────────────────────────────────────────────────────────────────────")
    else:
        print("\n⚠️ Hook System: Not available")
    
    print("\nType 'exit' to quit\n")

    # Configure agent options
    options = ClaudeAgentOptions(
        # ✅ STANDARD 1: Specific model version (MANDATORY)
        model="claude-sonnet-4-5-20250929",
        permission_mode="acceptEdits",
        setting_sources=["project"],
        
        # ✅ STANDARD 4: 1M context for meta-orchestrator
        # Note: Agent SDK may handle this via model selection
        # Extended context is enabled through claude-sonnet-4-5-20250929
        # which supports up to 1M tokens with beta features

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

        # All subagent definitions (11 agents: 6 specialized + 3 meta-cognitive + 1 self-improvement + meta-orchestrator)
        # Using dynamic discovery, but can override with manual entries
        agents={
            **discovered_agents,  # All auto-discovered agents
            # Ensure meta-cognitive agents are registered
            "meta-planning-analyzer": meta_planning_analyzer,
            "meta-query-helper": meta_query_helper,
        },

        # ✅ STANDARD 3 & 4: MCP servers configuration
        # Load from .mcp.json for proper MCP tool integration
        mcp_servers={
            "memory-keeper": {
                "command": "npx",
                "args": ["-y", "mcp-memory-keeper"]
            },
            "sequential-thinking": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
            },
            "obsidian": {
                "command": "uv",
                "args": ["run", "python", "tools/obsidian-mcp-server/server.py"],
                "env": {
                    "OBSIDIAN_API_KEY": os.getenv("OBSIDIAN_API_KEY", ""),
                    "OBSIDIAN_API_URL": os.getenv("OBSIDIAN_API_URL", "https://127.0.0.1:27124")
                }
            },
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN", "")
                }
            }
        }
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
                # Visual indicator for meta-orchestrator response
                print(f"\n\033[1;32m🎯 Meta-Orchestrator:\033[0m ", end="", flush=True)
                
                # Check if SDK supports streaming
                if hasattr(client, 'stream_response'):
                    # ✅ STREAMING MODE: Real-time response with Extended Thinking
                    full_response_parts = []
                    thinking_content_parts = []
                    thinking_phase_active = False
                    
                    async with client.stream_response(user_input) as stream:
                        async for chunk in stream:
                            # Handle different chunk types
                            if hasattr(chunk, 'type'):
                                # Thinking block start
                                if chunk.type == "thinking_start" or (
                                    chunk.type == "content_block_start" and 
                                    hasattr(chunk, 'content_block') and 
                                    getattr(chunk.content_block, 'type', None) == "thinking"
                                ):
                                    print("\n\n🧠 [Extended Thinking]", flush=True)
                                    print("─" * 70, flush=True)
                                    thinking_phase_active = True
                                
                                # Thinking delta
                                elif chunk.type == "thinking_delta" or (
                                    chunk.type == "content_block_delta" and
                                    hasattr(chunk, 'delta') and
                                    hasattr(chunk.delta, 'thinking')
                                ):
                                    content = chunk.delta.thinking if hasattr(chunk.delta, 'thinking') else ""
                                    print(content, end="", flush=True)
                                    thinking_content_parts.append(content)
                                
                                # Thinking end
                                elif chunk.type == "thinking_end" or (
                                    chunk.type == "content_block_stop" and thinking_phase_active
                                ):
                                    if thinking_content_parts:
                                        print("\n" + "─" * 70, flush=True)
                                        thinking_phase_active = False
                                
                                # Text delta
                                elif chunk.type == "text_delta" or (
                                    chunk.type == "content_block_delta" and
                                    hasattr(chunk, 'delta') and
                                    hasattr(chunk.delta, 'text')
                                ):
                                    # Show response header if transitioning from thinking
                                    if thinking_content_parts and not thinking_phase_active and not full_response_parts:
                                        print("\n📝 [Response]", flush=True)
                                        print("─" * 70, flush=True)
                                    
                                    content = chunk.delta.text if hasattr(chunk.delta, 'text') else str(chunk)
                                    print(content, end="", flush=True)
                                    full_response_parts.append(content)
                        
                        print()  # Final newline
                    
                    # Log streaming performance
                    if thinking_content_parts or full_response_parts:
                        logger.agent_call(
                            "meta-orchestrator",
                            "stream_response",
                            {
                                "thinking_chars": len("".join(thinking_content_parts)),
                                "response_chars": len("".join(full_response_parts)),
                                "streaming": "enabled"
                            }
                        )
                
                else:
                    # Agent SDK message-level async (not token-level streaming)
                    # But can still parse and display Extended Thinking from message blocks
                    await client.query(user_input)
                    
                    from claude_agent_sdk import types
                    
                    async for message in client.receive_response():
                        if isinstance(message, types.AssistantMessage):
                            # Parse content blocks to display Extended Thinking and response separately
                            for block in message.content:
                                if isinstance(block, types.ThinkingBlock):
                                    print(f"\n🧠 [Extended Thinking]")
                                    print("─" * 70)
                                    print(block.thinking)
                                    print("─" * 70)
                                
                                elif isinstance(block, types.TextBlock):
                                    print(f"\n📝 [Response]")
                                    print("─" * 70)
                                    print(block.text)
                                    print("─" * 70)
                                
                                elif isinstance(block, types.ToolUseBlock):
                                    print(f"\n🔧 [Using Tool: {block.name}]")
                        
                        elif isinstance(message, types.ResultMessage):
                            print(f"\n✅ Complete (Duration: {message.duration_ms}ms, Turns: {message.num_turns})")
                        
                        elif isinstance(message, types.SystemMessage):
                            # Skip system messages (init, etc.)
                            pass
                        
                        else:
                            # Fallback for unknown message types
                            print(message)
                
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
