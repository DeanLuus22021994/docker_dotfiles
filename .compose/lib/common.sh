#!/bin/bash
# Docker Compose - Common Library
# Standardized functions for all Docker Compose scripts
# This library provides consistent logging, validation, and utility functions

set -euo pipefail

# Colors for output (standardized across all scripts)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration (standardized paths)
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$BASE_DIR/.config"
COMPOSE_DIR="$BASE_DIR/.compose"
DOCKERFILES_DIR="$BASE_DIR/.dockerfiles"
REPORTS_DIR="$BASE_DIR/reports"
CACHE_DIR="$BASE_DIR/.cache"

# Standard stack definitions
STACKS=("basic-stack" "cluster-example" "swarm-stack" "mcp")

# Logging functions (standardized)
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

log_debug() {
    if [ "${DEBUG:-false}" = "true" ]; then
        echo -e "${PURPLE}[DEBUG]${NC} $1"
    fi
}

log_header() {
    echo -e "${CYAN}======================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}======================================${NC}"
}

# Docker validation functions
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    log_debug "Docker is running"
}

check_docker_compose() {
    if ! docker-compose --version >/dev/null 2>&1; then
        log_error "Docker Compose is not available."
        exit 1
    fi
    log_debug "Docker Compose is available"
}

check_buildx() {
    if ! docker buildx version >/dev/null 2>&1; then
        log_error "Docker Buildx is not available."
        exit 1
    fi
    log_debug "Docker Buildx is available"
}

# Directory validation functions
ensure_directory() {
    local dir=$1
    if [ ! -d "$dir" ]; then
        log_debug "Creating directory: $dir"
        mkdir -p "$dir"
    fi
}

validate_stack_exists() {
    local stack=$1
    if [ ! -d "$COMPOSE_DIR/$stack" ]; then
        log_error "Stack directory not found: $COMPOSE_DIR/$stack"
        return 1
    fi
    if [ ! -f "$COMPOSE_DIR/$stack/docker-compose.yml" ]; then
        log_error "Compose file not found: $COMPOSE_DIR/$stack/docker-compose.yml"
        return 1
    fi
    return 0
}

validate_config_exists() {
    local stack=$1
    if [ ! -d "$CONFIG_DIR/$stack" ]; then
        log_warning "Config directory not found: $CONFIG_DIR/$stack"
        return 1
    fi
    if [ ! -f "$CONFIG_DIR/$stack/config.yml" ]; then
        log_warning "Config file not found: $CONFIG_DIR/$stack/config.yml"
        return 1
    fi
    return 0
}

# Compose validation functions
validate_compose_syntax() {
    local stack=$1
    local compose_file="$COMPOSE_DIR/$stack/docker-compose.yml"

    log_debug "Validating compose syntax for $stack..."
    if docker-compose -f "$compose_file" config --quiet >/dev/null 2>&1; then
        log_success "$stack compose syntax is valid"
        return 0
    else
        log_error "$stack compose syntax is invalid"
        docker-compose -f "$compose_file" config 2>&1 || true
        return 1
    fi
}

validate_compose_services() {
    local stack=$1
    local compose_file="$COMPOSE_DIR/$stack/docker-compose.yml"

    log_debug "Validating services for $stack..."
    local services
    services=$(docker-compose -f "$compose_file" config 2>/dev/null | grep -A 100 "services:" | grep -E "^[[:space:]]*[a-zA-Z_][a-zA-Z0-9_]*:" | sed 's/:.*//' | sed 's/^[[:space:]]*//' | tr '\n' ' ')

    if [ -z "$services" ]; then
        log_error "$stack has no services defined"
        return 1
    fi

    log_debug "$stack services: $services"
    return 0
}

# Config validation functions
validate_config_services() {
    local stack=$1
    local config_file="$CONFIG_DIR/$stack/config.yml"

    if [ ! -f "$config_file" ]; then
        return 0
    fi

    log_debug "Validating config services for $stack..."
    local services
    services=$(grep -E "^[[:space:]]*[a-zA-Z_][a-zA-Z0-9_]*:" "$config_file" | grep -v "stack:" | grep -v "ci_cd:" | grep -v "environment:" | grep -v "volumes:" | grep -v "secrets:" | grep -v "network:" | head -20 | sed 's/:.*//' | sed 's/^[[:space:]]*//' | tr '\n' ' ')

    if [ -n "$services" ]; then
        log_debug "$stack config services: $services"
    fi
    return 0
}

# Stack operations
start_stack() {
    local stack=$1
    local compose_file="$COMPOSE_DIR/$stack/docker-compose.yml"

    log_info "Starting $stack..."
    if docker-compose -f "$compose_file" up -d --quiet-pull >/dev/null 2>&1; then
        log_success "$stack started successfully"
        return 0
    else
        log_error "Failed to start $stack"
        return 1
    fi
}

stop_stack() {
    local stack=$1
    local compose_file="$COMPOSE_DIR/$stack/docker-compose.yml"

    log_info "Stopping $stack..."
    if docker-compose -f "$compose_file" down --remove-orphans >/dev/null 2>&1; then
        log_success "$stack stopped successfully"
        return 0
    else
        log_error "Failed to stop $stack"
        return 1
    fi
}

cleanup_stack() {
    local stack=$1
    local compose_file="$COMPOSE_DIR/$stack/docker-compose.yml"

    log_info "Cleaning up $stack..."
    if docker-compose -f "$compose_file" down -v --remove-orphans >/dev/null 2>&1; then
        log_success "$stack cleaned up successfully"
        return 0
    else
        log_error "Failed to cleanup $stack"
        return 1
    fi
}

# Health check functions
check_stack_health() {
    local stack=$1
    local compose_file="$COMPOSE_DIR/$stack/docker-compose.yml"
    local timeout=${2:-30}

    log_debug "Checking $stack health (timeout: ${timeout}s)..."

    # Start services if not running
    start_stack "$stack" || return 1

    # Wait for services to initialize
    sleep 5

    local healthy=0
    local total=0
    local waited=0

    while [ $waited -lt $timeout ]; do
        local status
        status=$(docker-compose -f "$compose_file" ps --quiet 2>/dev/null | wc -l)
        total=$status

        local running
        running=$(docker-compose -f "$compose_file" ps 2>/dev/null | grep -c "Up" || echo "0")

        if [ "$running" -eq "$total" ] && [ "$total" -gt 0 ]; then
            healthy=$running
            break
        fi

        sleep 2
        waited=$((waited + 2))
    done

    if [ $healthy -eq $total ] && [ $total -gt 0 ]; then
        log_success "$stack is healthy ($healthy/$total services running)"
        return 0
    else
        log_warning "$stack health check failed ($healthy/$total services running)"
        return 1
    fi
}

# Docker resource cleanup
cleanup_docker_resources() {
    log_info "Cleaning up Docker resources..."

    docker system prune -f >/dev/null 2>&1 || true
    docker volume prune -f >/dev/null 2>&1 || true
    docker image prune -f >/dev/null 2>&1 || true
    docker network prune -f >/dev/null 2>&1 || true

    log_success "Docker resources cleaned up"
}

cleanup_build_cache() {
    log_info "Cleaning up build cache..."

    # Clean Buildx cache
    docker buildx prune -f >/dev/null 2>&1 || true

    # Clean local cache directories
    rm -rf "$CACHE_DIR/buildx" || true
    rm -rf "/tmp/.buildx-cache" || true
    rm -rf "/tmp/.buildx-cache-new" || true

    # Clean Python cache
    find "$BASE_DIR" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find "$BASE_DIR" -name "*.pyc" -delete 2>/dev/null || true
    find "$BASE_DIR" -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true
    find "$BASE_DIR" -name ".mypy_cache" -type d -exec rm -rf {} + 2>/dev/null || true
    find "$BASE_DIR" -name ".ruff_cache" -type d -exec rm -rf {} + 2>/dev/null || true

    log_success "Build cache cleaned up"
}

# Report generation
generate_report() {
    local report_file="$REPORTS_DIR/$(date +%Y%m%d_%H%M%S)_report.md"
    local title="${1:-Docker Stack Report}"

    ensure_directory "$REPORTS_DIR"

    log_info "Generating report: $report_file"

    cat > "$report_file" << EOF
# $title
Generated: $(date)

## System Information
- Docker Version: $(docker --version 2>/dev/null | sed 's/Docker version //' || echo "Not available")
- Docker Compose Version: $(docker-compose --version 2>/dev/null | sed 's/docker-compose version //' || echo "Not available")
- Base Directory: $BASE_DIR
- Config Directory: $CONFIG_DIR
- Compose Directory: $COMPOSE_DIR

## Stack Status
EOF

    for stack in "${STACKS[@]}"; do
        echo "### $stack" >> "$report_file"

        if validate_stack_exists "$stack" >/dev/null 2>&1; then
            echo "- ✅ Stack directory exists" >> "$report_file"

            if validate_compose_syntax "$stack" >/dev/null 2>&1; then
                echo "- ✅ Compose syntax valid" >> "$report_file"
            else
                echo "- ❌ Compose syntax invalid" >> "$report_file"
            fi

            if validate_config_exists "$stack" >/dev/null 2>&1; then
                echo "- ✅ Config file exists" >> "$report_file"
            else
                echo "- ⚠️  Config file missing" >> "$report_file"
            fi
        else
            echo "- ❌ Stack directory missing" >> "$report_file"
        fi

        echo "" >> "$report_file"
    done

    echo "## Report Complete" >> "$report_file"
    echo "Generated by Docker Compose Common Library" >> "$report_file"

    log_success "Report saved to: $report_file"
}

# Utility functions
show_usage() {
    local script_name="${1:-script}"
    cat << EOF
Docker Compose - $script_name

USAGE:
    $0 [COMMAND] [OPTIONS]

COMMANDS:
    validate    Validate all stacks
    test        Test stack deployments
    cleanup     Clean up resources
    report      Generate status report
    help        Show this help

EXAMPLES:
    $0 validate
    $0 test
    $0 cleanup
    $0 report

EOF
}

# Export functions for use in other scripts
export -f log_info log_success log_warning log_error log_debug log_header
export -f check_docker check_docker_compose check_buildx
export -f ensure_directory validate_stack_exists validate_config_exists
export -f validate_compose_syntax validate_compose_services validate_config_services
export -f start_stack stop_stack cleanup_stack check_stack_health
export -f cleanup_docker_resources cleanup_build_cache generate_report show_usage
export BASE_DIR CONFIG_DIR COMPOSE_DIR DOCKERFILES_DIR REPORTS_DIR CACHE_DIR
export STACKS