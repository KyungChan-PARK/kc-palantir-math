"""
Dynamic Layer Orchestrator - Palantir 3-Tier Ontology

The Dynamic tier manages learning, adaptation, and optimization.

Based on:
- Palantir Foundry Dynamic tier model  
- docs/palantir-ontology-research.md (H3 validated)
- Meta-cognitive system components

Components:
1. LearningCoordinator - Collective learning across all agents
2. WorkflowAdaptationEngine - Learn and adapt workflows
3. AutoOptimizer - Continuous optimization
4. EvolutionTracker - Long-term adaptation tracking
5. ModelSelector - Multi-factor Haiku/Sonnet decision

VERSION: 1.0.0
DATE: 2025-10-16
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path


# ============================================================================
# Component 1: Learning Coordinator
# ============================================================================

@dataclass
class AgentLearning:
    """Learning captured from single agent."""
    agent_name: str
    insight: str
    evidence: List[str]
    confidence: float
    timestamp: float
    applicable_to: List[str] = field(default_factory=list)  # Which agents can use this


class LearningCoordinator:
    """
    Collect and synthesize learnings from all agents.
    
    Implements collective intelligence:
    - One agent's learning available to all
    - Pattern extraction across agents
    - Knowledge redistribution
    """
    
    def __init__(self, memory_adapter=None):
        """
        Initialize learning coordinator.
        
        Args:
            memory_adapter: MemoryAdapter instance for persistence
        """
        # Use MemoryAdapter instead of memory-keeper MCP
        if memory_adapter is None:
            from pathlib import Path
            from tools.memory_adapter_tool import MemoryAdapter
            self.memory = MemoryAdapter(Path("/home/kc-palantir/math/memories"))
        else:
            self.memory = memory_adapter
        
        self.learnings: List[AgentLearning] = []
        self.patterns: Dict[str, List[str]] = {}
    
    def collect_learning(
        self,
        agent_name: str,
        insight: str,
        evidence: List[str],
        confidence: float
    ):
        """Collect learning from any agent."""
        learning = AgentLearning(
            agent_name=agent_name,
            insight=insight,
            evidence=evidence,
            confidence=confidence,
            timestamp=time.time()
        )
        
        self.learnings.append(learning)
        
        # Determine applicability
        learning.applicable_to = self._determine_applicability(learning)
    
    def _determine_applicability(self, learning: AgentLearning) -> List[str]:
        """Determine which agents can benefit from this learning."""
        # Simple heuristic
        applicable = []
        
        if "parallel" in learning.insight.lower():
            # Parallel execution benefits all agents
            applicable = ["*"]
        elif "documentation" in learning.insight.lower():
            # Documentation patterns for builder agents
            applicable = ["knowledge-builder", "example-generator"]
        else:
            # Default: Share with similar agents
            applicable = [learning.agent_name]
        
        return applicable
    
    def synthesize_patterns(self) -> Dict[str, List[str]]:
        """
        Extract common patterns from all learnings.
        
        Returns patterns that can be applied system-wide.
        """
        patterns = {
            "execution_patterns": [],
            "communication_patterns": [],
            "quality_patterns": [],
            "efficiency_patterns": []
        }
        
        for learning in self.learnings:
            insight_lower = learning.insight.lower()
            
            if any(kw in insight_lower for kw in ["parallel", "concurrent", "async"]):
                patterns["efficiency_patterns"].append(learning.insight)
            
            if any(kw in insight_lower for kw in ["validate", "quality", "test"]):
                patterns["quality_patterns"].append(learning.insight)
            
            if any(kw in insight_lower for kw in ["communicate", "pass data", "context"]):
                patterns["communication_patterns"].append(learning.insight)
        
        self.patterns = patterns
        return patterns
    
    async def redistribute_knowledge(self):
        """
        Redistribute learnings to applicable agents.
        
        Via memory tool adapter for persistence (Claude Code 2.0 pattern).
        """
        if not self.memory:
            return
        
        for learning in self.learnings:
            if learning.confidence < 0.7:
                continue  # Skip low-confidence learnings
            
            # Save to memory using Claude Code memory tool pattern
            memory_path = f"learnings/{learning.agent_name}_{int(learning.timestamp)}.json"
            learning_data = {
                "insight": learning.insight,
                "evidence": learning.evidence,
                "applicable_to": learning.applicable_to,
                "confidence": learning.confidence,
                "timestamp": learning.timestamp
            }
            
            # Create memory file
            self.memory.create(memory_path, json.dumps(learning_data, indent=2))


# ============================================================================
# Component 2: Workflow Adaptation Engine
# ============================================================================

@dataclass
class WorkflowPerformance:
    """Performance metrics for a workflow."""
    workflow_type: str
    agents_used: List[str]
    duration_ms: float
    success: bool
    quality_score: float


class WorkflowAdaptationEngine:
    """
    Learn and adapt workflows based on execution history.
    
    Solves Q2-4: Hardcoded workflows → Adaptive learning
    """
    
    def __init__(self):
        self.workflow_history: List[WorkflowPerformance] = []
        self.learned_workflows: Dict[str, List[str]] = {}
    
    def record_execution(
        self,
        workflow_type: str,
        agents_used: List[str],
        duration_ms: float,
        success: bool,
        quality_score: float = 0.0
    ):
        """Record workflow execution for learning."""
        perf = WorkflowPerformance(
            workflow_type=workflow_type,
            agents_used=agents_used,
            duration_ms=duration_ms,
            success=success,
            quality_score=quality_score
        )
        
        self.workflow_history.append(perf)
        
        # Learn if successful
        if success and quality_score > 0.8:
            self.learned_workflows[workflow_type] = agents_used
    
    def get_recommended_workflow(self, task_type: str) -> Optional[List[str]]:
        """
        Get recommended agent sequence for task type.
        
        Based on learned successful workflows.
        """
        return self.learned_workflows.get(task_type)
    
    def get_best_workflow_for_task(self, task_type: str) -> List[str]:
        """
        Return best workflow based on historical performance.
        
        If learned workflow exists, use it.
        Otherwise, use default heuristic.
        """
        learned = self.get_recommended_workflow(task_type)
        if learned:
            return learned
        
        # Default heuristics
        defaults = {
            "research_task": ["research-agent", "knowledge-builder", "quality-agent"],
            "quality_task": ["quality-agent"],
            "analysis_task": ["dependency-mapper", "meta-planning-analyzer"],
        }
        
        return defaults.get(task_type, ["research-agent"])


# ============================================================================
# Component 3: Auto Optimizer
# ============================================================================

class AutoOptimizer:
    """
    Continuous optimization based on metrics.
    
    Automatically improves system performance.
    """
    
    def __init__(self):
        self.optimizations_applied: List[Dict] = []
    
    def analyze_and_optimize(
        self,
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze metrics and apply optimizations.
        
        Returns optimization recommendations.
        """
        recommendations = []
        
        # Check latency
        if metrics.get("avg_duration_ms", 0) > 5000:
            recommendations.append({
                "type": "parallel_execution",
                "reason": "High latency detected",
                "expected_improvement": "90%"
            })
        
        # Check success rate
        if metrics.get("success_rate", 1.0) < 0.7:
            recommendations.append({
                "type": "trigger_self_improvement",
                "reason": "Low success rate",
                "threshold": "< 70%"
            })
        
        return {
            "optimizations": recommendations,
            "priority": "high" if len(recommendations) > 2 else "medium"
        }


# ============================================================================
# Component 4: Evolution Tracker
# ============================================================================

class EvolutionTracker:
    """Track long-term system evolution and adaptation."""
    
    def __init__(self):
        self.evolution_log: List[Dict] = []
    
    def record_evolution(
        self,
        component: str,
        change_type: str,
        impact: str
    ):
        """Record evolutionary change."""
        self.evolution_log.append({
            "component": component,
            "change_type": change_type,
            "impact": impact,
            "timestamp": time.time()
        })


# ============================================================================
# Component 5: Model Selector (Multi-Factor Decision Matrix)
# ============================================================================

@dataclass
class ModelSelectionFactors:
    """Factors for model selection decision."""
    criticality: int  # 1-10
    past_haiku_success_rate: float  # 0.0-1.0
    complexity_score: int  # 1-10
    time_budget: str  # "low", "medium", "high"
    task_type: str  # e.g., "ambiguity_resolution", "research", etc.


class ModelSelector:
    """
    Multi-factor decision matrix for Haiku vs Sonnet selection.
    
    Implements Q2-2: Adaptive switching with learning.
    """
    
    def __init__(self):
        self.selection_history: List[Dict] = []
        self.learned_preferences: Dict[str, str] = {}  # task_type → preferred_model
    
    def select_model(self, factors: ModelSelectionFactors) -> str:
        """
        Select optimal model using multi-factor decision.
        
        Weighting:
        - Criticality: 40%
        - Past success rate: 30%
        - Complexity: 20%
        - Time budget: 10%
        
        Returns:
            model_name: "claude-sonnet-4-5-20250929" or "claude-haiku-4-5"
        """
        # Check learned preference first
        if factors.task_type in self.learned_preferences:
            return self.learned_preferences[factors.task_type]
        
        # Calculate weighted score
        score = 0.0
        
        # Criticality (40%)
        if factors.criticality >= 9:
            score += 0.4  # High criticality → Sonnet
        elif factors.criticality <= 3:
            score -= 0.4  # Low criticality → Haiku
        
        # Past success rate (30%)
        if factors.past_haiku_success_rate < 0.6:
            score += 0.3  # Haiku struggles → Sonnet
        elif factors.past_haiku_success_rate > 0.9:
            score -= 0.3  # Haiku succeeds → Haiku
        
        # Complexity (20%)
        if factors.complexity_score >= 8:
            score += 0.2  # High complexity → Sonnet
        elif factors.complexity_score <= 3:
            score -= 0.2  # Low complexity → Haiku
        
        # Time budget (10%)
        if factors.time_budget == "low":
            score -= 0.1  # Tight deadline → Haiku (faster)
        
        # Decision
        if score > 0.3:
            model = "claude-sonnet-4-5-20250929"
        else:
            model = "claude-haiku-4-5"  # Placeholder (will be real model when available)
        
        # Record decision
        self.selection_history.append({
            "factors": factors,
            "score": score,
            "selected_model": model
        })
        
        return model
    
    def learn_from_execution(
        self,
        task_type: str,
        model_used: str,
        success: bool
    ):
        """
        Learn from execution outcome.
        
        Update learned preferences based on success/failure.
        """
        if success:
            # Record successful model for this task type
            self.learned_preferences[task_type] = model_used
        elif model_used == "claude-haiku-4-5":
            # Haiku failed → learn to use Sonnet for this task type
            self.learned_preferences[task_type] = "claude-sonnet-4-5-20250929"


# ============================================================================
# Unified Dynamic Tier Interface
# ============================================================================

import time

class DynamicTier:
    """
    Unified interface for all dynamic operations.
    
    Used by meta-orchestrator's dynamic tier coordination methods.
    """
    
    def __init__(self, memory_keeper_client=None):
        self.learning_coordinator = LearningCoordinator(memory_keeper_client)
        self.workflow_adaptation = WorkflowAdaptationEngine()
        self.auto_optimizer = AutoOptimizer()
        self.evolution_tracker = EvolutionTracker()
        self.model_selector = ModelSelector()
    
    def process_execution_results(
        self,
        execution_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process execution results for learning and optimization.
        
        Returns:
            insights: Learnings, optimizations, model recommendations
        """
        # Extract learning
        if "learnings" in execution_results:
            for learning in execution_results["learnings"]:
                self.learning_coordinator.collect_learning(
                    agent_name=learning["agent"],
                    insight=learning["insight"],
                    evidence=learning.get("evidence", []),
                    confidence=learning.get("confidence", 0.8)
                )
        
        # Synthesize patterns
        patterns = self.learning_coordinator.synthesize_patterns()
        
        # Get optimizations
        optimizations = self.auto_optimizer.analyze_and_optimize(
            execution_results.get("metrics", {})
        )
        
        return {
            "patterns": patterns,
            "optimizations": optimizations,
            "learnings_collected": len(self.learning_coordinator.learnings)
        }
    
    def select_model_for_task(
        self,
        task_description: str,
        criticality: int,
        complexity: int
    ) -> str:
        """
        Select optimal model using learned preferences.
        
        Args:
            task_description: What the task is
            criticality: 1-10 rating
            complexity: 1-10 rating
        
        Returns:
            model_name: Best model for this task
        """
        # Classify task type
        task_type = self._classify_task_type(task_description)
        
        # Get past success rate for Haiku on this task type
        past_success = self._get_haiku_success_rate(task_type)
        
        # Create factors
        factors = ModelSelectionFactors(
            criticality=criticality,
            past_haiku_success_rate=past_success,
            complexity_score=complexity,
            time_budget="medium",
            task_type=task_type
        )
        
        # Select model
        return self.model_selector.select_model(factors)
    
    def _classify_task_type(self, description: str) -> str:
        """Classify task into type for learning."""
        desc_lower = description.lower()
        
        if "ambig" in desc_lower or "clarif" in desc_lower:
            return "ambiguity_resolution"
        elif "research" in desc_lower:
            return "research"
        elif "build" in desc_lower or "create" in desc_lower:
            return "content_creation"
        elif "validate" in desc_lower or "quality" in desc_lower:
            return "quality_validation"
        else:
            return "general"
    
    def _get_haiku_success_rate(self, task_type: str) -> float:
        """Get historical Haiku success rate for task type."""
        # Placeholder: Would query execution history
        defaults = {
            "ambiguity_resolution": 0.45,  # Haiku struggles
            "research": 0.85,  # Haiku good
            "content_creation": 0.75,  # Haiku decent
            "quality_validation": 0.90,  # Haiku excellent
            "general": 0.70
        }
        
        return defaults.get(task_type, 0.70)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get dynamic tier metrics."""
        return {
            "learnings_collected": len(self.learning_coordinator.learnings),
            "patterns_synthesized": sum(len(p) for p in self.learning_coordinator.patterns.values()),
            "workflows_learned": len(self.workflow_adaptation.learned_workflows),
            "model_selections": len(self.model_selector.selection_history),
            "optimizations_applied": len(self.auto_optimizer.optimizations_applied)
        }

