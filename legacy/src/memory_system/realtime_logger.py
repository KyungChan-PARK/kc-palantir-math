#!/usr/bin/env python3
"""
Real-time Logger - 작업 중 모든 중요한 이벤트를 즉시 메모리에 저장
Context compacting이 언제 발생하더라도 작업 손실 없음
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

from memory_handler import get_memory_handler


class RealtimeLogger:
    """
    실시간으로 작업 내용을 메모리에 저장
    모든 중요한 작업은 즉시 incremental log에 기록됨
    """

    def __init__(self, session_id: Optional[str] = None):
        self.memory = get_memory_handler()
        self.session_id = session_id or datetime.now().strftime("%Y%m%d-%H%M%S")
        self.log_file = f"phase-progress/incremental-{datetime.now().strftime('%Y%m%d')}.jsonl"

    def log_action(
        self,
        action_type: str,
        description: str,
        details: Optional[Dict[str, Any]] = None,
        importance: str = "normal"
    ) -> Dict[str, Any]:
        """
        작업 즉시 로깅

        Args:
            action_type: 작업 유형 (tool_use, thinking, decision, progress, etc.)
            description: 작업 설명
            details: 추가 상세 정보
            importance: 중요도 (low, normal, high, critical)

        Returns:
            Status dictionary
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "action_type": action_type,
            "description": description,
            "importance": importance,
            "details": details or {}
        }

        # Append to incremental log (JSONL format)
        return self._append_to_log(log_entry)

    def log_tool_use(self, tool_name: str, tool_args: Dict[str, Any], result_summary: str) -> Dict[str, Any]:
        """
        도구 사용 로깅 (스마트 필터링)

        중요한 도구만 로깅:
        - Write, Edit, Create: 파일 변경
        - Sequential-thinking: 사고 과정
        - Bash (git): 코드 커밋

        무시하는 도구:
        - Read: 읽기만 하므로 상태 변경 없음
        - Glob, Grep: 검색만
        - View: 조회만
        """
        # 중요한 도구만 로깅
        important_tools = [
            "Write", "Edit", "Create", "Delete", "Rename",  # 파일 변경
            "mcp__sequential-thinking__sequentialthinking",  # 사고 과정
            "Bash",  # 명령 실행 (git, npm 등)
            "memory"  # 메모리 작업
        ]

        # 무시할 도구
        skip_tools = ["Read", "Glob", "Grep", "view"]

        # 스킵 조건
        if any(skip in tool_name for skip in skip_tools):
            return {"status": "skipped", "reason": "read-only operation"}

        # 중요한 도구만 로깅
        if not any(imp in tool_name for imp in important_tools):
            return {"status": "skipped", "reason": "non-critical operation"}

        return self.log_action(
            action_type="tool_use",
            description=f"Used tool: {tool_name}",
            details={
                "tool": tool_name,
                "args_summary": str(tool_args)[:100],  # 200 → 100 절반으로
                "result_preview": result_summary[:100]  # 200 → 100 절반으로
            },
            importance="critical" if tool_name in ["Write", "Edit", "Create"] else "high"
        )

    def log_thinking(self, thought: str, thought_number: int, total_thoughts: int) -> Dict[str, Any]:
        """Thinking 과정 로깅"""
        return self.log_action(
            action_type="thinking",
            description=f"Thought {thought_number}/{total_thoughts}",
            details={
                "thought": thought[:500],  # First 500 chars
                "thought_number": thought_number,
                "total_thoughts": total_thoughts
            },
            importance="high"
        )

    def log_decision(self, decision: str, rationale: str) -> Dict[str, Any]:
        """의사결정 로깅"""
        return self.log_action(
            action_type="decision",
            description=decision,
            details={
                "rationale": rationale
            },
            importance="critical"
        )

    def log_progress(self, task: str, status: str, details: Optional[str] = None) -> Dict[str, Any]:
        """진행상황 로깅"""
        return self.log_action(
            action_type="progress",
            description=f"{task}: {status}",
            details={
                "task": task,
                "status": status,
                "notes": details
            },
            importance="high" if status == "completed" else "normal"
        )

    def log_file_operation(self, operation: str, file_path: str, summary: str) -> Dict[str, Any]:
        """파일 작업 로깅 (Write, Edit, Create)"""
        return self.log_action(
            action_type="file_operation",
            description=f"{operation}: {file_path}",
            details={
                "operation": operation,
                "file": file_path,
                "summary": summary[:200]
            },
            importance="critical"
        )

    def create_snapshot(self, snapshot_name: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        현재 상태의 스냅샷 생성
        중요한 작업 후 또는 주기적으로 호출
        """
        timestamp = datetime.now()
        snapshot = {
            "snapshot_name": snapshot_name,
            "timestamp": timestamp.isoformat(),
            "session_id": self.session_id,
            "state": state,
            "log_file": self.log_file
        }

        snapshot_file = f"phase-progress/snapshot-{timestamp.strftime('%Y%m%d-%H%M%S')}.json"
        return self.memory.create(
            snapshot_file,
            json.dumps(snapshot, indent=2, ensure_ascii=False)
        )

    def get_recent_actions(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        최근 작업 목록 가져오기
        Context reset 후 재개할 때 사용

        Args:
            limit: 가져올 작업 수

        Returns:
            최근 작업 목록
        """
        result = self.memory.view(self.log_file)

        if result['status'] != 'success':
            return []

        # Parse JSONL
        lines = result['content'].strip().split('\n')
        actions = []

        for line in reversed(lines[-limit:]):  # Get last N lines
            try:
                actions.append(json.loads(line))
            except json.JSONDecodeError:
                continue

        return actions

    def reconstruct_context(self) -> Dict[str, Any]:
        """
        Incremental log에서 컨텍스트 재구성
        Context reset 후 호출

        Returns:
            재구성된 컨텍스트
        """
        recent_actions = self.get_recent_actions(limit=50)

        # 중요한 작업들만 추출
        important_actions = [
            a for a in recent_actions
            if a.get('importance') in ['high', 'critical']
        ]

        # 마지막 결정사항
        last_decisions = [
            a for a in recent_actions
            if a.get('action_type') == 'decision'
        ][-5:]

        # 마지막 진행상황
        last_progress = [
            a for a in recent_actions
            if a.get('action_type') == 'progress'
        ][-10:]

        # 마지막 파일 작업
        last_file_ops = [
            a for a in recent_actions
            if a.get('action_type') == 'file_operation'
        ][-10:]

        return {
            "total_actions": len(recent_actions),
            "important_actions_count": len(important_actions),
            "last_decisions": last_decisions,
            "last_progress": last_progress,
            "last_file_operations": last_file_ops,
            "can_resume": len(important_actions) > 0,
            "resume_point": important_actions[-1] if important_actions else None
        }

    def _append_to_log(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """Append entry to incremental log file"""
        try:
            # Read existing content
            result = self.memory.view(self.log_file)
            if result['status'] == 'success':
                content = result['content']
            else:
                content = ""

            # Append new entry (JSONL format)
            content += json.dumps(entry, ensure_ascii=False) + "\n"

            # Write back
            return self.memory.create(self.log_file, content)

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }


# Global instance
_realtime_logger = None


def get_realtime_logger(session_id: Optional[str] = None) -> RealtimeLogger:
    """Get or create global realtime logger instance"""
    global _realtime_logger
    if _realtime_logger is None:
        _realtime_logger = RealtimeLogger(session_id)
    return _realtime_logger


# Convenience functions
def log_now(action_type: str, description: str, **kwargs):
    """Quick logging function"""
    logger = get_realtime_logger()
    return logger.log_action(action_type, description, **kwargs)


def snapshot_now(name: str, state: Dict[str, Any]):
    """Quick snapshot function"""
    logger = get_realtime_logger()
    return logger.create_snapshot(name, state)


if __name__ == "__main__":
    # Test realtime logger
    logger = RealtimeLogger("test-session")

    # Simulate work
    logger.log_thinking("First thought about the problem", 1, 5)
    logger.log_tool_use("Read", {"file": "test.py"}, "File contents...")
    logger.log_decision("Use Python for implementation", "Python is more suitable")
    logger.log_file_operation("Write", "test.py", "Created new file")
    logger.log_progress("Implement memory system", "completed", "All tests passed")

    # Create snapshot
    logger.create_snapshot("after-memory-implementation", {
        "phase": "Phase 1",
        "completed": ["Memory system"]
    })

    # Reconstruct context
    context = logger.reconstruct_context()
    print("\n📊 Reconstructed Context:")
    print(json.dumps(context, indent=2, ensure_ascii=False))

    # Get recent actions
    print("\n📜 Recent Actions:")
    for action in logger.get_recent_actions(limit=5):
        print(f"  [{action['importance']}] {action['action_type']}: {action['description']}")
