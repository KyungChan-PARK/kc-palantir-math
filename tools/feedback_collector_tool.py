"""
User Feedback Collector - Captures structured user feedback

Based on:
- Q1-1: Structured feedback format (1-10 scoring)
- claude-code-2-0-deduplicated-final.md lines 8173-8234 (continuous conversation)

VERSION: 1.0.0
DATE: 2025-10-15
"""

import re
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class UserFeedback:
    """Structured user feedback."""
    accuracy: float  # 1-10
    efficiency: float  # 1-10
    user_confirmed: bool  # "정확합니다" detected
    corrections: Optional[str] = None
    raw_response: str = ""


class UserFeedbackCollector:
    """
    Captures structured user feedback in continuous conversation.
    
    Pattern: async with ClaudeSDKClient for multi-turn feedback collection
    """
    
    def format_feedback_request(self, summary: str) -> str:
        """
        Format feedback request for user.
        
        Based on Q1-1: C (Structured feedback format)
        """
        return f"""
{'='*70}
UNDERSTANDING CONFIRMATION
{'='*70}

{summary}

평가해주세요:
- 정확도 (1-10): 
- 효율성 (1-10):

또는 "정확합니다" 입력 시 10/10으로 처리됩니다.
수정사항이 있다면 설명해주세요.
{'='*70}
"""
    
    def parse_feedback(self, user_response: str) -> UserFeedback:
        """
        Parse user feedback from text response.
        
        Handles multiple formats:
        - "정확합니다" → 10/10
        - "정확도: 9, 효율성: 8" → 9/8
        - "9, 8" → 9/8
        - "수정: X를 Y로" → Extract corrections
        """
        text = user_response.strip()
        
        # Check for confirmation
        confirmation_keywords = ['정확', '확인', '맞습니다', '좋습니다', 'correct', 'yes']
        confirmed = any(keyword in text.lower() for keyword in confirmation_keywords)
        
        if confirmed and len(text) < 20:  # Short confirmation
            return UserFeedback(
                accuracy=10.0,
                efficiency=10.0,
                user_confirmed=True,
                raw_response=text
            )
        
        # Parse structured format
        accuracy_match = re.search(r'정확.*?(\d+)', text)
        efficiency_match = re.search(r'효율.*?(\d+)', text)
        
        # Try comma-separated format
        if not (accuracy_match and efficiency_match):
            numbers = re.findall(r'\d+', text)
            if len(numbers) >= 2:
                accuracy_match = numbers[0]
                efficiency_match = numbers[1]
        
        accuracy = float(accuracy_match.group(1) if hasattr(accuracy_match, 'group') else accuracy_match) if accuracy_match else 7.0
        efficiency = float(efficiency_match.group(1) if hasattr(efficiency_match, 'group') else efficiency_match) if efficiency_match else 7.0
        
        # Extract corrections
        corrections = None
        correction_keywords = ['수정', '아니', '잘못', '변경', 'correction', 'change']
        if any(keyword in text.lower() for keyword in correction_keywords):
            corrections = text
        
        return UserFeedback(
            accuracy=min(accuracy, 10.0),
            efficiency=min(efficiency, 10.0),
            user_confirmed=confirmed,
            corrections=corrections,
            raw_response=text
        )
    
    def calculate_user_satisfaction_score(self, feedback: UserFeedback) -> float:
        """
        Calculate satisfaction score (0-10) for quality calculation.
        
        Used in multi-dimensional quality score:
        Quality = (Precision × 0.4) + (Efficiency × 0.3) + (Satisfaction × 0.3)
        """
        # Average of accuracy and efficiency
        satisfaction = (feedback.accuracy + feedback.efficiency) / 2
        
        # Penalize if corrections needed
        if feedback.corrections:
            satisfaction *= 0.8  # 20% penalty
        
        # Boost if explicitly confirmed
        if feedback.user_confirmed:
            satisfaction = min(satisfaction * 1.1, 10.0)  # 10% bonus
        
        return satisfaction

