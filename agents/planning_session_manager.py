"""
Planning Session Manager

VERSION: 1.0.0
DATE: 2025-10-15
PURPOSE: Orchestrate real-time meta-cognitive feedback during AI planning

Coordinates:
1. AI assistant planning process observation
2. Real-time meta-orchestrator feedback at checkpoints
3. Planning trace persistence
4. Meta-learning accumulation and storage

Real-Time Feedback Loop:
    AI starts planning
      ↓
    Record steps (PlanningObserver)
      ↓
    Checkpoint (steps 3, 7, 12)
      → Query meta-planning-analyzer
      → Receive feedback
      → Apply improvements
      ↓
    Continue with enhanced approach
      ↓
    Save meta-learnings for future sessions

This creates a closed-loop meta-cognitive improvement system.
"""

import json
import asyncio
from typing import Dict, Any, Optional, Callable, List
from pathlib import Path
from datetime import datetime
from agents.planning_observer import PlanningObserver


class PlanningSessionManager:
    """
    Manages meta-cognitive feedback loop during AI planning sessions.
    
    This enables continuous improvement of the planning process itself by:
    1. Capturing planning steps as structured data
    2. Analyzing efficiency and quality at checkpoints
    3. Providing real-time feedback for course correction
    4. Accumulating meta-learnings across sessions
    """
    
    def __init__(
        self,
        meta_orchestrator_task_func: Optional[Callable] = None,
        checkpoint_steps: List[int] = None,
        output_dir: str = "outputs/planning-traces"
    ):
        """
        Initialize planning session manager.
        
        Args:
            meta_orchestrator_task_func: Function to call meta-planning-analyzer
                                        Signature: async (agent_name, task) -> str
            checkpoint_steps: Step counts at which to request feedback
            output_dir: Directory to save planning traces
        """
        self.task_func = meta_orchestrator_task_func
        self.checkpoint_steps = checkpoint_steps or [3, 7, 12, 20]
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.observer: Optional[PlanningObserver] = None
        self.feedback_history: List[Dict] = []
        self.session_active = False
    
    def start_planning_session(self, task_description: str) -> PlanningObserver:
        """
        Initialize planning observation.
        
        Args:
            task_description: Description of the task being planned
        
        Returns:
            PlanningObserver instance for recording steps
        """
        self.observer = PlanningObserver(task_description)
        self.feedback_history = []
        self.session_active = True
        
        print(f"\n{'='*70}")
        print(f"🧠 Meta-Cognitive Planning Session Started")
        print(f"{'='*70}")
        print(f"Task: {task_description}")
        print(f"Checkpoints: Steps {', '.join(map(str, self.checkpoint_steps))}")
        print(f"{'='*70}\n")
        
        return self.observer
    
    async def checkpoint_feedback(self) -> Dict[str, Any]:
        """
        Query meta-orchestrator for real-time feedback at checkpoints.
        
        This is called automatically when planning reaches checkpoint steps
        (3, 7, 12, 20). Meta-planning-analyzer reviews the planning trace
        and provides actionable feedback.
        
        Returns:
            Feedback dictionary with suggestions and meta-learnings
        """
        if not self.observer:
            return {"action": "continue", "reason": "No active session"}
        
        current_step = self.observer.get_current_step_count()
        
        # Check if we're at a checkpoint
        if current_step not in self.checkpoint_steps:
            return {"action": "continue"}
        
        print(f"\n{'─'*70}")
        print(f"🔄 CHECKPOINT {current_step}: Requesting Meta-Orchestrator Feedback")
        print(f"{'─'*70}\n")
        
        # Export current planning trace
        trace = self.observer.export_for_meta_orchestrator()
        
        # Query meta-planning-analyzer (if task_func provided)
        if self.task_func:
            try:
                feedback_raw = await self.task_func(
                    agent_name="meta-planning-analyzer",
                    task=f"""Analyze this AI planning trace and provide real-time feedback:

{json.dumps(trace, indent=2, ensure_ascii=False)}

Focus on:
1. Inefficiencies that can be corrected NOW
2. Missed opportunities for better approaches
3. Patterns to remember for future sessions

Provide specific, actionable feedback in JSON format."""
                )
                
                # Parse feedback
                feedback_data = self._parse_feedback(feedback_raw)
                self.feedback_history.append({
                    "checkpoint_step": current_step,
                    "feedback": feedback_data,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Display feedback
                self._display_feedback(feedback_data, current_step)
                
                return feedback_data
                
            except Exception as e:
                print(f"⚠️  Feedback request failed: {e}")
                return {"action": "continue", "error": str(e)}
        
        else:
            # No task_func = standalone mode (just log checkpoint)
            print(f"ℹ️  Checkpoint {current_step} reached (no meta-orchestrator available)")
            return {"action": "continue", "mode": "standalone"}
    
    def _parse_feedback(self, feedback_raw: str) -> Dict:
        """
        Parse feedback from meta-planning-analyzer.
        
        Args:
            feedback_raw: Raw response string (may contain JSON)
        
        Returns:
            Parsed feedback dictionary
        """
        # Try to extract JSON
        if "```json" in feedback_raw:
            start = feedback_raw.find("```json") + 7
            end = feedback_raw.find("```", start)
            feedback_raw = feedback_raw[start:end].strip()
        elif "```" in feedback_raw:
            start = feedback_raw.find("```") + 3
            end = feedback_raw.find("```", start)
            feedback_raw = feedback_raw[start:end].strip()
        
        try:
            return json.loads(feedback_raw)
        except json.JSONDecodeError:
            # Fallback: return raw text
            return {
                "action": "continue",
                "raw_feedback": feedback_raw,
                "parse_error": True
            }
    
    def _display_feedback(self, feedback: Dict, checkpoint_step: int):
        """
        Display feedback in user-friendly format.
        
        Args:
            feedback: Parsed feedback dictionary
            checkpoint_step: Which checkpoint this is
        """
        print(f"📊 Overall Quality: {feedback.get('overall_quality', 'N/A')}")
        
        # Inefficiencies detected
        inefficiencies = feedback.get("inefficiencies_detected", [])
        if inefficiencies:
            print(f"\n⚠️  {len(inefficiencies)} Inefficiency(ies) Detected:")
            for ineff in inefficiencies[:3]:  # Show top 3
                print(f"   Step {ineff.get('step')}: {ineff.get('issue')}")
                print(f"   → Suggestion: {ineff.get('suggestion')}")
                print(f"   Impact: {ineff.get('impact', 'unknown')}\n")
        
        # Missed opportunities
        missed = feedback.get("missed_opportunities", [])
        if missed:
            print(f"💡 {len(missed)} Missed Opportunity(ies):")
            for opp in missed[:2]:  # Show top 2
                print(f"   {opp.get('suggestion')}")
                print(f"   Benefit: {opp.get('potential_benefit', 'unknown')}\n")
        
        # Improvement suggestions
        improvements = feedback.get("improvement_suggestions", [])
        if improvements:
            print(f"✨ {len(improvements)} Improvement Suggestion(s):")
            for imp in improvements[:2]:  # Show top 2
                print(f"   Current: {imp.get('current_approach', 'N/A')}")
                print(f"   Better: {imp.get('better_approach', 'N/A')}")
                print(f"   Benefit: {imp.get('benefit', 'unknown')}\n")
        
        # Meta-learning
        meta_learning = feedback.get("meta_learning", {})
        if meta_learning and meta_learning.get("pattern_identified"):
            print(f"🎓 Meta-Learning Identified:")
            print(f"   Pattern: {meta_learning.get('pattern_identified')}")
            print(f"   Recommendation: {meta_learning.get('recommendation')}")
            
            if meta_learning.get("save_to_memory"):
                print(f"   → Will save to memory-keeper for future sessions")
        
        print(f"\n{'─'*70}\n")
    
    def finalize_planning(self, save_trace: bool = True) -> Dict:
        """
        Finalize planning session and save results.
        
        Args:
            save_trace: Whether to save planning trace to file
        
        Returns:
            Complete planning trace with feedback history
        """
        if not self.observer:
            return {}
        
        trace = self.observer.export_for_meta_orchestrator()
        
        # Add feedback history
        trace["feedback_history"] = self.feedback_history
        trace["checkpoints_reached"] = len(self.feedback_history)
        
        # Save to file
        if save_trace:
            filename = f"planning_trace_{self.observer.session_id}.json"
            output_path = self.output_dir / filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(trace, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Planning trace saved: {output_path}")
        
        # Print summary
        print(f"\n{'='*70}")
        print(f"🎯 Planning Session Complete")
        print(f"{'='*70}")
        print(self.observer.get_summary())
        print(f"Checkpoints reached: {len(self.feedback_history)}")
        print(f"{'='*70}\n")
        
        self.session_active = False
        return trace
    
    def get_current_step(self) -> int:
        """Get current step count"""
        return self.observer.get_current_step_count() if self.observer else 0
    
    def should_checkpoint(self) -> bool:
        """Check if current step is a checkpoint"""
        current = self.get_current_step()
        return current in self.checkpoint_steps
    
    def extract_meta_learnings(self) -> List[Dict]:
        """
        Extract all meta-learnings from feedback history.
        
        These patterns should be saved to memory-keeper for
        continuous improvement across sessions.
        
        Returns:
            List of meta-learning dictionaries
        """
        learnings = []
        
        for feedback_record in self.feedback_history:
            feedback = feedback_record.get("feedback", {})
            meta_learning = feedback.get("meta_learning", {})
            
            if meta_learning and meta_learning.get("pattern_identified"):
                learnings.append({
                    "pattern": meta_learning.get("pattern_identified"),
                    "recommendation": meta_learning.get("recommendation"),
                    "confidence": meta_learning.get("confidence", 0.8),
                    "checkpoint_step": feedback_record.get("checkpoint_step"),
                    "timestamp": feedback_record.get("timestamp")
                })
        
        return learnings

