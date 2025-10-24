#!/bin/bash
# Docker - Python MCP Setup Script
# Initializes and configures Python MCP servers for all Docker Compose stacks
# This script sets up persistent Python utilities in Docker volumes

set -e

# Configuration
VOLUME_NAME="docker_python_mcp"
SOURCE_DIR=".docker-compose/mcp/python_utils"
PYTHON_VERSION="3.14"

echo "🐳 Docker - Python MCP Setup"
echo "======================================"

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        echo "❌ Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to initialize Python volume
init_python_volume() {
    echo "📦 Initializing Python MCP volume: $VOLUME_NAME"

    if ! docker volume inspect "$VOLUME_NAME" >/dev/null 2>&1; then
        echo "  📦 Creating Docker volume..."
        docker volume create "$VOLUME_NAME"
    else
        echo "  📦 Volume already exists"
    fi

    echo "  🐍 Setting up Python environment..."
    docker run --rm \
        -v "$VOLUME_NAME:/app" \
        -w /app \
        "python:$PYTHON_VERSION-slim" \
        bash -c "
            echo '    Installing system dependencies...'
            apt-get update >/dev/null 2>&1 && apt-get install -y \
                curl \
                build-essential \
                pkg-config \
                git \
                >/dev/null 2>&1 && rm -rf /var/lib/apt/lists/*

            echo '    Creating Python virtual environment...'
            python -m venv .venv

            echo '    Installing uv package manager...'
            . .venv/bin/activate
            pip install --quiet uv

            echo '    ✅ Python environment ready'
        "
}

# Function to install Python utilities
install_python_utils() {
    echo "📦 Installing Python MCP utilities"

    if [ ! -d "$SOURCE_DIR" ]; then
        echo "❌ Error: Python utilities not found at $SOURCE_DIR"
        echo "   Please ensure the repository is complete."
        exit 1
    fi

    echo "  📋 Copying Python utilities to volume..."
    docker run --rm \
        -v "$VOLUME_NAME:/app" \
        -v "$(pwd):/host:ro" \
        -w /app \
        "python:$PYTHON_VERSION-slim" \
        bash -c "
            . .venv/bin/activate

            echo '    Installing Python dependencies...'
            uv pip install --quiet mkdocs requests beautifulsoup4 PyYAML pydantic pydantic-settings fastapi uvicorn mcp structlog click rich urllib3 lxml python-dotenv

            echo '    ✅ Python utilities installed'
        "

    echo "  📦 Installing package in development mode..."
    docker run --rm \
        -v "$VOLUME_NAME:/app" \
        -v "$(pwd)/$SOURCE_DIR:/source:ro" \
        -w /app \
        "python:$PYTHON_VERSION-slim" \
        bash -c "
            . .venv/bin/activate

            echo '    Copying source files...'
            cp -r /source/* /app/ 2>/dev/null || true

            if [ -f 'pyproject.toml' ]; then
                echo '    Installing package...'
                uv pip install --quiet -e .
                echo '    ✅ Package installed successfully'
            else
                echo '    ⚠️  No pyproject.toml found'
            fi
        "
}

# Function to verify installation
verify_installation() {
    echo "🔍 Verifying Python MCP installation"

    docker run --rm \
        -v "$VOLUME_NAME:/app" \
        -w /app \
        "python:$PYTHON_VERSION-slim" \
        bash -c "
            . .venv/bin/activate

            echo '  🧪 Testing Python imports...'
            python -c '
import sys
print(f\"Python version: {sys.version}\")

try:
    import docker_utils
    print(\"✅ docker_utils imported successfully\")
except ImportError as e:
    print(f\"❌ Import failed: {e}\")
    sys.exit(1)

try:
    from docker_utils.api import app
    print(\"✅ FastAPI app imported successfully\")
except ImportError as e:
    print(f\"❌ API import failed: {e}\")
    sys.exit(1)

print(\"🎉 All imports successful!\")
            '
        "
}

# Function to show usage information
show_usage() {
    echo ""
    echo "🎯 Usage:"
    echo "  Start a stack with Python MCP:"
    echo "    cd .docker-compose/basic-stack"
    echo "    docker-compose up -d"
    echo ""
    echo "  View Python MCP logs:"
    echo "    docker-compose logs -f python"
    echo ""
    echo "  Update Python utilities:"
    echo "    ./install-python-mcp.sh"
    echo ""
    echo "  Access Python MCP API:"
    echo "    - Basic stack: http://localhost:8001"
    echo "    - Cluster example: http://localhost:8000"
    echo "    - Swarm stack: http://localhost:8000"
}

# Main execution
main() {
    check_docker
    init_python_volume
    install_python_utils
    verify_installation

    echo ""
    echo "🎉 Python MCP setup complete!"
    echo "💡 Python utilities are now installed in Docker volume: $VOLUME_NAME"
    echo "   This volume persists across container rebuilds."

    show_usage
}

# Run main function
main "$@"