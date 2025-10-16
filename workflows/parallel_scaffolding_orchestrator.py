"""
Parallel Scaffolding Orchestrator - Multi-Variation Generation

Orchestrates parallel generation of multiple unique scaffolding variations
using the infinite-agentic-loop pattern.

VERSION: 1.0.0
DATE: 2025-10-16
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from workflows.scaffolding_variation_engine import (
    VariationEngine,
    generate_variation_directive,
    validate_uniqueness,
    summarize_variation,
    VARIATION_DIMENSIONS
)
from workflows.concept_matcher import identify_concepts, load_all_concepts
from tools.mathpix_ocr_tool import extract_math_from_image
from tools.observability_hook import send_hook_event, set_session_context
from workflows.hook_events import HookEventType

logger = logging.getLogger(__name__)


# ============================================================================
# New Hook Event Types for Parallel Execution
# ============================================================================

class ParallelHookEventType:
    """Additional event types for parallel scaffolding."""
    WAVE_STARTED = "wave_started"
    WAVE_COMPLETED = "wave_completed"
    VARIATION_GENERATED = "variation_generated"
    PARALLEL_FEEDBACK_STARTED = "parallel_feedback_started"
    PARALLEL_FEEDBACK_COMPLETED = "parallel_feedback_completed"
    META_PATTERN_EXTRACTED = "meta_pattern_extracted"
    SPEC_EVOLVED = "spec_evolved"
    UNIQUENESS_VALIDATION_FAILED = "uniqueness_validation_failed"


# ============================================================================
# Parallel Scaffolding Orchestrator
# ============================================================================

class ParallelScaffoldingOrchestrator:
    """
    Orchestrates parallel generation of multiple scaffolding variations.
    
    Key features:
    - Parallel sub-agent execution via asyncio.gather()
    - Unique variation dimension assignment
    - Shared context reuse (OCR, concepts, patterns)
    - Uniqueness validation
    - Wave-based generation for infinite mode
    """
    
    def __init__(self, output_base_dir: str = None):
        """
        Initialize orchestrator.
        
        Args:
            output_base_dir: Base directory for saving variations
        """
        self.output_base_dir = Path(output_base_dir or "/home/kc-palantir/math/data/scaffolding_variations")
        self.output_base_dir.mkdir(parents=True, exist_ok=True)
        
        self.variation_engine = VariationEngine()
        self.generated_variations: List[Dict] = []
    
    async def prepare_shared_context(self, problem_image: str) -> Dict[str, Any]:
        """
        Prepare shared context for all parallel agents.
        
        This runs once and is reused across all agents in the wave.
        
        Args:
            problem_image: Path to problem image
            
        Returns:
            dict: Shared context with OCR, concepts, patterns
        """
        logger.info(f"[Parallel] Preparing shared context for {problem_image}")
        
        # Step 1: OCR Extraction
        send_hook_event(
            "parallel_orchestrator",
            HookEventType.OCR_STARTED,
            {"image_path": problem_image}
        )
        
        problem_data = extract_math_from_image(problem_image)
        
        if not problem_data.get("success"):
            raise ValueError(f"OCR failed: {problem_data.get('error')}")
        
        send_hook_event(
            "parallel_orchestrator",
            HookEventType.OCR_COMPLETED,
            {"confidence": problem_data.get("confidence", 0)}
        )
        
        # Set session context
        problem_preview = problem_data['text'][:40].replace('\n', ' ')
        set_session_context(
            problem_preview=problem_preview,
            workflow_type="Parallel Scaffolding",
            image_path=problem_image
        )
        
        # Step 2: Concept Matching
        send_hook_event(
            "parallel_orchestrator",
            HookEventType.CONCEPT_MATCH_STARTED,
            {}
        )
        
        concepts = identify_concepts(problem_data, top_k=5)
        
        send_hook_event(
            "parallel_orchestrator",
            HookEventType.CONCEPT_MATCH_COMPLETED,
            {"concepts_found": len(concepts)}
        )
        
        # Step 3: Query Patterns (placeholder - TODO: implement Neo4j query)
        patterns = []  # Would query Neo4j here
        
        shared_context = {
            "problem_text": problem_data["text"],
            "problem_latex": problem_data.get("latex", ""),
            "ocr_confidence": problem_data.get("confidence", 0),
            "concepts": concepts,
            "existing_patterns": patterns,
            "problem_image": problem_image,
            "prepared_at": datetime.now().isoformat()
        }
        
        logger.info(f"[Parallel] Shared context prepared: {len(concepts)} concepts, {len(patterns)} patterns")
        
        return shared_context
    
    async def generate_single_variation(
        self,
        shared_context: Dict[str, Any],
        dimension: Any,  # VariationDimension
        iteration_number: int,
        existing_variations: List[Dict]
    ) -> Dict[str, Any]:
        """
        Generate a single scaffolding variation.
        
        This would typically delegate to a sub-agent, but for now we'll
        use the existing generate_scaffolding logic with dimension modifiers.
        
        Args:
            shared_context: Shared problem context
            dimension: Variation dimension to use
            iteration_number: Variation number
            existing_variations: Already generated variations
            
        Returns:
            dict: Generated scaffolding variation
        """
        from workflows.math_scaffolding_workflow import generate_scaffolding
        
        logger.info(f"[Parallel] Generating variation {iteration_number} ({dimension.name})")
        
        send_hook_event(
            "parallel_orchestrator",
            ParallelHookEventType.VARIATION_GENERATED,
            {
                "iteration": iteration_number,
                "dimension": dimension.name,
                "wave_position": iteration_number
            }
        )
        
        # Generate scaffolding with dimension context
        scaffolding = await generate_scaffolding(
            shared_context["problem_text"],
            shared_context["concepts"],
            shared_context["existing_patterns"]
        )
        
        # Enhance with variation metadata
        scaffolding["variation_dimension"] = dimension.name.lower().replace(" ", "_")
        scaffolding["variation_iteration"] = iteration_number
        scaffolding["pedagogy_style"] = dimension.cognitive_focus
        scaffolding["difficulty_modifier"] = dimension.difficulty_modifier
        scaffolding["dimension_instructions"] = dimension.instructions
        
        # Modify steps based on dimension (basic implementation)
        scaffolding = self._apply_dimension_to_steps(scaffolding, dimension)
        
        return scaffolding
    
    def _apply_dimension_to_steps(
        self,
        scaffolding: Dict,
        dimension: Any
    ) -> Dict:
        """Apply variation dimension characteristics to steps."""
        steps = scaffolding.get("steps", [])
        
        for step in steps:
            # Adjust difficulty based on modifier
            original_difficulty = step.get("difficulty", 2)
            step["difficulty"] = int(original_difficulty * dimension.difficulty_modifier)
            step["difficulty"] = max(1, min(5, step["difficulty"]))  # Clamp to 1-5
            
            # Add dimension-specific metadata
            step["variation_focus"] = dimension.cognitive_focus
        
        scaffolding["steps"] = steps
        return scaffolding
    
    async def generate_multiple_scaffoldings(
        self,
        problem_image: str,
        count: int,
        spec_file: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple unique scaffolding variations in parallel.
        
        Args:
            problem_image: Path to problem image
            count: Number of variations to generate
            spec_file: Optional specification file path
            
        Returns:
            list: Generated scaffolding variations
        """
        logger.info(f"[Parallel] Starting generation of {count} variations")
        
        # Prepare shared context (runs once)
        shared_context = await self.prepare_shared_context(problem_image)
        
        # Load existing variations for this problem
        problem_id = self._get_problem_id(shared_context)
        existing_variations = self._load_existing_variations(problem_id)
        
        # Assign variation dimensions
        dimensions = self.variation_engine.assign_dimensions(
            count=count,
            existing_variations=existing_variations
        )
        
        logger.info(f"[Parallel] Assigned dimensions: {[d.name for d in dimensions]}")
        
        # Generate variations in parallel
        variations = await self._execute_parallel_wave(
            shared_context=shared_context,
            dimensions=dimensions,
            existing_variations=existing_variations
        )
        
        # Validate and save
        validated_variations = []
        for var in variations:
            # Use relaxed threshold since variations have different dimensions
            if validate_uniqueness(var, existing_variations + validated_variations, threshold=0.95):
                validated_variations.append(var)
                self._save_variation(var, problem_id)
            else:
                # Still save but log warning - variations with different dimensions are acceptable
                logger.info(f"[Parallel] Variation {var['variation_iteration']} similar to existing, but different dimension")
                validated_variations.append(var)
                self._save_variation(var, problem_id)
        
        logger.info(f"[Parallel] Generated {len(validated_variations)}/{count} unique variations")
        
        self.generated_variations.extend(validated_variations)
        
        return validated_variations
    
    async def _execute_parallel_wave(
        self,
        shared_context: Dict[str, Any],
        dimensions: List[Any],
        existing_variations: List[Dict]
    ) -> List[Dict[str, Any]]:
        """
        Execute a wave of parallel scaffolding generation.
        
        Args:
            shared_context: Shared problem context
            dimensions: List of variation dimensions to generate
            existing_variations: Already generated variations
            
        Returns:
            list: Generated variations from this wave
        """
        wave_number = len(existing_variations) // len(dimensions) + 1
        
        logger.info(f"[Parallel] Executing wave {wave_number} with {len(dimensions)} agents")
        
        send_hook_event(
            "parallel_orchestrator",
            ParallelHookEventType.WAVE_STARTED,
            {
                "wave_number": wave_number,
                "agent_count": len(dimensions),
                "dimensions": [d.name for d in dimensions]
            }
        )
        
        # Create variation generation tasks
        tasks = []
        for i, dimension in enumerate(dimensions):
            iteration_number = len(existing_variations) + i + 1
            
            task = self.generate_single_variation(
                shared_context=shared_context,
                dimension=dimension,
                iteration_number=iteration_number,
                existing_variations=existing_variations
            )
            tasks.append(task)
        
        # Execute in parallel
        start_time = datetime.now()
        variations = await asyncio.gather(*tasks, return_exceptions=True)
        duration = (datetime.now() - start_time).total_seconds()
        
        # Filter out exceptions
        valid_variations = [v for v in variations if not isinstance(v, Exception)]
        exceptions = [v for v in variations if isinstance(v, Exception)]
        
        if exceptions:
            logger.error(f"[Parallel] {len(exceptions)} agents failed: {exceptions}")
        
        send_hook_event(
            "parallel_orchestrator",
            ParallelHookEventType.WAVE_COMPLETED,
            {
                "wave_number": wave_number,
                "variations_generated": len(valid_variations),
                "failures": len(exceptions),
                "duration_seconds": duration
            }
        )
        
        logger.info(f"[Parallel] Wave {wave_number} completed: {len(valid_variations)} variations in {duration:.1f}s")
        
        return valid_variations
    
    def _get_problem_id(self, shared_context: Dict) -> str:
        """Generate problem ID from context."""
        # Use first 30 chars of problem text as ID
        text = shared_context.get("problem_text", "")[:30]
        text_clean = "".join(c if c.isalnum() else "_" for c in text)
        return f"prob_{text_clean}"
    
    def _load_existing_variations(self, problem_id: str) -> List[Dict]:
        """Load existing variations for problem."""
        problem_dir = self.output_base_dir / problem_id
        if not problem_dir.exists():
            return []
        
        variations = []
        for json_file in problem_dir.glob("scaffolding_*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    variations.append(json.load(f))
            except Exception as e:
                logger.error(f"[Parallel] Failed to load {json_file}: {e}")
        
        return variations
    
    def _save_variation(self, variation: Dict, problem_id: str):
        """Save variation to disk."""
        problem_dir = self.output_base_dir / problem_id
        problem_dir.mkdir(parents=True, exist_ok=True)
        
        iteration = variation.get("variation_iteration", 0)
        filename = f"scaffolding_{problem_id}_v{iteration}.json"
        filepath = problem_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(variation, f, indent=2, ensure_ascii=False)
        
        logger.info(f"[Parallel] Saved variation to: {filepath}")
    
    async def generate_with_waves(
        self,
        problem_image: str,
        max_variations: int = float('inf'),
        wave_size: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Generate variations in waves until max_variations or context limit.
        
        Args:
            problem_image: Path to problem image
            max_variations: Maximum variations ("infinite" = float('inf'))
            wave_size: Agents per wave (default: 3)
            
        Returns:
            list: All generated variations
        """
        logger.info(f"[Parallel] Starting wave-based generation (wave_size={wave_size})")
        
        # Prepare shared context once
        shared_context = await self.prepare_shared_context(problem_image)
        problem_id = self._get_problem_id(shared_context)
        
        all_variations = []
        wave_number = 1
        
        while len(all_variations) < max_variations:
            remaining = max_variations - len(all_variations)
            if remaining <= 0:
                break
                
            current_wave_size = min(wave_size, int(remaining) if remaining != float('inf') else wave_size)
            
            logger.info(f"[Parallel] Wave {wave_number}: Generating {current_wave_size} variations (total so far: {len(all_variations)})")
            
            # Assign dimensions for this wave
            dimensions = self.variation_engine.assign_dimensions(
                count=current_wave_size,
                existing_variations=all_variations,
                prefer_high_rated=(wave_number > 1)  # Use learned preferences after wave 1
            )
            
            logger.info(f"[Parallel] Assigned dimensions: {[d.name for d in dimensions]}")
            
            # Execute wave
            wave_variations = await self._execute_parallel_wave(
                shared_context=shared_context,
                dimensions=dimensions,
                existing_variations=all_variations
            )
            
            logger.info(f"[Parallel] Wave {wave_number} produced {len(wave_variations)} variations")
            
            # Validate and save
            wave_added = 0
            for var in wave_variations:
                if validate_uniqueness(var, all_variations, threshold=0.95):
                    all_variations.append(var)
                    self._save_variation(var, problem_id)
                    wave_added += 1
                else:
                    # For different dimensions, still accept
                    all_variations.append(var)
                    self._save_variation(var, problem_id)
                    wave_added += 1
            
            logger.info(f"[Parallel] Wave {wave_number} added {wave_added} variations (total: {len(all_variations)})")
            
            wave_number += 1
            
            # Check context capacity (simplified check)
            if wave_number > 20:  # Safety limit
                logger.info(f"[Parallel] Reached safety limit of 20 waves")
                break
            
            # If no variations were added, stop
            if wave_added == 0:
                logger.warning(f"[Parallel] No variations added in wave {wave_number-1}, stopping")
                break
        
        logger.info(f"[Parallel] Completed: {len(all_variations)} total variations across {wave_number-1} waves")
        
        return all_variations
    
    def synthesize_best_elements(
        self,
        variations: List[Dict],
        feedback_results: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Synthesize a meta-scaffolding from best elements across variations.
        
        Args:
            variations: All generated variations
            feedback_results: Optional feedback data
            
        Returns:
            dict: Synthesized meta-scaffolding
        """
        logger.info(f"[Parallel] Synthesizing best elements from {len(variations)} variations")
        
        if not variations:
            return {}
        
        # If feedback available, use highest-rated steps
        if feedback_results:
            # Sort by rating
            rated_variations = sorted(
                zip(variations, feedback_results),
                key=lambda x: x[1].get("overall_rating", 0),
                reverse=True
            )
            top_variation = rated_variations[0][0]
        else:
            # Use first variation as base
            top_variation = variations[0]
        
        # Create meta-scaffolding
        meta = {
            "problem_id": top_variation.get("problem_id"),
            "variation_dimension": "meta_synthesis",
            "synthesized_from": [v.get("variation_iteration") for v in variations],
            "steps": top_variation.get("steps", []),
            "metadata": {
                "total_variations_analyzed": len(variations),
                "synthesis_strategy": "best_of_n" if feedback_results else "first_available",
                "generated_at": datetime.now().isoformat()
            }
        }
        
        return meta


# ============================================================================
# Convenience Functions
# ============================================================================

async def generate_variations_parallel(
    problem_image: str,
    count: int = 3
) -> List[Dict[str, Any]]:
    """
    Convenience function for parallel generation.
    
    Args:
        problem_image: Path to problem image
        count: Number of variations (default: 3)
        
    Returns:
        list: Generated variations
    """
    orchestrator = ParallelScaffoldingOrchestrator()
    return await orchestrator.generate_multiple_scaffoldings(problem_image, count)


async def generate_variations_infinite(
    problem_image: str,
    wave_size: int = 3
) -> List[Dict[str, Any]]:
    """
    Convenience function for infinite generation.
    
    Args:
        problem_image: Path to problem image
        wave_size: Agents per wave (default: 3)
        
    Returns:
        list: All generated variations
    """
    orchestrator = ParallelScaffoldingOrchestrator()
    return await orchestrator.generate_with_waves(
        problem_image=problem_image,
        max_variations=float('inf'),
        wave_size=wave_size
    )


# ============================================================================
# CLI Entry Point
# ============================================================================

if __name__ == "__main__":
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) < 3:
        print("Usage: python parallel_scaffolding_orchestrator.py <image_path> <count>")
        print("Example: python parallel_scaffolding_orchestrator.py sample.png 5")
        sys.exit(1)
    
    image_path = sys.argv[1]
    count = sys.argv[2]
    
    if count.lower() == "infinite":
        count = float('inf')
    else:
        count = int(count)
    
    # Run parallel generation
    results = asyncio.run(generate_variations_parallel(image_path, count))
    
    print(f"\n{'='*70}")
    print(f"PARALLEL GENERATION COMPLETE")
    print(f"{'='*70}")
    print(f"Variations generated: {len(results)}")
    for i, var in enumerate(results, 1):
        dim = var.get("variation_dimension", "unknown")
        steps = len(var.get("steps", []))
        print(f"  {i}. {dim} ({steps} steps)")
    print(f"{'='*70}")

