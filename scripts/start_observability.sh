#!/bin/bash
# Observability server starter

cd "$(dirname "$0")/../observability-server"

# Check if already running
if [ -f server.pid ]; then
    PID=$(cat server.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "⚠️  Server already running (PID: $PID)"
        echo "   Health: http://localhost:4000/health"
        exit 0
    fi
fi

# Start server
echo "🚀 Starting observability server..."
nohup python3 server.py > server.log 2>&1 &
SERVER_PID=$!
echo $SERVER_PID > server.pid

# Wait for startup
sleep 3

# Check health
if curl -s http://localhost:4000/health | grep -q "healthy"; then
    echo "✅ Observability server started successfully"
    echo "   PID: $SERVER_PID"
    echo "   Health: http://localhost:4000/health"
    echo "   Events: http://localhost:4000/events/recent"
    echo "   Dashboard: http://localhost:5173 (if dashboard running)"
    echo
    echo "Stop with: kill $SERVER_PID"
    echo "Or: ./scripts/stop_observability.sh"
else
    echo "❌ Server failed to start"
    echo "Check logs: tail -f observability-server/server.log"
    exit 1
fi

