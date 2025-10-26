#!/usr/bin/env bash
# Build all Docker images with BuildKit optimization
# Version: 1.0
# Last Modified: 2025-10-26

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
MAX_PARALLEL=4
USE_CACHE=true
PUSH_IMAGES=false
SINGLE_IMAGE=""
DOCKERFILE_DIR="./dockerfile"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --no-cache)
            USE_CACHE=false
            shift
            ;;
        --push)
            PUSH_IMAGES=true
            shift
            ;;
        --image)
            SINGLE_IMAGE="$2"
            shift 2
            ;;
        --parallel)
            MAX_PARALLEL="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --no-cache    Force rebuild without cache"
            echo "  --push        Push images to registry after build"
            echo "  --image NAME  Build single image only"
            echo "  --parallel N  Max parallel builds (default: 4)"
            echo "  --help        Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

echo -e "${CYAN}"
echo "========================================"
echo "  Docker BuildKit Image Builder"
echo "========================================"
echo -e "${NC}"

# Enable BuildKit
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# Get git commit SHA for tagging
GIT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "local")
BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo -e "${CYAN}Build Configuration:${NC}"
echo "  Git SHA: $GIT_SHA"
echo "  Build Date: $BUILD_DATE"
echo "  Use Cache: $USE_CACHE"
echo "  Push Images: $PUSH_IMAGES"
echo "  Max Parallel: $MAX_PARALLEL"
echo ""

# Get list of Dockerfiles
if [[ -n "$SINGLE_IMAGE" ]]; then
    DOCKERFILES=("$DOCKERFILE_DIR/$SINGLE_IMAGE.Dockerfile")
else
    mapfile -t DOCKERFILES < <(find "$DOCKERFILE_DIR" -name "*.Dockerfile" -type f | sort)
fi

if [[ ${#DOCKERFILES[@]} -eq 0 ]]; then
    echo -e "${RED}No Dockerfiles found in $DOCKERFILE_DIR${NC}"
    exit 1
fi

echo -e "${CYAN}Found ${#DOCKERFILES[@]} Dockerfiles to build${NC}\n"

# Build function
build_image() {
    local dockerfile=$1
    local basename=$(basename "$dockerfile" .Dockerfile)
    local image_name="docker-platform/$basename"
    
    echo -e "${YELLOW}Building: $basename${NC}"
    
    # Build arguments
    local build_args=(
        "build"
        "-f" "$dockerfile"
        "-t" "$image_name:latest"
        "-t" "$image_name:$GIT_SHA"
        "--label" "org.opencontainers.image.created=$BUILD_DATE"
        "--label" "org.opencontainers.image.revision=$GIT_SHA"
        "--label" "org.opencontainers.image.source=https://github.com/your-org/docker_dotfiles"
    )
    
    # Add cache arguments
    if [[ "$USE_CACHE" == "false" ]]; then
        build_args+=("--no-cache")
    fi
    
    # Add context
    build_args+=(".")
    
    # Build
    if docker "${build_args[@]}" > "/tmp/docker-build-$basename.log" 2>&1; then
        echo -e "${GREEN}✓ Built: $basename${NC}"
        
        # Push if requested
        if [[ "$PUSH_IMAGES" == "true" ]]; then
            echo -e "${CYAN}  Pushing: $image_name:latest${NC}"
            if docker push "$image_name:latest" > "/tmp/docker-push-$basename.log" 2>&1; then
                docker push "$image_name:$GIT_SHA" >> "/tmp/docker-push-$basename.log" 2>&1
                echo -e "${GREEN}  ✓ Pushed: $basename${NC}"
            else
                echo -e "${RED}  ✗ Push failed: $basename${NC}"
                cat "/tmp/docker-push-$basename.log"
            fi
        fi
        
        return 0
    else
        echo -e "${RED}✗ Build failed: $basename${NC}"
        cat "/tmp/docker-build-$basename.log"
        return 1
    fi
}

export -f build_image
export USE_CACHE PUSH_IMAGES GIT_SHA BUILD_DATE
export RED GREEN YELLOW CYAN NC

# Build images in parallel
echo -e "${CYAN}Starting parallel builds (max: $MAX_PARALLEL)...${NC}\n"

START_TIME=$(date +%s)

if command -v parallel &> /dev/null; then
    # Use GNU parallel if available
    printf '%s\n' "${DOCKERFILES[@]}" | parallel -j "$MAX_PARALLEL" build_image {}
else
    # Fallback to manual parallel execution
    pids=()
    count=0
    
    for dockerfile in "${DOCKERFILES[@]}"; do
        build_image "$dockerfile" &
        pids+=($!)
        ((count++))
        
        # Wait if max parallel reached
        if (( count >= MAX_PARALLEL )); then
            for pid in "${pids[@]}"; do
                wait "$pid"
            done
            pids=()
            count=0
        fi
    done
    
    # Wait for remaining
    for pid in "${pids[@]}"; do
        wait "$pid"
    done
fi

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo -e "\n${CYAN}========================================"
echo "  Build Complete"
echo "========================================${NC}\n"

echo -e "${GREEN}Total build time: ${DURATION}s${NC}"
echo -e "${GREEN}Images built: ${#DOCKERFILES[@]}${NC}\n"

# List built images
echo -e "${CYAN}Built images:${NC}"
docker images --filter "label=org.opencontainers.image.revision=$GIT_SHA" \
    --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

echo ""
