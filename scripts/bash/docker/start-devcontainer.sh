#!/usr/bin/env bash
# Start the Docker cluster stack with devcontainer
# This script validates environment variables and starts all services

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "========================================="
echo "  Docker Cluster Stack - DevContainer"
echo "========================================="
echo ""

# Validate environment variables
echo "Step 1: Validating environment variables..."
if command -v python3 &> /dev/null; then
    python3 "$SCRIPT_DIR/validate_env.py"
    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ Environment validation failed!"
        echo "Please fix the issues above and try again."
        exit 1
    fi
else
    echo "⚠️  Warning: Python 3 not found, skipping env validation"
fi

echo ""
echo "Step 2: Starting Docker Compose stack with devcontainer profile..."
cd "$PROJECT_ROOT"

# Start all services including devcontainer
docker-compose --profile dev up -d

echo ""
echo "Step 3: Waiting for services to become healthy..."
sleep 10

# Check service health
echo ""
docker-compose ps

echo ""
echo "========================================="
echo "✅ Stack started successfully!"
echo "========================================="
echo ""
echo "Services accessible at:"
echo "  - Load Balancer:    http://localhost:8080"
echo "  - React Dashboard:  http://localhost:3000"
echo "  - Docker API:       http://localhost:3001"
echo "  - Grafana:          http://localhost:3002"
echo "  - Prometheus:       http://localhost:9090"
echo "  - Alertmanager:     http://localhost:9093"
echo "  - PostgreSQL:       localhost:5432"
echo "  - Redis:            localhost:6379"
echo "  - Jupyter Lab:      http://localhost:8888"
echo "  - MinIO Console:    http://localhost:9001"
echo "  - MailHog UI:       http://localhost:8025"
echo "  - pgAdmin:          http://localhost:5050"
echo ""
echo "To attach to devcontainer:"
echo "  1. Open VS Code"
echo "  2. Run: 'Dev Containers: Attach to Running Container'"
echo "  3. Select: cluster-devcontainer"
echo ""
