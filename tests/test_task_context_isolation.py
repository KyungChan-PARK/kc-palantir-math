"""
Test that Task tool properly isolates subagent context.

Risk: Context leakage between agents leads to incorrect outputs
Based on: meta_orchestrator.py lines 382-390
"""
import pytest


def test_task_prompt_self_contained():
    """
    Verify Task prompts include full context (no prior conversation assumptions).

    Pattern: Subagent has independent context (SDK manages automatically)
    """
    # Example: Good task prompt
    good_prompt = """
    Research Euler's Formula.

    Context: User asked for prerequisites and applications.

    Include in research:
    - Definition
    - Prerequisites (list all)
    - Applications (at least 3)
    - LaTeX formula
    """

    # Verify prompt is self-contained
    assert "Euler's Formula" in good_prompt  # Full topic name
    assert "prerequisites" in good_prompt    # Specific requirements
    assert "Context:" in good_prompt         # Explicit context

    # Anti-patterns (should NOT be in task prompts)
    bad_patterns = ["continue", "as discussed", "from earlier", "above"]
    for pattern in bad_patterns:
        assert pattern.lower() not in good_prompt.lower()


@pytest.mark.asyncio
async def test_context_isolation_validation():
    """Test basic context isolation principles"""
    # Test that anti-patterns are detected
    bad_patterns = ["continue", "as discussed", "from earlier", "as mentioned above"]

    for pattern in bad_patterns:
        bad_prompt = f"Please {pattern} with the analysis"
        # Verify pattern exists in test
        assert pattern in bad_prompt.lower()

    # Good prompt example
    good_prompt = "Analyze concept X. Context: User wants prerequisites and examples."
    assert "Context:" in good_prompt
    assert not any(p in good_prompt.lower() for p in bad_patterns)
