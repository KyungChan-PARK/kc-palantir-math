#!/bin/bash

# Math Education Feedback Loop System - Quick Start Script
# VERSION: 3.2.0
# DATE: 2025-10-16

set -e

echo "========================================================================"
echo "Math Education Feedback Loop System - Quick Start"
echo "========================================================================"
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check prerequisites
echo "${YELLOW}[Step 1/4] Checking prerequisites...${NC}"
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 not found"; exit 1; }
command -v uv >/dev/null 2>&1 || { echo "❌ uv not found"; exit 1; }
echo "${GREEN}✅ Prerequisites OK${NC}"
echo ""

# Step 2: Stop any running servers
echo "${YELLOW}[Step 2/4] Stopping existing servers...${NC}"
pkill -f "server.py" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true
sleep 2
echo "${GREEN}✅ Servers stopped${NC}"
echo ""

# Step 3: Start Observability Server
echo "${YELLOW}[Step 3/4] Starting Observability Server...${NC}"
cd /home/kc-palantir/math/observability-server
nohup uv run python server.py > /tmp/obs_server.log 2>&1 &
SERVER_PID=$!
echo $SERVER_PID > /home/kc-palantir/math/server.pid

sleep 3

# Verify server is running
if curl -s http://localhost:4000/health | grep -q "healthy"; then
    echo "${GREEN}✅ Observability Server running (PID: $SERVER_PID)${NC}"
    echo "   URL: http://localhost:4000"
    echo "   WebSocket: ws://localhost:4000/stream"
    echo "   Log: /tmp/obs_server.log"
else
    echo "❌ Server failed to start"
    cat /tmp/obs_server.log
    exit 1
fi
echo ""

# Step 4: Ready to use
echo "${YELLOW}[Step 4/4] System Ready${NC}"
echo ""
echo "========================================================================"
echo "${GREEN}✅ System is ready!${NC}"
echo "========================================================================"
echo ""
echo "Quick Commands:"
echo ""
echo "  # Run all tests:"
echo "  cd /home/kc-palantir/math && python3 tests/run_all_tests.py"
echo ""
echo "  # Run feedback loop:"
echo "  cd /home/kc-palantir/math && python3 scripts/run_feedback_loop.py --image sample.png"
echo ""
echo "  # Run main agent:"
echo "  cd /home/kc-palantir/math && uv run python main.py"
echo ""
echo "  # View dashboard (optional):"
echo "  cd /home/kc-palantir/math/observability-dashboard && bun run dev"
echo "  # Then open: http://localhost:3000"
echo ""
echo "  # Stop server:"
echo "  kill \$(cat /home/kc-palantir/math/server.pid)"
echo ""
echo "========================================================================"

