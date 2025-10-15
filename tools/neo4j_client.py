"""
Neo4j Client Wrapper

Provides simplified interface for Neo4j operations used by agents.

Based on:
- Neo4j Python driver
- Palantir 3-tier ontology
- Reusability patterns from Socratic clarification

VERSION: 1.0.0
DATE: 2025-10-16
"""

from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase
import os


class Neo4jConceptGraphClient:
    """
    Neo4j client for math concept graph operations.
    
    Used by neo4j-query-agent and other agents needing graph access.
    """
    
    def __init__(
        self,
        uri: str = None,
        user: str = None,
        password: str = None,
        database: str = "math_concepts"
    ):
        """Initialize Neo4j connection."""
        self.uri = uri or os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.user = user or os.getenv('NEO4J_USER', 'neo4j')
        self.password = password or os.getenv('NEO4J_PASSWORD', 'password')
        self.database = database
        
        self.driver = None
    
    def connect(self):
        """Establish connection to Neo4j."""
        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.user, self.password)
        )
    
    def close(self):
        """Close Neo4j connection."""
        if self.driver:
            self.driver.close()
    
    def __enter__(self):
        """Context manager support."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup."""
        self.close()
    
    # ========================================================================
    # Semantic Tier Operations (Static Definitions)
    # ========================================================================
    
    def create_concept(
        self,
        concept_id: str,
        name: str,
        definition: str,
        difficulty: int,
        grade_level: str,
        chapter: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Create a new concept node."""
        with self.driver.session(database=self.database) as session:
            result = session.run(
                """
                CREATE (c:Concept {
                    id: $id,
                    name: $name,
                    definition: $definition,
                    difficulty: $difficulty,
                    grade_level: $grade_level,
                    chapter: $chapter,
                    created_at: datetime()
                })
                RETURN c
                """,
                id=concept_id,
                name=name,
                definition=definition,
                difficulty=difficulty,
                grade_level=grade_level,
                chapter=chapter
            )
            
            return {"created": True, "concept_id": concept_id}
    
    def add_dependency(
        self,
        source_concept_id: str,
        target_concept_id: str,
        strength: float = 0.9
    ) -> Dict[str, Any]:
        """Add REQUIRES relationship between concepts."""
        with self.driver.session(database=self.database) as session:
            result = session.run(
                """
                MATCH (source:Concept {id: $source}),
                      (target:Concept {id: $target})
                CREATE (source)-[:REQUIRES {
                    strength: $strength,
                    validated: false,
                    created_at: datetime()
                }]->(target)
                RETURN source, target
                """,
                source=source_concept_id,
                target=target_concept_id,
                strength=strength
            )
            
            return {"added": True}
    
    def query_prerequisites(
        self,
        concept_id: str,
        max_depth: int = 5
    ) -> List[Dict[str, Any]]:
        """Query all prerequisites for a concept."""
        with self.driver.session(database=self.database) as session:
            result = session.run(
                f"""
                MATCH path = (concept:Concept {{id: $concept_id}})
                             -[:REQUIRES*1..{max_depth}]->(prereq:Concept)
                RETURN prereq.id as id,
                       prereq.name as name,
                       prereq.difficulty as difficulty,
                       length(path) as depth
                ORDER BY depth
                """,
                concept_id=concept_id
            )
            
            return [dict(record) for record in result]
    
    # ========================================================================
    # Kinetic Tier Operations (Runtime Instances)
    # ========================================================================
    
    def create_problem_instance(
        self,
        problem_id: str,
        pattern_id: str,
        instance_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create problem instance using scaffolding pattern."""
        with self.driver.session(database=self.database) as session:
            result = session.run(
                """
                MATCH (pattern:ScaffoldPattern {id: $pattern_id})
                CREATE (p:Problem {
                    id: $problem_id,
                    instance_params: $params,
                    created_at: datetime()
                })
                CREATE (p)-[:USES_PATTERN]->(pattern)
                RETURN p
                """,
                problem_id=problem_id,
                pattern_id=pattern_id,
                params=instance_params
            )
            
            return {"created": True, "problem_id": problem_id}
    
    def record_student_attempt(
        self,
        student_id: str,
        problem_id: str,
        steps_completed: List[int],
        total_time: int,
        mistakes: List[Dict],
        success: bool
    ) -> Dict[str, Any]:
        """Record student's attempt on a problem."""
        with self.driver.session(database=self.database) as session:
            result = session.run(
                """
                MATCH (s:Student {id: $student_id}),
                      (p:Problem {id: $problem_id})
                CREATE (s)-[:ATTEMPTED {
                    timestamp: datetime(),
                    steps_completed: $steps,
                    total_time: $time,
                    mistakes: $mistakes,
                    success: $success
                }]->(p)
                RETURN s, p
                """,
                student_id=student_id,
                problem_id=problem_id,
                steps=steps_completed,
                time=total_time,
                mistakes=mistakes,
                success=success
            )
            
            return {"recorded": True}
    
    # ========================================================================
    # Dynamic Tier Operations (Learning & Adaptation)
    # ========================================================================
    
    def get_student_cluster(self, student_id: str) -> Optional[str]:
        """Get student's current performance cluster."""
        with self.driver.session(database=self.database) as session:
            result = session.run(
                """
                MATCH (s:Student {id: $student_id})
                      -[:BELONGS_TO]->(cluster:PerformanceCluster)
                RETURN cluster.id as cluster_id
                """,
                student_id=student_id
            )
            
            record = result.single()
            return record["cluster_id"] if record else None
    
    def get_optimal_pattern_for_cluster(
        self,
        cluster_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get optimal scaffolding pattern for cluster."""
        with self.driver.session(database=self.database) as session:
            result = session.run(
                """
                MATCH (cluster:PerformanceCluster {id: $cluster_id})
                      -[:OPTIMAL_PATTERN]->(pattern:ScaffoldPattern)
                RETURN pattern.id as pattern_id,
                       pattern.difficulty as difficulty,
                       pattern.steps as steps
                """,
                cluster_id=cluster_id
            )
            
            record = result.single()
            return dict(record) if record else None
    
    def update_cluster_metrics(
        self,
        cluster_id: str,
        new_time: int,
        success: bool
    ):
        """Update cluster aggregated metrics after student completion."""
        with self.driver.session(database=self.database) as session:
            session.run(
                """
                MATCH (c:PerformanceCluster {id: $cluster_id})
                SET c.avg_time = (c.avg_time * c.student_count + $new_time) / (c.student_count + 1),
                    c.success_rate = (c.success_rate * c.student_count + $success_int) / (c.student_count + 1),
                    c.updated_at = datetime()
                """,
                cluster_id=cluster_id,
                new_time=new_time,
                success_int=1 if success else 0
            )
    
    def find_ready_concepts(self, student_id: str) -> List[Dict[str, Any]]:
        """
        Find concepts student is ready to learn.
        
        Ready = All prerequisites mastered.
        """
        with self.driver.session(database=self.database) as session:
            result = session.run(
                """
                MATCH (s:Student {id: $student_id})-[:MASTERED]->(mastered:Concept)
                      <-[:REQUIRES]-(available:Concept)
                WHERE NOT (s)-[:MASTERED]->(available)
                RETURN DISTINCT available.id as id,
                       available.name as name,
                       available.difficulty as difficulty
                """,
                student_id=student_id
            )
            
            return [dict(record) for record in result]
    
    # ========================================================================
    # Analytics Queries
    # ========================================================================
    
    def get_concept_statistics(self, concept_id: str) -> Dict[str, Any]:
        """Get statistics for a concept."""
        with self.driver.session(database=self.database) as session:
            result = session.run(
                """
                MATCH (c:Concept {id: $concept_id})
                OPTIONAL MATCH (c)<-[:FOR_CONCEPT]-(patterns:ScaffoldPattern)
                OPTIONAL MATCH (s:Student)-[:MASTERED]->(c)
                RETURN c.name as name,
                       c.difficulty as difficulty,
                       count(DISTINCT patterns) as pattern_count,
                       count(DISTINCT s) as students_mastered
                """,
                concept_id=concept_id
            )
            
            record = result.single()
            return dict(record) if record else {}

