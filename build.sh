#!/usr/bin/env bash
# Docker Buildx and Bake build script for optimized container builds
# This script leverages advanced Docker features for maximum performance

set -euo pipefail

# Configuration
DOCKER_BUILDKIT=1
COMPOSE_DOCKER_CLI_BUILD=1
DOCKER_DEFAULT_PLATFORM=linux/amd64
BUILDKIT_PROGRESS=plain

export DOCKER_BUILDKIT COMPOSE_DOCKER_CLI_BUILD DOCKER_DEFAULT_PLATFORM BUILDKIT_PROGRESS

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Check if Docker Buildx is available
check_buildx() {
    if ! docker buildx version >/dev/null 2>&1; then
        log_error "Docker Buildx is not available. Please install Docker Desktop or Docker CE with Buildx."
        exit 1
    fi
}

# Setup Buildx builder
setup_builder() {
    local builder_name="devcontainer-builder"

    # Create builder if it doesn't exist
    if ! docker buildx ls | grep -q "$builder_name"; then
        log_info "Creating Buildx builder: $builder_name"
        docker buildx create --name "$builder_name" --driver docker-container --use
    else
        log_info "Using existing Buildx builder: $builder_name"
        docker buildx use "$builder_name"
    fi

    # Inspect and ensure builder is running
    docker buildx inspect --bootstrap
}

# Clean build cache
clean_cache() {
    log_info "Cleaning Docker build cache..."
    docker builder prune -f
    docker buildx prune -f

    # Clean local cache directory
    if [ -d "/tmp/.buildx-cache" ]; then
        rm -rf /tmp/.buildx-cache
    fi
    if [ -d "/tmp/.buildx-cache-new" ]; then
        rm -rf /tmp/.buildx-cache-new
    fi
}

# Build with Bake (default)
build_bake() {
    local target="${1:-dev}"
    local registry="${2:-}"
    local tag="${3:-latest}"

    log_info "Building with Docker Bake (target: $target, registry: $registry, tag: $tag)"

    # Set environment variables for Bake
    export REGISTRY="$registry"
    export TAG="$tag"

    # Build with Bake
    docker buildx bake \
        --load \
        --progress plain \
        "$target"
}

# Build with legacy docker build (fallback)
build_legacy() {
    local target="${1:-dev}"
    local registry="${2:-}"
    local tag="${3:-latest}"

    log_info "Building with legacy Docker build (target: $target)"

    local image_tag="${registry}devcontainer:$target-$tag"
    if [ "$target" = "dev" ] && [ -z "$registry" ]; then
        image_tag="devcontainer:latest"
    fi

    docker build \
        --target base \
        --tag "$image_tag" \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        --cache-from "type=local,src=/tmp/.buildx-cache" \
        --cache-to "type=local,dest=/tmp/.buildx-cache-new,mode=max" \
        --progress plain \
        -f .devcontainer/devcontainer.dockerfile \
        .
}

# Build all targets
build_all() {
    local registry="${1:-}"
    local tag="${2:-latest}"

    log_info "Building all targets with Bake"

    export REGISTRY="$registry"
    export TAG="$tag"

    docker buildx bake \
        --load \
        --progress plain \
        all
}

# Push to registry
push_images() {
    local registry="${1:-}"
    local tag="${2:-latest}"

    if [ -z "$registry" ]; then
        log_error "Registry is required for push operation"
        exit 1
    fi

    log_info "Pushing images to registry: $registry"

    export REGISTRY="$registry"
    export TAG="$tag"

    docker buildx bake \
        --push \
        --progress plain \
        all
}

# Show usage
usage() {
    cat << EOF
Docker Buildx and Bake Build Script

USAGE:
    $0 [COMMAND] [OPTIONS]

COMMANDS:
    bake [TARGET] [REGISTRY] [TAG]    Build with Docker Bake (default: dev)
    legacy [TARGET] [REGISTRY] [TAG]  Build with legacy docker build
    all [REGISTRY] [TAG]             Build all targets
    push REGISTRY [TAG]              Push all images to registry
    clean                            Clean build cache
    setup                            Setup Buildx builder

TARGETS:
    dev     Development container with full features (default)
    prod    Production container with minimal features
    ci      CI/CD container for automated builds

EXAMPLES:
    $0 bake                          # Build dev target
    $0 bake prod                     # Build production target
    $0 all myregistry.com v1.0.0     # Build all targets with registry and tag
    $0 push myregistry.com v1.0.0    # Push all images
    $0 clean                         # Clean cache

ENVIRONMENT VARIABLES:
    REGISTRY    Container registry (e.g., ghcr.io/myorg/)
    TAG         Image tag (default: latest)
    DOCKER_BUILDKIT    Enable BuildKit (default: 1)

EOF
}

# Main function
main() {
    check_buildx

    case "${1:-bake}" in
        bake)
            setup_builder
            build_bake "${2:-dev}" "${3:-}" "${4:-latest}"
            ;;
        legacy)
            build_legacy "${2:-dev}" "${3:-}" "${4:-latest}"
            ;;
        all)
            setup_builder
            build_all "${2:-}" "${3:-latest}"
            ;;
        push)
            if [ $# -lt 2 ]; then
                log_error "Registry is required for push"
                usage
                exit 1
            fi
            setup_builder
            push_images "$2" "${3:-latest}"
            ;;
        clean)
            clean_cache
            ;;
        setup)
            setup_builder
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