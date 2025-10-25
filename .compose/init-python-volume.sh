#!/bin/bash
# Initialize Python MCP utilities in Docker volume
# This script sets up the Python MCP server in a persistent Docker volume

set -e

VOLUME_NAME="docker_python_mcp"
PYTHON_VERSION="3.14"

echo "🐳 Initializing Python MCP utilities in Docker volume: $VOLUME_NAME"

# Create the volume if it doesn't exist
if ! docker volume inspect "$VOLUME_NAME" >/dev/null 2>&1; then
    echo "📦 Creating Docker volume: $VOLUME_NAME"
    docker volume create "$VOLUME_NAME"
else
    echo "📦 Volume $VOLUME_NAME already exists"
fi

# Create a temporary container to initialize the volume
echo "🔧 Setting up Python environment in volume..."

docker run --rm \
    -v "$VOLUME_NAME:/app" \
    -w /app \
    "python:$PYTHON_VERSION-slim" \
    bash -c "
        # Install system dependencies
        apt-get update && apt-get install -y \
            curl \
            build-essential \
            pkg-config \
            git \
            && rm -rf /var/lib/apt/lists/*

        # Create Python virtual environment
        python -m venv .venv
        . .venv/bin/activate

        # Upgrade pip
        pip install --upgrade pip

        # Install uv for faster package management
        pip install uv

        echo '✅ Python MCP volume initialized successfully'
        echo '📍 Volume location: /app'
        echo '🐍 Python version:' \$(python --version)
        echo '🔧 Virtual environment: /app/.venv'
    "

echo "🎉 Python MCP utilities volume ready!"
echo "💡 Use volume '$VOLUME_NAME' in your docker-compose.yml files"