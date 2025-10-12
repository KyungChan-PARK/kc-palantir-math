#!/usr/bin/env python3
"""
Sequential-Thinking + Memory Integration for Palantir System
Automatically stores thinking processes to memory for persistence across context resets
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import uuid

from .memory_handler import get_memory_handler


class ThinkingMemoryIntegration:
    """
    Integrates sequential-thinking MCP tool with memory system
    Stores all thinking steps for context recovery after auto-compacting
    """

    def __init__(self, session_id: Optional[str] = None):
        """
        Initialize thinking-memory integration

        Args:
            session_id: Optional session identifier (generates UUID if not provided)
        """
        self.memory = get_memory_handler()
        self.session_id = session_id or str(uuid.uuid4())[:8]
        self.session_start = datetime.now().isoformat()
        self.thinking_log_path = f"thinking-logs/session-{self.session_id}.xml"
        self.current_task = None
        self.thinking_steps = []

        # Initialize session log
        self._initialize_session()

    def _initialize_session(self):
        """Create initial session log file"""
        initial_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<thinking-session>
  <metadata>
    <session-id>{self.session_id}</session-id>
    <started>{self.session_start}</started>
    <status>active</status>
  </metadata>
  <context>
    <project>Palantir Math Education System</project>
    <phase>To be determined</phase>
  </context>
  <thinking-log>
    <!-- Thinking steps will be recorded here -->
  </thinking-log>
  <decisions>
    <!-- Important decisions will be recorded here -->
  </decisions>
  <progress>
    <!-- Task progress will be tracked here -->
  </progress>
</thinking-session>
"""
        result = self.memory.create(self.thinking_log_path, initial_content)
        if result['status'] != 'success':
            print(f"Warning: Could not initialize session log: {result.get('error')}")

    def record_thinking_step(
        self,
        thought: str,
        thought_number: int,
        total_thoughts: int,
        is_revision: bool = False,
        revises_thought: Optional[int] = None,
        branch_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Record a single thinking step to memory

        Args:
            thought: The thought content
            thought_number: Current thought number
            total_thoughts: Estimated total thoughts
            is_revision: Whether this revises previous thinking
            revises_thought: Which thought is being revised
            branch_id: Branch identifier if branching

        Returns:
            Status dictionary
        """
        step = {
            "thought_number": thought_number,
            "total_thoughts": total_thoughts,
            "thought": thought,
            "timestamp": datetime.now().isoformat(),
            "is_revision": is_revision,
            "revises_thought": revises_thought,
            "branch_id": branch_id
        }

        self.thinking_steps.append(step)

        # Create XML entry
        xml_entry = f"""
    <thought id="{thought_number}" timestamp="{step['timestamp']}">
      <content>{self._escape_xml(thought)}</content>
      <meta>
        <progress>{thought_number}/{total_thoughts}</progress>
        {"<revision>true</revision>" if is_revision else ""}
        {f"<revises>{revises_thought}</revises>" if revises_thought else ""}
        {f"<branch>{branch_id}</branch>" if branch_id else ""}
      </meta>
    </thought>"""

        # Append to thinking log
        return self._append_to_section("thinking-log", xml_entry)

    def record_decision(self, decision: str, rationale: str, alternatives: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Record an important decision

        Args:
            decision: The decision made
            rationale: Why this decision was made
            alternatives: Other options considered

        Returns:
            Status dictionary
        """
        timestamp = datetime.now().isoformat()
        xml_entry = f"""
    <decision timestamp="{timestamp}">
      <choice>{self._escape_xml(decision)}</choice>
      <rationale>{self._escape_xml(rationale)}</rationale>
"""
        if alternatives:
            xml_entry += "      <alternatives>\n"
            for alt in alternatives:
                xml_entry += f"        <alternative>{self._escape_xml(alt)}</alternative>\n"
            xml_entry += "      </alternatives>\n"

        xml_entry += "    </decision>"

        return self._append_to_section("decisions", xml_entry)

    def record_progress(self, task: str, status: str, details: Optional[str] = None) -> Dict[str, Any]:
        """
        Record task progress

        Args:
            task: Task name
            status: Status (pending/in_progress/completed/blocked)
            details: Additional details

        Returns:
            Status dictionary
        """
        timestamp = datetime.now().isoformat()
        xml_entry = f"""
    <task timestamp="{timestamp}">
      <name>{self._escape_xml(task)}</name>
      <status>{status}</status>
      {f"<details>{self._escape_xml(details)}</details>" if details else ""}
    </task>"""

        return self._append_to_section("progress", xml_entry)

    def update_context(self, phase: Optional[str] = None, additional_info: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Update session context information

        Args:
            phase: Current project phase
            additional_info: Additional context key-value pairs

        Returns:
            Status dictionary
        """
        # Read current content
        view_result = self.memory.view(self.thinking_log_path)
        if view_result['status'] != 'success':
            return view_result

        content = view_result['content']

        # Update phase if provided
        if phase:
            content = content.replace(
                "<phase>To be determined</phase>",
                f"<phase>{self._escape_xml(phase)}</phase>"
            )

        # Add additional info
        if additional_info:
            context_section = "<context>"
            for key, value in additional_info.items():
                context_section += f"\n    <{key}>{self._escape_xml(value)}</{key}>"

            # Insert before </context>
            content = content.replace("</context>", f"{context_section}\n  </context>")

        return self.memory.create(self.thinking_log_path, content)

    def generate_summary(self) -> str:
        """
        Generate a summary of the thinking session

        Returns:
            Summary text
        """
        summary_parts = [
            f"## Thinking Session Summary",
            f"**Session ID**: {self.session_id}",
            f"**Started**: {self.session_start}",
            f"**Thinking Steps**: {len(self.thinking_steps)}",
            "",
            "### Key Thoughts:"
        ]

        # Add key thoughts (first, last, and any revisions)
        if self.thinking_steps:
            # First thought
            first = self.thinking_steps[0]
            summary_parts.append(f"1. **Initial thought**: {first['thought'][:100]}...")

            # Revisions
            revisions = [s for s in self.thinking_steps if s.get('is_revision')]
            if revisions:
                summary_parts.append(f"\n**Revisions made**: {len(revisions)}")
                for rev in revisions[:3]:  # Show up to 3 revisions
                    summary_parts.append(f"   - Thought #{rev['thought_number']}: {rev['thought'][:80]}...")

            # Last thought
            if len(self.thinking_steps) > 1:
                last = self.thinking_steps[-1]
                summary_parts.append(f"\n**Final thought**: {last['thought'][:100]}...")

        return "\n".join(summary_parts)

    def create_recovery_checkpoint(self, checkpoint_name: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a checkpoint for context recovery after compacting

        Args:
            checkpoint_name: Name for this checkpoint
            state: State dictionary to save (current phase, completed tasks, etc.)

        Returns:
            Status dictionary
        """
        checkpoint_path = f"phase-progress/checkpoint-{checkpoint_name}.json"

        checkpoint_data = {
            "checkpoint_name": checkpoint_name,
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "state": state,
            "thinking_summary": self.generate_summary(),
            "thinking_log_path": self.thinking_log_path
        }

        return self.memory.create(
            checkpoint_path,
            json.dumps(checkpoint_data, indent=2, ensure_ascii=False)
        )

    def load_latest_checkpoint(self) -> Optional[Dict[str, Any]]:
        """
        Load the most recent checkpoint

        Returns:
            Checkpoint data or None if no checkpoints exist
        """
        # List checkpoint files
        view_result = self.memory.view("phase-progress")
        if view_result['status'] != 'success':
            return None

        content = view_result['content']
        if not content or "(empty)" in content:
            return None

        # Find checkpoint files
        checkpoint_files = [
            line.split()[1] for line in content.split('\n')
            if line.startswith('[FILE]') and 'checkpoint-' in line
        ]

        if not checkpoint_files:
            return None

        # Load the latest checkpoint (assuming sorted by name/timestamp)
        latest = sorted(checkpoint_files)[-1]
        checkpoint_result = self.memory.view(f"phase-progress/{latest}")

        if checkpoint_result['status'] == 'success':
            return json.loads(checkpoint_result['content'])

        return None

    def _append_to_section(self, section_name: str, xml_content: str) -> Dict[str, Any]:
        """Helper to append content to a specific XML section"""
        # Read current content
        view_result = self.memory.view(self.thinking_log_path)
        if view_result['status'] != 'success':
            return view_result

        content = view_result['content']

        # Find the section closing tag and insert before it
        closing_tag = f"</{section_name}>"
        if closing_tag in content:
            content = content.replace(closing_tag, f"{xml_content}\n  {closing_tag}")
        else:
            return {
                "status": "error",
                "error": f"Section not found: {section_name}"
            }

        # Write back
        return self.memory.create(self.thinking_log_path, content)

    def _escape_xml(self, text: str) -> str:
        """Escape XML special characters"""
        if not text:
            return ""
        return (text
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&apos;"))

    def close_session(self, status: str = "completed") -> Dict[str, Any]:
        """
        Close the current thinking session

        Args:
            status: Session status (completed/interrupted/error)

        Returns:
            Status dictionary
        """
        view_result = self.memory.view(self.thinking_log_path)
        if view_result['status'] != 'success':
            return view_result

        content = view_result['content']

        # Update status
        content = content.replace(
            "<status>active</status>",
            f"<status>{status}</status>"
        )

        # Add end timestamp
        end_time = datetime.now().isoformat()
        content = content.replace(
            "</metadata>",
            f"  <ended>{end_time}</ended>\n  </metadata>"
        )

        return self.memory.create(self.thinking_log_path, content)


# Global instance
_thinking_integration = None

def get_thinking_integration(session_id: Optional[str] = None) -> ThinkingMemoryIntegration:
    """Get or create global thinking-memory integration instance"""
    global _thinking_integration
    if _thinking_integration is None:
        _thinking_integration = ThinkingMemoryIntegration(session_id)
    return _thinking_integration


# Convenience function for Claude to use
def think_and_remember(
    thought: str,
    thought_number: int,
    total_thoughts: int,
    **kwargs
) -> Dict[str, Any]:
    """
    Wrapper for sequential thinking that automatically stores to memory

    Usage in Claude workflow:
        result = think_and_remember(
            "I need to first understand the project structure...",
            thought_number=1,
            total_thoughts=5
        )

    Args:
        thought: Current thought
        thought_number: Current thought number
        total_thoughts: Estimated total thoughts
        **kwargs: Additional parameters (is_revision, revises_thought, etc.)

    Returns:
        Status dictionary
    """
    integration = get_thinking_integration()
    return integration.record_thinking_step(
        thought=thought,
        thought_number=thought_number,
        total_thoughts=total_thoughts,
        **kwargs
    )


if __name__ == "__main__":
    # Test the integration
    print("Testing Thinking-Memory Integration\n")

    integration = ThinkingMemoryIntegration("test-session")

    # Simulate thinking process
    integration.update_context(phase="Phase 1: Infrastructure")

    integration.record_thinking_step(
        "First, I need to understand the project structure and requirements.",
        thought_number=1,
        total_thoughts=5
    )

    integration.record_thinking_step(
        "The project requires both memory system and sequential thinking integration.",
        thought_number=2,
        total_thoughts=5
    )

    integration.record_decision(
        decision="Use XML format for thinking logs",
        rationale="XML is structured, human-readable, and easy to parse",
        alternatives=["JSON format", "Plain text with markers"]
    )

    integration.record_progress(
        task="Memory handler implementation",
        status="completed",
        details="Created memory_handler.py with security features"
    )

    integration.record_thinking_step(
        "Wait, I should reconsider the file format. JSON might be more portable.",
        thought_number=3,
        total_thoughts=6,  # Adjusted total
        is_revision=True,
        revises_thought=1
    )

    # Create checkpoint
    checkpoint = integration.create_recovery_checkpoint(
        checkpoint_name="post-memory-handler",
        state={
            "phase": "Phase 1",
            "completed_tasks": ["Memory handler", "Thinking integration"],
            "next_task": "Context editing configuration"
        }
    )

    print(f"Checkpoint created: {checkpoint}\n")

    # Generate summary
    summary = integration.generate_summary()
    print(summary)

    # View the thinking log
    print("\n\nThinking log file:")
    log = integration.memory.view(integration.thinking_log_path)
    print(log['content'][:1000] + "..." if len(log.get('content', '')) > 1000 else log.get('content', ''))

    # Close session
    integration.close_session("completed")
