#!/usr/bin/env python3
"""
Master Test Runner - Run All Tests

Runs all feedback loop tests in sequence and reports results.

VERSION: 1.0.0
DATE: 2025-10-16
"""

import subprocess
import sys
from pathlib import Path
import logging

project_root = Path(__file__).parent.parent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


def run_test(test_file: str, test_name: str) -> bool:
    """
    Run a single test file.
    
    Args:
        test_file: Path to test file
        test_name: Human-readable test name
        
    Returns:
        bool: True if test passed
    """
    print(f"\n{'='*70}")
    print(f"Running: {test_name}")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(
            ["python3", test_file],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            # Check for "100%" or "SUCCESS" in output
            if "100.0%" in result.stdout or "SUCCESS" in result.stdout:
                print(f"✅ {test_name}: PASSED")
                return True
            else:
                print(f"⚠️  {test_name}: Completed but check output")
                print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
                return True
        else:
            print(f"❌ {test_name}: FAILED")
            print("STDOUT:", result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
            print("STDERR:", result.stderr[-500:] if len(result.stderr) > 500 else result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ {test_name}: TIMEOUT (>60s)")
        return False
    except Exception as e:
        print(f"❌ {test_name}: ERROR - {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("MASTER TEST SUITE - Feedback Loop System")
    print("="*70)
    print(f"Project: {project_root}")
    print("="*70)
    
    tests = [
        ("tests/test_main_integration.py", "Main.py Integration (3 tests)"),
        ("tests/test_claude_hooks_integration.py", "Claude Hooks Integration (6 tests)"),
        ("tests/test_feedback_loop_e2e.py", "E2E Test Suite (10 tests)"),
        ("tests/test_actual_problem_scaffolding.py", "Actual Problem Scaffolding"),
        ("tests/test_full_integration.py", "Full Integration Test"),
    ]
    
    results = []
    
    for test_file, test_name in tests:
        passed = run_test(test_file, test_name)
        results.append((test_name, passed))
    
    # Summary
    print(f"\n\n{'='*70}")
    print("MASTER TEST SUMMARY")
    print(f"{'='*70}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    failed = total - passed
    
    for test_name, passed_flag in results:
        status = "✅ PASSED" if passed_flag else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\n{'='*70}")
    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {passed/total*100:.1f}%")
    print(f"{'='*70}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is ready for production.")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Review output above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

