"""
Ask Agent Tool - Inter-Agent Query Mechanism

VERSION: 4.0.0
DATE: 2025-10-14
PURPOSE: Enable Socratic-Mediator to query other agents

Based on: SELF-IMPROVEMENT-IMPLEMENTATION-PLAN-v4.0.md Section VI (Phase 5)

Core Features:
1. Execute queries to other agents
2. Return structured responses
3. Log queries for analysis
"""

from typing import Optional, Dict, Any


async def ask_agent_tool(
    agent_name: str,
    question: str,
    agent_registry: Optional[Dict[str, Any]] = None
) -> str:
    """
    Ask a question to another agent and return the response.

    Used by Socratic-Mediator during root cause analysis to gather
    information from agents about their behavior and issues.

    Args:
        agent_name: Name of agent to query (e.g., "knowledge-builder")
        question: Question to ask the agent
        agent_registry: Registry of available agents (from Meta-Orchestrator)

    Returns:
        answer: Agent's response to the question
    """
    if not agent_registry:
        return f"[ERROR] Agent registry not available"

    if agent_name not in agent_registry:
        available = ", ".join(agent_registry.keys())
        return f"[ERROR] Agent '{agent_name}' not found. Available: {available}"

    try:
        # Get agent function from registry
        agent_func = agent_registry[agent_name]

        # Execute agent with question
        # In real implementation with Claude Agent SDK:
        # response = await agent_func(question)

        # Placeholder response
        response = f"[Simulated response from {agent_name}] I would answer: {question}"

        return response

    except Exception as e:
        return f"[ERROR] Failed to query {agent_name}: {str(e)}"
