#!/bin/bash
# Observability server stopper

cd "$(dirname "$0")/../observability-server"

if [ -f server.pid ]; then
    PID=$(cat server.pid)
    if ps -p $PID > /dev/null 2>&1; then
        kill $PID
        rm server.pid
        echo "✅ Observability server stopped (PID: $PID)"
    else
        echo "⚠️  Server not running (stale PID file removed)"
        rm server.pid
    fi
else
    echo "⚠️  No PID file found - server may not be running"
fi

