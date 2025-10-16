"""
Claude Vision Tool - Graph and Diagram Analysis

Uses Claude's multimodal capabilities to analyze mathematical graphs and diagrams.

VERSION: 1.0.0
DATE: 2025-10-16
"""

import anthropic
import base64
import json
import os
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def analyze_graph_with_vision(image_path: str, problem_context: str = "") -> Dict[str, Any]:
    """
    Analyze mathematical graph using Claude Vision API.
    
    Args:
        image_path: Path to image file
        problem_context: Optional context about the problem
        
    Returns:
        dict: {
            "graph_type": "linear_function",
            "equation": "y = 2x + 1",
            "key_points": [[0, 1], [1, 3], [2, 5]],
            "intercepts": {"x": -0.5, "y": 1},
            "slope": 2,
            "features": ["passes through (0,1)", ...],
            "confidence": 0.95
        }
    """
    logger.info(f"[Vision] Analyzing graph from {Path(image_path).name}...")
    
    try:
        # Get API key
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        
        client = anthropic.Anthropic(api_key=api_key)
        
        # Read and encode image
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        # Construct prompt
        analysis_prompt = f"""Analyze this mathematical graph/diagram image.

{f'Problem Context: {problem_context}' if problem_context else ''}

Extract and return in JSON format:
{{
  "graph_type": "linear_function|quadratic_function|coordinate_plane|etc",
  "equation": "equation of the function (if visible)",
  "key_points": [[x1, y1], [x2, y2], ...],  // Important points on graph
  "intercepts": {{"x": x_value, "y": y_value}},  // Where graph crosses axes
  "slope": number,  // For linear functions
  "vertex": [x, y],  // For quadratic functions
  "domain": "description",
  "range": "description",
  "features": ["feature1", "feature2", ...],  // Notable characteristics
  "geometric_shapes": ["triangle", "quadrilateral", ...],  // If geometric problem
  "measurements": {{"area": ..., "perimeter": ..., "angles": [...]}},  // If applicable
  "confidence": 0.0-1.0  // Your confidence in the analysis
}}

Be precise with numerical values. If uncertain, note it in confidence."""

        # Call Claude Vision API
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": analysis_prompt
                    }
                ]
            }]
        )
        
        # Extract JSON from response
        response_text = response.content[0].text
        
        # Try to parse JSON
        try:
            # Find JSON in response (might have explanatory text)
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                graph_data = json.loads(json_str)
            else:
                # Fallback: return full text
                graph_data = {"analysis": response_text, "confidence": 0.5}
        
        except json.JSONDecodeError:
            # Return raw analysis if JSON parsing fails
            graph_data = {"analysis": response_text, "confidence": 0.5}
        
        logger.info(f"[Vision] Analysis completed: {graph_data.get('graph_type', 'unknown')}")
        
        return {
            "success": True,
            "graph_data": graph_data,
            "raw_response": response_text
        }
        
    except FileNotFoundError:
        logger.error(f"[Vision] Image not found: {image_path}")
        return {
            "success": False,
            "error": f"Image not found: {image_path}"
        }
    
    except Exception as e:
        logger.error(f"[Vision] Error: {e}")
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    # Test with sample.png
    import logging
    logging.basicConfig(level=logging.INFO)
    
    test_image = "/home/kc-palantir/math/sample.png"
    result = analyze_graph_with_vision(
        test_image,
        problem_context="좌표평면에서 삼각형의 넓이 구하기"
    )
    
    print("\n" + "="*60)
    print("Claude Vision Analysis:")
    print("="*60)
    print(f"Success: {result.get('success')}")
    
    if result.get('success'):
        graph_data = result.get('graph_data', {})
        print(f"\nGraph Type: {graph_data.get('graph_type')}")
        print(f"Equation: {graph_data.get('equation')}")
        print(f"Key Points: {graph_data.get('key_points')}")
        print(f"Confidence: {graph_data.get('confidence')}")
    else:
        print(f"Error: {result.get('error')}")
    
    print("="*60)

