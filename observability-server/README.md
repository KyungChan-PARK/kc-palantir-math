# Observability Server

Lightweight event collection server for Math Education Multi-Agent System.

## Run Locally

```bash
pip install -r requirements.txt
python3 server.py
```

## Run with Docker

```bash
docker build -t obs-server .
docker run -d -p 4000:4000 -v $(pwd)/data:/app/data obs-server
```

## API

- POST /events - Receive events from hooks
- GET /events/recent?limit=100&session_id=X - Query events
- GET /events/sessions - List all sessions
- GET /health - Health check

