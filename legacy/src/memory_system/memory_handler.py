#!/usr/bin/env python3
"""
Memory Tool Handler for Palantir Math Education System
Provides secure, persistent memory storage across Claude sessions
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import re


class MemoryHandler:
    """
    Secure memory file handler with path traversal protection
    and size limits for the Palantir Ontology system
    """

    def __init__(self, base_path: str = ".claude/memories"):
        """
        Initialize memory handler

        Args:
            base_path: Base directory for memory files (relative to project root)
        """
        self.project_root = Path("/home/kc-palantir/math").resolve()
        self.memories_dir = (self.project_root / base_path).resolve()
        self.max_file_size = 1024 * 1024  # 1MB per file
        self.max_read_chars = 100000  # 100K characters per read

        # Ensure memories directory exists
        self.memories_dir.mkdir(parents=True, exist_ok=True)

    def _validate_path(self, path: str) -> Path:
        """
        Validate and resolve path to prevent directory traversal attacks

        Args:
            path: Requested file path

        Returns:
            Resolved, validated Path object

        Raises:
            ValueError: If path is invalid or outside memories directory
        """
        # Remove leading slash if present
        if path.startswith('/'):
            path = path[1:]

        # Remove 'memories/' prefix if present (for compatibility)
        if path.startswith('memories/'):
            path = path[9:]

        # Resolve full path
        full_path = (self.memories_dir / path).resolve()

        # Ensure path is within memories directory
        try:
            full_path.relative_to(self.memories_dir)
        except ValueError:
            raise ValueError(f"Path traversal detected: {path}")

        # Check for suspicious patterns
        suspicious = ['..', '%2e%2e', '..\\', '.%2f', '%00']
        if any(pattern in path.lower() for pattern in suspicious):
            raise ValueError(f"Suspicious path pattern: {path}")

        return full_path

    def _check_file_size(self, file_path: Path) -> None:
        """Check if file size is within limits"""
        if file_path.exists():
            size = file_path.stat().st_size
            if size > self.max_file_size:
                raise ValueError(f"File too large: {size} bytes (max {self.max_file_size})")

    def _sanitize_content(self, content: str) -> str:
        """
        Remove potentially sensitive information from content

        Args:
            content: Text content to sanitize

        Returns:
            Sanitized content
        """
        # Patterns for sensitive data (basic filtering)
        patterns = [
            (r'api[_-]?key["\s:=]+[\w-]+', '[API_KEY_REDACTED]'),
            (r'password["\s:=]+\S+', '[PASSWORD_REDACTED]'),
            (r'secret["\s:=]+\S+', '[SECRET_REDACTED]'),
        ]

        sanitized = content
        for pattern, replacement in patterns:
            sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)

        return sanitized

    def view(self, path: str, view_range: Optional[List[int]] = None) -> Dict[str, Any]:
        """
        View directory contents or file contents

        Args:
            path: Path to view (file or directory)
            view_range: Optional [start_line, end_line] for viewing specific lines

        Returns:
            Dict with status and content/listing
        """
        try:
            full_path = self._validate_path(path)

            if full_path.is_dir():
                # List directory contents
                items = []
                for item in sorted(full_path.iterdir()):
                    rel_path = item.relative_to(self.memories_dir)
                    if item.is_dir():
                        items.append(f"[DIR]  {rel_path}/")
                    else:
                        size = item.stat().st_size
                        items.append(f"[FILE] {rel_path} ({size} bytes)")

                return {
                    "status": "success",
                    "type": "directory",
                    "content": f"Directory: {path}\n" + "\n".join(items) if items else "(empty)"
                }

            elif full_path.is_file():
                # Read file contents
                self._check_file_size(full_path)

                with open(full_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                # Apply view range if specified
                if view_range:
                    start, end = view_range
                    lines = lines[start-1:end]  # 1-indexed to 0-indexed

                content = ''.join(lines)

                # Truncate if too long
                if len(content) > self.max_read_chars:
                    content = content[:self.max_read_chars] + f"\n... (truncated, {len(content) - self.max_read_chars} chars omitted)"

                return {
                    "status": "success",
                    "type": "file",
                    "content": content,
                    "lines": len(lines)
                }

            else:
                return {
                    "status": "error",
                    "error": f"Path does not exist: {path}"
                }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def create(self, path: str, file_text: str) -> Dict[str, Any]:
        """
        Create or overwrite a file

        Args:
            path: File path to create
            file_text: Content to write

        Returns:
            Dict with status
        """
        try:
            full_path = self._validate_path(path)

            # Don't allow creating directories with this method
            if full_path.suffix == '':
                return {
                    "status": "error",
                    "error": "Path must include file extension"
                }

            # Sanitize content
            sanitized_text = self._sanitize_content(file_text)

            # Check size before writing
            if len(sanitized_text.encode('utf-8')) > self.max_file_size:
                return {
                    "status": "error",
                    "error": f"Content too large (max {self.max_file_size} bytes)"
                }

            # Create parent directories if needed
            full_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(sanitized_text)

            return {
                "status": "success",
                "message": f"Created/updated: {path}",
                "bytes_written": len(sanitized_text.encode('utf-8'))
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def str_replace(self, path: str, old_str: str, new_str: str) -> Dict[str, Any]:
        """
        Replace text in a file

        Args:
            path: File path
            old_str: String to replace
            new_str: Replacement string

        Returns:
            Dict with status
        """
        try:
            full_path = self._validate_path(path)

            if not full_path.is_file():
                return {
                    "status": "error",
                    "error": f"File not found: {path}"
                }

            self._check_file_size(full_path)

            # Read file
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if old_str exists
            if old_str not in content:
                return {
                    "status": "error",
                    "error": f"String not found in file: {old_str[:50]}..."
                }

            # Replace
            new_content = content.replace(old_str, new_str, 1)  # Replace only first occurrence

            # Sanitize and write
            sanitized = self._sanitize_content(new_content)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(sanitized)

            return {
                "status": "success",
                "message": f"Replaced text in: {path}",
                "replacements": 1
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def insert(self, path: str, insert_line: int, insert_text: str) -> Dict[str, Any]:
        """
        Insert text at a specific line

        Args:
            path: File path
            insert_line: Line number to insert at (1-indexed)
            insert_text: Text to insert

        Returns:
            Dict with status
        """
        try:
            full_path = self._validate_path(path)

            if not full_path.is_file():
                return {
                    "status": "error",
                    "error": f"File not found: {path}"
                }

            self._check_file_size(full_path)

            # Read file
            with open(full_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Insert text
            if insert_line < 1 or insert_line > len(lines) + 1:
                return {
                    "status": "error",
                    "error": f"Invalid line number: {insert_line} (file has {len(lines)} lines)"
                }

            lines.insert(insert_line - 1, insert_text)

            # Sanitize and write
            new_content = ''.join(lines)
            sanitized = self._sanitize_content(new_content)

            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(sanitized)

            return {
                "status": "success",
                "message": f"Inserted text at line {insert_line} in: {path}"
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def delete(self, path: str) -> Dict[str, Any]:
        """
        Delete a file or directory

        Args:
            path: Path to delete

        Returns:
            Dict with status
        """
        try:
            full_path = self._validate_path(path)

            if not full_path.exists():
                return {
                    "status": "error",
                    "error": f"Path not found: {path}"
                }

            if full_path.is_dir():
                # Remove directory and contents
                import shutil
                shutil.rmtree(full_path)
                return {
                    "status": "success",
                    "message": f"Deleted directory: {path}"
                }
            else:
                # Remove file
                full_path.unlink()
                return {
                    "status": "success",
                    "message": f"Deleted file: {path}"
                }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def rename(self, old_path: str, new_path: str) -> Dict[str, Any]:
        """
        Rename or move a file/directory

        Args:
            old_path: Current path
            new_path: New path

        Returns:
            Dict with status
        """
        try:
            full_old_path = self._validate_path(old_path)
            full_new_path = self._validate_path(new_path)

            if not full_old_path.exists():
                return {
                    "status": "error",
                    "error": f"Source path not found: {old_path}"
                }

            if full_new_path.exists():
                return {
                    "status": "error",
                    "error": f"Destination already exists: {new_path}"
                }

            # Create parent directory if needed
            full_new_path.parent.mkdir(parents=True, exist_ok=True)

            # Rename/move
            full_old_path.rename(full_new_path)

            return {
                "status": "success",
                "message": f"Renamed: {old_path} → {new_path}"
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def execute_command(self, command_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a memory tool command

        Args:
            command_data: Command dictionary with 'command' key and parameters

        Returns:
            Result dictionary
        """
        command = command_data.get('command')

        if command == 'view':
            return self.view(
                command_data['path'],
                command_data.get('view_range')
            )
        elif command == 'create':
            return self.create(
                command_data['path'],
                command_data['file_text']
            )
        elif command == 'str_replace':
            return self.str_replace(
                command_data['path'],
                command_data['old_str'],
                command_data['new_str']
            )
        elif command == 'insert':
            return self.insert(
                command_data['path'],
                command_data['insert_line'],
                command_data['insert_text']
            )
        elif command == 'delete':
            return self.delete(command_data['path'])
        elif command == 'rename':
            return self.rename(
                command_data['old_path'],
                command_data['new_path']
            )
        else:
            return {
                "status": "error",
                "error": f"Unknown command: {command}"
            }


# Singleton instance
_memory_handler = None

def get_memory_handler() -> MemoryHandler:
    """Get or create the global memory handler instance"""
    global _memory_handler
    if _memory_handler is None:
        _memory_handler = MemoryHandler()
    return _memory_handler


if __name__ == "__main__":
    # Test the memory handler
    handler = get_memory_handler()

    # Test view (should show empty or existing structure)
    print("Testing view:", handler.view(""))

    # Test create
    print("\nTesting create:", handler.create(
        "test/hello.txt",
        "Hello from memory system!\nTimestamp: " + datetime.now().isoformat()
    ))

    # Test view file
    print("\nTesting view file:", handler.view("test/hello.txt"))

    # Test str_replace
    print("\nTesting str_replace:", handler.str_replace(
        "test/hello.txt",
        "Hello",
        "Greetings"
    ))

    # Test insert
    print("\nTesting insert:", handler.insert(
        "test/hello.txt",
        2,
        "This line was inserted!\n"
    ))

    # View result
    print("\nFinal content:", handler.view("test/hello.txt"))
