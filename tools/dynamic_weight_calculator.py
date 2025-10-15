"""
Dynamic Weight Calculator - Palantir Dynamic Tier

Adaptive metric weighting based on system state (error rate).

Based on:
- Q2-1-1: Error-rate based dynamic adjustment
- Palantir dynamic tier: Runtime optimization

VERSION: 1.0.0
DATE: 2025-10-15
"""

from typing import Dict
from dataclasses import dataclass


@dataclass
class WeightConfiguration:
    """Weight configuration with explanation."""
    quality: float
    efficiency: float
    learning: float
    reason: str
    adjustment_factor: str
    error_rate: float


class DynamicWeightCalculator:
    """
    Palantir Dynamic Tier: Adaptive metric weighting.
    
    Adjusts Quality/Efficiency/Learning weights based on error rate.
    
    Zones:
    - High error (>20%): Focus on Quality
    - Low error (<5%): Focus on Efficiency
    - Normal (5-20%): Balanced
    """
    
    def calculate_weights(
        self,
        error_rate: float,
        session_count: int = 0
    ) -> WeightConfiguration:
        """
        Calculate dynamic weights for result scoring.
        
        Args:
            error_rate: Current error rate (0.0-1.0)
            session_count: Number of sessions (for future enhancements)
        
        Returns:
            WeightConfiguration with adjusted weights
        """
        if error_rate > 0.2:  # Unstable zone
            return WeightConfiguration(
                quality=0.6,
                efficiency=0.2,
                learning=0.2,
                reason='high_error_rate_stability_focus',
                adjustment_factor='quality_+50%',
                error_rate=error_rate
            )
        
        elif error_rate < 0.05:  # Stable zone
            return WeightConfiguration(
                quality=0.3,
                efficiency=0.4,
                learning=0.3,
                reason='low_error_rate_efficiency_focus',
                adjustment_factor='efficiency_+33%',
                error_rate=error_rate
            )
        
        else:  # Normal zone
            return WeightConfiguration(
                quality=0.4,
                efficiency=0.3,
                learning=0.3,
                reason='balanced_standard_weights',
                adjustment_factor='none',
                error_rate=error_rate
            )
    
    def score_result(
        self,
        quality_score: float,
        efficiency_score: float,
        learning_score: float,
        error_rate: float
    ) -> Dict:
        """
        Calculate weighted result score.
        
        Args:
            quality_score: 0-10
            efficiency_score: 0-10
            learning_score: 0-10
            error_rate: 0.0-1.0
        
        Returns:
            Dict with total_score and breakdown
        """
        weights = self.calculate_weights(error_rate)
        
        total_score = (
            quality_score * weights.quality +
            efficiency_score * weights.efficiency +
            learning_score * weights.learning
        )
        
        return {
            'total_score': total_score,
            'weights_used': {
                'quality': weights.quality,
                'efficiency': weights.efficiency,
                'learning': weights.learning,
                'reason': weights.reason
            },
            'breakdown': {
                'quality_contribution': quality_score * weights.quality,
                'efficiency_contribution': efficiency_score * weights.efficiency,
                'learning_contribution': learning_score * weights.learning
            },
            'individual_scores': {
                'quality': quality_score,
                'efficiency': efficiency_score,
                'learning': learning_score
            }
        }

