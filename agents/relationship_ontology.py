"""
Formal Relationship Ontology

Based on OntoClean methodology and Math-KG research.
Defines logical properties of each relationship type.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Set, Optional

class RelationType(Enum):
    """12 relationship types from v0.2 taxonomy"""
    PREREQUISITE = "prerequisite"
    CO_REQUISITE = "co-requisite"
    INVERSE_OPERATION = "inverse-operation"
    EXTENSION = "extension"
    FORMALIZATION = "formalization"
    APPLICATION = "application"
    MUTUAL_DEFINITION = "mutual-definition"
    ABSTRACTION_LEVEL = "abstraction-level"
    COMPLEMENTARY = "complementary"
    SYNONYMS = "synonyms-notation"
    DOMAIN_MEMBERSHIP = "domain-membership"
    EQUIVALENCE = "equivalence"

@dataclass
class FormalProperties:
    """Formal logical properties of a relationship type"""
    transitive: bool  # A→B, B→C implies A→C
    symmetric: bool  # A→B implies B→A
    reflexive: bool  # A→A is valid
    anti_symmetric: bool  # A→B and B→A implies A=B
    acyclic: bool  # No cycles allowed (A→...→A)

# Ontology specification
RELATIONSHIP_ONTOLOGY: Dict[RelationType, FormalProperties] = {
    RelationType.PREREQUISITE: FormalProperties(
        transitive=True,  # A→B→C implies A→C (with strength decay)
        symmetric=False,
        reflexive=False,  # Concept is not its own prerequisite
        anti_symmetric=True,
        acyclic=True  # CRITICAL: No circular prerequisites
    ),

    RelationType.CO_REQUISITE: FormalProperties(
        transitive=False,  # A+B, B+C doesn't imply A+C
        symmetric=True,  # A+B implies B+A
        reflexive=False,
        anti_symmetric=False,
        acyclic=False
    ),

    RelationType.INVERSE_OPERATION: FormalProperties(
        transitive=False,
        symmetric=True,  # Inverse is symmetric
        reflexive=False,
        anti_symmetric=False,
        acyclic=False
    ),

    RelationType.EXTENSION: FormalProperties(
        transitive=True,  # A extends B extends C
        symmetric=False,
        reflexive=False,
        anti_symmetric=True,
        acyclic=True
    ),

    RelationType.FORMALIZATION: FormalProperties(
        transitive=True,  # A formalizes B formalizes C
        symmetric=False,
        reflexive=False,
        anti_symmetric=True,
        acyclic=True
    ),

    RelationType.APPLICATION: FormalProperties(
        transitive=False,  # A applies to B applies to C doesn't imply A→C
        symmetric=False,
        reflexive=False,
        anti_symmetric=False,
        acyclic=False
    ),

    RelationType.MUTUAL_DEFINITION: FormalProperties(
        transitive=False,  # A⇄B, B⇄C doesn't imply A⇄C
        symmetric=True,
        reflexive=False,
        anti_symmetric=False,
        acyclic=False
    ),

    RelationType.ABSTRACTION_LEVEL: FormalProperties(
        transitive=True,  # Abstraction levels form hierarchy
        symmetric=False,
        reflexive=False,
        anti_symmetric=True,
        acyclic=True
    ),

    RelationType.COMPLEMENTARY: FormalProperties(
        transitive=False,
        symmetric=True,  # If A complements B, B complements A
        reflexive=False,
        anti_symmetric=False,
        acyclic=False
    ),

    RelationType.SYNONYMS: FormalProperties(
        transitive=True,  # Synonym relationship is equivalence
        symmetric=True,
        reflexive=True,  # A is synonym of itself
        anti_symmetric=False,
        acyclic=False
    ),

    RelationType.DOMAIN_MEMBERSHIP: FormalProperties(
        transitive=False,  # Concept belongs to domain, but not transitive
        symmetric=False,
        reflexive=False,
        anti_symmetric=False,
        acyclic=False
    ),

    RelationType.EQUIVALENCE: FormalProperties(
        transitive=True,
        symmetric=True,
        reflexive=True,  # Everything equivalent to itself
        anti_symmetric=False,
        acyclic=False
    ),
}

class ValidationError:
    """Validation error with severity"""
    def __init__(
        self,
        severity: str,  # "ERROR" | "WARNING"
        check: str,
        message: str,
        suggestion: Optional[str] = None
    ):
        self.severity = severity
        self.check = check
        self.message = message
        self.suggestion = suggestion

    def __str__(self):
        s = f"[{self.severity}] {self.check}: {self.message}"
        if self.suggestion:
            s += f"\n  Suggestion: {self.suggestion}"
        return s

def validate_relationship_logic(
    rel_type: RelationType,
    source_id: str,
    target_id: str,
    existing_graph: Optional[Dict] = None
) -> List[ValidationError]:
    """
    Validate relationship against ontology rules.

    Args:
        rel_type: Relationship type
        source_id: Source concept ID
        target_id: Target concept ID
        existing_graph: Current knowledge graph (for cycle detection)

    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    props = RELATIONSHIP_ONTOLOGY.get(rel_type)

    if not props:
        errors.append(ValidationError(
            "ERROR",
            "unknown_type",
            f"Relationship type {rel_type} not in ontology"
        ))
        return errors

    # Check 1: Reflexivity
    if source_id == target_id:
        if not props.reflexive:
            errors.append(ValidationError(
                "ERROR",
                "reflexive_violation",
                f"{rel_type.value} is not reflexive, but source==target",
                f"Remove self-relation or use a reflexive type like {RelationType.EQUIVALENCE.value}"
            ))
        # If reflexive is allowed, this is OK

    # Check 2: Acyclic constraint
    if props.acyclic and existing_graph:
        if creates_cycle(source_id, target_id, rel_type, existing_graph):
            errors.append(ValidationError(
                "ERROR",
                "circular_dependency",
                f"Adding {source_id}→{target_id} creates a cycle in {rel_type.value}",
                "Review the dependency chain and break the cycle"
            ))

    # Check 3: Symmetry consistency
    if props.symmetric and existing_graph:
        reverse_rel = find_relation(target_id, source_id, rel_type, existing_graph)
        if not reverse_rel:
            errors.append(ValidationError(
                "WARNING",
                "symmetry_incomplete",
                f"{rel_type.value} is symmetric, but reverse {target_id}→{source_id} missing",
                "Add the reverse relationship"
            ))

    return errors

def creates_cycle(
    source_id: str,
    target_id: str,
    rel_type: RelationType,
    graph: Dict
) -> bool:
    """
    Check if adding source→target would create a cycle.

    Uses DFS to detect cycles.
    """
    # Build adjacency list for this relationship type
    adjacency = {}
    for rel in graph.get('relationships', []):
        if rel['relationship']['type'] == rel_type.value:
            src = rel['source_concept_id']
            tgt = rel['target_concept_id']
            if src not in adjacency:
                adjacency[src] = []
            adjacency[src].append(tgt)

    # Check if target can reach source (would create cycle)
    visited = set()

    def dfs(node):
        if node == source_id:
            return True
        if node in visited:
            return False
        visited.add(node)
        for neighbor in adjacency.get(node, []):
            if dfs(neighbor):
                return True
        return False

    return dfs(target_id)

def find_relation(
    source_id: str,
    target_id: str,
    rel_type: RelationType,
    graph: Dict
) -> Optional[Dict]:
    """Find a specific relationship in the graph"""
    for rel in graph.get('relationships', []):
        if (rel['source_concept_id'] == source_id and
            rel['target_concept_id'] == target_id and
            rel['relationship']['type'] == rel_type.value):
            return rel
    return None
