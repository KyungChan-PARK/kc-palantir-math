"""
Kinetic Runtime Class - Unified Runtime Capabilities

Extends KineticTier with observability, realtime, and computer-use.
Integrates with KineticWorkflowEngine, KineticDataFlowOrchestrator, KineticStateTransitionManager.

VERSION: 1.0.0
DATE: 2025-10-16
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio


class KineticRuntime:
    """
    Unified runtime layer for Palantir Kinetic tier.
    
    Combines:
    - KineticTier (workflow/dataflow/state)
    - EventReporter (observability)
    - RealtimeGateway (audio/text streaming)
    - ComputerUseAdapter (UI automation)
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        from kinetic_layer import KineticTier
        
        self.kinetic_tier = KineticTier()
        self.config = config or {}
        self._obs = None
        self._realtime = None
        self._computer_use = None
        
        # Initialize based on config
        if self.config.get('observability_enabled'):
            from integrations.observability.event_reporter import EventReporter
            self._obs = EventReporter("kinetic-runtime")
        
        if self.config.get('realtime_enabled'):
            from integrations.realtime.gateway_service import RealtimeGateway
            self._realtime = RealtimeGateway(self.config)
        
        if self.config.get('computer_use_enabled'):
            from integrations.computer_use.gemini_computer_use_adapter import ComputerUseAdapter
            from integrations.computer_use.gemini_planner_client import GeminiPlanner
            from integrations.computer_use.playwright_executor import PlaywrightExecutor
            
            planner = GeminiPlanner()
            executor = PlaywrightExecutor(headless=self.config.get('playwright_headless', False))
            self._computer_use = ComputerUseAdapter(planner, executor)
    
    async def execute_task(
        self,
        task: str,
        agents: List[str],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute workflow task with full runtime capabilities.
        
        Emits observability events at each stage.
        Supports realtime streaming if enabled.
        Can use computer-use for UI automation if needed.
        
        Args:
            task: Task description
            agents: Available agents for workflow
            context: Execution context
        
        Returns:
            Execution result with metrics
        """
        session_id = context.get('session_id', 'unknown')
        start_time = time.time()
        
        # Observability: Workflow start
        if self._obs:
            self._obs.notification(session_id, f"Workflow started: {task[:50]}")
        
        # Execute via kinetic tier
        try:
            result = await self.kinetic_tier.execute_task(task, agents, context)
            
            duration_ms = (time.time() - start_time) * 1000
            
            # Observability: Workflow complete
            if self._obs:
                self._obs.notification(
                    session_id,
                    f"Workflow complete in {duration_ms:.0f}ms",
                    level="success"
                )
            
            return {
                "success": result.success,
                "duration_ms": duration_ms,
                "outputs": result.outputs,
                "state": result.state.value,
                "inefficiencies": [i.value for i in result.inefficiencies_detected],
                "metrics": result.metrics,
                "runtime_features_used": {
                    "observability": self._obs is not None,
                    "realtime": self._realtime is not None,
                    "computer_use": self._computer_use is not None
                }
            }
            
        except Exception as e:
            # Observability: Workflow error
            if self._obs:
                self._obs.notification(session_id, f"Workflow error: {e}", level="error")
            
            raise
    
    async def start_realtime_gateway(self):
        """Start realtime gateway if enabled"""
        if self._realtime:
            await self._realtime.start_background()
    
    async def stop_realtime_gateway(self):
        """Stop realtime gateway"""
        if self._realtime:
            await self._realtime.stop()
    
    async def execute_ui_goal(self, goal: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute UI automation goal via computer-use"""
        if not self._computer_use:
            raise RuntimeError("Computer use not enabled in runtime config")
        
        session_id = context.get('session_id', 'unknown') if context else 'unknown'
        
        # Observability: UI automation start
        if self._obs:
            self._obs.notification(session_id, f"UI automation: {goal[:50]}")
        
        result = self._computer_use.accomplish(goal, context)
        
        # Observability: UI automation complete
        if self._obs:
            self._obs.notification(
                session_id,
                f"UI automation complete: {result.get('status')}",
                level="success" if result.get('status') == 'success' else "warning"
            )
        
        return result

