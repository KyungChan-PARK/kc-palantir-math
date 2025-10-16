#!/usr/bin/env python3
"""
Math Scaffolding Workflow CLI Runner

User-friendly script to run the complete math scaffolding workflow with feedback collection.

This workflow generates high-quality scaffolding for math problems through:
- OCR extraction (Mathpix)
- Concept matching (841 concepts)
- Pattern-based scaffolding generation
- Teacher feedback collection (quality assurance)
- Pattern learning (continuous improvement)

Usage:
    python scripts/run_math_scaffolding.py --image sample.png
    python scripts/run_math_scaffolding.py --image 3.png

VERSION: 2.0.0 - Renamed from run_feedback_loop
DATE: 2025-10-16
"""

import asyncio
import argparse
import logging
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from workflows.math_scaffolding_workflow import run_math_scaffolding_workflow


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run math scaffolding workflow on math problem image"
    )
    
    parser.add_argument(
        "--image",
        type=str,
        required=True,
        help="Path to problem image (e.g., sample.png)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Validate image path
    image_path = Path(args.image)
    if not image_path.exists():
        print(f"❌ Error: Image file not found: {image_path}")
        sys.exit(1)
    
    # Run workflow
    result = asyncio.run(run_math_scaffolding_workflow(str(image_path)))
    
    # Exit with appropriate code
    if result.get("success"):
        print("\n✅ Workflow completed successfully!")
        sys.exit(0)
    else:
        print(f"\n❌ Workflow failed: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()

