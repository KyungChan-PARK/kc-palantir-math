"""
Math Education Agents

Kenny Liao Claude Agent SDK 패턴 기반
VERSION: 3.0.0 - Added Self-Improvement System v4.0
"""

from .knowledge_builder import knowledge_builder
from .quality_agent import quality_agent
from .research_agent import research_agent
from .example_generator import example_generator
from .meta_orchestrator import meta_orchestrator, MetaOrchestratorLogic
from .dependency_mapper import dependency_mapper
from .self_improver_agent import self_improver_agent

# Socratic Requirements Agent (REPLACED socratic-planner and socratic-mediator)
# Purpose: Natural language → Programming-level precision
# Features: Recursive questioning, asymptotic convergence, self-improvement
from .socratic_requirements_agent import socratic_requirements_agent

# Infrastructure modules
from .error_handler import ErrorTracker, resilient_task, RetryConfig, human_escalation_handler
from .structured_logger import StructuredLogger, setup_structured_logger, AgentLogger, set_trace_id, get_trace_id
from .performance_monitor import PerformanceMonitor, AgentMetrics, PerformanceTimer
from .context_manager import ContextManager

# Self-Improvement System v4.0 modules
from .improvement_models import (
    ImprovementAction,
    ImpactAnalysis,
    QualityGateApproval,
    RootCauseAnalysis,
    IssueReport,
    ChangeStatus,
    ChangeRecord,
    ActionType
)
from .dependency_agent import DependencyAgent, DependencyNode, DependencyEdge, NodeType, EdgeType
from .self_improver import SelfImprover
from .improvement_manager import ImprovementManager
from .ask_agent_tool import ask_agent_tool

# Meta-cognitive components (NEW in v2.2.0)
from .meta_planning_analyzer import meta_planning_analyzer
from .planning_observer import PlanningObserver, PlanningStep
from .planning_session_manager import PlanningSessionManager
from .agent_registry import AgentRegistry

__all__ = [
    # Agent definitions (9 agents total: 5 specialized + 2 meta-cognitive + 1 self-improvement + meta-orchestrator)
    "knowledge_builder",
    "quality_agent",
    "research_agent",
    "example_generator",
    "meta_orchestrator",
    "meta_planning_analyzer",
    "socratic_requirements_agent",  # REPLACED socratic-planner and socratic-mediator
    "MetaOrchestratorLogic",
    "dependency_mapper",
    "self_improver_agent",
    # Infrastructure
    "ErrorTracker",
    "resilient_task",
    "RetryConfig",
    "human_escalation_handler",
    "StructuredLogger",
    
    # Meta-cognitive components
    "PlanningObserver",
    "PlanningStep",
    "PlanningSessionManager",
    "AgentRegistry",
    "setup_structured_logger",
    "AgentLogger",
    "set_trace_id",
    "get_trace_id",
    "PerformanceMonitor",
    "AgentMetrics",
    "PerformanceTimer",
    "ContextManager",
    # Self-Improvement System v4.0
    "ImprovementAction",
    "ImpactAnalysis",
    "QualityGateApproval",
    "RootCauseAnalysis",
    "IssueReport",
    "ChangeStatus",
    "ChangeRecord",
    "ActionType",
    "DependencyAgent",
    "DependencyNode",
    "DependencyEdge",
    "NodeType",
    "EdgeType",
    "SocraticMediator",
    "SelfImprover",
    "ImprovementManager",
    "ask_agent_tool"
]
