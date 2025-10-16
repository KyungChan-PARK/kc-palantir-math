#!/usr/bin/env python3
"""
Lightweight Observability Server

Minimal event collection server for Claude Code hook events.
Stores events in SQLite, provides query API.

Based on: disler/claude-code-hooks-multi-agent-observability architecture
Implementation: Simplified Python version (100 lines vs 1000+ line TypeScript)

Usage:
    python3 server.py
    # Server starts on http://localhost:4000

API:
    POST /events - Receive hook events
    GET /events/recent?limit=100 - Query recent events
    GET /health - Health check

VERSION: 1.0.0
DATE: 2025-10-16
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict, Any, List, Optional, Set
from contextlib import asynccontextmanager
import sqlite3
import json
from datetime import datetime
from pathlib import Path
import uvicorn
import asyncio


# Event schema (enhanced with session metadata)
class ObservabilityEvent(BaseModel):
    source_app: str
    session_id: str
    hook_event_type: str
    payload: Dict[str, Any]
    chat: Optional[List[Dict]] = None
    summary: Optional[str] = None
    session_name: Optional[str] = None  # Human-readable session name
    session_context: Optional[Dict[str, Any]] = None  # Additional context


# Database path
DB_PATH = Path(__file__).parent / "data" / "events.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# WebSocket clients storage
websocket_clients: Set[WebSocket] = set()


def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            source_app TEXT NOT NULL,
            session_id TEXT NOT NULL,
            hook_event_type TEXT NOT NULL,
            payload TEXT NOT NULL,
            chat TEXT,
            summary TEXT,
            session_name TEXT,
            session_context TEXT
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_session ON events(session_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON events(timestamp)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_event_type ON events(hook_event_type)")
    conn.commit()
    conn.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler (replaces deprecated on_event)"""
    # Startup
    init_db()
    print("✅ Observability server started")
    print(f"   Database: {DB_PATH}")
    print(f"   Listening on: http://localhost:4000")
    print(f"   WebSocket endpoint: ws://localhost:4000/stream")
    yield
    # Shutdown
    print("👋 Observability server shutting down")


# FastAPI app with lifespan
app = FastAPI(
    title="Math System Observability Server",
    lifespan=lifespan
)


@app.post("/events")
async def receive_event(event: ObservabilityEvent):
    """
    Receive and store hook event.
    
    Schema matches disler/claude-code-hooks-multi-agent-observability.
    Broadcasts to WebSocket clients in real-time.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.execute("""
            INSERT INTO events (timestamp, source_app, session_id, hook_event_type, payload, chat, summary, session_name, session_context)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            event.source_app,
            event.session_id,
            event.hook_event_type,
            json.dumps(event.payload),
            json.dumps(event.chat) if event.chat else None,
            event.summary,
            event.session_name,
            json.dumps(event.session_context) if event.session_context else None
        ))
        event_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Prepare event for broadcast
        broadcast_event = {
            "id": event_id,
            "timestamp": datetime.now().isoformat(),
            "source_app": event.source_app,
            "session_id": event.session_id,
            "hook_event_type": event.hook_event_type,
            "payload": event.payload,
            "chat": event.chat,
            "summary": event.summary,
            "session_name": event.session_name,
            "session_context": event.session_context
        }
        
        # Broadcast to all WebSocket clients
        if websocket_clients:
            message = json.dumps({"type": "event", "data": broadcast_event})
            disconnected = set()
            
            for client in websocket_clients:
                try:
                    await client.send_text(message)
                except:
                    disconnected.add(client)
            
            # Remove disconnected clients
            websocket_clients.difference_update(disconnected)
        
        return {"status": "ok", "event_type": event.hook_event_type, "id": event_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/events/recent")
async def get_recent_events(
    limit: int = 100,
    session_id: Optional[str] = None,
    event_type: Optional[str] = None
):
    """
    Query recent events with optional filtering.
    
    Args:
        limit: Maximum events to return (default 100)
        session_id: Filter by session ID
        event_type: Filter by hook event type
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        
        # Build query with filters
        query = "SELECT id, timestamp, source_app, session_id, hook_event_type, payload, chat, summary, session_name, session_context FROM events WHERE 1=1"
        params = []
        
        if session_id:
            query += " AND session_id = ?"
            params.append(session_id)
        
        if event_type:
            query += " AND hook_event_type = ?"
            params.append(event_type)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor = conn.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        # Convert to dict format
        events = []
        for row in rows:
            events.append({
                "id": row[0],
                "timestamp": row[1],
                "source_app": row[2],
                "session_id": row[3],
                "hook_event_type": row[4],
                "payload": json.loads(row[5]) if row[5] else {},
                "chat": json.loads(row[6]) if row[6] and row[6] != 'null' else None,
                "summary": row[7] if row[7] and row[7] != 'null' else None,
                "session_name": row[8] if row[8] and row[8] != 'null' else None,
                "session_context": json.loads(row[9]) if row[9] and row[9] != 'null' else None
            })
        
        return {"events": events, "count": len(events)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/events/sessions")
async def get_sessions():
    """Get list of all session IDs"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.execute("""
            SELECT DISTINCT session_id, 
                   COUNT(*) as event_count,
                   MIN(timestamp) as first_event,
                   MAX(timestamp) as last_event
            FROM events
            GROUP BY session_id
            ORDER BY last_event DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        
        sessions = []
        for row in rows:
            sessions.append({
                "session_id": row[0],
                "event_count": row[1],
                "first_event": row[2],
                "last_event": row[3]
            })
        
        return {"sessions": sessions}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time event streaming.
    Compatible with indydevdan dashboard.
    """
    await websocket.accept()
    websocket_clients.add(websocket)
    
    print(f"✅ WebSocket client connected (total: {len(websocket_clients)})")
    
    try:
        # Send recent 50 events on connection
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.execute("""
            SELECT id, timestamp, source_app, session_id, hook_event_type, payload, chat, summary, session_name, session_context
            FROM events 
            ORDER BY timestamp DESC 
            LIMIT 50
        """)
        rows = cursor.fetchall()
        conn.close()
        
        # Format events
        initial_events = []
        for row in rows:
            initial_events.append({
                "id": row[0],
                "timestamp": row[1],
                "source_app": row[2],
                "session_id": row[3],
                "hook_event_type": row[4],
                "payload": json.loads(row[5]) if row[5] else {},
                "chat": json.loads(row[6]) if row[6] and row[6] != 'null' else None,
                "summary": row[7] if row[7] and row[7] != 'null' else None,
                "session_name": row[8] if row[8] and row[8] != 'null' else None,
                "session_context": json.loads(row[9]) if row[9] and row[9] != 'null' else None
            })
        
        # Send initial batch (reversed to chronological order)
        initial_events.reverse()
        await websocket.send_json({"type": "initial", "data": initial_events})
        
        # Keep connection alive
        while True:
            data = await websocket.receive_text()
            # Echo back (heartbeat)
            await websocket.send_text(json.dumps({"type": "pong"}))
            
    except WebSocketDisconnect:
        websocket_clients.remove(websocket)
        print(f"WebSocket client disconnected (remaining: {len(websocket_clients)})")
    except Exception as e:
        print(f"WebSocket error: {e}")
        websocket_clients.discard(websocket)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "observability-server",
        "websocket_clients": len(websocket_clients)
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000, log_level="info")

