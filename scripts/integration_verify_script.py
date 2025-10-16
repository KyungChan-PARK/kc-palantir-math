#!/usr/bin/env python3
"""
Claude Code 2.0 Integration Verification Script

Verifies all components of the Claude Code 2.0 integration:
1. Agent exports to .claude/agents/
2. Hook system configuration
3. Memory tool adapter
4. Parallel tool calling prompts
5. Session management
6. Streaming configuration

Usage:
    python3 scripts/verify_claude_code_integration.py

VERSION: 1.0.0
DATE: 2025-10-16
"""

from pathlib import Path
import json
import sys

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))


def verify_agent_exports():
    """Verify all 18 agents exported to .claude/agents/"""
    print("\n" + "=" * 70)
    print("1. Verifying Agent Exports")
    print("=" * 70)
    
    agents_dir = parent_dir / ".claude" / "agents"
    
    if not agents_dir.exists():
        print("❌ .claude/agents/ directory not found")
        return False
    
    expected_agents = [
        'meta-orchestrator.md',
        'research-agent.md',
        'knowledge-builder.md',
        'quality-agent.md',
        'socratic-requirements-agent.md',
        'test-automation-specialist.md',
        'security-auditor.md',
        'performance-engineer.md',
        'problem-scaffolding-generator-agent.md',
        'dynamic-learning-agent.md',
        'neo4j-query-agent.md',
        'personalization-engine-agent.md',
        'problem-decomposer-agent.md',
        'semantic-manager-agent.md',
        'kinetic-execution-agent.md',
        'meta-query-helper.md',
        'meta-planning-analyzer.md',
        'self-improver-agent.md'
    ]
    
    found_count = 0
    missing = []
    
    for agent_file in expected_agents:
        if (agents_dir / agent_file).exists():
            found_count += 1
            print(f"  ✅ {agent_file}")
        else:
            missing.append(agent_file)
            print(f"  ❌ {agent_file} - MISSING")
    
    print(f"\nResult: {found_count}/18 agents found")
    
    if missing:
        print(f"Missing: {', '.join(missing)}")
        return False
    
    return True


def verify_hooks_system():
    """Verify hook scripts and configuration"""
    print("\n" + "=" * 70)
    print("2. Verifying Hooks System")
    print("=" * 70)
    
    hooks_dir = parent_dir / ".claude" / "hooks"
    settings_file = parent_dir / ".claude" / "settings.json"
    
    expected_hooks = [
        'pre_tool_validation.py',
        'post_tool_learning.py',
        'session_metrics_reporter.py',
        'semantic_tier_guard.py'
    ]
    
    all_found = True
    
    # Check hook scripts
    for hook_file in expected_hooks:
        hook_path = hooks_dir / hook_file
        if hook_path.exists():
            # Check if executable
            import os
            if os.access(hook_path, os.X_OK):
                print(f"  ✅ {hook_file} (executable)")
            else:
                print(f"  ⚠️  {hook_file} (not executable)")
                all_found = False
        else:
            print(f"  ❌ {hook_file} - MISSING")
            all_found = False
    
    # Check settings.json
    if settings_file.exists():
        try:
            with open(settings_file, 'r') as f:
                settings = json.load(f)
            
            if 'hooks' in settings:
                hook_count = len(settings['hooks'])
                print(f"  ✅ settings.json ({hook_count} hook events configured)")
            else:
                print(f"  ⚠️  settings.json (no hooks configured)")
                all_found = False
        except Exception as e:
            print(f"  ❌ settings.json - Invalid JSON: {e}")
            all_found = False
    else:
        print(f"  ❌ settings.json - MISSING")
        all_found = False
    
    return all_found


def verify_memory_tool_adapter():
    """Verify memory tool adapter implementation"""
    print("\n" + "=" * 70)
    print("3. Verifying Memory Tool Adapter")
    print("=" * 70)
    
    try:
        from tools.memory_adapter_tool import MemoryAdapter
        
        # Test basic functionality
        test_memory_dir = parent_dir / "memories" / "test"
        adapter = MemoryAdapter(test_memory_dir)
        
        # Test create
        adapter.create("test_file.txt", "Test content")
        
        # Test view
        content = adapter.view("test_file.txt")
        assert content == "Test content", "View failed"
        
        # Test str_replace
        adapter.str_replace("test_file.txt", "Test", "Updated")
        content = adapter.view("test_file.txt")
        assert content == "Updated content", "Replace failed"
        
        # Cleanup
        adapter.delete("test_file.txt")
        
        print("  ✅ MemoryAdapter import successful")
        print("  ✅ create() method works")
        print("  ✅ view() method works")
        print("  ✅ str_replace() method works")
        print("  ✅ delete() method works")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Memory tool adapter verification failed: {e}")
        return False


def verify_prompts():
    """Verify advanced prompts in meta-orchestrator"""
    print("\n" + "=" * 70)
    print("4. Verifying Advanced Prompts")
    print("=" * 70)
    
    meta_orchestrator_file = parent_dir / "agents" / "meta_orchestrator.py"
    
    if not meta_orchestrator_file.exists():
        print("  ❌ meta_orchestrator.py not found")
        return False
    
    content = meta_orchestrator_file.read_text()
    
    checks = {
        "Parallel tool calling": "<use_parallel_tool_calls>" in content,
        "Extended thinking": "<extended_thinking_usage>" in content,
        "Context management": "<context_management>" in content,
        "Tier coordination": "<tier_coordination>" in content
    }
    
    all_passed = True
    for check_name, passed in checks.items():
        if passed:
            print(f"  ✅ {check_name} prompt found")
        else:
            print(f"  ❌ {check_name} prompt MISSING")
            all_passed = False
    
    return all_passed


def verify_streaming_config():
    """Verify streaming configuration in main.py"""
    print("\n" + "=" * 70)
    print("5. Verifying Streaming Configuration")
    print("=" * 70)
    
    main_file = parent_dir / "main.py"
    
    if not main_file.exists():
        print("  ❌ main.py not found")
        return False
    
    content = main_file.read_text()
    
    checks = {
        "include_partial_messages": 'include_partial_messages=True' in content,
        "Fine-grained streaming beta": 'fine-grained-tool-streaming-2025-05-14' in content,
        "Context management beta": 'context-management-2025-06-27' in content,
        "Session tracking (user)": 'user=f"math-system-' in content,
        "Resume support": 'resume=args.resume' in content,
        "Fork session support": 'fork_session=bool(args.fork)' in content
    }
    
    all_passed = True
    for check_name, passed in checks.items():
        if passed:
            print(f"  ✅ {check_name}")
        else:
            print(f"  ❌ {check_name} - MISSING")
            all_passed = False
    
    return all_passed


def verify_semantic_migrations():
    """Verify all agents use SemanticAgentDefinition"""
    print("\n" + "=" * 70)
    print("6. Verifying Semantic Agent Migrations")
    print("=" * 70)
    
    agent_files = [
        'knowledge_builder.py',
        'research_agent.py',
        'quality_agent.py',
        'meta_query_helper.py',
        'meta_planning_analyzer.py',
        'agent_registry.py'
    ]
    
    all_passed = True
    
    for agent_file in agent_files:
        file_path = parent_dir / "agents" / agent_file
        if not file_path.exists():
            print(f"  ❌ {agent_file} not found")
            all_passed = False
            continue
        
        content = file_path.read_text()
        
        if 'from semantic_layer import SemanticAgentDefinition' in content:
            print(f"  ✅ {agent_file} - uses SemanticAgentDefinition")
        else:
            print(f"  ❌ {agent_file} - still uses AgentDefinition")
            all_passed = False
    
    return all_passed


def verify_tier_key_fix():
    """Verify orchestrate_semantic has 'tier' key"""
    print("\n" + "=" * 70)
    print("7. Verifying orchestrate_semantic 'tier' Key")
    print("=" * 70)
    
    meta_orchestrator_file = parent_dir / "agents" / "meta_orchestrator.py"
    
    if not meta_orchestrator_file.exists():
        print("  ❌ meta_orchestrator.py not found")
        return False
    
    content = meta_orchestrator_file.read_text()
    
    # Find orchestrate_semantic method and check returns
    import re
    
    # Extract orchestrate_semantic method
    match = re.search(r'def orchestrate_semantic\(.*?\n(.*?)(?=\n    def |\nclass |\Z)', content, re.DOTALL)
    
    if not match:
        print("  ❌ orchestrate_semantic method not found")
        return False
    
    method_content = match.group(1)
    
    # Count return statements with 'tier' key
    return_statements = re.findall(r'return\s+\{[^}]*\}', method_content)
    tier_returns = [r for r in return_statements if '"tier"' in r or "'tier'" in r]
    
    print(f"  Found {len(return_statements)} return statements")
    print(f"  {len(tier_returns)} have 'tier' key")
    
    if len(tier_returns) == len(return_statements):
        print(f"  ✅ All return statements have 'tier' key")
        return True
    else:
        print(f"  ❌ Some return statements missing 'tier' key")
        return False


def main():
    """Run all verification checks"""
    print("\n" + "=" * 70)
    print("CLAUDE CODE 2.0 INTEGRATION VERIFICATION")
    print("=" * 70)
    
    results = {
        "Agent Exports": verify_agent_exports(),
        "Hooks System": verify_hooks_system(),
        "Memory Tool Adapter": verify_memory_tool_adapter(),
        "Advanced Prompts": verify_prompts(),
        "Streaming Config": verify_streaming_config(),
        "Semantic Migrations": verify_semantic_migrations(),
        "Tier Key Fix": verify_tier_key_fix()
    }
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for component, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {component}")
    
    print()
    print("=" * 70)
    print(f"Overall: {passed}/{total} components verified")
    print("=" * 70)
    
    if passed == total:
        print("\n🎉 All verifications passed! Claude Code 2.0 integration complete.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} component(s) failed verification.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

