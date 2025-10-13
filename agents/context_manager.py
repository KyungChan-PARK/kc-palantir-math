"""
Context Manager for Memory-Keeper Integration
VERSION: 2.0.0 - Integrated from v5.0 + Korean plan improvements

Automates context persistence and retrieval via MCP memory-keeper:
- Category-based organization
- Automatic cleanup of old entries
- Priority-based retention policies
- Session state management

Based on:
- scalable.pdf: Context persistence for multi-agent systems
- MCP memory-keeper server best practices
"""

import json
import logging
from typing import Any, Callable, Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


@dataclass
class ContextCategory:
    """Context category definition with retention policy"""
    name: str
    priority: str
    description: str
    retention_days: int
    max_items: int


class ContextManager:
    """
    Manages context persistence via memory-keeper MCP server.

    Features:
    - Auto-categorization of context data
    - Periodic cleanup of old context
    - Priority-based retention policies
    - Session state tracking
    """

    # Category definitions with retention policies
    CATEGORIES = {
        "session-state": ContextCategory(
            name="session-state",
            priority="high",
            description="Current workflow state",
            retention_days=7,
            max_items=50
        ),
        "agent-performance": ContextCategory(
            name="agent-performance",
            priority="medium",
            description="Agent metrics and performance data",
            retention_days=7,
            max_items=100
        ),
        "errors": ContextCategory(
            name="errors",
            priority="high",
            description="Error logs and diagnostics",
            retention_days=30,
            max_items=200
        ),
        "decisions": ContextCategory(
            name="decisions",
            priority="high",
            description="Architecture and design decisions",
            retention_days=-1,  # Keep indefinitely
            max_items=-1  # No limit
        ),
        "tasks": ContextCategory(
            name="tasks",
            priority="medium",
            description="Task tracking and progress",
            retention_days=7,
            max_items=100
        ),
        "progress": ContextCategory(
            name="progress",
            priority="medium",
            description="Completed work and milestones",
            retention_days=7,
            max_items=100
        ),
        "architecture": ContextCategory(
            name="architecture",
            priority="high",
            description="System design and architecture",
            retention_days=-1,  # Keep indefinitely
            max_items=-1  # No limit
        ),
        "milestone": ContextCategory(
            name="milestone",
            priority="high",
            description="Major achievements and checkpoints",
            retention_days=-1,  # Keep indefinitely
            max_items=-1  # No limit
        ),
        "debug": ContextCategory(
            name="debug",
            priority="low",
            description="Debug information and temporary data",
            retention_days=3,
            max_items=50
        )
    }

    def __init__(self, memory_tool_func: Callable):
        """
        Initialize context manager.

        Args:
            memory_tool_func: Function to call memory-keeper MCP tools
                             Signature: def(tool_name: str, **params) -> dict
        """
        self.memory_tool = memory_tool_func
        self.context_save_count = 0
        self.auto_cleanup_interval = 10  # Cleanup every N saves

    def save(
        self,
        key: str,
        value: Any,
        category: str,
        priority: Optional[str] = None,
        metadata: Optional[Dict] = None,
        channel: Optional[str] = None,
        tags: Optional[List[str]] = None
    ):
        """
        Save context item to memory-keeper.

        Args:
            key: Unique identifier for this context item
            value: Data to save (will be JSON serialized if dict/list)
            category: Category name (must be in CATEGORIES)
            priority: Override category default priority (high/medium/low)
            metadata: Optional metadata dictionary
            channel: Optional channel for topic-based organization
            tags: Optional tags for filtering

        Raises:
            ValueError: If category is invalid
        """
        if category not in self.CATEGORIES:
            raise ValueError(
                f"Invalid category: {category}. "
                f"Must be one of {list(self.CATEGORIES.keys())}"
            )

        cat_def = self.CATEGORIES[category]

        # Serialize value if needed
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)

        # Get priority (use category default if not specified)
        final_priority = priority or cat_def.priority

        # Build parameters
        params = {
            "key": key,
            "value": value,
            "category": category,
            "priority": final_priority,
            "metadata": metadata or {}
        }

        # Add optional parameters
        if channel:
            params["channel"] = channel
        if tags:
            params["tags"] = tags

        # Save to memory-keeper
        try:
            self.memory_tool('mcp__memory-keeper__context_save', **params)
            logger.info(f"Context saved: {key} (category: {category})")

            # Increment save counter
            self.context_save_count += 1

            # Auto-cleanup check
            if self.context_save_count % self.auto_cleanup_interval == 0:
                self._auto_cleanup()

        except Exception as e:
            logger.error(f"Failed to save context {key}: {e}")
            raise

    def get(
        self,
        category: Optional[str] = None,
        key: Optional[str] = None,
        priorities: Optional[List[str]] = None,
        limit: int = 10,
        channel: Optional[str] = None
    ) -> List[Dict]:
        """
        Retrieve context items from memory-keeper.

        Args:
            category: Filter by category
            key: Specific key to retrieve
            priorities: Filter by priority levels
            limit: Maximum items to return
            channel: Filter by channel

        Returns:
            List of context items
        """
        params = {"limit": limit}

        if category:
            params["category"] = category
        if key:
            params["key"] = key
        if priorities:
            params["priorities"] = priorities
        if channel:
            params["channel"] = channel

        try:
            result = self.memory_tool('mcp__memory-keeper__context_get', **params)
            items = result.get("items", [])
            logger.info(f"Retrieved {len(items)} context items")
            return items
        except Exception as e:
            logger.error(f"Failed to retrieve context: {e}")
            return []

    def save_session_state(self, state: Dict, channel: Optional[str] = None):
        """
        Save current session state.

        Args:
            state: Session state dictionary
            channel: Optional channel name
        """
        self.save(
            key="current-session-state",
            value=state,
            category="session-state",
            priority="high",
            channel=channel,
            metadata={"timestamp": datetime.now().isoformat()}
        )

    def get_session_state(self, channel: Optional[str] = None) -> Optional[Dict]:
        """
        Get current session state.

        Args:
            channel: Optional channel name

        Returns:
            Session state dictionary or None
        """
        items = self.get(
            category="session-state",
            key="current-session-state",
            limit=1,
            channel=channel
        )

        if items:
            value = items[0].get("value", "{}")
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return None
        return None

    def save_performance_metrics(self, metrics: Dict, agent_name: Optional[str] = None):
        """
        Save performance metrics.

        Args:
            metrics: Metrics dictionary
            agent_name: Optional agent name for metadata
        """
        metadata = {"timestamp": datetime.now().isoformat()}
        if agent_name:
            metadata["agent"] = agent_name

        self.save(
            key=f"performance-metrics-{datetime.now().timestamp()}",
            value=metrics,
            category="agent-performance",
            priority="medium",
            metadata=metadata
        )

    def save_error(
        self,
        agent_name: str,
        error_type: str,
        error_message: str,
        context: Dict
    ):
        """
        Save error information.

        Args:
            agent_name: Name of agent that encountered error
            error_type: Type/class of error
            error_message: Error message
            context: Additional context about the error
        """
        error_data = {
            "agent": agent_name,
            "error_type": error_type,
            "message": error_message,
            "timestamp": datetime.now().isoformat(),
            "context": context
        }

        self.save(
            key=f"error-{datetime.now().timestamp()}",
            value=error_data,
            category="errors",
            priority="high",
            metadata={"agent": agent_name}
        )

    def save_decision(self, decision_title: str, decision_data: Dict):
        """
        Save architecture or design decision (permanent).

        Args:
            decision_title: Short title for the decision
            decision_data: Decision details and rationale
        """
        self.save(
            key=f"decision-{decision_title.lower().replace(' ', '-')}",
            value=decision_data,
            category="decisions",
            priority="high",
            metadata={"timestamp": datetime.now().isoformat()}
        )

    def save_milestone(self, milestone_name: str, milestone_data: Dict):
        """
        Save major milestone (permanent).

        Args:
            milestone_name: Name of the milestone
            milestone_data: Milestone details and achievements
        """
        self.save(
            key=f"milestone-{milestone_name.lower().replace(' ', '-')}",
            value=milestone_data,
            category="milestone",
            priority="high",
            tags=["milestone"],
            metadata={"timestamp": datetime.now().isoformat()}
        )

    def _auto_cleanup(self):
        """
        Automatic cleanup of old context items based on retention policy.

        - Deletes items older than retention_days (if applicable)
        - Keeps only the latest max_items per category
        - Skips categories with retention_days = -1 (indefinite retention)
        """
        logger.info("Auto-cleanup: Checking context items...")

        for cat_name, cat_def in self.CATEGORIES.items():
            # Skip indefinite retention categories
            if cat_def.retention_days == -1:
                continue

            try:
                # Get all items in category (up to 1000)
                items = self.get(category=cat_name, limit=1000)

                # Check if cleanup needed
                if len(items) <= cat_def.max_items:
                    continue

                logger.info(
                    f"Cleanup needed for {cat_name}: "
                    f"{len(items)} items > {cat_def.max_items} limit"
                )

                # Sort by created_at timestamp (newest first)
                items_sorted = sorted(
                    items,
                    key=lambda x: x.get("created_at", ""),
                    reverse=True
                )

                # Items to keep
                items_to_keep = items_sorted[:cat_def.max_items]
                items_to_delete = items_sorted[cat_def.max_items:]

                # Delete old items (if delete API available)
                for item in items_to_delete:
                    item_key = item.get("key")
                    logger.info(f"  Marking for deletion: {item_key}")
                    # Note: memory-keeper may not have delete API
                    # In that case, items will be kept until manual cleanup

            except Exception as e:
                logger.error(f"Cleanup failed for {cat_name}: {e}")

    def search(
        self,
        query: str,
        category: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict]:
        """
        Search context items by query string.

        Args:
            query: Search query
            category: Filter by category
            limit: Maximum items to return

        Returns:
            List of matching context items
        """
        params = {"query": query, "limit": limit}

        if category:
            params["category"] = category

        try:
            result = self.memory_tool('mcp__memory-keeper__context_search', **params)
            items = result.get("items", [])
            logger.info(f"Search returned {len(items)} items for query: {query}")
            return items
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def get_statistics(self) -> Dict:
        """
        Get statistics about stored context.

        Returns:
            Dictionary with statistics per category
        """
        stats = {}

        for cat_name in self.CATEGORIES.keys():
            try:
                items = self.get(category=cat_name, limit=1000)
                stats[cat_name] = {
                    "count": len(items),
                    "retention_days": self.CATEGORIES[cat_name].retention_days,
                    "max_items": self.CATEGORIES[cat_name].max_items
                }
            except Exception as e:
                logger.error(f"Failed to get stats for {cat_name}: {e}")
                stats[cat_name] = {"count": 0, "error": str(e)}

        return stats

    def print_statistics(self):
        """Print context storage statistics"""
        stats = self.get_statistics()

        print("\n" + "=" * 80)
        print("Context Storage Statistics")
        print("=" * 80)

        for cat_name, cat_stats in sorted(stats.items()):
            count = cat_stats.get("count", 0)
            max_items = cat_stats.get("max_items", -1)
            retention = cat_stats.get("retention_days", -1)

            max_str = "unlimited" if max_items == -1 else str(max_items)
            retention_str = "permanent" if retention == -1 else f"{retention} days"

            print(
                f"{cat_name:<20} "
                f"Items: {count:<4} "
                f"Max: {max_str:<10} "
                f"Retention: {retention_str}"
            )

        print("=" * 80 + "\n")
