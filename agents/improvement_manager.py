"""
Improvement Manager - Change History and Rollback

VERSION: 4.0.0
DATE: 2025-10-14
PURPOSE: Track improvement changes and enable rollback

Based on: SELF-IMPROVEMENT-IMPLEMENTATION-PLAN-v4.0.md Section III (Phase 3)

Core Features:
1. Change history logging
2. File backup before modifications
3. Rollback capability
4. Session quota management (max 5 improvements/session)
5. Statistics and reporting
"""

import uuid
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from agents.improvement_models import ImprovementAction, ChangeStatus, ChangeRecord


class ImprovementManager:
    """
    Manages improvement change history and rollback.

    Safety mechanisms (from v4.0 spec):
    - Max 5 improvements per session
    - Confidence threshold > 70%
    - Automatic backup before changes
    - Rollback on verification failure
    - Complete change history logging
    """

    def __init__(
        self,
        max_per_session: int = 5,
        backup_dir: str = "/tmp/improvement_backups"
    ):
        """
        Initialize Improvement Manager.

        Args:
            max_per_session: Maximum improvements allowed per session
            backup_dir: Directory for file backups
        """
        self.max_per_session = max_per_session
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        self.changes_log: List[ChangeRecord] = []
        self.session_count = 0  # Count for current session

    def can_make_improvement(self) -> Tuple[bool, str]:
        """
        Check if system can make another improvement.

        Returns:
            (can_improve, reason): Boolean and reason string
        """
        if self.session_count >= self.max_per_session:
            return False, f"Session quota reached ({self.session_count}/{self.max_per_session})"

        return True, "OK"

    def log_change(
        self,
        action: ImprovementAction,
        status: ChangeStatus,
        files_modified: Optional[List[str]] = None,
        backup_path: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> str:
        """
        Log an improvement change.

        Args:
            action: ImprovementAction that was attempted
            status: Current status of the change
            files_modified: List of file paths modified
            backup_path: Path to backup directory (if created)
            error_message: Error message if failed

        Returns:
            change_id: Unique identifier for this change
        """
        change_id = str(uuid.uuid4())[:8]

        record = ChangeRecord(
            change_id=change_id,
            action=action,
            status=status,
            timestamp=datetime.now().isoformat(),
            files_modified=files_modified or [],
            backup_path=backup_path,
            error_message=error_message
        )

        self.changes_log.append(record)

        if status == ChangeStatus.APPLIED:
            self.session_count += 1

        return change_id

    def backup_file(self, file_path: str) -> str:
        """
        Create backup of file before modification.

        Args:
            file_path: Path to file to backup

        Returns:
            backup_path: Path to backup file
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Create backup with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.{timestamp}.backup"
        backup_path = self.backup_dir / backup_name

        shutil.copy2(file_path, backup_path)

        return str(backup_path)

    def rollback_last(self) -> bool:
        """
        Rollback the last applied change.

        Returns:
            success: Whether rollback succeeded
        """
        # Find last APPLIED change
        last_applied = None
        for record in reversed(self.changes_log):
            if record.status == ChangeStatus.APPLIED:
                last_applied = record
                break

        if not last_applied:
            print("No applied changes to rollback")
            return False

        if not last_applied.backup_path:
            print(f"No backup available for change {last_applied.change_id}")
            return False

        # Restore from backup
        try:
            backup_path = Path(last_applied.backup_path)

            if not backup_path.exists():
                print(f"Backup file not found: {backup_path}")
                return False

            # Restore each modified file
            for file_path in last_applied.files_modified:
                target_path = Path(file_path)

                if target_path.exists():
                    shutil.copy2(backup_path, target_path)
                    print(f"Restored: {file_path}")

            # Update status
            last_applied.status = ChangeStatus.ROLLED_BACK

            # Decrement session count
            if self.session_count > 0:
                self.session_count -= 1

            print(f"✓ Rollback successful for change {last_applied.change_id}")
            return True

        except Exception as e:
            print(f"✗ Rollback failed: {e}")
            return False

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get improvement statistics.

        Returns:
            stats: Dictionary with counts and metrics
        """
        total = len(self.changes_log)
        applied = sum(1 for r in self.changes_log if r.status == ChangeStatus.APPLIED)
        failed = sum(1 for r in self.changes_log if r.status == ChangeStatus.FAILED)
        rolled_back = sum(1 for r in self.changes_log if r.status == ChangeStatus.ROLLED_BACK)

        success_rate = applied / total if total > 0 else 0.0

        return {
            "total_changes": total,
            "applied": applied,
            "failed": failed,
            "rolled_back": rolled_back,
            "success_rate": success_rate,
            "session_count": self.session_count,
            "session_quota": self.max_per_session,
            "quota_remaining": self.max_per_session - self.session_count
        }

    def get_change_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent change history.

        Args:
            limit: Maximum number of records to return

        Returns:
            history: List of change records as dictionaries
        """
        recent = self.changes_log[-limit:]
        return [record.to_dict() for record in reversed(recent)]

    def reset_session(self):
        """Reset session counter (call at session start)"""
        self.session_count = 0
