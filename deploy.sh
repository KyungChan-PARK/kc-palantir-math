#!/bin/bash
"""
Production Deployment Script

Deploys Math Education Multi-Agent System with runtime capabilities.

Steps:
1. Pre-deployment validation
2. Build Docker containers
3. Start services
4. Health checks
5. Smoke tests

VERSION: 1.0.0
DATE: 2025-10-16
"""

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║          Math Education System - Production Deployment              ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo

# Check prerequisites
echo "=== Pre-Deployment Validation ==="
echo

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not installed"
    exit 1
fi
echo "✓ Docker: $(docker --version | head -1)"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not installed"
    exit 1
fi
echo "✓ Docker Compose: $(docker-compose --version | head -1)"

# Check API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY not set"
    echo "   Set with: export ANTHROPIC_API_KEY=sk-ant-..."
    echo "   Or create .env file"
    read -p "   Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✓ ANTHROPIC_API_KEY: set (${#ANTHROPIC_API_KEY} chars)"
fi

# Check tests
echo
echo "=== Running Tests ==="
echo
python3 -m pytest tests/test_runtime_integration.py -q
if [ $? -ne 0 ]; then
    echo "❌ Tests failed"
    exit 1
fi
echo "✓ All tests passing"

# Build containers
echo
echo "=== Building Docker Containers ==="
echo
docker-compose build
echo "✓ Containers built"

# Start services
echo
echo "=== Starting Services ==="
echo
docker-compose up -d

# Wait for services to be ready
echo
echo "=== Health Checks ==="
echo

sleep 5

# Check observability server
echo -n "Observability server: "
if curl -s http://localhost:4000/health | grep -q "healthy"; then
    echo "✓ Healthy"
else
    echo "❌ Not responding"
    docker-compose logs observability-server
    exit 1
fi

# Check math system container
echo -n "Math agent system: "
if docker ps | grep -q math-agents; then
    echo "✓ Running"
else
    echo "❌ Not running"
    docker-compose logs math-agent-system
    exit 1
fi

# Smoke test - send test event
echo
echo "=== Smoke Test ==="
echo

curl -X POST http://localhost:4000/events \
  -H "Content-Type: application/json" \
  -d '{
    "source_app": "deployment-test",
    "session_id": "test-001",
    "hook_event_type": "SessionStart",
    "payload": {"test": true}
  }' 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ Observability event POST successful"
else
    echo "❌ Event POST failed"
    exit 1
fi

# Query events
EVENTS=$(curl -s http://localhost:4000/events/recent?limit=1)
if echo "$EVENTS" | grep -q "test-001"; then
    echo "✓ Event stored and retrievable"
else
    echo "❌ Event not stored"
fi

# Final status
echo
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                    DEPLOYMENT SUCCESSFUL                             ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo
echo "Services:"
echo "  Observability Server: http://localhost:4000"
echo "    - Health: http://localhost:4000/health"
echo "    - Events: http://localhost:4000/events/recent"
echo "    - Sessions: http://localhost:4000/events/sessions"
echo
echo "  Math Agent System: Running in container"
echo "    - Logs: docker-compose logs -f math-agent-system"
echo "    - Shell: docker-compose exec math-agent-system bash"
echo
echo "Management:"
echo "  View logs: docker-compose logs -f"
echo "  Stop: docker-compose down"
echo "  Restart: docker-compose restart"
echo "  Status: docker-compose ps"
echo
echo "✅ System ready for production use"

