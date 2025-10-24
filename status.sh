#!/bin/bash
# Docker - Status Check Script
# Shows the current status of Python MCP servers and Docker stacks

set -e

echo "🐳 Docker - Status Check"
echo "=================================="

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running"
    exit 1
fi

echo "✅ Docker is running"

# Check Python MCP volume
VOLUME_NAME="docker_python_mcp"
if docker volume inspect "$VOLUME_NAME" >/dev/null 2>&1; then
    echo "✅ Python MCP volume exists: $VOLUME_NAME"
else
    echo "❌ Python MCP volume missing: $VOLUME_NAME"
    echo "   Run: ./setup-python-mcp.sh"
fi

# Check running containers
echo ""
echo "🚢 Running Containers:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(python|node|db|redis)" || echo "   No stack containers running"

# Check available stacks
echo ""
echo "📁 Available Stacks:"
for stack in basic-stack cluster-example swarm-stack; do
    if [ -d ".docker-compose/$stack" ]; then
        echo "   ✅ $stack"
    else
        echo "   ❌ $stack (missing)"
    fi
done

# Show usage
echo ""
echo "🎯 Quick Commands:"
echo "  Setup Python MCP:    ./setup-python-mcp.sh"
echo "  Start basic stack:   docker compose -f .docker-compose/basic-stack/docker-compose.yml up -d"
echo "  View logs:           docker compose -f .docker-compose/basic-stack/docker-compose.yml logs -f python"
echo "  Stop all:            docker compose -f .docker-compose/basic-stack/docker-compose.yml down"
echo ""
echo "🔗 Service URLs (when running):"
echo "  Basic Stack MCP:     http://localhost:8001"
echo "  Cluster MCP:         http://localhost:8000"
echo "  Frontend:            http://localhost:3000"