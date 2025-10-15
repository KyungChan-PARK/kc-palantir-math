"""
Planning Observer - Captures AI planning process for meta-cognitive improvement

VERSION: 1.0.0
DATE: 2025-10-15
PURPOSE: Record AI assistant planning steps for meta-orchestrator analysis

Records:
- Query understanding steps
- Codebase analysis queries
- Design decision rationale
- Alternative approaches considered
- Trade-off analysis

Usage:
    observer = PlanningObserver("Implement streaming system")
    observer.record_query("Check main.py", "Need current state", ["SDK version"])
    observer.record_decision("Use streaming", "Better UX", ["blocking", "hybrid"])
    trace = observer.export_for_meta_orchestrator()
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime
import json


@dataclass
class PlanningStep:
    """Single step in AI planning process"""
    step_number: int
    step_type: str  # "query", "analysis", "decision", "trade-off"
    content: str
    reasoning: str
    alternatives_considered: List[str]
    chosen_approach: str
    confidence: float
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            "step": self.step_number,
            "type": self.step_type,
            "content": self.content,
            "reasoning": self.reasoning,
            "alternatives": self.alternatives_considered,
            "chosen": self.chosen_approach,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }


class PlanningObserver:
    """
    Observes and records AI planning process in real-time.
    
    This enables meta-cognitive improvement by capturing how AI assistants
    approach complex tasks, make decisions, and explore alternatives.
    
    Meta-orchestrator can analyze these traces to:
    - Identify inefficiencies in planning
    - Suggest better approaches
    - Learn patterns for future sessions
    - Improve overall planning quality
    """
    
    def __init__(self, task_description: str):
        """
        Initialize planning observer.
        
        Args:
            task_description: Description of the task being planned
        """
        self.task_description = task_description
        self.steps: List[PlanningStep] = []
        self.session_id = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.start_time = datetime.now()
    
    def record_query(
        self,
        query: str,
        reasoning: str,
        expected_insights: List[str],
        metadata: Dict[str, Any] = None
    ) -> PlanningStep:
        """
        Record a codebase query made during planning.
        
        Args:
            query: The query or search being performed
            reasoning: Why this query is needed
            expected_insights: What information is expected
            metadata: Additional metadata (file paths, tool names, etc.)
        
        Returns:
            PlanningStep that was recorded
        """
        step = PlanningStep(
            step_number=len(self.steps) + 1,
            step_type="query",
            content=query,
            reasoning=reasoning,
            alternatives_considered=expected_insights,
            chosen_approach=query,
            confidence=0.8,
            timestamp=datetime.now().isoformat(),
            metadata=metadata or {}
        )
        self.steps.append(step)
        return step
    
    def record_analysis(
        self,
        analysis: str,
        findings: List[str],
        implications: List[str],
        metadata: Dict[str, Any] = None
    ) -> PlanningStep:
        """
        Record an analysis step.
        
        Args:
            analysis: What is being analyzed
            findings: Key findings from analysis
            implications: What these findings mean for the plan
            metadata: Additional context
        
        Returns:
            PlanningStep that was recorded
        """
        step = PlanningStep(
            step_number=len(self.steps) + 1,
            step_type="analysis",
            content=analysis,
            reasoning=f"Findings: {', '.join(findings[:3])}",
            alternatives_considered=implications,
            chosen_approach=analysis,
            confidence=0.85,
            timestamp=datetime.now().isoformat(),
            metadata=metadata or {}
        )
        self.steps.append(step)
        return step
    
    def record_decision(
        self,
        decision: str,
        reasoning: str,
        alternatives: List[str],
        trade_offs: Dict[str, List[str]],
        metadata: Dict[str, Any] = None
    ) -> PlanningStep:
        """
        Record a design decision.
        
        Args:
            decision: The decision made
            reasoning: Why this decision was chosen
            alternatives: Other options considered
            trade_offs: {"pros": [...], "cons": [...]}
            metadata: Additional context
        
        Returns:
            PlanningStep that was recorded
        """
        step = PlanningStep(
            step_number=len(self.steps) + 1,
            step_type="decision",
            content=decision,
            reasoning=reasoning,
            alternatives_considered=alternatives,
            chosen_approach=decision,
            confidence=self._calculate_confidence(trade_offs),
            timestamp=datetime.now().isoformat(),
            metadata=metadata or {}
        )
        self.steps.append(step)
        return step
    
    def record_trade_off(
        self,
        option_a: str,
        option_b: str,
        comparison: Dict[str, Any],
        chosen: str,
        metadata: Dict[str, Any] = None
    ) -> PlanningStep:
        """
        Record a trade-off analysis between two options.
        
        Args:
            option_a: First option
            option_b: Second option
            comparison: Comparison data
            chosen: Which option was chosen
            metadata: Additional context
        
        Returns:
            PlanningStep that was recorded
        """
        step = PlanningStep(
            step_number=len(self.steps) + 1,
            step_type="trade-off",
            content=f"Compare: {option_a} vs {option_b}",
            reasoning=json.dumps(comparison),
            alternatives_considered=[option_a, option_b],
            chosen_approach=chosen,
            confidence=0.75,
            timestamp=datetime.now().isoformat(),
            metadata=metadata or {}
        )
        self.steps.append(step)
        return step
    
    def export_for_meta_orchestrator(self) -> Dict:
        """
        Export planning trace for meta-orchestrator analysis.
        
        Returns:
            Dictionary with complete planning trace
        """
        duration_seconds = (datetime.now() - self.start_time).total_seconds()
        
        return {
            "session_id": self.session_id,
            "task_description": self.task_description,
            "total_steps": len(self.steps),
            "duration_seconds": duration_seconds,
            "planning_trace": [step.to_dict() for step in self.steps],
            "summary": {
                "queries": sum(1 for s in self.steps if s.step_type == "query"),
                "analyses": sum(1 for s in self.steps if s.step_type == "analysis"),
                "decisions": sum(1 for s in self.steps if s.step_type == "decision"),
                "trade_offs": sum(1 for s in self.steps if s.step_type == "trade-off"),
                "avg_confidence": sum(s.confidence for s in self.steps) / len(self.steps) if self.steps else 0.0
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def save_trace(self, output_path: str):
        """
        Save planning trace to file.
        
        Args:
            output_path: Path to save JSON trace
        """
        trace = self.export_for_meta_orchestrator()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(trace, f, indent=2, ensure_ascii=False)
    
    def _calculate_confidence(self, trade_offs: Dict[str, List[str]]) -> float:
        """
        Calculate confidence based on trade-off analysis.
        
        Args:
            trade_offs: {"pros": [...], "cons": [...]}
        
        Returns:
            Confidence score (0.0-1.0)
        """
        pros = len(trade_offs.get("pros", []))
        cons = len(trade_offs.get("cons", []))
        
        if pros == 0 and cons == 0:
            return 0.5  # No analysis = low confidence
        
        # More pros = higher confidence
        ratio = pros / (pros + cons) if (pros + cons) > 0 else 0.5
        
        # Map to 0.6-0.95 range (never 100% confident)
        return 0.6 + (ratio * 0.35)
    
    def get_current_step_count(self) -> int:
        """Get current number of steps recorded"""
        return len(self.steps)
    
    def get_summary(self) -> str:
        """
        Get human-readable summary of planning process.
        
        Returns:
            Summary string
        """
        if not self.steps:
            return "No steps recorded yet"
        
        trace = self.export_for_meta_orchestrator()
        summary = trace["summary"]
        
        return f"""Planning Session Summary:
Task: {self.task_description}
Duration: {trace['duration_seconds']:.1f}s
Total Steps: {trace['total_steps']}
  - Queries: {summary['queries']}
  - Analyses: {summary['analyses']}
  - Decisions: {summary['decisions']}
  - Trade-offs: {summary['trade_offs']}
Average Confidence: {summary['avg_confidence']:.2f}
"""

