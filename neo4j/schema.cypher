// ============================================================================
// Math Education System - Neo4j Graph Schema
// ============================================================================
// 
// Complete Learning Graph integrating all 3 Palantir tiers:
// - Semantic Tier: Concept definitions, dependencies, scaffolding patterns
// - Kinetic Tier: Problem instances, student attempts
// - Dynamic Tier: Performance clusters, learning patterns, evolution
//
// Based on: 26 Socratic questions, 95%+ precision
// Date: 2025-10-16
// Version: 1.0.0
// ============================================================================

// ============================================================================
// SEMANTIC TIER: Static Definitions
// ============================================================================

// Constraint: Unique concept IDs
CREATE CONSTRAINT concept_id_unique IF NOT EXISTS
FOR (c:Concept) REQUIRE c.id IS UNIQUE;

// Constraint: Unique scaffold pattern IDs
CREATE CONSTRAINT scaffold_pattern_id_unique IF NOT EXISTS
FOR (s:ScaffoldPattern) REQUIRE s.id IS UNIQUE;

// Constraint: Unique student IDs
CREATE CONSTRAINT student_id_unique IF NOT EXISTS
FOR (s:Student) REQUIRE s.id IS UNIQUE;

// Index: Concept by grade level
CREATE INDEX concept_grade_level IF NOT EXISTS
FOR (c:Concept) ON (c.grade_level);

// Index: Concept by difficulty
CREATE INDEX concept_difficulty IF NOT EXISTS
FOR (c:Concept) ON (c.difficulty);

// ============================================================================
// Node: Concept (Mathematical Concept)
// ============================================================================
// Properties:
//   id: Unique identifier (e.g., 'prime_number')
//   name: Korean name (e.g., '소수')
//   definition: Full definition text
//   difficulty: 1-10 rating
//   grade_level: 'elementary_X', 'middle_X', 'high_X', 'university'
//   chapter: Chapter name (e.g., '수와 연산')
//   atomic_factors: ['definition', 'examples', 'tests']
//   created_at: Timestamp
//   updated_at: Timestamp
// ============================================================================

// ============================================================================
// Relationship: REQUIRES (Concept dependency)
// ============================================================================
// Properties:
//   strength: 0.0-1.0 (how critical is this prerequisite)
//   validated: boolean (has this dependency been confirmed)
//   created_at: Timestamp
// ============================================================================

// ============================================================================
// Relationship: ENABLES (Concept unlocks another)
// ============================================================================
// Inverse of REQUIRES, for forward navigation
// ============================================================================

// ============================================================================
// Node: ScaffoldPattern (Reusable scaffolding template)
// ============================================================================
// Properties:
//   id: Unique identifier
//   concept_id: Associated concept
//   difficulty: 1-10
//   steps: JSON array of step templates
//     [{template: '...', hint: '...', validation: '...'}, ...]
//   usage_count: How many times used
//   success_rate: Average success across all uses
//   created_at: Timestamp
// ============================================================================

// ============================================================================
// Node: StepTemplate (Individual step in scaffolding)
// ============================================================================
// Properties:
//   id: Unique identifier
//   action_type: 'division', 'multiplication', 'substitution', etc.
//   hint_template: Template string for hint
//   validation_rule: How to validate student answer
//   difficulty: 1-10
// ============================================================================

// ============================================================================
// Relationship: FOR_CONCEPT
// ============================================================================
// Links ScaffoldPattern to its Concept
// ============================================================================

// ============================================================================
// Relationship: PART_OF
// ============================================================================
// Links StepTemplate to ScaffoldPattern
// Properties:
//   order: 1, 2, 3, ... (sequence order)
// ============================================================================

// ============================================================================
// KINETIC TIER: Runtime Instances
// ============================================================================

// ============================================================================
// Node: Problem (Specific problem instance)
// ============================================================================
// Properties:
//   id: Unique identifier
//   instance_params: JSON (e.g., {n: 60} for prime factorization)
//   created_at: Timestamp
//   difficulty_actual: Actual difficulty (may differ from pattern)
// ============================================================================

// ============================================================================
// Relationship: USES_PATTERN
// ============================================================================
// Links Problem instance to ScaffoldPattern template
// ============================================================================

// ============================================================================
// Node: Student
// ============================================================================
// Properties:
//   id: Unique identifier
//   name: Student name (optional)
//   cluster: Current PerformanceCluster assignment
//   created_at: Timestamp
//   last_active: Timestamp
// ============================================================================

// ============================================================================
// Relationship: ATTEMPTED
// ============================================================================
// Student attempted a Problem
// Properties:
//   problem_id: Reference
//   timestamp: When
//   steps_completed: [1,2,3,4,5] (which steps finished)
//   total_time: Total seconds spent
//   mistakes: JSON [{step: 2, type: 'division_error'}, ...]
//   hints_used: [1, 3] (which hint numbers)
//   success: boolean
//   final_score: 0.0-1.0
// ============================================================================

// ============================================================================
// Relationship: MASTERED
// ============================================================================
// Student mastered a Concept
// Properties:
//   level: 0.0-1.0 mastery level
//   achieved_at: Timestamp
//   problems_solved: Count
//   total_time_spent: Cumulative seconds
// ============================================================================

// ============================================================================
// DYNAMIC TIER: Learning & Adaptation
// ============================================================================

// ============================================================================
// Node: PerformanceCluster (Aggregated student groups)
// ============================================================================
// Properties:
//   id: Unique identifier
//   pattern_id: Associated ScaffoldPattern
//   cluster_name: Descriptive name
//   student_count: How many students in cluster
//   avg_time: Average completion time (seconds)
//   success_rate: 0.0-1.0
//   common_mistakes: JSON array of mistake types
//   optimal_scaffolding_level: 'minimal', 'medium', 'detailed'
//   effective_hint_sequence: [1, 3] (which hints work best)
//   recommended_next_concepts: [concept_ids]
//   updated_at: Last update timestamp
// ============================================================================

// ============================================================================
// Relationship: BELONGS_TO
// ============================================================================
// Student belongs to PerformanceCluster
// Properties:
//   assignment_confidence: 0.0-1.0
//   assigned_at: Timestamp
// ============================================================================

// ============================================================================
// Relationship: OPTIMAL_PATTERN
// ============================================================================
// Cluster's optimal ScaffoldPattern
// Properties:
//   validation_score: How well this pattern works for cluster
// ============================================================================

// ============================================================================
// Node: LearningPattern (Cross-student insights)
// ============================================================================
// Properties:
//   id: Unique identifier
//   description: Pattern description
//   applicable_to: [concept_ids]
//   success_rate_improvement: 0.0-1.0 (e.g., 0.35 = +35%)
//   students_matching: Count
//   discovered_at: Timestamp
// ============================================================================

// ============================================================================
// Relationship: MATCHES
// ============================================================================
// Student matches a LearningPattern
// ============================================================================

// ============================================================================
// Relationship: DIFFICULTY_EVOLVED
// ============================================================================
// Concept difficulty changed based on student data
// Properties:
//   initial: Original difficulty
//   current: Current difficulty
//   reason: Why it changed
//   updated_at: Timestamp
// ============================================================================

// ============================================================================
// Node: DifficultyAdjustment (Track evolution)
// ============================================================================
// Properties:
//   adjustment_value: +/- amount
//   reason: Explanation
//   student_data_basis: How many students' data
//   created_at: Timestamp
// ============================================================================

// ============================================================================
// Example Usage Queries
// ============================================================================

// Query 1: Find concepts student is ready to learn
// MATCH (s:Student {id: $student_id})-[:MASTERED]->(mastered:Concept)
//       <-[:REQUIRES]-(available:Concept)
// WHERE NOT (s)-[:MASTERED]->(available)
// RETURN available

// Query 2: Get optimal scaffolding for student
// MATCH (s:Student {id: $student_id})-[:BELONGS_TO]->(cluster:PerformanceCluster)
//       -[:OPTIMAL_PATTERN]->(pattern:ScaffoldPattern)
// RETURN pattern

// Query 3: Find students with similar learning patterns
// MATCH (s1:Student)-[:MATCHES]->(lp:LearningPattern)
//       <-[:MATCHES]-(s2:Student)
// WHERE s1.id = $student_id AND s1.id <> s2.id
// RETURN s2

// Query 4: Analyze concept prerequisite chain
// MATCH path = (concept:Concept {id: $concept_id})
//              -[:REQUIRES*]->(prereq:Concept)
// RETURN path

// Query 5: Update cluster metrics after student completion
// MATCH (s:Student {id: $student_id})-[:BELONGS_TO]->(c:PerformanceCluster)
// SET c.avg_time = (c.avg_time * c.student_count + $new_time) / (c.student_count + 1)
// SET c.updated_at = timestamp()

