"""
Hook Event Types - Observability Event Definitions

Defines all event types used in the feedback loop workflow for observability tracking.

VERSION: 1.0.0
DATE: 2025-10-16
"""


class HookEventType:
    """Event types for feedback loop workflow observability."""
    
    # OCR phase
    OCR_STARTED = "ocr_started"
    OCR_COMPLETED = "ocr_completed"
    OCR_FAILED = "ocr_failed"
    
    # Concept matching phase
    CONCEPT_MATCH_STARTED = "concept_match_started"
    CONCEPT_MATCH_COMPLETED = "concept_match_completed"
    
    # Pattern query phase
    PATTERN_QUERY_STARTED = "pattern_query_started"
    PATTERN_QUERY_COMPLETED = "pattern_query_completed"
    
    # Scaffolding generation phase
    SCAFFOLDING_STARTED = "scaffolding_started"
    SCAFFOLDING_COMPLETED = "scaffolding_completed"
    
    # Feedback collection phase
    FEEDBACK_STARTED = "feedback_started"
    FEEDBACK_STEP_COLLECTED = "feedback_step_collected"
    FEEDBACK_COMPLETED = "feedback_completed"
    
    # Pattern learning phase
    LEARNING_STARTED = "learning_started"
    PATTERN_EXTRACTED = "pattern_extracted"
    LEARNING_COMPLETED = "learning_completed"
    
    # Neo4j storage phase
    NEO4J_WRITE_STARTED = "neo4j_write_started"
    NEO4J_WRITE_COMPLETED = "neo4j_write_completed"
    
    # Validation phase
    VALIDATION_COMPLETED = "validation_completed"
    
    # Parallel execution phase (infinite-agentic-loop integration)
    WAVE_STARTED = "wave_started"
    WAVE_COMPLETED = "wave_completed"
    VARIATION_GENERATED = "variation_generated"
    PARALLEL_FEEDBACK_STARTED = "parallel_feedback_started"
    PARALLEL_FEEDBACK_COMPLETED = "parallel_feedback_completed"
    META_PATTERN_EXTRACTED = "meta_pattern_extracted"
    SPEC_EVOLVED = "spec_evolved"
    UNIQUENESS_VALIDATION_FAILED = "uniqueness_validation_failed"
    
    @classmethod
    def all_types(cls) -> list:
        """Get all event types as a list."""
        return [
            value for key, value in cls.__dict__.items()
            if not key.startswith('_') and isinstance(value, str)
        ]

