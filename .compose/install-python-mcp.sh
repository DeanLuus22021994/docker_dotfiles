#!/bin/bash
# Install Python MCP utilities into Docker volume
# This script copies the Python utilities to the persistent volume and installs them

set -e

VOLUME_NAME="docker_python_mcp"
SOURCE_DIR=".docker-compose/mcp/python_utils"

echo "📦 Installing Python MCP utilities into volume: $VOLUME_NAME"

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "❌ Error: Source directory $SOURCE_DIR not found"
    exit 1
fi

# Copy Python utilities to volume
echo "📋 Copying Python utilities to volume..."
docker run --rm \
    -v "$VOLUME_NAME:/app" \
    -v "$(pwd):/host:ro" \
    -w /app \
    "python:3.14-slim" \
    bash -c "
        # Copy source files
        cp -r /host/$SOURCE_DIR/* /app/ 2>/dev/null || true

        # Activate virtual environment
        . .venv/bin/activate

        # Install the package in development mode
        if [ -f 'pyproject.toml' ]; then
            echo '📦 Installing Python package...'
            pip install -e .
        else
            echo '⚠️  No pyproject.toml found, installing requirements.txt if present...'
            [ -f 'requirements.txt' ] && pip install -r requirements.txt
        fi

        echo '✅ Python MCP utilities installed successfully'
    "

echo "🎉 Python MCP utilities installed in volume!"
echo "🚀 Ready to run MCP servers in Docker Compose stacks"