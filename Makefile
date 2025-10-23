.PHONY: help validate build test clean up down logs ps

# Default target
help:
	@echo "Docker Compose Management - Available targets:"
	@echo ""
	@echo "  make validate    - Validate all Docker Compose configurations"
	@echo "  make build       - Build all Docker images"
	@echo "  make test        - Run validation and tests on all stacks"
	@echo "  make clean       - Remove all containers, volumes, and images"
	@echo "  make up          - Start all services in basic-stack"
	@echo "  make down        - Stop all services"
	@echo "  make logs        - View logs from all services"
	@echo "  make ps          - List running containers"
	@echo ""

# Validate all docker-compose configurations
validate:
	@echo "Validating all Docker Compose stacks..."
	python .docker-compose/validate_stacks.py

# Build all images with caching
build:
	@echo "Building all Docker images..."
	python .docker-compose/validate_stacks.py --build

# Run validation and integration tests
test:
	@echo "Running validation and tests..."
	python .docker-compose/validate_stacks.py --build --test

# Clean up Docker resources
clean:
	@echo "Cleaning up Docker resources..."
	python .docker-compose/validate_stacks.py --cleanup
	docker system prune -f
	@echo "Cleanup complete!"

# Start basic-stack services
up:
	@echo "Starting basic-stack services..."
	docker-compose -f .docker-compose/basic-stack/docker-compose.yml up -d

# Stop all services
down:
	@echo "Stopping all services..."
	docker-compose -f .docker-compose/basic-stack/docker-compose.yml down

# View logs
logs:
	docker-compose -f .docker-compose/basic-stack/docker-compose.yml logs -f

# List running containers
ps:
	docker-compose -f .docker-compose/basic-stack/docker-compose.yml ps
