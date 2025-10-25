# Cluster Dashboard - Makefile
.PHONY: help install dev build docker-build docker-run docker-stop deploy clean

help: ## Show this help message
	@echo "Cluster Dashboard - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	@echo "Installing dependencies..."
	@cd web-content && npm install --legacy-peer-deps

dev: ## Start development server
	@echo "Starting development server..."
	@cd web-content && npm run dev

build: ## Build production bundle
	@echo "Building production bundle..."
	@cd web-content && npm run build

docker-build: build ## Build Docker image
	@echo "Building Docker image..."
	@cd web-content && docker build -t cluster-dashboard:latest .

docker-run: ## Run Docker container
	@echo "Starting Docker container..."
	@docker stop cluster-dashboard 2>/dev/null || true
	@docker rm cluster-dashboard 2>/dev/null || true
	@docker run -d \
		--name cluster-dashboard \
		-p 3000:80 \
		--restart unless-stopped \
		cluster-dashboard:latest
	@echo "Dashboard running at http://localhost:3000"

docker-stop: ## Stop Docker container
	@echo "Stopping Docker container..."
	@docker stop cluster-dashboard 2>/dev/null || true
	@docker rm cluster-dashboard 2>/dev/null || true

deploy: docker-build docker-run ## Build and deploy with Docker

clean: ## Clean build artifacts and dependencies
	@echo "Cleaning build artifacts..."
	@cd web-content && rm -rf dist node_modules package-lock.json

lint: ## Run ESLint
	@cd web-content && npm run lint

type-check: ## Run TypeScript type checking
	@cd web-content && npm run type-check

test: lint type-check ## Run all tests
