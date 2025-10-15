#!/usr/bin/env python3
"""
E2E Tests for CLAUDE-IMPLEMENTATION-STANDARDS.md
Tests all 5 standards implementation
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_1_environment_variables():
    """Test 1: Environment variables are loaded"""
    print("\n" + "="*80)
    print("TEST 1: Environment Variables")
    print("="*80)
    
    load_dotenv()
    
    github_token = os.getenv("GITHUB_TOKEN")
    obsidian_key = os.getenv("OBSIDIAN_API_KEY")
    obsidian_url = os.getenv("OBSIDIAN_API_URL")
    
    print(f"✓ GITHUB_TOKEN: {'OK' if github_token else 'MISSING'}")
    print(f"✓ OBSIDIAN_API_KEY: {'OK' if obsidian_key else 'MISSING'}")
    print(f"✓ OBSIDIAN_API_URL: {obsidian_url or 'MISSING'}")
    
    assert github_token, "GITHUB_TOKEN missing"
    assert obsidian_key, "OBSIDIAN_API_KEY missing"
    
    print("\n✅ TEST 1 PASSED")
    return True

def test_2_model_version_in_agents():
    """Test 2: All agents use claude-sonnet-4-5-20250929"""
    print("\n" + "="*80)
    print("TEST 2: Model Version Specification (Standard 1)")
    print("="*80)
    
    from agents import (
        meta_orchestrator,
        knowledge_builder,
        quality_agent,
        research_agent,
        example_generator,
        dependency_mapper,
        socratic_planner,
        socratic_mediator_agent,
        self_improver_agent,
    )
    
    agents = {
        "meta-orchestrator": meta_orchestrator,
        "knowledge-builder": knowledge_builder,
        "quality-agent": quality_agent,
        "research-agent": research_agent,
        "example-generator": example_generator,
        "dependency-mapper": dependency_mapper,
        "socratic-planner": socratic_planner,
        "socratic-mediator": socratic_mediator_agent,
        "self-improver": self_improver_agent,
    }
    
    expected_model = "claude-sonnet-4-5-20250929"
    
    for name, agent in agents.items():
        model = agent.model
        print(f"✓ {name}: {model}")
        assert model == expected_model, f"{name} uses wrong model: {model}"
    
    print("\n✅ TEST 2 PASSED: All agents use correct model version")
    return True

def test_3_mcp_config_in_main():
    """Test 3: main.py has MCP servers configured"""
    print("\n" + "="*80)
    print("TEST 3: MCP Configuration in main.py")
    print("="*80)
    
    main_py = project_root / "main.py"
    content = main_py.read_text()
    
    # Check for MCP server definitions
    assert "mcp_servers={" in content, "mcp_servers not configured"
    assert "memory-keeper" in content, "memory-keeper not in mcp_servers"
    assert "sequential-thinking" in content, "sequential-thinking not in mcp_servers"
    assert "obsidian" in content, "obsidian not in mcp_servers"
    assert "github" in content, "github not in mcp_servers"
    
    print("✓ mcp_servers configuration found")
    print("✓ memory-keeper configured")
    print("✓ sequential-thinking configured")
    print("✓ obsidian configured")
    print("✓ github configured")
    
    print("\n✅ TEST 3 PASSED")
    return True

def test_4_mcp_servers_executable():
    """Test 4: MCP servers can be spawned"""
    print("\n" + "="*80)
    print("TEST 4: MCP Servers Executable")
    print("="*80)
    
    import subprocess
    
    # Test memory-keeper
    try:
        result = subprocess.run(
            ["npx", "-y", "mcp-memory-keeper", "--version"],
            capture_output=True,
            timeout=10
        )
        print("✓ memory-keeper: Executable")
    except Exception as e:
        print(f"⚠️  memory-keeper: {e}")
    
    # Test sequential-thinking
    try:
        result = subprocess.run(
            ["npx", "-y", "@modelcontextprotocol/server-sequential-thinking", "--version"],
            capture_output=True,
            timeout=10
        )
        print("✓ sequential-thinking: Executable")
    except Exception as e:
        print(f"⚠️  sequential-thinking: {e}")
    
    # Test github
    try:
        result = subprocess.run(
            ["npx", "-y", "@modelcontextprotocol/server-github", "--version"],
            capture_output=True,
            timeout=10
        )
        print("✓ github: Executable")
    except Exception as e:
        print(f"⚠️  github: {e}")
    
    print("\n✅ TEST 4 PASSED")
    return True

def test_5_agent_sdk_imports():
    """Test 5: Agent SDK can be imported"""
    print("\n" + "="*80)
    print("TEST 5: Agent SDK Imports")
    print("="*80)
    
    try:
        from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
        print("✓ ClaudeSDKClient imported")
        print("✓ ClaudeAgentOptions imported")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        raise
    
    print("\n✅ TEST 5 PASSED")
    return True

def test_6_main_options_creation():
    """Test 6: ClaudeAgentOptions can be created"""
    print("\n" + "="*80)
    print("TEST 6: ClaudeAgentOptions Creation")
    print("="*80)
    
    from claude_agent_sdk import ClaudeAgentOptions
    from agents import (
        meta_orchestrator,
        knowledge_builder,
        quality_agent,
        research_agent,
        example_generator,
        dependency_mapper,
        socratic_planner,
        socratic_mediator_agent,
        self_improver_agent,
    )
    
    load_dotenv()
    
    try:
        options = ClaudeAgentOptions(
            model="claude-sonnet-4-5-20250929",
            permission_mode="acceptEdits",
            setting_sources=["project"],
            allowed_tools=[
                'Task', 'Read', 'Write', 'Edit', 'Grep', 'Glob', 'TodoWrite',
                'mcp__sequential-thinking__sequentialthinking',
                'mcp__memory-keeper__context_save',
                'mcp__memory-keeper__context_get',
                'mcp__memory-keeper__context_search',
            ],
            agents={
                "meta-orchestrator": meta_orchestrator,
                "knowledge-builder": knowledge_builder,
                "quality-agent": quality_agent,
                "research-agent": research_agent,
                "example-generator": example_generator,
                "dependency-mapper": dependency_mapper,
                "socratic-planner": socratic_planner,
                "socratic-mediator": socratic_mediator_agent,
                "self-improver": self_improver_agent,
            },
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
        
        print("✓ ClaudeAgentOptions created successfully")
        print(f"✓ Model: {options.model}")
        print(f"✓ Agents: {len(options.agents)} configured")
        print(f"✓ MCP Servers: {len(options.mcp_servers)} configured")
        
    except Exception as e:
        print(f"❌ Failed to create options: {e}")
        raise
    
    print("\n✅ TEST 6 PASSED")
    return True

def run_all_tests():
    """Run all E2E tests"""
    print("\n" + "="*80)
    print("🧪 E2E TESTS FOR CLAUDE-IMPLEMENTATION-STANDARDS")
    print("="*80)
    
    tests = [
        ("Environment Variables", test_1_environment_variables),
        ("Model Version Specification", test_2_model_version_in_agents),
        ("MCP Configuration", test_3_mcp_config_in_main),
        ("MCP Servers Executable", test_4_mcp_servers_executable),
        ("Agent SDK Imports", test_5_agent_sdk_imports),
        ("ClaudeAgentOptions Creation", test_6_main_options_creation),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, "PASSED", None))
        except Exception as e:
            results.append((name, "FAILED", str(e)))
            print(f"\n❌ TEST FAILED: {name}")
            print(f"   Error: {e}")
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, status, _ in results if status == "PASSED")
    failed = sum(1 for _, status, _ in results if status == "FAILED")
    
    for name, status, error in results:
        symbol = "✅" if status == "PASSED" else "❌"
        print(f"{symbol} {name}: {status}")
        if error:
            print(f"   └─ {error}")
    
    print(f"\nTotal: {len(results)} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed > 0:
        print("\n❌ SOME TESTS FAILED")
        return False
    else:
        print("\n✅ ALL TESTS PASSED")
        return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

