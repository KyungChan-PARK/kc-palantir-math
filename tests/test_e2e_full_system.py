#!/usr/bin/env python3
"""
Full System E2E Test
Tests complete agent system with MCP integration
"""

import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def test_full_system_startup():
    """Test 7: Full system can start"""
    print("\n" + "="*80)
    print("TEST 7: Full System Startup")
    print("="*80)
    
    from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
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
    
    print("Creating ClaudeAgentOptions...")
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
    
    print("✓ Options created")
    
    print("\nInitializing ClaudeSDKClient...")
    try:
        async with ClaudeSDKClient(options=options) as client:
            print("✓ Client initialized successfully")
            print("✓ MCP servers should be spawning...")
            
            # Wait a bit for MCP servers to initialize
            await asyncio.sleep(2)
            
            print("✓ System is running")
            
            # Don't actually send a query in test
            # Just verify the system can start
            
        print("✓ Client closed cleanly")
        
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        import traceback
        traceback.print_exc()
        raise
    
    print("\n✅ TEST 7 PASSED: Full system startup successful")
    return True

async def run_integration_tests():
    """Run integration tests"""
    print("\n" + "="*80)
    print("🔗 INTEGRATION E2E TESTS")
    print("="*80)
    
    tests = [
        ("Full System Startup", test_full_system_startup),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = await test_func()
            results.append((name, "PASSED", None))
        except Exception as e:
            results.append((name, "FAILED", str(e)))
            print(f"\n❌ TEST FAILED: {name}")
            print(f"   Error: {e}")
    
    # Summary
    print("\n" + "="*80)
    print("📊 INTEGRATION TEST SUMMARY")
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
        print("\n✅ ALL INTEGRATION TESTS PASSED")
        return True

if __name__ == "__main__":
    success = asyncio.run(run_integration_tests())
    sys.exit(0 if success else 1)

