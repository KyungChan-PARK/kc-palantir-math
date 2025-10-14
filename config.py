"""
Project Configuration
Dynamic path resolution for cross-platform portability

VERSION: 1.0.0
"""

from pathlib import Path
from typing import Optional


def find_project_root(marker_files: tuple = ("pyproject.toml", ".git")) -> Path:
    """
    Find project root by searching for marker files/directories.

    Args:
        marker_files: Files/directories that indicate project root

    Returns:
        Path to project root

    Raises:
        RuntimeError: If project root cannot be found
    """
    current = Path(__file__).resolve().parent

    # Check current directory and all parents
    for parent in [current] + list(current.parents):
        if any((parent / marker).exists() for marker in marker_files):
            return parent

    raise RuntimeError(
        f"Could not find project root. Looking for {marker_files} "
        f"starting from {current}"
    )


# Project root
PROJECT_ROOT = find_project_root()

# Core directories
AGENTS_DIR = PROJECT_ROOT / "agents"
TESTS_DIR = PROJECT_ROOT / "tests"
TOOLS_DIR = PROJECT_ROOT / "tools"

# Output directories
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
DEPENDENCY_MAP_DIR = OUTPUTS_DIR / "dependency-map"
RESEARCH_REPORTS_DIR = OUTPUTS_DIR / "research-reports"

# Math vault - prefer Windows-accessible path for Obsidian compatibility
WINDOWS_OBSIDIAN_PATH = Path("/mnt/c/Users/packr/Documents/obsidian-vault/Math")
if WINDOWS_OBSIDIAN_PATH.exists():
    MATH_VAULT_DIR = WINDOWS_OBSIDIAN_PATH
else:
    MATH_VAULT_DIR = PROJECT_ROOT / "math-vault"

# Memory directories
CLAUDE_DIR = PROJECT_ROOT / ".claude"
MEMORIES_DIR = CLAUDE_DIR / "memories"
PHASE_PROGRESS_DIR = MEMORIES_DIR / "phase-progress"

# Cache files
DEPENDENCY_CACHE_FILE = PROJECT_ROOT / ".dependency_cache.pkl"


def ensure_directories() -> None:
    """Create all required output directories if they don't exist."""
    dirs_to_create = [
        TESTS_DIR,
        TOOLS_DIR,
        OUTPUTS_DIR,
        DEPENDENCY_MAP_DIR,
        RESEARCH_REPORTS_DIR,
        MATH_VAULT_DIR,
        MEMORIES_DIR,
        PHASE_PROGRESS_DIR,
    ]

    for directory in dirs_to_create:
        directory.mkdir(parents=True, exist_ok=True)


def get_output_path(filename: str, output_type: str = "dependency-map") -> Path:
    """
    Get full path for output file.

    Args:
        filename: Name of the file
        output_type: Type of output ("dependency-map", "research-reports", "math-vault")

    Returns:
        Full path to output file
    """
    output_dirs = {
        "dependency-map": DEPENDENCY_MAP_DIR,
        "research-reports": RESEARCH_REPORTS_DIR,
        "math-vault": MATH_VAULT_DIR,
    }

    output_dir = output_dirs.get(output_type, OUTPUTS_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    return output_dir / filename


# Initialize directories on import
try:
    ensure_directories()
except Exception as e:
    # Don't fail import if directory creation fails
    # (e.g., in restricted environments)
    import warnings
    warnings.warn(f"Could not create output directories: {e}")


if __name__ == "__main__":
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Agents directory: {AGENTS_DIR}")
    print(f"Math vault: {MATH_VAULT_DIR}")
    print(f"Dependency map: {DEPENDENCY_MAP_DIR}")
    print(f"Research reports: {RESEARCH_REPORTS_DIR}")
