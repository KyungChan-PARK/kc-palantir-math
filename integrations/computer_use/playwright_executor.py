"""
Playwright-based UI Automation Executor

Implements ComputerUseExecutor protocol using Playwright.
Executes UIAction sequences for agent-driven automation.

Features:
- Browser automation (Chromium/Firefox/WebKit)
- Screenshot capture for context
- DOM snapshot for debugging
- Error recovery

VERSION: 1.0.0
DATE: 2025-10-16
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional
from integrations.computer_use.gemini_computer_use_adapter import UIAction, ActionType


class PlaywrightExecutor:
    """
    Executes UI actions using Playwright.
    
    Implements ComputerUseExecutor protocol.
    """
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self._browser = None
        self._page = None
    
    async def _ensure_browser(self):
        """Lazy initialize browser"""
        if self._browser:
            return
        
        try:
            from playwright.async_api import async_playwright
            
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(headless=self.headless)
            self._page = await self._browser.new_page()
            
        except ImportError:
            raise RuntimeError(
                "Playwright not installed. Install with: pip install playwright && playwright install"
            )
    
    async def run(self, actions: List[UIAction]) -> Dict[str, Any]:
        """
        Execute a sequence of UI actions.
        
        Args:
            actions: List of UIAction to execute
        
        Returns:
            Execution summary with status and artifacts
        """
        await self._ensure_browser()
        
        results = []
        
        for i, action in enumerate(actions):
            try:
                result = await self._execute_single_action(action)
                results.append({
                    "index": i,
                    "action": action.action.value,
                    "status": "success",
                    "result": result
                })
            except Exception as e:
                results.append({
                    "index": i,
                    "action": action.action.value,
                    "status": "error",
                    "error": str(e)
                })
                # Stop on error
                break
        
        # Capture final screenshot
        screenshot = await self._page.screenshot() if self._page else None
        
        return {
            "status": "success" if all(r["status"] == "success" for r in results) else "partial",
            "actions_executed": len(results),
            "total_actions": len(actions),
            "results": results,
            "screenshot": screenshot
        }
    
    async def _execute_single_action(self, action: UIAction) -> Dict[str, Any]:
        """Execute a single UI action"""
        
        if action.action == ActionType.NAVIGATE:
            await self._page.goto(action.value)
            return {"url": action.value}
        
        elif action.action == ActionType.CLICK:
            await self._page.click(action.selector)
            return {"selector": action.selector}
        
        elif action.action == ActionType.TYPE:
            await self._page.fill(action.selector, action.value)
            return {"selector": action.selector, "text": action.value}
        
        elif action.action == ActionType.KEY:
            await self._page.keyboard.press(action.value)
            return {"key": action.value}
        
        elif action.action == ActionType.WAIT:
            await self._page.wait_for_timeout(action.wait_ms or 1000)
            return {"wait_ms": action.wait_ms}
        
        else:
            raise ValueError(f"Unknown action type: {action.action}")
    
    async def cleanup(self):
        """Close browser and cleanup"""
        if self._browser:
            await self._browser.close()
        if hasattr(self, '_playwright'):
            await self._playwright.stop()

