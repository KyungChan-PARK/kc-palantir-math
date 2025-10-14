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
from .socratic_planner import socratic_planner
from .socratic_mediator_agent import socratic_mediator_agent
from .self_improver_agent import self_improver_agent

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
from .socratic_mediator import SocraticMediator
from .self_improver import SelfImprover
from .improvement_manager import ImprovementManager
from .ask_agent_tool import ask_agent_tool

__all__ = [
    # Agent definitions (8 agents total: 6 specialized + 2 self-improvement)
    "knowledge_builder",
    "quality_agent",
    "research_agent",
    "example_generator",
    "meta_orchestrator",
    "MetaOrchestratorLogic",
    "dependency_mapper",
    "socratic_planner",
    "socratic_mediator_agent",
    "self_improver_agent",
    # Infrastructure
    "ErrorTracker",
    "resilient_task",
    "RetryConfig",
    "human_escalation_handler",
    "StructuredLogger",
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
