#!/bin/bash
# Docker Stack Validation and Cleanup Script
# Provides comprehensive validation and cleanup without Python dependencies

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$BASE_DIR/.config"
COMPOSE_DIR="$BASE_DIR/.compose"
REPORTS_DIR="$BASE_DIR/reports"

# Create reports directory
mkdir -p "$REPORTS_DIR"

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Cleanup functions
cleanup_docker() {
    log_info "Cleaning up Docker resources..."
    docker system prune -f > /dev/null 2>&1 || true
    docker volume prune -f > /dev/null 2>&1 || true
    docker image prune -f > /dev/null 2>&1 || true
    log_success "Docker cleanup completed"
}

cleanup_cache() {
    log_info "Cleaning up build cache..."
    rm -rf "$BASE_DIR/.cache/buildx" || true
    rm -rf "$BASE_DIR/.pytest_cache" || true
    rm -rf "$BASE_DIR/.mypy_cache" || true
    rm -rf "$BASE_DIR/.ruff_cache" || true
    find "$BASE_DIR" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    log_success "Cache cleanup completed"
}

# Validation functions
validate_compose_file() {
    local stack=$1
    local compose_file="$COMPOSE_DIR/$stack/docker-compose.yml"

    if [ ! -f "$compose_file" ]; then
        log_error "Compose file not found: $compose_file"
        return 1
    fi

    log_info "Validating $stack configuration..."
    if docker-compose -f "$compose_file" config --quiet > /dev/null 2>&1; then
        log_success "$stack configuration is valid"
        return 0
    else
        log_error "$stack configuration is invalid"
        docker-compose -f "$compose_file" config 2>&1 || true
        return 1
    fi
}

validate_config_consistency() {
    local stack=$1
    local config_file="$CONFIG_DIR/$stack/config.yml"
    local compose_file="$COMPOSE_DIR/$stack/docker-compose.yml"

    if [ ! -f "$config_file" ]; then
        log_warning "Config file not found: $config_file"
        return 0
    fi

    log_info "Checking $stack config-compose consistency..."

    # Extract service names from config
    local config_services=$(grep -E "^[[:space:]]*[a-zA-Z_][a-zA-Z0-9_]*:" "$config_file" | grep -v "stack:" | grep -v "ci_cd:" | grep -v "environment:" | grep -v "volumes:" | grep -v "secrets:" | grep -v "network:" | head -10 | sed 's/:.*//' | sed 's/^[[:space:]]*//')

    # Extract service names from compose
    local compose_services=$(docker-compose -f "$compose_file" config 2>/dev/null | grep -A 100 "services:" | grep -E "^[[:space:]]*[a-zA-Z_][a-zA-Z0-9_]*:" | sed 's/:.*//' | sed 's/^[[:space:]]*//' | head -10)

    # Basic check - just ensure we have services defined
    if [ -n "$config_services" ] && [ -n "$compose_services" ]; then
        log_success "$stack has both config and compose services defined"
        return 0
    else
        log_warning "$stack missing service definitions"
        return 1
    fi
}

# Testing functions
test_deployment() {
    local stack=$1
    local compose_file="$COMPOSE_DIR/$stack/docker-compose.yml"

    log_info "Testing $stack deployment..."

    # Start services
    if ! docker-compose -f "$compose_file" up -d --quiet-pull > /dev/null 2>&1; then
        log_error "Failed to start $stack services"
        return 1
    fi

    # Wait for services to initialize
    sleep 15

    # Check service status
    local status_output
    status_output=$(docker-compose -f "$compose_file" ps 2>/dev/null)

    if echo "$status_output" | grep -q "Up"; then
        local up_count=$(echo "$status_output" | grep -c "Up")
        local total_count=$(echo "$status_output" | grep -v "Name" | grep -v "^--" | wc -l)
        log_success "$stack deployed: $up_count/$total_count services running"
        return 0
    else
        log_error "$stack deployment failed - no services running"
        echo "$status_output"
        return 1
    fi
}

cleanup_deployment() {
    local stack=$1
    local compose_file="$COMPOSE_DIR/$stack/docker-compose.yml"

    log_info "Cleaning up $stack deployment..."
    docker-compose -f "$compose_file" down -v --remove-orphans > /dev/null 2>&1 || true
}

# Main functions
validate_all_stacks() {
    log_info "Starting comprehensive stack validation..."
    echo "=========================================="

    local stacks=("basic-stack" "cluster-example" "swarm-stack" "mcp")
    local results=()
    local failed=0

    for stack in "${stacks[@]}"; do
        log_info "Processing stack: $stack"
        echo "---"

        # Validate compose file
        if ! validate_compose_file "$stack"; then
            results+=("$stack: COMPOSE_INVALID")
            ((failed++))
            continue
        fi

        # Validate config consistency
        if ! validate_config_consistency "$stack"; then
            results+=("$stack: CONFIG_INCONSISTENT")
            ((failed++))
            continue
        fi

        results+=("$stack: VALID")
        echo ""
    done

    # Summary
    echo "=========================================="
    log_info "Validation Summary:"
    printf '%s\n' "${results[@]}"

    if [ $failed -eq 0 ]; then
        log_success "All stacks validated successfully!"
        return 0
    else
        log_error "$failed stack(s) failed validation"
        return 1
    fi
}

test_all_deployments() {
    log_info "Starting deployment testing..."
    echo "=========================================="

    local stacks=("basic-stack" "cluster-example" "swarm-stack" "mcp")
    local results=()
    local failed=0

    for stack in "${stacks[@]}"; do
        log_info "Testing deployment: $stack"

        if test_deployment "$stack"; then
            results+=("$stack: DEPLOY_SUCCESS")
        else
            results+=("$stack: DEPLOY_FAILED")
            ((failed++))
        fi

        # Always cleanup
        cleanup_deployment "$stack"
        echo ""
    done

    # Summary
    echo "=========================================="
    log_info "Deployment Test Summary:"
    printf '%s\n' "${results[@]}"

    if [ $failed -eq 0 ]; then
        log_success "All deployments tested successfully!"
        return 0
    else
        log_error "$failed deployment(s) failed"
        return 1
    fi
}

generate_report() {
    local report_file="$REPORTS_DIR/automation_report_$(date +%Y%m%d_%H%M%S).md"

    log_info "Generating comprehensive report..."

    cat > "$report_file" << EOF
# Docker Stack Automation Report
Generated: $(date)

## System Information
- Docker Version: $(docker --version 2>/dev/null || echo "Not available")
- Docker Compose Version: $(docker-compose --version 2>/dev/null || echo "Not available")
- Base Directory: $BASE_DIR

## Validation Results
$(validate_all_stacks 2>&1)

## Deployment Test Results
$(test_all_deployments 2>&1)

## Configuration Summary
- Config Directory: $CONFIG_DIR
- Compose Directory: $COMPOSE_DIR
- Stacks Found: $(ls -1 "$CONFIG_DIR" | wc -l)
- Compose Files: $(find "$COMPOSE_DIR" -name "docker-compose.yml" | wc -l)

## Recommendations
1. Ensure all config files have corresponding compose files
2. Validate environment variables are properly set
3. Check volume mounts and network configurations
4. Monitor service health checks
5. Review resource limits and constraints

---
Report generated by Docker Stack Automation Script
EOF

    log_success "Report saved to: $report_file"
}

# Main execution
main() {
    local action="${1:-all}"

    case "$action" in
        "validate")
            cleanup_cache
            validate_all_stacks
            ;;
        "test")
            cleanup_docker
            test_all_deployments
            ;;
        "cleanup")
            cleanup_cache
            cleanup_docker
            ;;
        "report")
            generate_report
            ;;
        "all")
            log_info "Running full automation suite..."
            cleanup_cache
            cleanup_docker
            validate_all_stacks
            test_all_deployments
            generate_report
            ;;
        *)
            echo "Usage: $0 {validate|test|cleanup|report|all}"
            echo "  validate - Validate all stack configurations"
            echo "  test     - Test all stack deployments"
            echo "  cleanup  - Clean up Docker resources and cache"
            echo "  report   - Generate comprehensive report"
            echo "  all      - Run full automation suite"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"