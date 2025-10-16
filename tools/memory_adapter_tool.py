"""
Memory Tool Adapter for Claude Code 2.0

Implements Claude Code's memory_20250818 tool pattern for cross-session persistence.
Replaces MCP memory-keeper with file-based memory system compatible with
context editing and Dynamic Tier learning.

Features:
- View directory/file contents (with optional line ranges)
- Create/overwrite files
- String replacement in files
- Insert text at specific lines
- Delete files/directories
- Rename/move files

Usage:
    from tools.memory_adapter_tool import MemoryAdapter
    
    memory = MemoryAdapter(Path("/home/kc-palantir/math/memories"))
    
    # View directory
    contents = memory.view("/memories")
    
    # Create learning file
    memory.create("/memories/learnings/pattern_001.json", '{"insight": "..."}')
    
    # Update file
    memory.str_replace("/memories/learnings/pattern_001.json", 
                      '"confidence": 0.8', 
                      '"confidence": 0.9')

VERSION: 1.0.0
DATE: 2025-10-16
"""

from pathlib import Path
from typing import Optional, Tuple
import json


class MemoryAdapter:
    """
    Claude Code memory tool adapter for cross-session persistence.
    
    Implements the memory_20250818 tool pattern from Claude Code 2.0.
    Provides file-based storage compatible with Dynamic Tier learning.
    """
    
    def __init__(self, memory_dir: Path):
        """
        Initialize memory adapter.
        
        Args:
            memory_dir: Base directory for memory storage (e.g., /memories/)
        """
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
    
    def view(self, path: str, view_range: Optional[Tuple[int, int]] = None) -> str:
        """
        View directory or file contents (Claude Code memory tool pattern).
        
        Args:
            path: Path relative to memory_dir (can start with / or not)
            view_range: Optional (start_line, end_line) tuple for partial view
        
        Returns:
            Directory listing or file contents
        
        Examples:
            view("/memories") -> "learnings\npatterns\nsessions"
            view("/memories/learnings/pattern_001.json") -> '{"insight": "..."}'
            view("/memories/learnings/pattern_001.json", (1, 10)) -> First 10 lines
        """
        # Normalize path (remove leading /)
        normalized_path = path.lstrip('/')
        full_path = self.memory_dir / normalized_path
        
        # Security: Ensure path stays within memory_dir
        try:
            full_path = full_path.resolve()
            full_path.relative_to(self.memory_dir.resolve())
        except ValueError:
            raise PermissionError(f"Path traversal detected: {path}")
        
        if full_path.is_dir():
            # List directory contents
            items = sorted([item.name for item in full_path.iterdir()])
            return "\n".join(items) if items else "(empty directory)"
        else:
            # Read file contents
            if not full_path.exists():
                raise FileNotFoundError(f"File not found: {path}")
            
            content = full_path.read_text()
            
            if view_range:
                lines = content.splitlines()
                start, end = view_range
                # 1-indexed, inclusive range
                content = "\n".join(lines[start-1:end])
            
            return content
    
    def create(self, path: str, file_text: str):
        """
        Create or overwrite file.
        
        Args:
            path: Path relative to memory_dir
            file_text: Contents to write
        
        Examples:
            create("/memories/learnings/pattern_001.json", '{"insight": "..."}')
        """
        normalized_path = path.lstrip('/')
        full_path = self.memory_dir / normalized_path
        
        # Security check
        try:
            full_path = full_path.resolve()
            full_path.relative_to(self.memory_dir.resolve())
        except ValueError:
            raise PermissionError(f"Path traversal detected: {path}")
        
        # Create parent directories if needed
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        full_path.write_text(file_text)
    
    def str_replace(self, path: str, old_str: str, new_str: str):
        """
        Replace text in file (first occurrence only).
        
        Args:
            path: Path relative to memory_dir
            old_str: Text to find
            new_str: Replacement text
        
        Raises:
            ValueError: If old_str not found in file
        
        Examples:
            str_replace("/memories/config.json", '"version": "1.0"', '"version": "2.0"')
        """
        normalized_path = path.lstrip('/')
        full_path = self.memory_dir / normalized_path
        
        # Security check
        try:
            full_path = full_path.resolve()
            full_path.relative_to(self.memory_dir.resolve())
        except ValueError:
            raise PermissionError(f"Path traversal detected: {path}")
        
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        content = full_path.read_text()
        
        if old_str not in content:
            raise ValueError(f"String '{old_str}' not found in {path}")
        
        # Replace first occurrence only
        new_content = content.replace(old_str, new_str, 1)
        full_path.write_text(new_content)
    
    def insert(self, path: str, insert_line: int, insert_text: str):
        """
        Insert text at specific line number.
        
        Args:
            path: Path relative to memory_dir
            insert_line: Line number to insert at (1-indexed)
            insert_text: Text to insert
        
        Examples:
            insert("/memories/todo.txt", 2, "- New task\n")
        """
        normalized_path = path.lstrip('/')
        full_path = self.memory_dir / normalized_path
        
        # Security check
        try:
            full_path = full_path.resolve()
            full_path.relative_to(self.memory_dir.resolve())
        except ValueError:
            raise PermissionError(f"Path traversal detected: {path}")
        
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        lines = full_path.read_text().splitlines(keepends=True)
        
        # Insert at line (1-indexed)
        lines.insert(insert_line - 1, insert_text)
        
        full_path.write_text(''.join(lines))
    
    def delete(self, path: str):
        """
        Delete file or directory.
        
        Args:
            path: Path relative to memory_dir
        
        Examples:
            delete("/memories/old_file.txt")
        """
        normalized_path = path.lstrip('/')
        full_path = self.memory_dir / normalized_path
        
        # Security check
        try:
            full_path = full_path.resolve()
            full_path.relative_to(self.memory_dir.resolve())
        except ValueError:
            raise PermissionError(f"Path traversal detected: {path}")
        
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        if full_path.is_dir():
            import shutil
            shutil.rmtree(full_path)
        else:
            full_path.unlink()
    
    def rename(self, old_path: str, new_path: str):
        """
        Rename or move file/directory.
        
        Args:
            old_path: Current path relative to memory_dir
            new_path: New path relative to memory_dir
        
        Examples:
            rename("/memories/draft.txt", "/memories/final.txt")
        """
        old_normalized = old_path.lstrip('/')
        new_normalized = new_path.lstrip('/')
        
        old_full = self.memory_dir / old_normalized
        new_full = self.memory_dir / new_normalized
        
        # Security check both paths
        try:
            old_full = old_full.resolve()
            old_full.relative_to(self.memory_dir.resolve())
            
            # For new path, check parent exists and is safe
            new_full.parent.mkdir(parents=True, exist_ok=True)
            new_full = new_full.resolve()
            new_full.relative_to(self.memory_dir.resolve())
        except ValueError:
            raise PermissionError(f"Path traversal detected")
        
        if not old_full.exists():
            raise FileNotFoundError(f"File not found: {old_path}")
        
        old_full.rename(new_full)


# Backward compatibility with existing code
def create_memory_adapter(memory_dir: str = "/home/kc-palantir/math/memories") -> MemoryAdapter:
    """Factory function for easy memory adapter creation."""
    return MemoryAdapter(Path(memory_dir))

