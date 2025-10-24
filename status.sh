#!/bin/bash
# Docker - Status Check Script
# Shows the current status of Python MCP servers and Docker stacks

set -e

# Source common library
source ".compose/lib/common.sh"

log_header "Docker - Status Check"

# Check if Docker is running (using common library)
check_docker

# Check Python MCP volume
VOLUME_NAME="docker_python_mcp"
if docker volume inspect "$VOLUME_NAME" >/dev/null 2>&1; then
    log_success "Python MCP volume exists: $VOLUME_NAME"
else
    log_error "Python MCP volume missing: $VOLUME_NAME"
    log_info "Run: ./setup-python-mcp.sh"
fi

# Check running containers
echo ""
log_info "Running Containers:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(python|node|db|redis|nginx|mariadb|postgresql)" || log_warning "No stack containers running"

# Check available stacks
echo ""
log_info "Available Stacks:"
for stack in "${STACKS[@]}"; do
    if validate_stack_exists "$stack" >/dev/null 2>&1; then
        log_success "$stack"
    else
        log_error "$stack (missing)"
    fi
done

# Show usage
echo ""
log_info "Quick Commands:"
echo "  Setup Python MCP:    ./setup-python-mcp.sh"
echo "  Start basic stack:   docker compose -f .compose/basic-stack/docker-compose.yml up -d"
echo "  View logs:           docker compose -f .compose/basic-stack/docker-compose.yml logs -f python"
echo "  Stop all:            docker compose -f .compose/basic-stack/docker-compose.yml down"
echo ""
log_info "Service URLs (when running):"
echo "  Basic Stack MCP:     http://localhost:8001"
echo "  Cluster MCP:         http://localhost:8000"
echo "  Frontend:            http://localhost:3000"