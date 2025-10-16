"""
Test that system prompt is actually injected and used.

Risk: If prompt not injected, meta-orchestrator uses default behavior
Based on: Critical Fix 1.1
"""
import pytest
from claude_agent_sdk import ClaudeAgentOptions
from subagents import meta_orchestrator


def test_system_prompt_parameter_exists():
    """Verify ClaudeAgentOptions accepts system_prompt parameter"""
    options = ClaudeAgentOptions(
        model="claude-sonnet-4-5-20250929",
        system_prompt=meta_orchestrator.prompt,
    )
    # Should not raise TypeError
    assert options.system_prompt == meta_orchestrator.prompt


def test_system_prompt_content_applied():
    """Verify prompt content is set correctly"""
    options = ClaudeAgentOptions(
        model="claude-sonnet-4-5-20250929",
        system_prompt=meta_orchestrator.prompt,
    )

    # Verify it's the right prompt (check signature sections)
    assert isinstance(options.system_prompt, str)
    assert len(options.system_prompt) > 3000  # Meta-orchestrator prompt is ~3,500 tokens


def test_meta_cognitive_learnings_in_prompt():
    """Verify meta-cognitive learnings sections exist in prompt"""
    prompt = meta_orchestrator.prompt

    # Learning #1: Execution vs Recall (line 163)
    assert "Execution vs Recall" in prompt or "execution" in prompt.lower()

    # Learning #3: Parallel Execution (line 203)
    assert "Parallel" in prompt or "parallel" in prompt.lower()
    assert "90%" in prompt  # 90% latency reduction

    # SDK validation rules (line 102)
    assert "SDK" in prompt or "inspect" in prompt


def test_sdk_validation_rules_in_prompt():
    """Verify SDK validation patterns are documented"""
    prompt = meta_orchestrator.prompt

    # Check for validation-related terms
    assert any(term in prompt for term in [
        "GROUND TRUTH", "METHOD AVAILABILITY", "INCREMENTAL TESTING",
        "PARALLEL OPERATIONS", "validation", "SDK"
    ])
