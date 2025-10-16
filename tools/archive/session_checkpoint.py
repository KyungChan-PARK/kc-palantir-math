"""
Session Checkpoint System for Claude Code 2.0

Automatic checkpoint saving for long-running sessions:
- Save every 10 turns
- Save on critical operations
- Load on --resume or --continue
- Compatible with context editing

Features:
- Incremental checkpoint saves
- Session state persistence
- Automatic recovery
- Turn-level granularity

Usage:
    from tools.session_checkpoint import SessionCheckpoint
    
    checkpoint = SessionCheckpoint(session_id="math-system-20251016")
    
    # Save checkpoint
    checkpoint.save_checkpoint(
        turn_number=5,
        agent_state={"current_agent": "research-agent"},
        context_summary="Researching Pythagorean Theorem"
    )
    
    # Load checkpoint
    state = checkpoint.load_checkpoint()

VERSION: 1.0.0
DATE: 2025-10-16
"""

from pathlib import Path
from typing import Dict, Any, Optional
import json
from datetime import datetime


class SessionCheckpoint:
    """
    Manages session checkpoints for resumable workflows.
    
    Checkpoints enable:
    - Resume after interruption
    - Context window transitions
    - Multi-session workflows
    - Error recovery
    """
    
    def __init__(self, session_id: str, checkpoint_dir: str = "/home/kc-palantir/math/.claude/checkpoints"):
        """
        Initialize checkpoint manager.
        
        Args:
            session_id: Unique session identifier
            checkpoint_dir: Directory for checkpoint storage
        """
        self.session_id = session_id
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoint_file = self.checkpoint_dir / f"{session_id}.json"
        self.turn_counter = 0
    
    def save_checkpoint(
        self,
        turn_number: int,
        agent_state: Dict[str, Any],
        context_summary: str = "",
        metrics: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Save session checkpoint.
        
        Args:
            turn_number: Current conversation turn
            agent_state: Current agent execution state
            context_summary: Brief summary of current context
            metrics: Optional performance metrics
        
        Returns:
            True if save successful
        """
        try:
            checkpoint_data = {
                "session_id": self.session_id,
                "turn_number": turn_number,
                "timestamp": datetime.now().isoformat(),
                "agent_state": agent_state,
                "context_summary": context_summary,
                "metrics": metrics or {},
                "checkpoint_version": "1.0.0"
            }
            
            # Write checkpoint
            with open(self.checkpoint_file, 'w') as f:
                json.dump(checkpoint_data, f, indent=2)
            
            self.turn_counter = turn_number
            return True
            
        except Exception as e:
            print(f"WARNING: Failed to save checkpoint: {e}")
            return False
    
    def load_checkpoint(self) -> Optional[Dict[str, Any]]:
        """
        Load session checkpoint.
        
        Returns:
            Checkpoint data or None if not found
        """
        try:
            if not self.checkpoint_file.exists():
                return None
            
            with open(self.checkpoint_file, 'r') as f:
                checkpoint_data = json.load(f)
            
            self.turn_counter = checkpoint_data.get('turn_number', 0)
            return checkpoint_data
            
        except Exception as e:
            print(f"WARNING: Failed to load checkpoint: {e}")
            return None
    
    def should_save_checkpoint(self, turn_number: int, force: bool = False) -> bool:
        """
        Determine if checkpoint should be saved.
        
        Args:
            turn_number: Current turn number
            force: Force save regardless of interval
        
        Returns:
            True if checkpoint should be saved
        """
        if force:
            return True
        
        # Save every 10 turns
        return turn_number % 10 == 0
    
    def get_checkpoint_info(self) -> Dict[str, Any]:
        """
        Get checkpoint metadata without loading full checkpoint.
        
        Returns:
            Metadata dict with session info
        """
        if not self.checkpoint_file.exists():
            return {
                "exists": False,
                "session_id": self.session_id
            }
        
        try:
            with open(self.checkpoint_file, 'r') as f:
                data = json.load(f)
            
            return {
                "exists": True,
                "session_id": self.session_id,
                "turn_number": data.get('turn_number', 0),
                "timestamp": data.get('timestamp'),
                "context_summary": data.get('context_summary', '')
            }
        except:
            return {
                "exists": False,
                "session_id": self.session_id,
                "error": "Corrupted checkpoint"
            }
    
    def delete_checkpoint(self):
        """Delete checkpoint file."""
        if self.checkpoint_file.exists():
            self.checkpoint_file.unlink()


def create_checkpoint_manager(session_id: str) -> SessionCheckpoint:
    """Factory function for easy checkpoint manager creation."""
    return SessionCheckpoint(session_id)

