FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

# Create data directory for SQLite
RUN mkdir -p /app/data

# Expose port
EXPOSE 4000

# Run server
CMD ["python3", "server.py"]

