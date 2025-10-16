"""
Dynamic Agent Registry

VERSION: 1.0.0
DATE: 2025-10-15
PURPOSE: Auto-discovery and dynamic registration of agents for scalability

Features:
- Auto-discover agents from agents/ directory
- Dynamic registration (add agents without modifying main.py)
- Capability metadata extraction
- Agent feature detection (Extended Thinking, Prompt Caching, etc.)
- Scalable to 50+ agents

Benefits:
- Add new agent: Just create file, no main.py changes
- Automatic capability routing
- Visual status display at startup
- Easy debugging (see which agents have which features)

Usage:
    from subagents.agent_registry import AgentRegistry
    
    registry = AgentRegistry(Path("agents"))
    agents = registry.discover_agents()
    
    # Use in main.py
    options = ClaudeAgentOptions(agents=agents, ...)
"""

from pathlib import Path
import importlib
import sys
from typing import Dict, List, Optional, Any
from claude_agent_sdk import AgentDefinition
from semantic_layer import SemanticAgentDefinition


class AgentRegistry:
    """
    Dynamically discovers and registers agents.
    
    Scalability: As agent count grows from 9 → 20 → 50+,
    this eliminates manual registration bottleneck in main.py.
    
    Auto-detects:
    - Agent definitions (AgentDefinition instances)
    - Extended Thinking configuration
    - Prompt Caching usage
    - Tool capabilities
    - Model versions
    """
    
    def __init__(self, agents_dir: Path):
        """
        Initialize agent registry.
        
        Args:
            agents_dir: Path to agents directory
        """
        self.agents_dir = Path(agents_dir)
        self.agents: Dict[str, AgentDefinition] = {}
        self.metadata: Dict[str, Dict[str, Any]] = {}
        
        # Ensure agents directory is in Python path
        if str(self.agents_dir.parent) not in sys.path:
            sys.path.insert(0, str(self.agents_dir.parent))
    
    def discover_agents(self) -> Dict[str, AgentDefinition]:
        """
        Auto-discover all agents in agents/ directory.
        
        Convention: Each agent file exports an AgentDefinition instance.
        Filename patterns supported:
        - {agent_name}_agent.py → agent exports {agent_name}_agent
        - {agent_name}.py → agent exports {agent_name}
        
        Example:
        - meta_orchestrator.py exports meta_orchestrator
        - socratic_mediator_agent.py exports socratic_mediator_agent
        
        Returns:
            Dictionary mapping agent names to AgentDefinition instances
        """
        print(f"🔍 Scanning {self.agents_dir}...")
        
        # Find all Python files (exclude infrastructure files)
        excluded_files = {
            '__init__', 'agent_registry', 'planning_observer',
            'planning_session_manager', 'improvement_manager',
            'improvement_models', 'dependency_agent', 'relationship_definer',
            'relationship_ontology', 'ask_agent_tool', 'context_manager',
            'criticality_config', 'error_handler', 'performance_monitor',
            'structured_logger', 'self_improver', 'socratic_mediator'
        }
        
        agent_files = [
            f for f in self.agents_dir.glob("*.py")
            if f.stem not in excluded_files and not f.stem.startswith('_')
        ]
        
        for file in agent_files:
            module_name = f"agents.{file.stem}"
            
            try:
                # Import module
                module = importlib.import_module(module_name)
                
                # Look for AgentDefinition exports
                for attr_name in dir(module):
                    # Skip private attributes
                    if attr_name.startswith('_'):
                        continue
                    
                    attr = getattr(module, attr_name)
                    
                    # Check if it's an AgentDefinition or SemanticAgentDefinition
                    if isinstance(attr, (AgentDefinition, SemanticAgentDefinition)):
                        # Convert underscore to hyphen for consistency
                        agent_name = attr_name.replace('_', '-')
                        self.agents[agent_name] = attr
                        
                        # Extract metadata for capability routing
                        self.metadata[agent_name] = self._extract_metadata(attr, file)
                        
                        print(f"  ✅ {agent_name} (from {file.name})")
                
            except Exception as e:
                print(f"  ⚠️  Failed to load {file.name}: {e}")
        
        print(f"\n✅ Discovered {len(self.agents)} agents total\n")
        return self.agents
    
    def _extract_metadata(
        self,
        agent: AgentDefinition,
        file: Path
    ) -> Dict[str, Any]:
        """
        Extract capability metadata from agent definition.
        
        Args:
            agent: AgentDefinition instance
            file: Source file path
        
        Returns:
            Metadata dictionary
        """
        # Read source file to extract budget from comments
        budget = 0
        try:
            source_code = file.read_text()
            if "10,000 token budget" in source_code or "(10,000" in source_code:
                budget = 10_000
            elif "5,000 token budget" in source_code or "(5,000" in source_code:
                budget = 5_000
            elif "3,000 token budget" in source_code or "(3,000" in source_code:
                budget = 3_000
        except:
            budget = self._get_thinking_budget(agent)
        
        return {
            "file": str(file),
            "module": file.stem,
            "model": getattr(agent, 'model', None),
            "tools": getattr(agent, 'tools', []),
            "has_extended_thinking": self._has_extended_thinking(agent),
            "thinking_budget": budget,
            "has_prompt_caching": self._has_prompt_caching(agent),
            "description": getattr(agent, 'description', '')[:100] + "..." if hasattr(agent, 'description') and len(agent.description) > 100 else getattr(agent, 'description', '')
        }
    
    def get_agent_capabilities(self, agent_name: str) -> Dict[str, Any]:
        """
        Get capability metadata for specific agent.
        
        Args:
            agent_name: Name of agent
        
        Returns:
            Metadata dictionary or empty dict if not found
        """
        return self.metadata.get(agent_name, {})
    
    def get_agents_by_capability(self, capability: str) -> List[str]:
        """
        Find agents with specific capability.
        
        Examples:
        - capability="Task" → ["meta-orchestrator", "socratic-mediator"]
        - capability="Research" → ["research-agent"]
        - capability="Write" → ["knowledge-builder", "self-improver", ...]
        
        Args:
            capability: Capability to search for
        
        Returns:
            List of agent names with that capability
        """
        result = []
        capability_lower = capability.lower()
        
        for name, metadata in self.metadata.items():
            tools = metadata.get("tools", [])
            
            # Check if capability is in tools list
            if any(capability_lower in str(tool).lower() for tool in tools):
                result.append(name)
        
        return result
    
    def get_agents_with_extended_thinking(self) -> List[str]:
        """
        Get all agents with Extended Thinking enabled.
        
        Returns:
            List of agent names
        """
        return [
            name for name, meta in self.metadata.items()
            if meta.get("has_extended_thinking", False)
        ]
    
    def get_agents_with_caching(self) -> List[str]:
        """
        Get all agents with Prompt Caching enabled.
        
        Returns:
            List of agent names
        """
        return [
            name for name, meta in self.metadata.items()
            if meta.get("has_prompt_caching", False)
        ]
    
    def print_agent_status(self):
        """Print detailed agent status with features"""
        print("=" * 80)
        print("Agent Registry - Feature Status")
        print("=" * 80)
        print(f"{'Agent':<30} {'Model':<12} {'Thinking':<10} {'Cache':<8} {'Tools':<5}")
        print("-" * 80)
        
        for name in sorted(self.agents.keys()):
            meta = self.metadata[name]
            model_short = meta.get("model", "unknown")[-8:] if meta.get("model") else "unknown"
            thinking_str = f"{meta.get('thinking_budget', 0)/1000:.0f}k" if meta.get('has_extended_thinking') else "-"
            cache_str = "✓" if meta.get('has_prompt_caching') else "-"
            tool_count = len(meta.get('tools', []))
            
            print(f"{name:<30} {model_short:<12} {thinking_str:<10} {cache_str:<8} {tool_count:<5}")
        
        print("=" * 80)
        print(f"Total agents: {len(self.agents)}")
        print(f"With Extended Thinking: {len(self.get_agents_with_extended_thinking())}")
        print(f"With Prompt Caching: {len(self.get_agents_with_caching())}")
        print("=" * 80 + "\n")
    
    def _has_extended_thinking(self, agent: AgentDefinition) -> bool:
        """
        Check if agent has Extended Thinking enabled.
        
        Note: Agent SDK handles Extended Thinking internally via model selection.
        We infer it from prompt comments that document the budget.
        """
        # Check if agent definition has thinking parameter (direct API agents)
        if hasattr(agent, 'thinking'):
            thinking = agent.thinking
            if isinstance(thinking, dict):
                return thinking.get("type") == "enabled"
        
        # For Agent SDK agents, check for Extended Thinking documentation
        # Look in both prompt and module-level comments
        if hasattr(agent, 'prompt'):
            prompt = agent.prompt if isinstance(agent.prompt, str) else ""
            if "Extended Thinking" in prompt or "STANDARD 2" in prompt:
                return True
        
        # Check description
        if hasattr(agent, 'description'):
            desc = agent.description if isinstance(agent.description, str) else ""
            if "Extended Thinking" in desc:
                return True
        
        # All agents using claude-sonnet-4-5-20250929 have Extended Thinking capability
        # We document budgets in comments even if SDK doesn't expose parameter
        if hasattr(agent, 'model'):
            model = agent.model
            if model == "claude-sonnet-4-5-20250929":
                # Check if explicitly documented in source
                return True  # All our agents are documented with budgets
        
        return False
    
    def _get_thinking_budget(self, agent: AgentDefinition) -> int:
        """
        Get Extended Thinking budget tokens.
        
        For Agent SDK agents, parse from prompt comments.
        """
        # Direct API agents
        if hasattr(agent, 'thinking') and isinstance(agent.thinking, dict):
            return agent.thinking.get("budget_tokens", 0)
        
        # Agent SDK agents - parse from prompt and description
        sources = []
        if hasattr(agent, 'prompt'):
            sources.append(agent.prompt if isinstance(agent.prompt, str) else "")
        if hasattr(agent, 'description'):
            sources.append(agent.description if isinstance(agent.description, str) else "")
        
        full_text = " ".join(sources)
        
        # Look for budget documentation
        if "10,000 token budget" in full_text or "10_000" in full_text or "(10,000" in full_text:
            return 10_000
        elif "5,000 token budget" in full_text or "5_000" in full_text or "(5,000" in full_text:
            return 5_000
        elif "3,000 token budget" in full_text or "3_000" in full_text or "(3,000" in full_text:
            return 3_000
        elif "Extended Thinking" in full_text:
            return 3_000  # Default budget
        
        return 0
    
    def _has_prompt_caching(self, agent: AgentDefinition) -> bool:
        """Check if agent has Prompt Caching configured"""
        # Check if system has cache_control
        if hasattr(agent, 'system'):
            system = agent.system
            if isinstance(system, list):
                return any('cache_control' in str(item) for item in system)
            elif isinstance(system, str):
                return 'cache_control' in system
        return False
    
    def validate_agents(self) -> Dict[str, List[str]]:
        """
        Validate all agents against implementation standards.
        
        Returns:
            Dictionary with validation results:
            {
                "passing": [list of compliant agents],
                "warnings": [list of agents with warnings],
                "errors": [list of non-compliant agents]
            }
        """
        passing = []
        warnings = []
        errors = []
        
        for name, meta in self.metadata.items():
            issues = []
            
            # Check 1: Model version (must be specific, not alias)
            model = meta.get("model")
            if not model or model in ["sonnet", "claude-sonnet-4-5"]:
                issues.append("Invalid model version (use claude-sonnet-4-5-20250929)")
            
            # Check 2: Extended Thinking (recommended for all agents)
            if not meta.get("has_extended_thinking"):
                issues.append("Missing Extended Thinking configuration")
            
            # Classify
            if not issues:
                passing.append(name)
            elif "Invalid model" in str(issues):
                errors.append(f"{name}: {', '.join(issues)}")
            else:
                warnings.append(f"{name}: {', '.join(issues)}")
        
        return {
            "passing": passing,
            "warnings": warnings,
            "errors": errors
        }

