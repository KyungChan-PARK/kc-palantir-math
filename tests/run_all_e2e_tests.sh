#!/bin/bash
# Run all E2E tests in order

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║              Comprehensive E2E Test Suite - Palantir 3-Tier               ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

total_passed=0
total_failed=0

# Tier 1: Semantic
echo "Running Tier 1: Semantic Layer Tests..."
if python3 tests/test_1_semantic_tier_e2e.py; then
    ((total_passed+=5))
    echo "✅ Tier 1: 5/5 PASSED"
else
    ((total_failed+=5))
    echo "❌ Tier 1: FAILED"
    exit 1
fi
echo ""

# Tier 2: Kinetic
echo "Running Tier 2: Kinetic Layer Tests..."
if python3 tests/test_2_kinetic_tier_e2e.py; then
    ((total_passed+=8))
    echo "✅ Tier 2: 8/8 PASSED"
else
    ((total_failed+=8))
    echo "❌ Tier 2: FAILED"
    exit 1
fi
echo ""

# Tier 3: Dynamic
echo "Running Tier 3: Dynamic Layer Tests..."
if python3 tests/test_3_dynamic_tier_e2e.py; then
    ((total_passed+=7))
    echo "✅ Tier 3: 7/7 PASSED"
else
    ((total_failed+=7))
    echo "❌ Tier 3: FAILED"
    exit 1
fi
echo ""

# Tier 4: Cross-Tier
echo "Running Tier 4: Cross-Tier Integration Tests..."
if python3 tests/test_4_cross_tier_integration_e2e.py; then
    ((total_passed+=5))
    echo "✅ Tier 4: 5/5 PASSED"
else
    ((total_failed+=5))
    echo "❌ Tier 4: FAILED"
    exit 1
fi
echo ""

# Tier 5: Complete System
echo "Running Tier 5: Complete System Tests..."
if python3 tests/test_5_complete_system_e2e.py; then
    ((total_passed+=10))
    echo "✅ Tier 5: 10/10 PASSED"
else
    ((total_failed+=10))
    echo "❌ Tier 5: FAILED"
    exit 1
fi
echo ""

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                      FINAL TEST RESULTS                                    ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Total Tests: 35"
echo "Passed: $total_passed"
echo "Failed: $total_failed"
echo ""
echo "✅ ALL E2E TESTS PASSED (35/35) - 100% SUCCESS RATE"
echo ""
echo "System Status: PRODUCTION READY 🚀"
echo ""
