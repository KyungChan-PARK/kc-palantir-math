"""
Agent File Criticality Configuration

Criticality Scale:
- 10: Mission-critical (system failure if broken)
- 7-9: Core components (major functionality affected)
- 4-6: Standard components (feature-specific impact)
- 1-3: Low-risk (documentation, examples, configs)
"""

from pathlib import Path
import fnmatch
from typing import Dict, List

AGENT_CRITICALITY: Dict[str, int] = {
    # Mission-critical infrastructure
    "agents/meta_orchestrator.py": 10,
    "agents/improvement_models.py": 10,
    "main.py": 10,

    # Core agents
    "agents/relationship_definer.py": 9,
    "agents/self_improver_agent.py": 9,
    "agents/socratic_mediator_agent.py": 8,
    "agents/knowledge_builder.py": 8,

    # Standard agents
    "agents/research_agent.py": 6,
    "agents/quality_agent.py": 7,
    "agents/dependency_agent.py": 6,

    # Support modules
    "agents/example_generator.py": 4,
    "config.py": 5,
    "tools/*.py": 3,

    # Low-risk
    "docs/*.md": 1,
    "tests/*.py": 2,
    "examples/*.json": 1,
}

def get_criticality_score(file_path: str) -> int:
    """
    Calculate criticality score for a file.

    Args:
        file_path: Path to file (relative or absolute)

    Returns:
        Criticality score (1-10)
    """
    try:
        file_path = str(Path(file_path).relative_to(Path.cwd()))
    except ValueError:
        # If path is already relative or cannot be made relative, use as is
        file_path = str(Path(file_path))

    # Exact match
    if file_path in AGENT_CRITICALITY:
        return AGENT_CRITICALITY[file_path]

    # Pattern match (glob)
    for pattern, score in AGENT_CRITICALITY.items():
        if fnmatch.fnmatch(file_path, pattern):
            return score

    # Default: medium criticality
    return 5

def calculate_dynamic_thresholds(
    affected_files: List[str]
) -> Dict[str, float]:
    """
    Calculate dynamic quality gate thresholds.

    Args:
        affected_files: List of file paths being modified

    Returns:
        Dictionary with thresholds
    """
    if not affected_files:
        # No files: use defaults
        return {
            "cis_threshold": 20,
            "coverage_threshold": 0.80,
            "verification_rounds": 1
        }

    # Calculate weighted average criticality
    scores = [get_criticality_score(f) for f in affected_files]
    avg_criticality = sum(scores) / len(scores)
    max_criticality = max(scores)

    # Dynamic thresholds (inverse relationship)
    # Higher criticality → stricter thresholds
    cis_threshold = max(5, 30 - (avg_criticality * 1.5))
    coverage_threshold = min(0.95, 0.65 + (avg_criticality * 0.03))

    # Verification rounds based on max criticality
    if max_criticality >= 9:
        verification_rounds = 2
    else:
        verification_rounds = 1

    return {
        "cis_threshold": cis_threshold,
        "coverage_threshold": coverage_threshold,
        "verification_rounds": verification_rounds,
        "avg_criticality": avg_criticality,
        "max_criticality": max_criticality
    }
