"""
Gemini Computer Use Adapter (skeleton)

Purpose:
- Define integration boundaries to leverage Google DeepMind Gemini "Computer
  Use" style capabilities (UI control, action planning) from our agent
  orchestrator.

This adapter is intentionally lightweight and framework-agnostic. It exposes a
minimal interface that a concrete Gemini client can implement outside this
repository.

Reference:
- Blog: https://blog.google/technology/google-deepmind/gemini-computer-use-model/

Design:
- Planner interface: produce action plans given goals and current UI state
- Executor interface: execute an action (click, type, navigate) via injected
  driver (e.g., Playwright, Selenium, OS automation)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol


class ActionType(str, Enum):
    CLICK = "click"
    TYPE = "type"
    NAVIGATE = "navigate"
    KEY = "key"
    WAIT = "wait"


@dataclass
class UIAction:
    """Represents a single UI action in a plan."""

    action: ActionType
    selector: Optional[str] = None
    value: Optional[str] = None
    wait_ms: Optional[int] = None


class ComputerUsePlanner(Protocol):
    """Protocol for a Gemini-backed planner that generates UI action plans."""

    def plan(self, goal: str, context: Dict[str, Any]) -> List[UIAction]:
        ...


class ComputerUseExecutor(Protocol):
    """Protocol for an executor that can run UI actions using a driver."""

    def run(self, actions: List[UIAction]) -> Dict[str, Any]:
        ...


class ComputerUseAdapter:
    """High-level coordinator that bridges planner and executor."""

    def __init__(self, planner: ComputerUsePlanner, executor: ComputerUseExecutor):
        self.planner = planner
        self.executor = executor

    def accomplish(self, goal: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Plan then execute to accomplish a UI goal.

        Args:
            goal: Natural-language goal, e.g., "Download the latest report as CSV"
            context: Optional environment/DOM state snapshot

        Returns:
            Execution summary with status and any outputs
        """
        ctx = context or {}
        actions = self.planner.plan(goal, ctx)
        result = self.executor.run(actions)
        return {
            "goal": goal,
            "actions": [a.__dict__ for a in actions],
            "result": result,
        }


