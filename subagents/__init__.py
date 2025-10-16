"""
Subagents - Specialized AI Agents

VERSION: 3.1.0 - Consistent Naming Convention
All agents follow *_agent.py pattern for immediate role recognition.

Architecture:
- Main Agent: meta-orchestrator (system prompt in .claude/CLAUDE.md)
- Subagents: 11 specialized agents (delegated via Task tool)
"""

# Core Math Education Subagents (6)
from .file_builder_agent import knowledge_builder
from .validator_agent import quality_agent
from .web_research_agent import research_agent
from .requirements_agent import socratic_requirements_agent
from .decomposer_agent import problem_decomposer_agent
from .problem_generator_agent import problem_scaffolding_generator_agent

# Extended Functionality Subagents (3)
from .graph_query_agent import neo4j_query_agent
from .personalization_agent import personalization_engine_agent
from .feedback_learning_agent import feedback_learning_agent

# System Improvement Subagents (2)
from .code_improver_agent import self_improver_agent
from .planning_analyzer_agent import meta_planning_analyzer
from .query_helper_agent import meta_query_helper

__all__ = [
    # Core Math Education (6)
    "knowledge_builder",           # file_builder_agent.py
    "quality_agent",               # validator_agent.py
    "research_agent",              # web_research_agent.py
    "socratic_requirements_agent", # requirements_agent.py
    "problem_decomposer_agent",    # decomposer_agent.py
    "problem_scaffolding_generator_agent", # problem_generator_agent.py
    # Extended Functionality (4 - added feedback-learning)
    "neo4j_query_agent",           # graph_query_agent.py
    "personalization_engine_agent", # personalization_agent.py
    "feedback_learning_agent",     # feedback_learning_agent.py
    # System Improvement (2)
    "self_improver_agent",         # code_improver_agent.py
    "meta_planning_analyzer",      # planning_analyzer_agent.py
    "meta_query_helper",           # query_helper_agent.py
]
