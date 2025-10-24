#!/bin/bash
# Docker Compose - Automation Script
# Unified automation for validation, testing, cleanup, and reporting

set -euo pipefail

# Source common library
source ".compose/lib/common.sh"

# Script configuration
SCRIPT_NAME="$(basename "$0")"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Available stacks
STACKS=(
    "basic-stack"
    "cluster-example"
    "mcp"
    "observability"
    "swarm-stack"
    "github-actions-runner"
)

# Colors for output (defined in common.sh)
# log_header, log_success, log_error, log_warning, log_info functions available

# Validate all stacks
validate_all_stacks() {
    log_header "Validating All Docker Compose Stacks"

    local failed_stacks=()
    local total_stacks=${#STACKS[@]}
    local valid_count=0

    for stack in "${STACKS[@]}"; do
        log_info "Validating stack: $stack"

        if validate_stack_exists "$stack"; then
            if validate_compose_syntax "$stack"; then
                log_success "✓ $stack - Valid"
                ((valid_count++))
            else
                log_error "✗ $stack - Syntax error"
                failed_stacks+=("$stack")
            fi
        else
            log_warning "! $stack - Stack file not found"
        fi
    done

    echo ""
    log_info "Validation Summary: $valid_count/$total_stacks stacks valid"

    if [ ${#failed_stacks[@]} -gt 0 ]; then
        log_error "Failed stacks: ${failed_stacks[*]}"
        return 1
    fi

    log_success "All stacks validated successfully"
    return 0
}

# Test all deployments
test_all_deployments() {
    log_header "Testing All Stack Deployments"

    local failed_tests=()
    local total_tests=0
    local passed_tests=0

    # Test basic-stack deployment
    if validate_stack_exists "basic-stack"; then
        ((total_tests++))
        log_info "Testing basic-stack deployment..."

        if test_stack_deployment "basic-stack"; then
            log_success "✓ basic-stack deployment test passed"
            ((passed_tests++))
        else
            log_error "✗ basic-stack deployment test failed"
            failed_tests+=("basic-stack")
        fi
    fi

    # Test cluster-example deployment
    if validate_stack_exists "cluster-example"; then
        ((total_tests++))
        log_info "Testing cluster-example deployment..."

        if test_stack_deployment "cluster-example"; then
            log_success "✓ cluster-example deployment test passed"
            ((passed_tests++))
        else
            log_error "✗ cluster-example deployment test failed"
            failed_tests+=("cluster-example")
        fi
    fi

    echo ""
    log_info "Deployment Test Summary: $passed_tests/$total_tests tests passed"

    if [ ${#failed_tests[@]} -gt 0 ]; then
        log_error "Failed tests: ${failed_tests[*]}"
        return 1
    fi

    log_success "All deployment tests passed"
    return 0
}

# Generate comprehensive report
generate_report() {
    log_header "Generating Comprehensive Report"

    local report_file="$PROJECT_ROOT/automation-report-$(date +%Y%m%d-%H%M%S).md"

    {
        echo "# Docker Compose Automation Report"
        echo "Generated: $(date)"
        echo ""

        echo "## System Information"
        echo "- Docker Version: $(docker --version)"
        echo "- Docker Compose Version: $(docker compose version)"
        echo "- Project Root: $PROJECT_ROOT"
        echo ""

        echo "## Stack Validation Results"
        for stack in "${STACKS[@]}"; do
            if validate_stack_exists "$stack"; then
                if validate_compose_syntax "$stack" >/dev/null 2>&1; then
                    echo "- ✅ $stack - Valid"
                else
                    echo "- ❌ $stack - Syntax Error"
                fi
            else
                echo "- ⚠️  $stack - Not Found"
            fi
        done
        echo ""

        echo "## Running Containers"
        echo "\`\`\`"
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "No containers running"
        echo "\`\`\`"
        echo ""

        echo "## Docker Images"
        echo "\`\`\`"
        docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep -E "(docker_|devcontainer)" || echo "No custom images found"
        echo "\`\`\`"
        echo ""

        echo "## Docker Volumes"
        echo "\`\`\`"
        docker volume ls --format "table {{.Name}}\t{{.Driver}}" | grep -E "docker_" || echo "No docker volumes found"
        echo "\`\`\`"
        echo ""

        echo "## Recommendations"
        echo "1. Ensure all stacks use custom docker_* images"
        echo "2. Verify health checks are properly configured"
        echo "3. Check volume naming follows docker_service_type convention"
        echo "4. Validate environment variables are properly set"
        echo ""

    } > "$report_file"

    log_success "Report generated: $report_file"
}

# Cleanup Docker resources
cleanup_resources() {
    log_header "Cleaning Up Docker Resources"

    log_info "Removing stopped containers..."
    docker container prune -f >/dev/null 2>&1 || true

    log_info "Removing unused images..."
    docker image prune -f >/dev/null 2>&1 || true

    log_info "Removing unused volumes..."
    docker volume prune -f >/dev/null 2>&1 || true

    log_info "Removing unused networks..."
    docker network prune -f >/dev/null 2>&1 || true

    log_success "Docker cleanup completed"
}

# Show usage information
usage() {
    cat << EOF
Docker Compose Automation Script

USAGE:
    $0 COMMAND [OPTIONS]

COMMANDS:
    validate        Validate all Docker Compose stacks
    test           Test all stack deployments
    cleanup        Clean up Docker resources
    report         Generate comprehensive report
    all            Run validate, test, and report

EXAMPLES:
    $0 validate     # Validate all stacks
    $0 test         # Test all deployments
    $0 cleanup      # Clean up resources
    $0 report       # Generate report
    $0 all          # Run full automation suite

EOF
}

# Main function
main() {
    # Check if Docker is available
    check_docker

    case "${1:-help}" in
        validate)
            validate_all_stacks
            ;;
        test)
            test_all_deployments
            ;;
        cleanup)
            cleanup_resources
            ;;
        report)
            generate_report
            ;;
        all)
            validate_all_stacks && test_all_deployments && generate_report
            ;;
        -h|--help|help)
            usage
            ;;
        *)
            log_error "Unknown command: $1"
            usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"