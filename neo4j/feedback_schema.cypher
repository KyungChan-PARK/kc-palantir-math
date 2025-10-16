// ============================================================================
// Feedback Learning Extension - Neo4j Schema
// ============================================================================
// 
// Extends the main schema to support feedback-driven learning.
// Adds FeedbackSession, LearnedPattern, and FeedbackAnnotation nodes.
//
// Based on: Closed feedback loop architecture
// Date: 2025-10-16
// Version: 1.0.0
// ============================================================================

// ============================================================================
// FEEDBACK TIER: Learning & Improvement
// ============================================================================

// Constraint: Unique feedback session IDs
CREATE CONSTRAINT feedback_session_id_unique IF NOT EXISTS
FOR (fs:FeedbackSession) REQUIRE fs.id IS UNIQUE;

// Constraint: Unique learned pattern IDs
CREATE CONSTRAINT learned_pattern_id_unique IF NOT EXISTS
FOR (lp:LearnedPattern) REQUIRE lp.id IS UNIQUE;

// Index: Feedback sessions by date
CREATE INDEX feedback_session_date IF NOT EXISTS
FOR (fs:FeedbackSession) ON (fs.timestamp);

// Index: Learned patterns by confidence
CREATE INDEX learned_pattern_confidence IF NOT EXISTS
FOR (lp:LearnedPattern) ON (lp.confidence);

// ============================================================================
// Node: FeedbackSession
// ============================================================================
// Represents a complete feedback collection session
//
// Properties:
//   id: Unique identifier (e.g., 'fs_20251016_120000')
//   problem_id: Associated problem instance
//   image_source: Original image file
//   reviewer: Who provided feedback (e.g., 'teacher_kc')
//   timestamp: When feedback was collected
//   overall_rating: Overall quality rating
//   patterns_extracted: Number of patterns discovered
//   ocr_confidence: OCR extraction confidence
// ============================================================================

// ============================================================================
// Node: FeedbackAnnotation
// ============================================================================
// Individual feedback on a single step
//
// Properties:
//   id: Unique identifier
//   step_id: Step number (1-indexed)
//   session_id: Parent session
//   rating: 1-5 rating
//   comment: Free text comment
//   suggested_fix: Suggested improvement
//   learning_point: Extracted learning insight
// ============================================================================

// ============================================================================
// Node: LearnedPattern
// ============================================================================
// Reusable pattern extracted from feedback
//
// Properties:
//   id: Unique identifier (e.g., 'lp_emphasize_smallest_prime')
//   type: Pattern type ('question_improvement', 'hint_effectiveness', etc.)
//   rule: Description of the pattern rule
//   confidence: 0.0-1.0 (1.0 = human validated)
//   applicable_concepts: JSON array of concept IDs
//   improvement_rate: Measured improvement (0.0-1.0)
//   reuse_count: How many times applied
//   cypher_query: Auto-apply query
//   examples: JSON array of before/after examples
//   discovered_date: When pattern was discovered
//   source: Who suggested it
//   tested: Boolean (A/B tested or not)
//   auto_apply: Boolean (auto-apply in production)
// ============================================================================

// ============================================================================
// Relationship: HAS_ANNOTATION
// ============================================================================
// FeedbackSession has multiple FeedbackAnnotations
// ============================================================================

// ============================================================================
// Relationship: EXTRACTED_FROM
// ============================================================================
// LearnedPattern was extracted from FeedbackAnnotation
//
// Properties:
//   extraction_confidence: How confident the extraction was
//   extraction_method: 'manual', 'automatic', 'hybrid'
// ============================================================================

// ============================================================================
// Relationship: IMPROVED_BY
// ============================================================================
// StepTemplate was improved by LearnedPattern
//
// Properties:
//   applied_date: When pattern was applied
//   before_text: Original question template
//   after_text: Improved question template
//   effectiveness: Measured effectiveness (updated after use)
// ============================================================================

// ============================================================================
// Relationship: APPLICABLE_TO
// ============================================================================
// LearnedPattern is applicable to Concept
//
// Properties:
//   relevance_score: 0.0-1.0
//   validated: Boolean
// ============================================================================

// ============================================================================
// Example Usage Queries
// ============================================================================

// Query 1: Create feedback session
// CREATE (fs:FeedbackSession {
//   id: 'fs_20251016_120000',
//   problem_id: 'prob_sample_001',
//   image_source: 'sample.png',
//   reviewer: 'teacher_kc',
//   timestamp: datetime(),
//   overall_rating: 'needs_improvement',
//   patterns_extracted: 0,
//   ocr_confidence: 0.95
// })

// Query 2: Create feedback annotation
// CREATE (ann:FeedbackAnnotation {
//   id: 'fb_step_2_001',
//   step_id: 2,
//   session_id: 'fs_20251016_120000',
//   rating: 3,
//   comment: 'Should specify smallest prime',
//   suggested_fix: '60을 가장 작은 소수로 나누면?',
//   learning_point: 'Emphasize conceptual understanding'
// })
// 
// MATCH (fs:FeedbackSession {id: 'fs_20251016_120000'})
// CREATE (fs)-[:HAS_ANNOTATION]->(ann)

// Query 3: Create learned pattern
// CREATE (lp:LearnedPattern {
//   id: 'lp_emphasize_smallest_prime',
//   type: 'question_improvement',
//   rule: 'Add "가장 작은 소수" to division questions',
//   confidence: 1.0,
//   applicable_concepts: ['prime_factorization', 'gcd', 'lcm'],
//   improvement_rate: 0.15,
//   reuse_count: 0,
//   cypher_query: 'MATCH (s:StepTemplate)...',
//   examples: '[{"before": "...", "after": "..."}]',
//   discovered_date: datetime(),
//   source: 'teacher_kc',
//   tested: false,
//   auto_apply: false
// })

// Query 4: Link pattern to annotation
// MATCH (ann:FeedbackAnnotation {id: 'fb_step_2_001'}),
//       (lp:LearnedPattern {id: 'lp_emphasize_smallest_prime'})
// CREATE (lp)-[:EXTRACTED_FROM {
//   extraction_confidence: 1.0,
//   extraction_method: 'manual'
// }]->(ann)

// Query 5: Apply pattern to step templates
// MATCH (lp:LearnedPattern {id: 'lp_emphasize_smallest_prime'}),
//       (s:StepTemplate)
// WHERE s.concept_id IN lp.applicable_concepts
//   AND s.action_type = 'division'
// CREATE (s)-[:IMPROVED_BY {
//   applied_date: datetime(),
//   before_text: s.question_template,
//   after_text: s.question_template + ' (가장 작은 소수)',
//   effectiveness: null
// }]->(lp)
// SET s.question_template = s.question_template + ' (가장 작은 소수)'
// SET s.last_updated = datetime()

// Query 6: Find applicable patterns for a concept
// MATCH (lp:LearnedPattern)
// WHERE $concept_id IN lp.applicable_concepts
//   AND lp.confidence > 0.8
//   AND lp.auto_apply = true
// RETURN lp
// ORDER BY lp.confidence DESC, lp.improvement_rate DESC

// Query 7: Update pattern effectiveness after use
// MATCH (lp:LearnedPattern {id: $pattern_id})
// SET lp.reuse_count = lp.reuse_count + 1
// SET lp.improvement_rate = $measured_improvement

// Query 8: Get feedback statistics
// MATCH (fs:FeedbackSession)-[:HAS_ANNOTATION]->(ann:FeedbackAnnotation)
// WHERE fs.timestamp > datetime() - duration({days: 30})
// RETURN fs.reviewer,
//        COUNT(ann) as annotations_count,
//        AVG(ann.rating) as avg_rating,
//        SUM(CASE WHEN ann.rating < 4 THEN 1 ELSE 0 END) as needs_improvement_count

// ============================================================================
// End of Feedback Schema Extension
// ============================================================================

