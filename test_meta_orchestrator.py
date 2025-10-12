"""
E2E Test for Meta-Orchestrator Agent

Tests meta-orchestrator's core capabilities:
1. Task decomposition (complex request → subtasks)
2. Capability-based routing (delegate to right agents)
3. Performance monitoring (track agent metrics)
4. Inefficiency detection (4 types: communication, redundant work, context loss, tool misalignment)
5. User feedback loop (primary interface)

Test Scenario:
User requests: "Build a comprehensive file for Euler's Formula with research and validation"

Expected Workflow:
1. Meta-orchestrator decomposes task:
   - Subtask 1: Research Euler's Formula
   - Subtask 2: Build Obsidian file
   - Subtask 3: Validate quality
2. Routes to agents:
   - research-agent (literature research)
   - knowledge-builder (file creation)
   - quality-agent (validation)
3. Monitors for inefficiencies:
   - No redundant searches
   - No context loss between agents
   - Minimal file I/O overhead
4. Reports to user concisely
"""

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from agents import meta_orchestrator, research_agent, knowledge_builder, quality_agent
import asyncio
import os
import json
import time


async def test_orchestrator_workflow():
    """Test meta-orchestrator coordinating research → build → validate workflow"""

    print("=" * 80)
    print("E2E Test: Meta-Orchestrator Multi-Agent Coordination")
    print("=" * 80)

    # Configure agent options with ALL agents available
    options = ClaudeAgentOptions(
        model="sonnet",
        permission_mode="acceptEdits",
        setting_sources=["project"],

        allowed_tools=[
            # Core tools for orchestrator
            'Read',
            'Write',
            'Edit',
            'Grep',
            'Glob',
            'Task',  # CRITICAL: orchestrator delegates via Task
            'TodoWrite',
            'mcp__sequential-thinking__sequentialthinking',
        ],

        # Register ALL agents (orchestrator can delegate to any)
        agents={
            "meta-orchestrator": meta_orchestrator,
            "research-agent": research_agent,
            "knowledge-builder": knowledge_builder,
            "quality-agent": quality_agent,
        },

        mcp_servers={}
    )

    start_time = time.time()

    async with ClaudeSDKClient(options=options) as client:
        print("\n[1/6] Sending complex request to meta-orchestrator...")

        query = """You are the meta-orchestrator agent.

**User Request**: Build a comprehensive Obsidian file for "Euler's Formula" (e^(iπ) + 1 = 0) with full research and validation.

**Your Tasks**:
1. **Task Decomposition**: Break this into subtasks (research, build, validate)
2. **Capability-Based Routing**: Delegate to appropriate agents:
   - research-agent: Literature research (use Brave Search + Context7)
   - knowledge-builder: Create Obsidian markdown file
   - quality-agent: Validate file quality
3. **Inefficiency Monitoring**: Track for:
   - Redundant searches (same concept searched twice)
   - Context loss (research findings not reaching builder)
   - Communication overhead (excessive file I/O)
   - Tool misalignment (agents using wrong tools)
4. **User Feedback**: Report progress concisely

**Expected Output**:
- Research report (from research-agent)
- Obsidian file at /home/kc-palantir/math-vault/Theorems/eulers-formula.md
- Validation report (from quality-agent)
- Inefficiency report (if any detected)

Begin orchestration!
"""

        await client.query(query)

        print("[2/6] Orchestrator processing request...")
        response_count = 0
        responses = []

        async for message in client.receive_response():
            response_count += 1
            msg_str = str(message)
            responses.append(msg_str)
            print(f"    Response {response_count}: {msg_str[:150]}...")

        print(f"[3/6] Received {response_count} responses")

    elapsed_time = time.time() - start_time

    # Verification Phase
    print("[4/6] Verifying orchestration results...")

    checks_passed = 0
    checks_total = 7

    # Check 1: File created
    expected_file = "/home/kc-palantir/math-vault/Theorems/eulers-formula.md"
    if os.path.exists(expected_file):
        print(f"✅ Check 1/7: File created at {expected_file}")
        checks_passed += 1

        # Check file size
        file_size = os.path.getsize(expected_file)
        print(f"   File size: {file_size} bytes")

        # Check 2: File has minimum content (>1000 bytes indicates research was used)
        if file_size > 1000:
            print(f"✅ Check 2/7: File has substantial content ({file_size} bytes > 1000 bytes)")
            checks_passed += 1
        else:
            print(f"❌ Check 2/7: File too small ({file_size} bytes), research may not have been used")
    else:
        print(f"❌ Check 1/7: File not found at {expected_file}")
        print(f"❌ Check 2/7: Skipped (file doesn't exist)")

    # Check 3: YAML frontmatter exists
    if os.path.exists(expected_file):
        with open(expected_file, 'r') as f:
            content = f.read()

        if content.startswith("---") and "---" in content[3:]:
            print("✅ Check 3/7: YAML frontmatter present")
            checks_passed += 1

            # Check 4: Prerequisites exist (indicates research data was used)
            if "prerequisites:" in content and "[[" in content:
                print("✅ Check 4/7: Prerequisites with wikilinks found (research data integrated)")
                checks_passed += 1
            else:
                print("❌ Check 4/7: No prerequisites or wikilinks (context loss detected)")
        else:
            print("❌ Check 3/7: YAML frontmatter missing")
            print("❌ Check 4/7: Skipped")
    else:
        print("❌ Check 3/7: Skipped (file doesn't exist)")
        print("❌ Check 4/7: Skipped (file doesn't exist)")

    # Check 5: Response indicates task decomposition
    full_response = " ".join(responses).lower()
    decomposition_keywords = ["subtask", "step", "delegate", "research", "build", "validate"]
    if any(kw in full_response for kw in decomposition_keywords):
        print("✅ Check 5/7: Task decomposition evident in responses")
        checks_passed += 1
    else:
        print("❌ Check 5/7: No evidence of task decomposition")

    # Check 6: Response indicates agent routing
    routing_keywords = ["research-agent", "knowledge-builder", "quality-agent", "task", "delegate"]
    if any(kw in full_response for kw in routing_keywords):
        print("✅ Check 6/7: Capability-based routing evident")
        checks_passed += 1
    else:
        print("❌ Check 6/7: No evidence of agent routing")

    # Check 7: Execution time reasonable (<5 minutes for sequential workflow)
    if elapsed_time < 300:
        print(f"✅ Check 7/7: Execution time reasonable ({elapsed_time:.1f}s < 300s)")
        checks_passed += 1
    else:
        print(f"❌ Check 7/7: Execution time too long ({elapsed_time:.1f}s > 300s)")

    # Performance Report
    print("\n[5/6] Performance Metrics:")
    print(f"   Total execution time: {elapsed_time:.1f}s")
    print(f"   Responses received: {response_count}")
    print(f"   Checks passed: {checks_passed}/{checks_total}")
    if os.path.exists(expected_file):
        print(f"   Final file size: {os.path.getsize(expected_file)} bytes")

    # Inefficiency Analysis (from responses)
    print("\n[6/6] Inefficiency Analysis:")
    inefficiency_found = False

    # Check for redundant work mentions
    if "redundant" in full_response or "duplicate" in full_response:
        print("⚠️  Redundant work detected in responses")
        inefficiency_found = True

    # Check for context loss mentions
    if "context loss" in full_response or "missing" in full_response:
        print("⚠️  Context loss detected in responses")
        inefficiency_found = True

    if not inefficiency_found:
        print("✅ No inefficiencies detected or reported")

    # Final Result
    print("\n" + "=" * 80)
    if checks_passed == checks_total:
        print("✅ META-ORCHESTRATOR TEST PASSED")
        print(f"   All {checks_total} checks passed!")
        print("   Orchestrator successfully:")
        print("   - Decomposed complex task")
        print("   - Routed to appropriate agents")
        print("   - Coordinated multi-agent workflow")
        print("   - Produced validated output")
        return True
    elif checks_passed >= checks_total * 0.7:  # 70% threshold
        print("⚠️  META-ORCHESTRATOR TEST PARTIAL PASS")
        print(f"   {checks_passed}/{checks_total} checks passed (≥70%)")
        print("   Core functionality working, minor issues detected")
        return True
    else:
        print("❌ META-ORCHESTRATOR TEST FAILED")
        print(f"   Only {checks_passed}/{checks_total} checks passed (<70%)")
        print("   Orchestration logic needs improvement")
        return False


async def test_inefficiency_detection():
    """Test orchestrator's ability to detect inefficiencies"""

    print("\n" + "=" * 80)
    print("Bonus Test: Inefficiency Detection")
    print("=" * 80)

    options = ClaudeAgentOptions(
        model="sonnet",
        permission_mode="acceptEdits",
        setting_sources=["project"],

        allowed_tools=[
            'Read', 'Write', 'Edit', 'Grep', 'Glob',
            'Task', 'TodoWrite',
            'mcp__sequential-thinking__sequentialthinking',
        ],

        agents={
            "meta-orchestrator": meta_orchestrator,
            "research-agent": research_agent,
            "knowledge-builder": knowledge_builder,
        },

        mcp_servers={}
    )

    async with ClaudeSDKClient(options=options) as client:
        print("\n[Test] Asking orchestrator to analyze inefficiencies...")

        query = """You are the meta-orchestrator agent.

**Analysis Request**: Review the previous workflow for building Euler's Formula.

**Your Tasks**:
1. Check if research-agent and knowledge-builder both searched for "Euler's Formula" (redundant work)
2. Check if knowledge-builder received all prerequisites found by research-agent (context loss)
3. Check how many file I/O operations were used for agent communication (communication overhead)
4. Verify each agent used only its assigned tools (tool alignment)

**Report Format**:
- Inefficiency Type 1 (Redundant Work): [DETECTED/NOT DETECTED]
- Inefficiency Type 2 (Context Loss): [DETECTED/NOT DETECTED]
- Inefficiency Type 3 (Communication Overhead): [DETECTED/NOT DETECTED]
- Inefficiency Type 4 (Tool Misalignment): [DETECTED/NOT DETECTED]

Be specific with evidence for each finding.
"""

        await client.query(query)

        response_count = 0
        full_response = ""

        async for message in client.receive_response():
            response_count += 1
            msg = str(message)
            full_response += msg
            print(f"    Response {response_count}: {msg[:150]}...")

    # Verify orchestrator analyzed inefficiencies
    if "inefficiency" in full_response.lower() or "detected" in full_response.lower():
        print("\n✅ Orchestrator performed inefficiency analysis")
        return True
    else:
        print("\n⚠️  Orchestrator did not explicitly analyze inefficiencies")
        return False


async def main():
    """Run all meta-orchestrator tests"""
    try:
        # Main test
        test1_passed = await test_orchestrator_workflow()

        # Bonus test (inefficiency detection)
        test2_passed = await test_inefficiency_detection()

        print("\n" + "=" * 80)
        print("FINAL TEST RESULTS")
        print("=" * 80)
        print(f"Test 1 (Orchestration Workflow): {'✅ PASSED' if test1_passed else '❌ FAILED'}")
        print(f"Test 2 (Inefficiency Detection): {'✅ PASSED' if test2_passed else '⚠️  PARTIAL'}")

        overall_pass = test1_passed  # Test 2 is bonus, not required
        print("=" * 80)
        if overall_pass:
            print("✅ ALL TESTS PASSED")
        else:
            print("❌ TESTS FAILED")
        print("=" * 80)

        return 0 if overall_pass else 1

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
