FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv (fast Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Copy project files
COPY pyproject.toml uv.lock ./
COPY agents/ ./agents/
COPY integrations/ ./integrations/
COPY hooks/ ./hooks/
COPY tools/ ./tools/
COPY scripts/ ./scripts/
COPY tests/ ./tests/
COPY .claude/ ./.claude/
COPY main.py config.py ./
COPY kinetic_layer.py kinetic_layer_runtime.py ./
COPY semantic_layer.py dynamic_layer_orchestrator.py ./

# Install dependencies
RUN uv sync --frozen

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/math-vault /tmp/math-agent-logs

# Default command
CMD ["uv", "run", "main.py"]

