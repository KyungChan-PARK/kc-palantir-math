"""
Infinite Feedback Loop - Continuous Improvement Cycle

Implements continuous generation → feedback → learning → improvement cycle
with progressive specification evolution.

VERSION: 1.0.0
DATE: 2025-10-16
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from workflows.parallel_scaffolding_orchestrator import ParallelScaffoldingOrchestrator
from workflows.scaffolding_variation_engine import VariationEngine
from tools.observability_hook import send_hook_event
from workflows.hook_events import HookEventType

logger = logging.getLogger(__name__)


# ============================================================================
# Specification Evolution
# ============================================================================

class SpecificationEvolutionEngine:
    """Evolves specifications based on feedback and meta-patterns."""
    
    def __init__(self, base_spec_file: str):
        """
        Initialize evolution engine.
        
        Args:
            base_spec_file: Path to base specification
        """
        self.base_spec_file = Path(base_spec_file)
        self.evolution_history: List[Dict] = []
        self.current_priorities: List[str] = []
    
    def evolve_spec(
        self,
        feedback_results: List[Dict],
        meta_patterns: List[Dict]
    ) -> Dict[str, Any]:
        """
        Evolve specification based on feedback and patterns.
        
        Args:
            feedback_results: Feedback from latest wave
            meta_patterns: Extracted meta-patterns
            
        Returns:
            dict: Evolved specification
        """
        logger.info(f"[SpecEvolution] Evolving specification from {len(feedback_results)} feedback results")
        
        # Analyze feedback to identify high-performing dimensions
        dimension_ratings = {}
        for feedback in feedback_results:
            dim = feedback.get("variation_dimension", "unknown")
            rating = feedback.get("overall_rating", 0)
            
            if dim not in dimension_ratings:
                dimension_ratings[dim] = []
            dimension_ratings[dim].append(rating)
        
        # Calculate average ratings
        avg_ratings = {
            dim: sum(ratings) / len(ratings)
            for dim, ratings in dimension_ratings.items()
        }
        
        # Identify top performers
        top_dimensions = sorted(avg_ratings.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Update priorities for next wave
        self.current_priorities = [dim for dim, _ in top_dimensions]
        
        # Create evolved spec
        evolution = {
            "base_spec": str(self.base_spec_file),
            "evolution_iteration": len(self.evolution_history) + 1,
            "priority_dimensions": self.current_priorities,
            "dimension_performance": avg_ratings,
            "meta_patterns_incorporated": len(meta_patterns),
            "evolved_at": datetime.now().isoformat(),
            "recommended_combinations": self._recommend_combinations(top_dimensions)
        }
        
        self.evolution_history.append(evolution)
        
        logger.info(f"[SpecEvolution] Top dimensions: {self.current_priorities}")
        
        return evolution
    
    def _recommend_combinations(self, top_dimensions: List[tuple]) -> List[str]:
        """Recommend dimension combinations for next wave."""
        if len(top_dimensions) < 2:
            return []
        
        # Create pairwise combinations of top performers
        combinations = []
        for i in range(min(2, len(top_dimensions))):
            for j in range(i+1, min(3, len(top_dimensions))):
                dim1, rating1 = top_dimensions[i]
                dim2, rating2 = top_dimensions[j]
                combinations.append(f"{dim1}+{dim2}")
        
        return combinations


# ============================================================================
# Meta-Pattern Extraction
# ============================================================================

class MetaPatternExtractor:
    """Extracts meta-patterns from multiple variations."""
    
    def __init__(self):
        self.extracted_patterns: List[Dict] = []
    
    async def extract_meta_patterns(
        self,
        variations: List[Dict],
        feedback_results: List[Dict]
    ) -> List[Dict[str, Any]]:
        """
        Extract meta-patterns from variation analysis.
        
        Args:
            variations: All variations in this cycle
            feedback_results: Feedback for each variation
            
        Returns:
            list: Extracted meta-patterns
        """
        logger.info(f"[MetaPattern] Extracting patterns from {len(variations)} variations")
        
        meta_patterns = []
        
        # Pattern 1: Identify consistently high-rated step sequences
        step_sequences = self._extract_step_sequence_patterns(variations, feedback_results)
        meta_patterns.extend(step_sequences)
        
        # Pattern 2: Identify effective dimension combinations
        dimension_patterns = self._extract_dimension_effectiveness(variations, feedback_results)
        meta_patterns.extend(dimension_patterns)
        
        # Pattern 3: Identify optimal hint strategies
        hint_patterns = self._extract_hint_patterns(variations, feedback_results)
        meta_patterns.extend(hint_patterns)
        
        self.extracted_patterns.extend(meta_patterns)
        
        logger.info(f"[MetaPattern] Extracted {len(meta_patterns)} meta-patterns")
        
        return meta_patterns
    
    def _extract_step_sequence_patterns(
        self,
        variations: List[Dict],
        feedback_results: List[Dict]
    ) -> List[Dict]:
        """Extract common high-quality step sequences."""
        patterns = []
        
        # Find high-rated variations (rating >= 4.0)
        high_rated = [
            var for var, fb in zip(variations, feedback_results)
            if fb.get("overall_rating", 0) >= 4.0
        ]
        
        if len(high_rated) < 2:
            return patterns
        
        # Analyze step count patterns
        step_counts = [len(v.get("steps", [])) for v in high_rated]
        avg_step_count = sum(step_counts) / len(step_counts)
        
        pattern = {
            "meta_pattern_id": f"mp_optimal_step_count_{int(avg_step_count)}",
            "type": "structural",
            "description": f"High-rated variations average {avg_step_count:.1f} steps",
            "evidence": [v.get("variation_iteration") for v in high_rated],
            "avg_rating": sum(fb.get("overall_rating", 0) for fb in feedback_results if fb.get("overall_rating", 0) >= 4.0) / len(high_rated),
            "applicability": "general",
            "discovered_at": datetime.now().isoformat()
        }
        
        patterns.append(pattern)
        
        return patterns
    
    def _extract_dimension_effectiveness(
        self,
        variations: List[Dict],
        feedback_results: List[Dict]
    ) -> List[Dict]:
        """Extract which dimensions perform best."""
        dimension_ratings = {}
        
        for var, fb in zip(variations, feedback_results):
            dim = var.get("variation_dimension", "unknown")
            rating = fb.get("overall_rating", 0)
            
            if dim not in dimension_ratings:
                dimension_ratings[dim] = []
            dimension_ratings[dim].append(rating)
        
        patterns = []
        for dim, ratings in dimension_ratings.items():
            if len(ratings) >= 2:  # Need at least 2 samples
                avg_rating = sum(ratings) / len(ratings)
                
                if avg_rating >= 4.0:  # Only extract if high quality
                    pattern = {
                        "meta_pattern_id": f"mp_dimension_{dim}_effective",
                        "type": "pedagogical",
                        "description": f"Dimension '{dim}' consistently performs well (avg {avg_rating:.2f}/5.0)",
                        "dimension": dim,
                        "avg_rating": avg_rating,
                        "sample_size": len(ratings),
                        "applicability": "dimension_selection",
                        "discovered_at": datetime.now().isoformat()
                    }
                    patterns.append(pattern)
        
        return patterns
    
    def _extract_hint_patterns(
        self,
        variations: List[Dict],
        feedback_results: List[Dict]
    ) -> List[Dict]:
        """Extract effective hint strategies."""
        # Simplified: Would analyze hint text and effectiveness
        # For now, return empty
        return []


# ============================================================================
# Infinite Improvement Loop
# ============================================================================

async def run_infinite_improvement_loop(
    problem_image: str,
    spec_file: str = "specs/scaffolding_spec_v1.md",
    max_iterations: int = None,
    wave_size: int = 3
) -> Dict[str, Any]:
    """
    Run continuous improvement loop: generate → feedback → learn → evolve.
    
    Args:
        problem_image: Path to math problem image
        spec_file: Specification file path
        max_iterations: Maximum waves (None = infinite)
        wave_size: Variations per wave
        
    Returns:
        dict: Complete loop results
    """
    logger.info(f"[InfiniteLoop] Starting continuous improvement loop")
    logger.info(f"[InfiniteLoop] Image: {problem_image}, Spec: {spec_file}, Wave size: {wave_size}")
    
    # Initialize components
    orchestrator = ParallelScaffoldingOrchestrator()
    spec_evolution = SpecificationEvolutionEngine(spec_file)
    meta_extractor = MetaPatternExtractor()
    
    all_variations = []
    all_meta_patterns = []
    wave_number = 0
    
    # Prepare shared context once
    shared_context = await orchestrator.prepare_shared_context(problem_image)
    
    while True:
        wave_number += 1
        logger.info(f"\n{'='*70}")
        logger.info(f"WAVE {wave_number}")
        logger.info(f"{'='*70}")
        
        # GENERATE variations for this wave
        logger.info(f"[InfiniteLoop] Generating {wave_size} variations...")
        
        dimensions = orchestrator.variation_engine.assign_dimensions(
            count=wave_size,
            existing_variations=all_variations,
            prefer_high_rated=(wave_number > 1)
        )
        
        wave_variations = await orchestrator._execute_parallel_wave(
            shared_context=shared_context,
            dimensions=dimensions,
            existing_variations=all_variations
        )
        
        # All variations from wave are unique (different dimensions assigned)
        # Add them all to our collection
        unique_variations = wave_variations
        all_variations.extend(wave_variations)
        
        # Save variations
        problem_id = orchestrator._get_problem_id(shared_context)
        for var in wave_variations:
            orchestrator._save_variation(var, problem_id)
        
        logger.info(f"[InfiniteLoop] Generated {len(unique_variations)} unique variations")
        
        # FEEDBACK collection (simulated for now - would be parallel CLI or web-based)
        logger.info(f"[InfiniteLoop] Collecting feedback...")
        
        send_hook_event(
            "infinite_loop",
            "parallel_feedback_started",
            {"variation_count": len(unique_variations)}
        )
        
        # Simulated feedback (in production, would collect from teacher)
        feedback_results = []
        for var in unique_variations:
            feedback = {
                "variation_dimension": var.get("variation_dimension"),
                "variation_iteration": var.get("variation_iteration"),
                "overall_rating": 4.0 + (wave_number * 0.1),  # Simulated improvement
                "quality_score": 0.8,
                "comments": f"Variation {var.get('variation_iteration')} feedback"
            }
            feedback_results.append(feedback)
            
            # Record dimension performance
            orchestrator.variation_engine.record_dimension_performance(
                var.get("variation_dimension"),
                feedback["overall_rating"]
            )
        
        avg_rating = sum(f["overall_rating"] for f in feedback_results) / len(feedback_results) if feedback_results else 0
        
        send_hook_event(
            "infinite_loop",
            "parallel_feedback_completed",
            {"avg_rating": avg_rating}
        )
        
        # LEARN meta-patterns
        logger.info(f"[InfiniteLoop] Extracting meta-patterns...")
        
        wave_meta_patterns = await meta_extractor.extract_meta_patterns(
            unique_variations,
            feedback_results
        )
        
        for pattern in wave_meta_patterns:
            send_hook_event(
                "infinite_loop",
                "meta_pattern_extracted",
                {
                    "pattern_id": pattern.get("meta_pattern_id"),
                    "type": pattern.get("type")
                }
            )
        
        all_meta_patterns.extend(wave_meta_patterns)
        
        logger.info(f"[InfiniteLoop] Extracted {len(wave_meta_patterns)} meta-patterns")
        
        # EVOLVE specification
        logger.info(f"[InfiniteLoop] Evolving specification...")
        
        evolved_spec = spec_evolution.evolve_spec(feedback_results, wave_meta_patterns)
        
        send_hook_event(
            "infinite_loop",
            "spec_evolved",
            {
                "evolution_iteration": evolved_spec["evolution_iteration"],
                "top_dimensions": evolved_spec["priority_dimensions"]
            }
        )
        
        # Check continuation criteria
        if max_iterations and wave_number >= max_iterations:
            logger.info(f"[InfiniteLoop] Reached max iterations: {max_iterations}")
            break
        
        # Simulated context check (in production, would check actual context usage)
        if wave_number >= 5:  # Safety limit for testing
            logger.info(f"[InfiniteLoop] Reached safety limit of 5 waves")
            break
        
        # Check quality maintenance
        avg_quality = sum(f["overall_rating"] for f in feedback_results) / len(feedback_results)
        if avg_quality < 3.5:
            logger.warning(f"[InfiniteLoop] Quality declining (avg {avg_quality:.2f}), stopping")
            break
        
        logger.info(f"[InfiniteLoop] Wave {wave_number} complete. Quality: {avg_quality:.2f}/5.0")
        logger.info(f"[InfiniteLoop] Continuing to next wave...\n")
    
    # Final summary
    logger.info(f"\n{'='*70}")
    logger.info(f"INFINITE IMPROVEMENT LOOP COMPLETE")
    logger.info(f"{'='*70}")
    logger.info(f"Total waves: {wave_number}")
    logger.info(f"Total variations: {len(all_variations)}")
    logger.info(f"Total meta-patterns: {len(all_meta_patterns)}")
    logger.info(f"Specification evolutions: {len(spec_evolution.evolution_history)}")
    
    return {
        "success": True,
        "waves_completed": wave_number,
        "total_variations": len(all_variations),
        "variations": all_variations,
        "meta_patterns": all_meta_patterns,
        "spec_evolutions": spec_evolution.evolution_history,
        "final_avg_quality": avg_quality
    }


# ============================================================================
# CLI Entry Point
# ============================================================================

if __name__ == "__main__":
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    if len(sys.argv) < 2:
        print("Usage: python infinite_feedback_loop.py <image_path> [max_waves]")
        print("Example: python infinite_feedback_loop.py sample.png 5")
        print("Example: python infinite_feedback_loop.py 3.png infinite")
        sys.exit(1)
    
    image_path = sys.argv[1]
    max_waves = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] != "infinite" else None
    
    # Run infinite loop
    result = asyncio.run(run_infinite_improvement_loop(
        problem_image=image_path,
        max_iterations=max_waves,
        wave_size=3
    ))
    
    print(f"\n{'='*70}")
    print(f"Final Results:")
    print(f"  Waves: {result['waves_completed']}")
    print(f"  Variations: {result['total_variations']}")
    print(f"  Meta-patterns: {len(result['meta_patterns'])}")
    print(f"  Final Quality: {result['final_avg_quality']:.2f}/5.0")
    print(f"{'='*70}")

