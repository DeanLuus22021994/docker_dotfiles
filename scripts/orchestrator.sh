#!/usr/bin/env bash
#
# Bash Orchestrator for Docker Infrastructure Scripts
# Central orchestrator for all Bash-based automation scripts
# Delegates tasks to specialized scripts organized by function (SRP)
#
# Usage:
#   ./orchestrator.sh <task> <action>
#
# Examples:
#   ./orchestrator.sh docker start-devcontainer
#   ./orchestrator.sh docs serve
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Color output functions
success() { echo -e "\033[92m✓ $1\033[0m"; }
error() { echo -e "\033[91m✗ $1\033[0m" >&2; }
info() { echo -e "\033[94mℹ $1\033[0m"; }
warning() { echo -e "\033[93m⚠ $1\033[0m"; }
header() { echo -e "\033[1m\033[94m$1\033[0m"; }

# Display help
show_help() {
    header "\n=== Bash Orchestrator ==="
    echo ""
    echo "Available Tasks:"
    echo ""
    
    echo "docker"
    echo "  start-devcontainer  Start development container"
    echo ""
    
    echo "docs"
    echo "  serve               Serve documentation"
    echo ""
    
    echo "validate"
    echo "  env                 Validate environment variables (uses Python)"
    echo "  configs             Validate configuration files (uses Python)"
    echo ""
    
    echo "Examples:"
    echo "  ./orchestrator.sh docker start-devcontainer"
    echo "  ./orchestrator.sh docs serve"
    echo "  ./orchestrator.sh validate env"
    echo ""
}

# Execute task
execute_task() {
    local task="$1"
    local action="$2"
    
    case "$task" in
        docker)
            case "$action" in
                start-devcontainer)
                    script="${SCRIPT_DIR}/bash/docker/start-devcontainer.sh"
                    if [[ -f "$script" ]]; then
                        info "Starting devcontainer..."
                        bash "$script"
                    else
                        error "Script not found: $script"
                        exit 1
                    fi
                    ;;
                *)
                    error "Unknown docker action: $action"
                    info "Available: start-devcontainer"
                    exit 1
                    ;;
            esac
            ;;
        
        docs)
            case "$action" in
                serve)
                    script="${SCRIPT_DIR}/bash/docs/serve-docs.sh"
                    if [[ -f "$script" ]]; then
                        info "Starting documentation server..."
                        bash "$script"
                    else
                        error "Script not found: $script"
                        exit 1
                    fi
                    ;;
                *)
                    error "Unknown docs action: $action"
                    info "Available: serve"
                    exit 1
                    ;;
            esac
            ;;
        
        validate)
            case "$action" in
                env)
                    script="${SCRIPT_DIR}/python/validation/validate_env.py"
                    if [[ -f "$script" ]]; then
                        info "Validating environment variables..."
                        python3 "$script"
                    else
                        error "Script not found: $script"
                        exit 1
                    fi
                    ;;
                configs)
                    script="${SCRIPT_DIR}/python/validation/validate_configs.py"
                    if [[ -f "$script" ]]; then
                        info "Validating configuration files..."
                        python3 "$script"
                    else
                        error "Script not found: $script"
                        exit 1
                    fi
                    ;;
                *)
                    error "Unknown validate action: $action"
                    info "Available: env, configs"
                    exit 1
                    ;;
            esac
            ;;
        
        help)
            show_help
            exit 0
            ;;
        
        *)
            error "Unknown task: $task"
            show_help
            exit 1
            ;;
    esac
}

# Main execution
if [[ $# -lt 2 ]] || [[ "$1" == "help" ]]; then
    show_help
    exit 0
fi

TASK="$1"
ACTION="$2"

execute_task "$TASK" "$ACTION"
success "Task completed: $TASK $ACTION"
