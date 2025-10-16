#!/usr/bin/env python3
"""
Bulk Agent Enhancement Script

Adds runtime capabilities to multiple agents at once.
Applies Mixin pattern without modifying core logic.

Usage:
    python3 bulk_enhance_agents.py neo4j_query problem_decomposer personalization_engine

VERSION: 1.0.0
DATE: 2025-10-16
"""

import sys
from pathlib import Path


AGENT_ENHANCEMENTS = {
    'neo4j_query_agent': {
        'features': ['observability'],
        'version': '2.0.0',
        'changes': 'Added ObservabilityMixin for query performance tracking'
    },
    'problem_decomposer_agent': {
        'features': ['observability', 'realtime'],
        'version': '2.0.0',
        'changes': 'Added ObservabilityMixin + RealtimeMixin for interactive decomposition'
    },
    'personalization_engine_agent': {
        'features': ['observability'],
        'version': '2.0.0',
        'changes': 'Added ObservabilityMixin for recommendation tracking'
    },
    'problem_scaffolding_generator_agent': {
        'features': ['observability', 'computer_use'],
        'version': '2.0.0',
        'changes': 'Added ObservabilityMixin + ComputerUseMixin for UI testing'
    },
    'dynamic_learning_agent': {
        'features': ['observability', 'realtime', 'computer_use'],
        'version': '2.0.0',
        'changes': 'Added all runtime capabilities for adaptive workflows'
    },
    'self_improver_agent': {
        'features': ['observability'],
        'version': '2.0.0',
        'changes': 'Added ObservabilityMixin for improvement tracking'
    },
    'socratic_requirements_agent': {
        'features': ['observability', 'realtime'],
        'version': '2.0.0',
        'changes': 'Added ObservabilityMixin + RealtimeMixin for voice clarification'
    }
}


def enhance_agent_file(agent_name: str, agents_dir: Path):
    """Add runtime enhancement to agent file"""
    
    file_path = agents_dir / f"{agent_name}.py"
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return False
    
    config = AGENT_ENHANCEMENTS.get(agent_name)
    if not config:
        print(f"⚠️ No enhancement config for {agent_name}")
        return False
    
    # Read existing content
    content = file_path.read_text()
    
    # Check if already enhanced
    if 'RUNTIME_AVAILABLE' in content:
        print(f"⏭️ {agent_name} already enhanced")
        return True
    
    # Find agent definition line
    import re
    definition_pattern = rf'^{agent_name} = .*AgentDefinition\('
    
    if not re.search(definition_pattern, content, re.MULTILINE):
        # Try with SemanticAgentDefinition
        definition_pattern = rf'^{agent_name} = SemanticAgentDefinition\('
    
    match = re.search(definition_pattern, content, re.MULTILINE)
    
    if not match:
        print(f"❌ Could not find AgentDefinition for {agent_name}")
        return False
    
    # Insert runtime import before definition
    import_insert = f"""
try:
    from lib.runtime_enhancers import enhance_agent
    RUNTIME_AVAILABLE = True
except ImportError:
    RUNTIME_AVAILABLE = False

"""
    
    # Replace definition name
    content = re.sub(
        rf'^{agent_name} = ',
        f'_{agent_name}_definition = ',
        content,
        count=1,
        flags=re.MULTILINE
    )
    
    # Add import before first definition
    first_def_pos = content.find(f'_{agent_name}_definition = ')
    content = content[:first_def_pos] + import_insert + content[first_def_pos:]
    
    # Add enhancement at end of file
    features_str = ', '.join(f"'{f}'" for f in config['features'])
    enhancement_code = f"""
# Runtime integration
if RUNTIME_AVAILABLE:
    {agent_name} = enhance_agent(
        _{agent_name}_definition,
        features=[{features_str}],
        session_id=None
    )
else:
    {agent_name} = _{agent_name}_definition
"""
    
    # Append enhancement
    content = content.rstrip() + '\n' + enhancement_code + '\n'
    
    # Update version in docstring
    content = re.sub(
        r'VERSION: [\d.]+',
        f'VERSION: {config["version"]} - RUNTIME INTEGRATION',
        content,
        count=1
    )
    
    # Add changelog entry
    changelog_pattern = r'(CHANGELOG:\n)'
    changelog_entry = f'  v{config["version"]} (2025-10-16):\n    - {config["changes"]}\n'
    content = re.sub(changelog_pattern, r'\1' + changelog_entry, content, count=1)
    
    # Write back
    file_path.write_text(content)
    
    print(f"✅ Enhanced {agent_name} with {config['features']}")
    return True


def main():
    """Process all specified agents"""
    if len(sys.argv) < 2:
        print("Usage: python3 bulk_enhance_agents.py agent1 agent2 ...")
        print("\nAvailable agents:")
        for name in AGENT_ENHANCEMENTS.keys():
            print(f"  - {name}")
        sys.exit(1)
    
    agents_to_process = sys.argv[1:]
    agents_dir = Path(__file__).parent.parent / "agents"
    
    print("=" * 70)
    print(f"Bulk Agent Enhancement - {len(agents_to_process)} agents")
    print("=" * 70)
    print()
    
    success_count = 0
    for agent_name in agents_to_process:
        if enhance_agent_file(agent_name, agents_dir):
            success_count += 1
    
    print()
    print("=" * 70)
    print(f"Enhanced: {success_count}/{len(agents_to_process)} agents")
    print("=" * 70)
    
    return 0 if success_count == len(agents_to_process) else 1


if __name__ == "__main__":
    sys.exit(main())

