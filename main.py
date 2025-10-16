"""
Math Education Agent System - Kenneth-Liao Pattern

Architecture:
- Main Agent: meta-orchestrator (system prompt in .claude/CLAUDE.md)
- Subagents: 12 specialized agents (defined inline)
- Pattern: ClaudeSDKClient with AgentDefinition dict

VERSION: 3.1.0 - Kenneth-Liao Pattern + Feedback Loop Integration
DATE: 2025-10-16
"""

import asyncio
from dotenv import load_dotenv
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

# Import all 12 subagent definitions from subagents/ directory
from subagents import (
    knowledge_builder,
    quality_agent,
    research_agent,
    socratic_requirements_agent,
    neo4j_query_agent,
    problem_decomposer_agent,
    problem_scaffolding_generator_agent,
    personalization_engine_agent,
    feedback_learning_agent,
    self_improver_agent,
    meta_planning_analyzer,
    meta_query_helper,
)

# Optional: Import infrastructure for enhanced features
try:
    from infrastructure import StructuredLogger, PerformanceMonitor, ErrorTracker
    INFRASTRUCTURE_AVAILABLE = True
except ImportError:
    INFRASTRUCTURE_AVAILABLE = False


async def main():
    # Load environment variables
    load_dotenv()
    
    print("=" * 80)
    print("Math Education Multi-Agent System v3.0 - Kenneth-Liao Pattern")
    print("=" * 80)
    print()
    print("Architecture:")
    print("  Main Agent: meta-orchestrator")
    print("  Subagents: 12 specialized agents")
    print("  Pattern: Kenneth-Liao (ClaudeSDKClient + AgentDefinition)")
    print()
    print("Commands:")
    print("  'exit' - Exit the system")
    print("=" * 80)
    print()
    
    # Optional: Initialize infrastructure
    logger = None
    perf_monitor = None
    error_tracker = None
    
    if INFRASTRUCTURE_AVAILABLE:
        from datetime import datetime
        logger = StructuredLogger(log_dir="/tmp/math-agent-logs")
        perf_monitor = PerformanceMonitor()
        error_tracker = ErrorTracker(max_retries=3)
        logger.system_event("system_start", "Math agent system starting")
        print("✅ Infrastructure initialized (logging, monitoring, error tracking)")
        print()
    
    # Configure Claude Agent SDK options
    options = ClaudeAgentOptions(
        # Model configuration
        model="claude-sonnet-4-5-20250929",
        permission_mode="acceptEdits",
        
        # System prompt from .claude/CLAUDE.md
        system_prompt={
            "type": "preset",
            "preset": "claude_code"
        },
        setting_sources=["project"],
        
        # Main agent tools (meta-orchestrator)
        allowed_tools=[
            'Task',      # Required for subagent delegation
            'Read',
            'Write',
            'Edit',
            'Grep',
            'Glob',
            'TodoWrite',
            'mcp__sequential-thinking__sequentialthinking',
            'mcp__memory-keeper__context_save',
            'mcp__memory-keeper__context_get',
            'mcp__memory-keeper__context_search',
        ],
        
        # Subagent definitions (11 agents)
        agents={
            "knowledge-builder": knowledge_builder,
            "quality-agent": quality_agent,
            "research-agent": research_agent,
            "socratic-requirements-agent": socratic_requirements_agent,
            "neo4j-query-agent": neo4j_query_agent,
            "problem-decomposer": problem_decomposer_agent,
            "problem-scaffolding-generator": problem_scaffolding_generator_agent,
            "personalization-engine": personalization_engine_agent,
            "feedback-learning-agent": feedback_learning_agent,
            "self-improver": self_improver_agent,
            "meta-planning-analyzer": meta_planning_analyzer,
            "meta-query-helper": meta_query_helper,
        },
        
        # MCP servers
        mcp_servers={
            "memory-keeper": {
                "command": "npx",
                "args": ["-y", "mcp-memory-keeper"]
            },
            "sequential-thinking": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
            },
        }
    )
    
    # Start conversation loop (kenneth-liao pattern)
    async with ClaudeSDKClient(options=options) as client:
        print("🎯 Meta-Orchestrator ready. Type your request below.")
        print()
        
        conversation_turns = 0
        
        while True:
            # Get user input
            try:
                user_input = input("\033[1;34mYou:\033[0m ")
            except (EOFError, KeyboardInterrupt):
                print("\n\nExiting...")
                break
            
            # Handle exit
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye!")
                if logger:
                    logger.system_event("system_shutdown", "User exit")
                if perf_monitor:
                    perf_monitor.print_summary()
                break
            
            if not user_input.strip():
                continue
            
            conversation_turns += 1
            
            # Send query to Claude
            try:
                print(f"\n\033[1;32m🎯 Meta-Orchestrator:\033[0m ", end="", flush=True)
                
                await client.query(user_input)
                
                # Receive and display response
                from claude_agent_sdk import types
                
                async for message in client.receive_response():
                    if isinstance(message, types.AssistantMessage):
                        for block in message.content:
                            if isinstance(block, types.TextBlock):
                                print(block.text, end="", flush=True)
                            elif isinstance(block, types.ThinkingBlock):
                                print(f"\n\n🧠 [Thinking...]\n{block.thinking}", end="", flush=True)
                            elif isinstance(block, types.ToolUseBlock):
                                print(f"\n\n🔧 [Tool: {block.name}]", end="", flush=True)
                    
                    elif isinstance(message, types.ResultMessage):
                        print(f"\n\n✅ Complete (Duration: {message.duration_ms}ms, Turns: {message.num_turns})")
                        if perf_monitor:
                            perf_monitor.record_execution("meta-orchestrator", message.duration_ms, True)
                
                print()  # New line after response
                
            except Exception as e:
                print(f"\n\n❌ Error: {e}")
                if error_tracker:
                    error_tracker.record_error("meta-orchestrator", str(conversation_turns), e, {})
                if logger:
                    logger.error("meta-orchestrator", type(e).__name__, str(e))


if __name__ == "__main__":
    # Enable nested async (required for some environments)
    import nest_asyncio
    nest_asyncio.apply()
    
    # Run the main conversation loop
    asyncio.run(main())
