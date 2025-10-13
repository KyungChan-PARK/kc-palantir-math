"""
Dependency Agent - AST-based Static Analysis

VERSION: 4.0.0
DATE: 2025-10-14
PURPOSE: Replace conceptual dependency-mapper with code-level dependency analysis

Based on: SELF-IMPROVEMENT-IMPLEMENTATION-PLAN-v4.0.md Section II

Core Features:
1. AST parsing of Python codebase
2. Dependency graph construction (NetworkX)
3. Graph caching (Pickle + Git commit versioning)
4. Bidirectional dependency traversal
5. Change Impact Analysis (CIA) protocol
"""

import ast
import networkx as nx
import pickle
from pathlib import Path
from typing import Dict, List, Set, Optional
import subprocess
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Data Structures (from v4.0 plan)
# ============================================================================

class NodeType(Enum):
    """Node types in dependency graph"""
    MODULE = "module"
    CLASS = "class"
    FUNCTION = "function"


class EdgeType(Enum):
    """Edge types representing different dependency relationships"""
    IMPORTS = "imports"
    DEFINES = "defines"
    CALLS = "calls"
    INHERITS_FROM = "inherits_from"


@dataclass
class DependencyNode:
    """Node attributes in dependency graph"""
    node_id: str  # e.g., "agents.meta_orchestrator.MetaOrchestrator.execute_task"
    node_type: NodeType
    file_path: str
    start_line: int
    end_line: int
    signature: str  # For functions: full signature
    docstring_summary: Optional[str] = None
    is_critical: bool = False  # Mission-critical flag


@dataclass
class DependencyEdge:
    """Edge attributes in dependency graph"""
    source: str  # node_id
    target: str  # node_id
    edge_type: EdgeType
    line_number: int  # Where dependency occurs
    is_conditional: bool = False  # Inside if/try block
    call_frequency: Optional[float] = None  # For future dynamic analysis


# ============================================================================
# AST Visitor (from v4.0 plan lines 108-221)
# ============================================================================

class DependencyVisitor(ast.NodeVisitor):
    """
    AST visitor to extract dependency relationships.

    Traverses Python AST and builds dependency graph edges:
    - IMPORTS: module imports
    - DEFINES: class/function definitions
    - CALLS: function calls
    - INHERITS_FROM: class inheritance
    """

    def __init__(self, graph: nx.DiGraph, file_path: str):
        self.graph = graph
        self.file_path = file_path
        self.current_module = None
        self.current_class = None
        self.current_function = None

    def visit_Import(self, node: ast.Import):
        """Handle: import module"""
        for alias in node.names:
            module_name = alias.name
            if self.current_module:
                self.graph.add_edge(
                    self.current_module,
                    module_name,
                    edge_type=EdgeType.IMPORTS,
                    line_number=node.lineno
                )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Handle: from module import name"""
        if node.module:
            for alias in node.names:
                imported = f"{node.module}.{alias.name}"
                if self.current_module:
                    self.graph.add_edge(
                        self.current_module,
                        imported,
                        edge_type=EdgeType.IMPORTS,
                        line_number=node.lineno
                    )
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Handle: def function_name(...)"""
        func_id = f"{self.current_module}.{node.name}"
        if self.current_class:
            func_id = f"{self.current_class}.{node.name}"

        # Add function node
        self.graph.add_node(
            func_id,
            node_type=NodeType.FUNCTION,
            file_path=self.file_path,
            start_line=node.lineno,
            end_line=node.end_lineno or node.lineno,
            signature=ast.unparse(node.args) if hasattr(ast, 'unparse') else str(node.args),
            docstring_summary=ast.get_docstring(node)
        )

        # Add DEFINES edge
        parent = self.current_class or self.current_module
        if parent:
            self.graph.add_edge(
                parent,
                func_id,
                edge_type=EdgeType.DEFINES,
                line_number=node.lineno
            )

        # Visit function body for CALLS edges
        old_func = self.current_function
        self.current_function = func_id
        self.generic_visit(node)
        self.current_function = old_func

    def visit_Call(self, node: ast.Call):
        """Handle: function_call()"""
        callee = "unknown"

        if isinstance(node.func, ast.Name):
            callee = node.func.id
        elif isinstance(node.func, ast.Attribute):
            if hasattr(ast, 'unparse'):
                callee = ast.unparse(node.func)
            else:
                callee = f"{node.func.attr}"

        if self.current_function and callee != "unknown":
            self.graph.add_edge(
                self.current_function,
                callee,
                edge_type=EdgeType.CALLS,
                line_number=node.lineno
            )

        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        """Handle: class ClassName"""
        class_id = f"{self.current_module}.{node.name}"

        self.graph.add_node(
            class_id,
            node_type=NodeType.CLASS,
            file_path=self.file_path,
            start_line=node.lineno,
            end_line=node.end_lineno or node.lineno
        )

        # Handle inheritance
        for base in node.bases:
            base_class = "unknown"
            if isinstance(base, ast.Name):
                base_class = base.id
            elif isinstance(base, ast.Attribute):
                if hasattr(ast, 'unparse'):
                    base_class = ast.unparse(base)

            if base_class != "unknown":
                self.graph.add_edge(
                    class_id,
                    base_class,
                    edge_type=EdgeType.INHERITS_FROM,
                    line_number=node.lineno
                )

        # Visit class body
        old_class = self.current_class
        self.current_class = class_id
        self.generic_visit(node)
        self.current_class = old_class


# ============================================================================
# Dependency Agent (from v4.0 plan lines 223-503)
# ============================================================================

class DependencyAgent:
    """
    AST-based dependency analysis with graph caching.

    Replaces conceptual dependency-mapper with code-level analysis.
    Implements Change Impact Analysis (CIA) protocol from v4.0 spec.

    PDF specification: Build graph once, cache for repeated queries.
    Cost: O(n files) initially, O(1) for subsequent queries.
    """

    def __init__(self, project_root: str = "/home/kc-palantir/math"):
        self.project_root = Path(project_root)
        self.graph = nx.DiGraph()
        self.cache_path = Path("/tmp/dependency_graph_cache.pkl")
        self.last_scan_commit = None

        # Mission-critical agents (PDF specification)
        self.critical_components = {
            "knowledge-builder",
            "quality-agent",
            "meta-orchestrator"
        }

    def _get_git_commit_hash(self) -> str:
        """Get current Git commit hash for version tracking"""
        try:
            result = subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=self.project_root,
                stderr=subprocess.DEVNULL
            )
            return result.decode().strip()
        except:
            return "no-git"

    def _cache_exists(self) -> bool:
        """Check if cache file exists"""
        return self.cache_path.exists()

    def _load_from_cache(self) -> nx.DiGraph:
        """Load graph from pickle cache"""
        with open(self.cache_path, 'rb') as f:
            data = pickle.load(f)
            self.graph = data['graph']
            self.last_scan_commit = data['commit']
        return self.graph

    def _save_to_cache(self):
        """Save graph to pickle cache"""
        data = {
            'graph': self.graph,
            'commit': self.last_scan_commit
        }
        with open(self.cache_path, 'wb') as f:
            pickle.dump(data, f)

    def build_and_cache_graph(self) -> nx.DiGraph:
        """
        Build dependency graph from AST parsing, cache result.

        PDF specification: Run once at system start, cache for repeated queries.
        Cost: O(n files) initially, O(1) for subsequent queries.

        Returns:
            NetworkX DiGraph with nodes and edges representing code dependencies
        """
        current_commit = self._get_git_commit_hash()

        # Check cache validity
        if (self.last_scan_commit == current_commit and
            self._cache_exists()):
            print("Loading dependency graph from cache...")
            return self._load_from_cache()

        print("Building dependency graph from AST parsing...")
        self.graph.clear()

        # Parse all Python files
        py_files = list(self.project_root.glob("**/*.py"))
        for py_file in py_files:
            # Skip test files and venv
            if "test" in str(py_file) or ".venv" in str(py_file):
                continue

            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    source = f.read()

                tree = ast.parse(source, filename=str(py_file))

                # Extract module name
                module_path = py_file.relative_to(self.project_root)
                module_name = str(module_path).replace('/', '.').replace('.py', '')

                # Add module node
                self.graph.add_node(
                    module_name,
                    node_type=NodeType.MODULE,
                    file_path=str(py_file)
                )

                # Visit AST
                visitor = DependencyVisitor(self.graph, str(py_file))
                visitor.current_module = module_name
                visitor.visit(tree)

            except Exception as e:
                print(f"Warning: Failed to parse {py_file}: {e}")

        # Mark critical components
        for node in self.graph.nodes():
            agent_name = node.split('.')[0] if '.' in node else node
            if agent_name in self.critical_components:
                self.graph.nodes[node]['is_critical'] = True

        # Cache the result
        self.last_scan_commit = current_commit
        self._save_to_cache()

        print(f"Graph built: {self.graph.number_of_nodes()} nodes, "
              f"{self.graph.number_of_edges()} edges")

        return self.graph

    def get_dependents(self, node_id: str, depth: int = 2) -> List[str]:
        """
        Get all nodes that depend on this node (incoming edges).

        "Who calls this?"

        Args:
            node_id: Node identifier in graph
            depth: Maximum traversal depth

        Returns:
            List of node IDs that depend on the given node
        """
        if node_id not in self.graph:
            return []

        dependents = set()
        queue = [(node_id, 0)]
        visited = {node_id}

        while queue:
            current, d = queue.pop(0)
            if d >= depth:
                continue

            # Get predecessors (nodes with edges pointing to current)
            for pred in self.graph.predecessors(current):
                if pred not in visited:
                    visited.add(pred)
                    dependents.add(pred)
                    queue.append((pred, d + 1))

        return list(dependents)

    def get_dependencies(self, node_id: str, depth: int = 2) -> List[str]:
        """
        Get all nodes this node depends on (outgoing edges).

        "What does this call?"

        Args:
            node_id: Node identifier in graph
            depth: Maximum traversal depth

        Returns:
            List of node IDs that the given node depends on
        """
        if node_id not in self.graph:
            return []

        dependencies = set()
        queue = [(node_id, 0)]
        visited = {node_id}

        while queue:
            current, d = queue.pop(0)
            if d >= depth:
                continue

            # Get successors (nodes current points to)
            for succ in self.graph.successors(current):
                if succ not in visited:
                    visited.add(succ)
                    dependencies.add(succ)
                    queue.append((succ, d + 1))

        return list(dependencies)

    def get_impact_set(self, start_nodes: List[str], depth: int = 2) -> List[DependencyNode]:
        """
        Generate Candidate Impact Set (CIS) via bidirectional traversal.

        Academic specification: SIS → CIS generation.

        Args:
            start_nodes: Starting Impact Set (SIS) - nodes being modified
            depth: Traversal depth for impact analysis

        Returns:
            List of DependencyNode objects in Candidate Impact Set
        """
        cis_node_ids = set()

        for node_id in start_nodes:
            # Bidirectional traversal
            dependents = self.get_dependents(node_id, depth)
            dependencies = self.get_dependencies(node_id, depth)

            cis_node_ids.update(dependents)
            cis_node_ids.update(dependencies)

        # Remove original nodes
        cis_node_ids -= set(start_nodes)

        # Convert to DependencyNode objects
        cis_nodes = []
        for node_id in cis_node_ids:
            if node_id in self.graph:
                node_data = self.graph.nodes[node_id]
                cis_nodes.append(DependencyNode(
                    node_id=node_id,
                    node_type=node_data.get('node_type', NodeType.MODULE),
                    file_path=node_data.get('file_path', ''),
                    start_line=node_data.get('start_line', 0),
                    end_line=node_data.get('end_line', 0),
                    signature=node_data.get('signature', ''),
                    docstring_summary=node_data.get('docstring_summary'),
                    is_critical=node_data.get('is_critical', False)
                ))

        return cis_nodes

    def perform_dependency_analysis(
        self,
        proposed_changes: List
    ):
        """
        PDF specification: Use cached graph to analyze impact.

        Returns ImpactAnalysis with CIS, metrics, and critical flag.

        Args:
            proposed_changes: List of ImprovementAction objects

        Returns:
            ImpactAnalysis object with SIS, CIS, metrics
        """
        # Load cached graph
        if not self._cache_exists():
            self.build_and_cache_graph()
        else:
            self._load_from_cache()

        # Extract SIS (Starting Impact Set)
        sis_nodes = []
        for action in proposed_changes:
            target = action.target_agent
            # Normalize to module name
            if '.' not in target:
                target = f"agents.{target}"
            sis_nodes.append(target)

        # Generate CIS
        cis_nodes = self.get_impact_set(sis_nodes, depth=2)

        # Calculate metrics
        cis_size = len(cis_nodes)
        critical_affected = any(node.is_critical for node in cis_nodes)

        # Estimate test coverage (placeholder - requires test suite analysis)
        test_coverage = 0.85  # Default assumption

        # Generate impact report
        impact_report = self._generate_impact_report(sis_nodes, cis_nodes)

        # Import here to avoid circular dependency
        from agents.improvement_models import ImpactAnalysis
        return ImpactAnalysis(
            sis=sis_nodes,
            cis=[n.node_id for n in cis_nodes],
            cis_size=cis_size,
            critical_affected=critical_affected,
            test_coverage=test_coverage,
            impact_report=impact_report
        )

    def _generate_impact_report(
        self,
        sis: List[str],
        cis: List[DependencyNode]
    ) -> str:
        """Generate human-readable impact analysis report"""
        report = "# Impact Analysis Report\n\n"
        report += "## Starting Impact Set (SIS)\n"
        for node in sis:
            report += f"- {node}\n"
        report += f"\n## Candidate Impact Set (CIS) - {len(cis)} nodes\n"

        # Group by criticality
        critical_nodes = [n for n in cis if n.is_critical]
        non_critical_nodes = [n for n in cis if not n.is_critical]

        if critical_nodes:
            report += "\n### ⚠️ Critical Components Affected\n"
            for node in critical_nodes:
                report += f"- {node.node_id} ({node.file_path})\n"

        if non_critical_nodes:
            report += "\n### Standard Components\n"
            for node in non_critical_nodes[:10]:  # Limit to first 10
                report += f"- {node.node_id}\n"
            if len(non_critical_nodes) > 10:
                report += f"- ... and {len(non_critical_nodes) - 10} more\n"

        return report
