# syntax=docker/dockerfile:1

# Consolidated Multi-stage Python Dockerfile for all Docker Compose stacks
# Optimized for Python 3.14 free-threaded execution with BuildKit caching
# Supports basic-stack, cluster-example, and swarm-stack configurations

FROM python:3.14-slim AS base
WORKDIR /app

# Install comprehensive system dependencies with BuildKit caching
RUN --mount=type=cache,target=/var/cache/apt \
  --mount=type=cache,target=/var/lib/apt \
  apt-get update && apt-get install -y \
  curl \
  build-essential \
  pkg-config \
  postgresql-client \
  redis-tools \
  docker.io \
  && rm -rf /var/lib/apt/lists/*

# Create non-root user optimized for container security
RUN useradd --create-home --shell /bin/bash --uid 1001 app \
  && chown -R app:app /app
USER app

FROM base AS deps
# Copy dependency files first for better caching
COPY --chown=app:app pyproject.toml ./
COPY --chown=app:app python_utils/ ./python_utils/

# Create virtual environment with pip cache mounting
RUN --mount=type=cache,target=/tmp/.cache/pip,uid=1001 \
  python -m venv /app/.venv \
  && /app/.venv/bin/pip install --no-cache-dir --upgrade pip \
  && /app/.venv/bin/pip install --no-cache-dir -e .

FROM deps AS runner
# Copy virtual environment from deps stage
COPY --from=deps --chown=app:app /app/.venv /app/.venv
# Copy application code
COPY --chown=app:app . .

# Activate virtual environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app/python_utils:/app
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8000

# Python 3.14 optimizations
ENV PYTHONOPTIMIZE=1
ENV PYTHONDONTWRITEBYTECODE=1

# Stack-specific environment variables (can be overridden by docker-compose)
ENV CLUSTER_MODE=${CLUSTER_MODE:-false}
ENV SWARM_MODE=${SWARM_MODE:-false}
ENV REDIS_URL=${REDIS_URL:-redis://redis:6379}
ENV POSTGRES_URL=${POSTGRES_URL:-postgresql://postgres:password@postgres:5432/scuba_db}
ENV DOCKER_HOST=${DOCKER_HOST:-unix:///var/run/docker.sock}

# Health check optimized for Python 3.14
HEALTHCHECK --interval=15s --timeout=5s --start-period=20s --retries=5 \
  CMD python -c "import sys; print('Python OK'); sys.exit(0)" || exit 1

EXPOSE 8000

# Default command - can be overridden by docker-compose
CMD ["python", "-m", "uvicorn", "react_scuba_utils.api:app", "--host", "0.0.0.0", "--port", "8000"]
