"""
E2E Test for Example Generator (Phase 3 - Milestone 2)

Tests the example-generator's ability to:
1. Read an existing mathematical document
2. Generate graded examples (easy → hard)
3. Include step-by-step solutions with LaTeX
4. Add Python/SymPy implementations
5. Create counterexamples
6. Insert examples into document using Edit tool

Success criteria:
- Examples section added or enhanced
- At least 3 graded examples with solutions
- Python implementation included
- LaTeX formulas properly formatted
- Document size increased significantly
"""

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from agents import example_generator
import asyncio
import os
import re


async def test_example_generator():
    """Test example-generator in isolation: Add examples to Pythagorean Theorem"""

    print("=" * 80)
    print("Phase 3 - Milestone 2: Example Generator Isolation Test")
    print("=" * 80)

    options = ClaudeAgentOptions(
        model="sonnet",
        permission_mode="acceptEdits",
        setting_sources=["project"],

        allowed_tools=[
            'Read',
            'Edit',
            'TodoWrite',
            'Bash',  # For Python verification
        ],

        agents={
            "example-generator": example_generator,
        },

        mcp_servers={}
    )

    test_file = "/home/kc-palantir/math-vault/Theorems/pythagorean-theorem-test.md"

    # === SETUP: Create minimal document ===
    print("\n[SETUP] Creating minimal document for testing...")
    print("-" * 80)

    minimal_content = """---
type: theorem
id: pythagorean-theorem-test
domain: geometry
level: middle-school
difficulty: 3
language: en
prerequisites:
  - "[[right-triangle]]"
  - "[[square]]"
created: 2025-10-12
---

# Pythagorean Theorem

## Definition

In a right triangle, the square of the length of the hypotenuse (the side opposite the right angle) is equal to the sum of the squares of the lengths of the other two sides.

## Mathematical Formula

$$
a^2 + b^2 = c^2
$$

where:
- $a$ and $b$ are the lengths of the two legs
- $c$ is the length of the hypotenuse

## Prerequisites

To understand this theorem, you need:
- [[right-triangle]]: A triangle with one 90-degree angle
- [[square]]: The result of multiplying a number by itself

## Related Concepts

- [[distance-formula]]
- [[trigonometry]]
"""

    # Write minimal document
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(minimal_content)

    initial_size = os.path.getsize(test_file)
    print(f"✅ Minimal document created ({initial_size} bytes)")
    print(f"   Location: {test_file}")

    async with ClaudeSDKClient(options=options) as client:

        # === REQUEST: Add Examples ===
        print("\n[REQUEST] Delegating example generation to example-generator...")
        print("-" * 80)

        query = f"""Please delegate to example-generator to add comprehensive examples to: {test_file}

The example-generator should:
1. Read the existing document
2. Generate at least 3 graded examples (easy → intermediate → advanced)
3. Include step-by-step solutions with LaTeX
4. Add Python/SymPy implementation showing how to:
   - Solve for unknown side
   - Verify Pythagorean triple
5. Add at least 1 counterexample or common mistake
6. Use Edit tool to insert Examples section after Mathematical Formula section

This is the Pythagorean Theorem, so examples should involve:
- Finding hypotenuse given two legs
- Finding a leg given hypotenuse and other leg
- Real-world applications (ladders, ramps, etc.)
"""

        await client.query(query)

        response_count = 0
        async for message in client.receive_response():
            response_count += 1
            if response_count <= 5:
                msg_str = str(message)[:120]
                print(f"  Response {response_count}: {msg_str}...")

        print(f"\n  Total responses: {response_count}")

    # === VERIFICATION ===
    print("\n" + "=" * 80)
    print("Example Generation Verification")
    print("=" * 80)

    # Read enhanced document
    with open(test_file, 'r', encoding='utf-8') as f:
        enhanced_content = f.read()

    enhanced_size = os.path.getsize(test_file)
    size_increase = enhanced_size - initial_size

    # Check 1: File size increased
    size_increased = enhanced_size > initial_size * 1.5  # At least 50% increase
    print(f"\n[1/8] File size increased significantly: {'✅' if size_increased else '❌'}")
    print(f"      Initial: {initial_size} bytes → Enhanced: {enhanced_size} bytes (+{size_increase} bytes)")

    # Check 2: Examples section exists
    has_examples_section = '## Examples' in enhanced_content
    print(f"[2/8] Examples section added: {'✅' if has_examples_section else '❌'}")

    # Check 3: Multiple examples (at least 3)
    example_count = enhanced_content.count('### Example')
    examples_ok = example_count >= 3
    print(f"[3/8] Multiple examples (≥3): {'✅' if examples_ok else '❌'} ({example_count} found)")

    # Check 4: Solutions present
    has_solutions = 'Solution' in enhanced_content or 'Step' in enhanced_content
    print(f"[4/8] Step-by-step solutions: {'✅' if has_solutions else '❌'}")

    # Check 5: LaTeX formulas in examples
    latex_display_count = len(re.findall(r'\$\$.*?\$\$', enhanced_content, re.DOTALL))
    latex_inline_count = len(re.findall(r'\$[^\$]+\$', enhanced_content))
    latex_ok = (latex_display_count + latex_inline_count) > initial_size // 100  # Reasonable formula density
    print(f"[5/8] LaTeX formulas present: {'✅' if latex_ok else '❌'} (display: {latex_display_count}, inline: {latex_inline_count})")

    # Check 6: Python implementation
    has_python = '```python' in enhanced_content
    print(f"[6/8] Python implementation: {'✅' if has_python else '❌'}")

    # Check 7: Counterexample or common mistakes
    has_counterexample = ('Counterexample' in enhanced_content or
                         'Common Mistake' in enhanced_content or
                         'incorrect' in enhanced_content.lower())
    print(f"[7/8] Counterexample/common mistakes: {'✅' if has_counterexample else '❌'}")

    # Check 8: Practice problems (optional but good)
    has_practice = 'Practice' in enhanced_content
    print(f"[8/8] Practice problems (optional): {'✅' if has_practice else '⚠️  Not required'}")

    # === CONTENT PREVIEW ===
    print("\n" + "-" * 80)
    print("Enhanced Document Preview:")
    print("-" * 80)

    # Extract Examples section
    examples_match = re.search(r'## Examples\n(.*?)(?=\n## |$)', enhanced_content, re.DOTALL)
    if examples_match:
        examples_preview = examples_match.group(1)[:800]
        print(examples_preview)
        if len(examples_match.group(1)) > 800:
            print("\n... (truncated)")
    else:
        print("Examples section not found")

    # === FINAL ASSESSMENT ===
    print("\n" + "=" * 80)
    print("Test Results Summary")
    print("=" * 80)

    checks = [
        ("File size increased", size_increased),
        ("Examples section added", has_examples_section),
        ("Multiple examples", examples_ok),
        ("Solutions present", has_solutions),
        ("LaTeX formulas", latex_ok),
        ("Python implementation", has_python),
        ("Counterexample", has_counterexample),
        ("Practice problems", has_practice),
    ]

    passed_count = sum(1 for _, passed in checks if passed)
    total_count = len(checks)

    print(f"\nChecks passed: {passed_count}/{total_count}")
    for check_name, passed in checks:
        print(f"  {'✅' if passed else '❌'} {check_name}")

    # Success threshold: 6/8 checks must pass (practice problems optional)
    success = passed_count >= 6

    print("\n" + "=" * 80)
    if success:
        print("✅ EXAMPLE GENERATOR TEST PASSED")
        print("   Example-generator successfully created comprehensive examples")
    else:
        print("❌ EXAMPLE GENERATOR TEST FAILED")
        print(f"   Only {passed_count}/{total_count} checks passed (need 6/8)")
    print("=" * 80)

    return success


async def main():
    """Run example generator isolation test"""
    print("\n" + "=" * 80)
    print("Phase 3 - Milestone 2 Test Suite: Example Generator")
    print("Testing example-generator's ability to create high-quality examples")
    print("=" * 80)

    try:
        test_success = await test_example_generator()

        print("\n" + "=" * 80)
        print("Test Summary")
        print("=" * 80)
        print(f"Example Generator: {'✅ PASSED' if test_success else '❌ FAILED'}")

        print("\n" + "=" * 80)
        if test_success:
            print("✅ MILESTONE 2 TEST PASSED")
            print("   Ready to proceed to Milestone 3 (Full Pipeline Integration)")
        else:
            print("❌ MILESTONE 2 TEST FAILED")
            print("   Need to improve example-generator implementation")
        print("=" * 80)

        return 0 if test_success else 1

    except Exception as e:
        print(f"\n❌ ERROR during test: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()

    exit_code = asyncio.run(main())
    exit(exit_code)
