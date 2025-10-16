"""
Mathpix OCR Tool - Mathematical Problem Extraction

Extracts mathematical notation from images using Mathpix API.

VERSION: 1.0.0
DATE: 2025-10-16
API: https://docs.mathpix.com/
"""

import requests
import json
import base64
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import logging

from tools.observability_hook import send_hook_event
from workflows.hook_events import HookEventType

logger = logging.getLogger(__name__)

# Mathpix API Configuration
MATHPIX_APP_ID = "kc_palantir_math"
MATHPIX_APP_KEY = "c89149d2c80f6a6a96e812da4c07d10ba7f74316f26414825ffbb3ed588c34d9"
MATHPIX_API_URL = "https://api.mathpix.com/v3/text"


def extract_math_from_image(image_path: str) -> Dict[str, Any]:
    """
    Extract mathematical notation from image using Mathpix OCR.
    
    Args:
        image_path: Path to image file
        
    Returns:
        dict: {
            "text": "Extracted plain text",
            "latex": "LaTeX notation",
            "confidence": 0.95,
            "success": True
        }
    """
    image_path_obj = Path(image_path)
    
    # Send observability hook: OCR started
    send_hook_event(
        "mathpix_ocr",
        HookEventType.OCR_STARTED,
        {
            "image_path": str(image_path),
            "image_name": image_path_obj.name
        }
    )
    
    logger.info(f"[OCR] Extracting math from {image_path_obj.name}...")
    
    try:
        # Read and encode image
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Prepare API request
        headers = {
            "app_id": MATHPIX_APP_ID,
            "app_key": MATHPIX_APP_KEY,
            "Content-type": "application/json"
        }
        
        payload = {
            "src": f"data:image/png;base64,{image_data}",
            "formats": [
                "text", 
                "latex_styled",
                "data",      # Graph/table data extraction
                "chart"      # Chart coordinate extraction
            ],
            "metadata": {
                "source": "feedback_loop_workflow",
                "timestamp": datetime.now().isoformat(),
                "include_graph_data": True
            }
        }
        
        # Call Mathpix API
        response = requests.post(
            MATHPIX_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract relevant fields
            extracted_data = {
                "text": result.get("text", ""),
                "latex": result.get("latex_styled", ""),
                "data": result.get("data", None),  # Graph/table data
                "chart": result.get("chart", None),  # Chart coordinates
                "confidence": result.get("confidence", 0.0),
                "success": True,
                "has_graph": bool(result.get("data") or result.get("chart")),
                "raw_response": result
            }
            
            # Save OCR result
            output_dir = Path("/home/kc-palantir/math/data/ocr_results")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = output_dir / f"ocr_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(extracted_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"[OCR] Success! Confidence: {extracted_data['confidence']:.2%}")
            logger.info(f"[OCR] Saved to: {output_file}")
            
            # Send observability hook: OCR completed
            send_hook_event(
                "mathpix_ocr",
                HookEventType.OCR_COMPLETED,
                {
                    "confidence": extracted_data["confidence"],
                    "text_length": len(extracted_data["text"]),
                    "latex_length": len(extracted_data["latex"]),
                    "output_file": str(output_file)
                }
            )
            
            return extracted_data
            
        else:
            error_msg = f"API returned status {response.status_code}: {response.text}"
            logger.error(f"[OCR] {error_msg}")
            
            # Send observability hook: OCR failed
            send_hook_event(
                "mathpix_ocr",
                HookEventType.OCR_FAILED,
                {
                    "error": error_msg,
                    "status_code": response.status_code
                }
            )
            
            return {
                "text": "",
                "latex": "",
                "confidence": 0.0,
                "success": False,
                "error": error_msg
            }
            
    except FileNotFoundError:
        error_msg = f"Image file not found: {image_path}"
        logger.error(f"[OCR] {error_msg}")
        
        send_hook_event(
            "mathpix_ocr",
            HookEventType.OCR_FAILED,
            {"error": error_msg}
        )
        
        return {
            "text": "",
            "latex": "",
            "confidence": 0.0,
            "success": False,
            "error": error_msg
        }
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(f"[OCR] {error_msg}")
        
        send_hook_event(
            "mathpix_ocr",
            HookEventType.OCR_FAILED,
            {"error": error_msg}
        )
        
        return {
            "text": "",
            "latex": "",
            "confidence": 0.0,
            "success": False,
            "error": error_msg
        }


if __name__ == "__main__":
    # Test with sample.png
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    test_image = "/home/kc-palantir/math/sample.png"
    result = extract_math_from_image(test_image)
    
    print("\n" + "="*60)
    print("OCR Result:")
    print("="*60)
    print(f"Success: {result['success']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"\nExtracted Text:\n{result['text']}")
    print(f"\nLaTeX:\n{result['latex']}")
    print("="*60)

