#!/usr/bin/env bash
# Build static documentation site with MkDocs
# Version: 1.0
# Last Modified: 2025-10-26

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
SERVE=false
DEPLOY=false
CLEAN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --serve)
            SERVE=true
            shift
            ;;
        --deploy)
            DEPLOY=true
            shift
            ;;
        --clean)
            CLEAN=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --serve   Build and serve locally (default port: 8000)"
            echo "  --deploy  Build and deploy to GitHub Pages"
            echo "  --clean   Clean build directory before building"
            echo "  --help    Show this help"
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
echo "  MkDocs Documentation Builder"
echo "========================================"
echo -e "${NC}"

# Check if MkDocs is installed
if ! command -v mkdocs &> /dev/null; then
    echo -e "${RED}MkDocs not installed!${NC}"
    echo -e "${CYAN}Install with: pip install mkdocs mkdocs-material${NC}"
    exit 1
fi

# Clean if requested
if [[ "$CLEAN" == "true" ]]; then
    echo -e "${YELLOW}Cleaning build directory...${NC}"
    rm -rf site/
    echo -e "${GREEN}✓ Cleaned${NC}\n"
fi

# Build documentation
echo -e "${CYAN}Building documentation...${NC}"

if mkdocs build --clean --strict; then
    echo -e "${GREEN}✓ Documentation built successfully${NC}"
    echo -e "${CYAN}Output directory: ./site/${NC}\n"
else
    echo -e "${RED}✗ Build failed${NC}"
    exit 1
fi

# Serve locally
if [[ "$SERVE" == "true" ]]; then
    echo -e "${CYAN}Starting local server...${NC}"
    echo -e "${GREEN}Documentation available at: http://127.0.0.1:8000${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop${NC}\n"
    mkdocs serve
fi

# Deploy to GitHub Pages
if [[ "$DEPLOY" == "true" ]]; then
    echo -e "${CYAN}Deploying to GitHub Pages...${NC}"
    
    if mkdocs gh-deploy --clean --force; then
        echo -e "${GREEN}✓ Deployed successfully${NC}"
        echo -e "${CYAN}Documentation available at: https://your-username.github.io/docker_dotfiles/${NC}\n"
    else
        echo -e "${RED}✗ Deployment failed${NC}"
        exit 1
    fi
fi

if [[ "$SERVE" != "true" ]] && [[ "$DEPLOY" != "true" ]]; then
    echo -e "${GREEN}Documentation build complete!${NC}"
    echo -e "${CYAN}To serve locally: $0 --serve${NC}"
    echo -e "${CYAN}To deploy: $0 --deploy${NC}\n"
fi
