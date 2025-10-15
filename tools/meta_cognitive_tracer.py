"""
Meta-Cognitive Tracer - Tracks Decisions, Learnings, and Impacts

Based on:
- Socratic requirements clarification (95% precision)
- Palantir 3-tier ontology research
- claude-code-2-0-deduplicated-final.md prompt templates

VERSION: 1.0.0
DATE: 2025-10-15
"""

import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import json


@dataclass
class DecisionTrace:
    """Palantir Semantic: What was decided"""
    decision: str
    reasoning: str
    alternatives: List[str]
    chosen_why: str
    timestamp: float
    confidence: float
    
    
@dataclass  
class LearningTrace:
    """Palantir Dynamic: What was learned"""
    insight: str
    source: str  # "documentation" | "error" | "pattern" | "user_feedback"
    confidence: float
    applicable_to: List[str]
    evidence: List[str]
    timestamp: float


@dataclass
class ImpactTrace:
    """Palantir Kinetic: What effects occurred"""
    change: str
    predicted_impact: Dict[str, Any]
    actual_impact: Dict[str, Any]
    side_effects: List[str]
    prediction_accuracy: float
    timestamp: float


class MetaCognitiveTracer:
    """
    Traces meta-cognitive process for agent self-improvement.
    
    Palantir 3-Tier Integration:
    - Semantic: Definitions of what to track
    - Kinetic: Execution of tracking
    - Dynamic: Learning from traces
    
    Output to Agents:
    - Via structured parameter (Task meta_cognitive_context)
    - Via memory-keeper query pattern
    - Via prompt template injection
    """
    
    def __init__(self, memory_keeper_client=None):
        self.memory = memory_keeper_client
        self.current_trace = {
            "decisions": [],
            "learnings": [],
            "impacts": []
        }
        self.session_id = f"trace_{int(time.time())}"
    
    # ========================================================================
    # TRACING METHODS (Kinetic Tier)
    # ========================================================================
    
    def trace_decision(
        self,
        decision: str,
        reasoning: str,
        alternatives: List[str],
        chosen_why: str,
        confidence: float = 0.8
    ) -> DecisionTrace:
        """
        Track a decision point.
        
        Example:
            tracer.trace_decision(
                decision="Use parallel execution for file reads",
                reasoning="Independent operations, no dependencies",
                alternatives=["Sequential reads", "Batch processing"],
                chosen_why="90% latency reduction per Claude Code docs",
                confidence=0.95
            )
        """
        trace = DecisionTrace(
            decision=decision,
            reasoning=reasoning,
            alternatives=alternatives,
            chosen_why=chosen_why,
            timestamp=time.time(),
            confidence=confidence
        )
        
        self.current_trace["decisions"].append(asdict(trace))
        return trace
    
    def trace_learning(
        self,
        insight: str,
        source: str,
        confidence: float,
        applicable_to: List[str],
        evidence: List[str]
    ) -> LearningTrace:
        """
        Track a learning moment.
        
        Example:
            tracer.trace_learning(
                insight="PreToolUse hooks prevent TypeErrors before execution",
                source="documentation",
                confidence=0.98,
                applicable_to=["SDK integration", "Agent execution"],
                evidence=["claude-code-2-0-deduplicated-final.md lines 9541-9574"]
            )
        """
        trace = LearningTrace(
            insight=insight,
            source=source,
            confidence=confidence,
            applicable_to=applicable_to,
            evidence=evidence,
            timestamp=time.time()
        )
        
        self.current_trace["learnings"].append(asdict(trace))
        return trace
    
    def trace_impact(
        self,
        change: str,
        predicted_impact: Dict[str, Any],
        actual_impact: Dict[str, Any],
        side_effects: List[str]
    ) -> ImpactTrace:
        """
        Track impact chain.
        
        Example:
            tracer.trace_impact(
                change="Added PreToolUse validation hook",
                predicted_impact={"type_errors": 0, "rework": 0},
                actual_impact={"type_errors": 0, "rework": 0},
                side_effects=["Slight latency increase +50ms"]
            )
        """
        accuracy = self._calculate_prediction_accuracy(
            predicted_impact,
            actual_impact
        )
        
        trace = ImpactTrace(
            change=change,
            predicted_impact=predicted_impact,
            actual_impact=actual_impact,
            side_effects=side_effects,
            prediction_accuracy=accuracy,
            timestamp=time.time()
        )
        
        self.current_trace["impacts"].append(asdict(trace))
        return trace
    
    # ========================================================================
    # MEMORY-KEEPER INTEGRATION (Dynamic Tier)
    # ========================================================================
    
    async def save_to_memory_keeper(
        self,
        task_type: str,
        success: bool,
        quality_score: float
    ):
        """
        Save complete trace to memory-keeper for future retrieval.
        
        Palantir Dynamic: Learning persistence
        """
        if not self.memory:
            return
        
        # Extract prompt template if successful
        prompt_template = None
        if success and quality_score >= 9.0:
            prompt_template = self._extract_prompt_template()
        
        trace_data = {
            "session_id": self.session_id,
            "task_type": task_type,
            "success": success,
            "quality_score": quality_score,
            "trace": self.current_trace,
            "prompt_template": prompt_template,
            "effectiveness_score": self._calculate_effectiveness(),
            "timestamp": time.time()
        }
        
        await self.memory.context_save(
            key=f"meta_cognitive_trace_{task_type}_{self.session_id}",
            context=trace_data
        )
    
    async def query_similar_traces(
        self,
        task_description: str,
        min_effectiveness: float = 8.0
    ) -> List[Dict]:
        """
        Query memory-keeper for similar past traces.
        
        Pattern: claude-code-2-0-deduplicated-final.md memory-keeper usage
        """
        if not self.memory:
            return []
        
        results = await self.memory.context_search(
            query=task_description,
            filter={"effectiveness_score": f">{min_effectiveness}"}
        )
        
        return results or []
    
    # ========================================================================
    # PROMPT CONTEXT GENERATION (Output to Agents)
    # ========================================================================
    
    async def generate_meta_cognitive_context(
        self,
        task_description: str
    ) -> str:
        """
        Generate meta-cognitive context for agent prompt.
        
        Based on:
        - Q-Final-2: Structured parameter + Memory-keeper pattern
        - claude-code-2-0-deduplicated-final.md {{template}} pattern
        
        Returns: Formatted context string with {{variables}} filled
        """
        # Query memory for similar tasks
        similar_traces = await self.query_similar_traces(task_description)
        
        if not similar_traces:
            return ""
        
        best_trace = max(similar_traces, key=lambda x: x.get('effectiveness_score', 0))
        
        # Format as prompt context (claude-code-2-0 pattern)
        context = f"""
[META-COGNITIVE CONTEXT]
similar_task: {best_trace['task_type']}
success_rate: {best_trace.get('quality_score', 0)}/10

Past Decision (APPLY THIS):
- {best_trace['trace']['decisions'][-1]['decision'] if best_trace['trace']['decisions'] else 'N/A'}
- Why: {best_trace['trace']['decisions'][-1]['chosen_why'] if best_trace['trace']['decisions'] else 'N/A'}

Learning (CRITICAL):
- {best_trace['trace']['learnings'][-1]['insight'] if best_trace['trace']['learnings'] else 'N/A'}
- Evidence: {best_trace['trace']['learnings'][-1]['evidence'][0] if best_trace['trace']['learnings'] else 'N/A'}

Expected Impact:
- {best_trace['trace']['impacts'][-1]['change'] if best_trace['trace']['impacts'] else 'N/A'}
- Accuracy: {best_trace['trace']['impacts'][-1].get('prediction_accuracy', 0):.0%} if best_trace['trace']['impacts'] else 'N/A'

Prompt Template (HIGH QUALITY):
{best_trace.get('prompt_template', 'N/A')}
"""
        
        return context
    
    def generate_structured_context(self, task_description: str) -> Dict:
        """
        Generate structured meta-cognitive context as dict.
        
        For use as Task parameter:
            Task(
                agent="...",
                prompt="...",
                meta_cognitive_context=tracer.generate_structured_context(...)
            )
        """
        return {
            "current_trace": self.current_trace,
            "recent_decisions": self.current_trace["decisions"][-3:],
            "recent_learnings": self.current_trace["learnings"][-3:],
            "recent_impacts": self.current_trace["impacts"][-3:]
        }
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _calculate_prediction_accuracy(
        self,
        predicted: Dict,
        actual: Dict
    ) -> float:
        """Calculate how accurate prediction was."""
        if not predicted or not actual:
            return 0.0
        
        # Simple metric: matching keys with similar values
        matches = 0
        total = len(predicted)
        
        for key in predicted:
            if key in actual:
                if isinstance(predicted[key], (int, float)):
                    # Numeric: within 20% is "accurate"
                    if abs(predicted[key] - actual[key]) / (predicted[key] or 1) < 0.2:
                        matches += 1
                elif predicted[key] == actual[key]:
                    matches += 1
        
        return matches / total if total > 0 else 0.0
    
    def _calculate_effectiveness(self) -> float:
        """Calculate overall trace effectiveness score."""
        # Based on decision confidence, learning confidence, impact accuracy
        decision_avg = sum(
            d.get('confidence', 0.5) 
            for d in self.current_trace["decisions"]
        ) / len(self.current_trace["decisions"]) if self.current_trace["decisions"] else 0.5
        
        learning_avg = sum(
            l.get('confidence', 0.5)
            for l in self.current_trace["learnings"]
        ) / len(self.current_trace["learnings"]) if self.current_trace["learnings"] else 0.5
        
        impact_avg = sum(
            i.get('prediction_accuracy', 0.5)
            for i in self.current_trace["impacts"]
        ) / len(self.current_trace["impacts"]) if self.current_trace["impacts"] else 0.5
        
        return (decision_avg + learning_avg + impact_avg) / 3 * 10  # 0-10 scale
    
    def _extract_prompt_template(self) -> str:
        """Extract reusable prompt template from successful execution."""
        # Analyze current trace to identify template pattern
        # This would be more sophisticated in real implementation
        return "{{USER_REQUEST}}\n\n[META-CONTEXT]{{LEARNED_PATTERN}}"
    
    def export_trace(self) -> Dict:
        """Export complete trace for analysis or storage."""
        return {
            "session_id": self.session_id,
            "trace": self.current_trace,
            "effectiveness_score": self._calculate_effectiveness(),
            "timestamp": time.time()
        }
    
    def clear_trace(self):
        """Start new trace."""
        self.current_trace = {
            "decisions": [],
            "learnings": [],
            "impacts": []
        }
        self.session_id = f"trace_{int(time.time())}"

