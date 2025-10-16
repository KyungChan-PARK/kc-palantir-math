"""
Export Agents to Claude Code Format

Exports all SemanticAgentDefinition instances to .claude/agents/*.md format
for automatic subagent discovery by Claude Code.

Features:
- Auto-discovery of all agent definitions
- Semantic role to trigger keyword mapping
- YAML frontmatter generation
- Tool permission extraction
- Batch export of all agents

Usage:
    python3 tools/export_agents_to_claude_format.py
    
    # Creates .claude/agents/ with 18 .md files

VERSION: 1.0.0
DATE: 2025-10-16
"""

from pathlib import Path
import importlib
import sys

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from semantic_layer import SemanticAgentDefinition, SemanticRole
from claude_agent_sdk import AgentDefinition


def export_agent_to_claude_format(agent: SemanticAgentDefinition, agent_name: str, output_dir: Path):
    """
    Export SemanticAgentDefinition to .claude/agents/*.md format.
    
    Args:
        agent: Agent definition instance
        agent_name: Name of the agent
        output_dir: Output directory (.claude/agents/)
    """
    # Convert underscores to hyphens for Claude Code convention
    name = agent_name.replace('_', '-')
    
    # Map semantic role to description trigger keywords
    role_keywords = {
        SemanticRole.ORCHESTRATOR: "MUST BE USED for coordination tasks",
        SemanticRole.SPECIALIST: "Use PROACTIVELY for specialized tasks",
        SemanticRole.VALIDATOR: "Use immediately after code changes",
        SemanticRole.CLARIFIER: "Use when requirements are ambiguous",
        SemanticRole.BUILDER: "Use for content creation tasks",
        SemanticRole.ANALYZER: "Use for analysis and insights",
        SemanticRole.IMPROVER: "Use for system improvement"
    }
    
    # Build description with role trigger
    description = agent.description
    
    if hasattr(agent, 'semantic_role') and agent.semantic_role in role_keywords:
        description += f" {role_keywords[agent.semantic_role]}"
    
    # Extract tools (default to common set if not specified)
    if hasattr(agent, 'tools') and agent.tools:
        tools_str = ', '.join(agent.tools)
    else:
        # Default tools based on role
        if hasattr(agent, 'semantic_role'):
            if agent.semantic_role == SemanticRole.VALIDATOR:
                tools_str = 'Read, Grep, Glob'  # Read-only
            elif agent.semantic_role == SemanticRole.BUILDER:
                tools_str = 'Read, Write, Edit, Grep, Glob'
            elif agent.semantic_role == SemanticRole.ORCHESTRATOR:
                tools_str = 'Task, Read, Write, Edit, Grep, Glob, TodoWrite'
            else:
                tools_str = 'Read, Write, Edit, Grep, Glob, Bash'
        else:
            tools_str = 'Read, Write, Edit, Grep, Glob'
    
    # Generate markdown file with YAML frontmatter
    content = f"""---
name: {name}
description: {description}
tools: {tools_str}
model: sonnet
---

{agent.prompt}
"""
    
    # Write to output directory
    output_path = output_dir / f"{name}.md"
    output_path.write_text(content)
    print(f"✅ Exported: {name}.md")


def export_all_agents():
    """
    Export all agents to .claude/agents/ directory.
    
    Discovers all agent definitions from agents/ directory and exports them
    to Claude Code compatible .md format.
    """
    print("=" * 70)
    print("Exporting Agents to Claude Code Format")
    print("=" * 70)
    print()
    
    # Add agents directory to path
    agents_dir = Path(__file__).parent.parent / "agents"
    if str(agents_dir) not in sys.path:
        sys.path.insert(0, str(agents_dir))
    
    # Output directory
    output_dir = Path(__file__).parent.parent / ".claude" / "agents"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Output directory: {output_dir}")
    print()
    
    # List of agent modules to export
    agent_modules = [
        'meta_orchestrator',
        'research_agent',
        'knowledge_builder',
        'quality_agent',
        'socratic_requirements_agent',
        'test_automation_specialist',
        'security_auditor',
        'performance_engineer',
        'problem_scaffolding_generator_agent',
        'dynamic_learning_agent',
        'neo4j_query_agent',
        'personalization_engine_agent',
        'problem_decomposer_agent',
        'semantic_manager_agent',
        'kinetic_execution_agent',
        'meta_query_helper',
        'meta_planning_analyzer',
        'self_improver_agent'
    ]
    
    exported_count = 0
    failed_count = 0
    
    for module_name in agent_modules:
        try:
            # Import module
            module = importlib.import_module(f"agents.{module_name}")
            
            # Find agent definition
            agent_def = None
            agent_var_name = None
            
            # Try common naming patterns
            for attr_name in dir(module):
                if attr_name.startswith('_'):
                    continue
                
                attr = getattr(module, attr_name)
                
                # Check if it's an AgentDefinition or SemanticAgentDefinition
                if isinstance(attr, (AgentDefinition, SemanticAgentDefinition)):
                    agent_def = attr
                    agent_var_name = attr_name
                    break
            
            if agent_def is None:
                print(f"⚠️  Skipped {module_name}: No agent definition found")
                failed_count += 1
                continue
            
            # Export to .claude/agents/
            export_agent_to_claude_format(agent_def, agent_var_name, output_dir)
            exported_count += 1
            
        except Exception as e:
            print(f"❌ Failed to export {module_name}: {e}")
            failed_count += 1
    
    print()
    print("=" * 70)
    print(f"Export Complete: {exported_count} agents exported, {failed_count} failed")
    print("=" * 70)
    print()
    
    # List exported files
    if exported_count > 0:
        print("Exported agents:")
        for md_file in sorted(output_dir.glob("*.md")):
            print(f"  - {md_file.name}")
    
    return exported_count, failed_count


if __name__ == "__main__":
    export_all_agents()

