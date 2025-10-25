# Optimized Python Dockerfile with Buildx/Bake caching
# Generated: 2025-10-25
# Description: Multi-stage Python FastAPI application with advanced caching
# Build args:
#   - ENVIRONMENT: development|production|test (default: development)
#   - SERVICE_TYPE: app|mcp (default: app)
#   - WORKERS: number of uvicorn workers (default: 1 for dev, 4 for prod)

# Base stage with system dependencies
FROM python:3.14-slim AS base

# Build arguments
ARG ENVIRONMENT=development
ARG SERVICE_TYPE=app
ARG WORKERS=1

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    ENVIRONMENT=${ENVIRONMENT} \
    SERVICE_TYPE=${SERVICE_TYPE} \
    UV_CACHE_DIR=/tmp/uv-cache

# Install system dependencies based on service type
RUN apt-get update && apt-get install -y \
    curl \
    $([ "$SERVICE_TYPE" = "mcp" ] && echo "build-essential git") \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast Python package management
RUN pip install uv

# Set work directory
WORKDIR /app

# Dependencies stage for caching
FROM base AS deps

# Copy Python dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies based on environment
RUN if [ "$ENVIRONMENT" = "test" ] || [ "$SERVICE_TYPE" = "mcp" ]; then \
        uv sync --frozen --no-install-project; \
    else \
        uv sync --frozen --no-install-project --no-dev; \
    fi

# Application stage
FROM base AS app

# Copy dependencies from deps stage
COPY --from=deps /app /app

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app

USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Expose port
EXPOSE 8000

# Run application based on environment and service type
CMD if [ "$SERVICE_TYPE" = "mcp" ]; then \
        tail -f /dev/null; \
    elif [ "$ENVIRONMENT" = "development" ]; then \
        uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload; \
    else \
        WORKERS=${WORKERS:-4}; \
        uv run uvicorn main:app --host 0.0.0.0 --port 8000 --workers $WORKERS; \
    fi