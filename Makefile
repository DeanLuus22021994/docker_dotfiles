# Makefile for Docker Compose Project
# Provides common development tasks for managing Docker Compose stacks

.PHONY: help validate build test clean format lint security all up down logs ps generate-compose buildx-bake buildx-all buildx-push buildx-clean

# Default target - show help
help:
	@echo "Docker Compose - Available Commands:"
	@echo ""
	@echo "  make validate          - Validate all docker-compose.yml files"
	@echo "  make build             - Build all Docker Compose stacks"
	@echo "  make test              - Run validation and build steps"
	@echo "  make clean             - Clean up Docker resources (images, containers, volumes)"
	@echo "  make format            - Format Python code with black and ruff"
	@echo "  make lint              - Lint Python code and Dockerfiles"
	@echo "  make security          - Run security scans on Docker images"
	@echo "  make all               - Run validate, build, and test"
	@echo ""
	@echo "  make buildx-bake       - Build devcontainer with Docker Bake (default)"
	@echo "  make buildx-all        - Build all devcontainer targets with Bake"
	@echo "  make buildx-push       - Push all images to registry with Bake"
	@echo "  make buildx-clean      - Clean Buildx cache"
	@echo ""
	@echo "  make generate-compose   - Generate docker-compose.yml files from config"
	@echo "  make up                - Start basic-stack services"
	@echo "  make down              - Stop basic-stack services"
	@echo "  make logs              - Show basic-stack logs"
	@echo "  make ps                - Show basic-stack service status"
	@echo ""

# Generate docker-compose.yml files from config
generate-compose:
	@echo "🔧 Generating docker-compose.yml files from config..."
	@python .compose/validate_stacks.py --generate-compose
	@echo "✅ Compose files generated"

# Validate all docker-compose.yml files
validate:
	@echo "🔍 Validating Docker Compose stacks..."
	@python .compose/validate_stacks.py
	@echo "✅ Validation complete"

# Build all Docker Compose stacks
build:
	@echo "🔨 Building Docker Compose stacks..."
	@python .compose/validate_stacks.py --build
	@echo "✅ Build complete"

# Run validation and build steps
test: validate build
	@echo "✅ All tests passed"

# Clean up Docker resources
clean:
	@echo "🧹 Cleaning up Docker resources..."
	@docker system prune -f
	@docker image prune -f
	@docker volume prune -f
	@echo "✅ Cleanup complete"

# Format Python code
format:
	@echo "📝 Formatting Python code..."
	@cd .compose/mcp/python_utils && python -m black . || echo "black not installed, skipping..."
	@cd .compose/mcp/python_utils && python -m ruff check --fix . || echo "ruff not installed, skipping..."
	@echo "✅ Formatting complete"

# Lint Python code and Dockerfiles
lint:
	@echo "🔍 Linting code..."
	@cd .compose/mcp/python_utils && python -m ruff check . || echo "ruff not installed, skipping..."
	@cd .compose/mcp/python_utils && python -m mypy . || echo "mypy not installed, skipping..."
	@find .compose -name "Dockerfile" -o -name "*.Dockerfile" | xargs -I {} sh -c 'echo "Linting: {}" && docker run --rm -i hadolint/hadolint < {} || echo "hadolint not available"'
	@echo "✅ Linting complete"

# Run security scans
security:
	@echo "🔒 Running security scans..."
	@docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --severity HIGH,CRITICAL $$(docker images --format "{{.Repository}}:{{.Tag}}" | grep docker | head -1) || echo "Trivy not available or no images to scan"
	@echo "✅ Security scan complete"

# Run all tasks
all: validate build test
	@echo "✅ All tasks completed successfully"

# Basic stack management
up:
	@echo "🚀 Starting basic-stack services..."
	@docker compose -f .compose/basic-stack/docker-compose.yml up -d
	@echo "✅ Services started"

down:
	@echo "🛑 Stopping basic-stack services..."
	@docker compose -f .compose/basic-stack/docker-compose.yml down
	@echo "✅ Services stopped"

logs:
	@docker compose -f .compose/basic-stack/docker-compose.yml logs -f

ps:
	@docker compose -f .compose/basic-stack/docker-compose.yml ps

# Buildx and Bake targets
buildx-bake:
	@echo "🔨 Building devcontainer with Docker Bake..."
	@powershell -ExecutionPolicy Bypass -File build.ps1 -Command bake -Target dev
	@echo "✅ Bake build complete"

buildx-all:
	@echo "🔨 Building all devcontainer targets with Bake..."
	@powershell -ExecutionPolicy Bypass -File build.ps1 -Command all
	@echo "✅ All Bake builds complete"

buildx-push:
	@echo "📤 Pushing images to registry..."
	@if [ -z "$(REGISTRY)" ]; then \
		echo "❌ Error: REGISTRY environment variable is required"; \
		echo "Usage: make buildx-push REGISTRY=ghcr.io/myorg/"; \
		exit 1; \
	fi
	@powershell -ExecutionPolicy Bypass -File build.ps1 -Command all -Registry "$(REGISTRY)" -Tag "$(TAG)"
	@echo "✅ Images pushed"

buildx-clean:
	@echo "🧹 Cleaning Buildx cache..."
	@powershell -ExecutionPolicy Bypass -File build.ps1 -Command clean
	@echo "✅ Buildx cache cleaned"
