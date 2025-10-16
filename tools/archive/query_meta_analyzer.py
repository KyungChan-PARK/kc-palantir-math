"""
Real Meta-Planning-Analyzer Query Tool

VERSION: 1.0.0
DATE: 2025-10-15
PURPOSE: Actually query meta-planning-analyzer agent (NOT simulated)

This tool makes REAL LLM calls to meta-planning-analyzer agent.
It is NOT simulation or self-feedback.

Usage:
    from tools.query_meta_analyzer import query_real_meta_analyzer
    
    planning_trace = {...}  # From PlanningObserver
    feedback = query_real_meta_analyzer(planning_trace, show_thinking=True)
    
    # Returns REAL analysis from agent's Extended Thinking
    # NOT our imagination or assumptions
"""

import json
import os
from anthropic import Anthropic
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def query_real_meta_analyzer(planning_trace: dict, show_thinking: bool = True) -> dict:
    """
    Query REAL meta-planning-analyzer agent with actual LLM call.
    
    This is NOT simulated. This makes actual API call to Claude.
    
    Args:
        planning_trace: Planning trace dict from PlanningObserver.export_for_meta_orchestrator()
        show_thinking: Whether to display Extended Thinking process
    
    Returns:
        Real feedback dict from agent's analysis
        
    Raises:
        ValueError: If ANTHROPIC_API_KEY not set
        Exception: If agent query fails
    """
    # Import agent definition
    from agents.meta_planning_analyzer import meta_planning_analyzer
    
    # Get agent's actual prompt (this is the agent's brain)
    agent_prompt = meta_planning_analyzer.prompt
    
    # Build query for agent
    trace_json = json.dumps(planning_trace, indent=2, ensure_ascii=False)
    
    user_query = f'''Analyze this AI planning trace and provide real, actionable feedback:

{trace_json}

Focus on:
1. Query efficiency - Are the right questions asked in right order?
2. Missed optimizations from holistic project view
3. Integration concerns with existing codebase structure
4. Patterns to extract for future meta-learning

Requirements:
- Be specific (reference step numbers)
- Be actionable (provide exact suggestions)
- Consider whole project (not isolated suggestions)
- Provide code examples where helpful

Return feedback in JSON format with structure:
{{
  "overall_quality": "excellent|good|needs_improvement|poor",
  "efficiency_score": 0.0-1.0,
  "inefficiencies_detected": [...],
  "improvement_suggestions": [...],
  "positive_patterns": [...],
  "meta_learning": {{...}}
}}'''
    
    # Get API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not set. Cannot query real agent.\n"
            "This tool requires actual LLM call, not simulation."
        )
    
    # REAL LLM call to Anthropic
    client = Anthropic(api_key=api_key)
    
    print("="*70)
    print("🤖 Querying REAL meta-planning-analyzer agent")
    print("="*70)
    print("   Model: claude-sonnet-4-5-20250929")
    print("   Extended Thinking: 10,000 token budget")
    print("   Prompt Caching: Enabled (agent prompt ~10k tokens)")
    print("   Mode: " + ("Streaming" if show_thinking else "Non-streaming"))
    print("="*70)
    print()
    
    if show_thinking:
        # Streaming mode - show Extended Thinking process
        thinking_parts = []
        response_parts = []
        
        with client.messages.stream(
            model="claude-sonnet-4-5-20250929",
            max_tokens=16_000,
            
            # Extended Thinking for deep analysis
            thinking={"type": "enabled", "budget_tokens": 10_000},
            
            # Cache agent prompt (reused across queries)
            system=[{
                "type": "text",
                "text": agent_prompt,
                "cache_control": {"type": "ephemeral"}
            }],
            
            messages=[{"role": "user", "content": user_query}]
        ) as stream:
            
            for event in stream:
                if event.type == "content_block_start":
                    if event.content_block.type == "thinking":
                        print("🧠 [Meta-Planning-Analyzer Extended Thinking]")
                        print("-" * 70)
                
                elif event.type == "content_block_delta":
                    if event.delta.type == "thinking_delta":
                        content = event.delta.thinking
                        print(content, end="", flush=True)
                        thinking_parts.append(content)
                    
                    elif event.delta.type == "text_delta":
                        response_parts.append(event.delta.text)
                
                elif event.type == "content_block_stop":
                    if thinking_parts and not response_parts:
                        print("\n" + "-" * 70)
                        print("\n📝 [Agent Response]")
                        print("-" * 70)
            
            # Get final message for cache stats
            final_msg = stream.get_final_message()
            
            # Log cache performance
            if hasattr(final_msg.usage, 'cache_read_input_tokens'):
                cache_read = final_msg.usage.cache_read_input_tokens
                if cache_read > 0:
                    print(f"\n💾 Prompt cache hit: {cache_read:,} tokens")
            
            response_text = "".join(response_parts)
    
    else:
        # Non-streaming mode
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=16_000,
            thinking={"type": "enabled", "budget_tokens": 10_000},
            system=[{
                "type": "text",
                "text": agent_prompt,
                "cache_control": {"type": "ephemeral"}
            }],
            messages=[{"role": "user", "content": user_query}]
        )
        
        # Extract text (skip thinking block)
        for block in response.content:
            if block.type == "text":
                response_text = block.text
                break
    
    # Parse JSON from response
    if "```json" in response_text:
        json_start = response_text.find("```json") + 7
        json_end = response_text.find("```", json_start)
        response_text = response_text[json_start:json_end].strip()
    elif "```" in response_text:
        json_start = response_text.find("```") + 3
        json_end = response_text.find("```", json_start)
        response_text = response_text[json_start:json_end].strip()
    
    # Try to parse JSON
    try:
        feedback = json.loads(response_text)
        print("\n✅ Feedback received and parsed successfully")
        return feedback
    except json.JSONDecodeError as e:
        print(f"\n⚠️ JSON parsing failed: {e}")
        print(f"   Returning raw feedback...")
        return {
            "raw_feedback": response_text,
            "parse_error": True,
            "error_message": str(e)
        }


def validate_feedback_quality(feedback: dict, planning_trace: dict) -> dict:
    """
    Validate that feedback is real and useful (not generic).
    
    Args:
        feedback: Feedback dict from query_real_meta_analyzer()
        planning_trace: Original planning trace
    
    Returns:
        Validation result dict
    """
    checks = {}
    
    # Check 1: Has specific suggestions
    checks["has_suggestions"] = (
        len(feedback.get("improvement_suggestions", [])) > 0 or
        len(feedback.get("inefficiencies_detected", [])) > 0
    )
    
    # Check 2: References actual steps from trace
    feedback_str = json.dumps(feedback, ensure_ascii=False)
    trace_steps = planning_trace.get("total_steps", 0)
    
    checks["references_steps"] = any(
        f"step {i}" in feedback_str.lower() or f"단계 {i}" in feedback_str
        for i in range(1, trace_steps + 1)
    )
    
    # Check 3: Is actionable (has concrete suggestions)
    checks["is_actionable"] = (
        "suggestion" in feedback_str.lower() or
        "recommend" in feedback_str.lower()
    )
    
    # Check 4: Not just generic advice
    checks["specific_to_trace"] = (
        checks["references_steps"] and
        len(feedback_str) > 500  # Substantial feedback
    )
    
    # Overall quality
    quality_score = sum(checks.values()) / len(checks)
    
    return {
        "checks": checks,
        "quality_score": quality_score,
        "is_valid": quality_score >= 0.75,
        "recommendation": "Use feedback" if quality_score >= 0.75 else "Re-query with more specific prompt"
    }

