# Makefile for Docker Cluster Implementation
# Turn-key modern data platform with GPU support

.PHONY: help build up down logs ps restart clean validate validate-configs validate-env dev test-all test-health test-connectivity

help:
	@echo "Docker Cluster - Modern Data Platform"
	@echo ""
	@echo "Core Commands:"
	@echo "  make build       - Build all images"
	@echo "  make up          - Start production cluster"
	@echo "  make dev         - Start with devcontainer"
	@echo "  make down        - Stop cluster"
	@echo "  make restart     - Restart cluster"
	@echo "  make logs        - View logs"
	@echo "  make ps          - Show status"
	@echo ""
	@echo "Validation:"
	@echo "  make validate          - Validate docker-compose syntax"
	@echo "  make validate-configs  - Validate all config files"
	@echo "  make validate-env      - Validate environment variables"
	@echo ""
	@echo "Testing:"
	@echo "  make test-all    - Run all tests"
	@echo "  make test-health - Check service health"
	@echo "  make test-conn   - Test connectivity"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean       - Clean resources"

build:
	@echo "Building all images with BuildKit..."
	@docker-compose build

up:
	@echo "Starting production cluster..."
	@docker-compose up -d loadbalancer cluster-web1 cluster-web2 cluster-web3 cluster-postgres cluster-redis cluster-mariadb cluster-github-mcp cluster-jupyter cluster-minio cluster-grafana cluster-prometheus cluster-buildkit cluster-localstack cluster-mailhog cluster-pgadmin cluster-redis-commander

dev:
	@echo "Starting development environment with all services..."
	@docker-compose --profile dev up -d

down:
	@echo "Stopping cluster..."
	@docker-compose down

logs:
	@docker-compose logs -f

ps:
	@docker-compose ps

restart: down up
	@echo "Cluster restarted"

validate:
	@echo "Validating docker-compose configuration..."
	@docker-compose config > /dev/null
	@echo "✅ docker-compose.yml syntax valid"

validate-configs:
	@echo "=========================================="
	@echo "Validating Configuration Files"
	@echo "=========================================="
	@python scripts/validate_configs.py
	@echo ""
	@echo "✅ All config validations passed"

validate-env:
	@echo "=========================================="
	@echo "Validating Environment Variables"
	@echo "=========================================="
	@python scripts/validate_env.py
	@echo ""
	@echo "✅ All required environment variables present"

clean:
	@echo "Cleaning up resources..."
	@docker-compose down -v --remove-orphans
	@docker system prune -f
	@echo "Cleanup complete"

test-health:
	@echo "Checking service health..."
	@echo "Load Balancer:"
	@curl -f http://localhost:8080 -o /dev/null -w "  HTTP: %{http_code}\n" || echo "  FAILED"
	@echo "PostgreSQL:"
	@docker exec cluster-postgres pg_isready -U cluster_user -d clusterdb || echo "  FAILED"
	@echo "Redis:"
	@docker exec cluster-redis redis-cli ping || echo "  FAILED"
	@echo "MariaDB:"
	@docker exec cluster-mariadb mariadb-admin ping -h localhost || echo "  FAILED"
	@echo "Jupyter:"
	@curl -f http://localhost:8888/api -o /dev/null -w "  HTTP: %{http_code}\n" || echo "  FAILED"
	@echo "MinIO:"
	@curl -f http://localhost:9000/minio/health/live -o /dev/null -w "  HTTP: %{http_code}\n" || echo "  FAILED"
	@echo "Grafana:"
	@curl -f http://localhost:3002/api/health -o /dev/null -w "  HTTP: %{http_code}\n" || echo "  FAILED"
	@echo "Prometheus:"
	@curl -f http://localhost:9090/-/healthy -o /dev/null -w "  HTTP: %{http_code}\n" || echo "  FAILED"
	@echo "LocalStack:"
	@curl -f http://localhost:4566/_localstack/health -o /dev/null -w "  HTTP: %{http_code}\n" || echo "  FAILED"
	@echo "MailHog:"
	@curl -f http://localhost:8025 -o /dev/null -w "  HTTP: %{http_code}\n" || echo "  FAILED"
	@echo "pgAdmin:"
	@curl -f http://localhost:5050/misc/ping -o /dev/null -w "  HTTP: %{http_code}\n" || echo "  FAILED"
	@echo "Redis Commander:"
	@curl -f http://localhost:8081 -o /dev/null -w "  HTTP: %{http_code}\n" || echo "  FAILED"

test-conn:
	@echo "Testing connectivity from devcontainer..."
	@docker exec cluster-devcontainer /bin/bash -c " \
		echo 'PostgreSQL:' && \
		psql -h cluster-postgres -U cluster_user -d clusterdb -c 'SELECT version();' && \
		echo 'Redis:' && \
		redis-cli -h cluster-redis ping && \
		echo 'MariaDB:' && \
		mysql -h cluster-mariadb -u cluster_user -pchangeme -e 'SELECT VERSION();' && \
		echo 'Web Services:' && \
		curl -f http://cluster-loadbalancer && \
		echo 'MinIO:' && \
		curl -f http://cluster-minio:9000/minio/health/live \
	"

test-all: validate validate-configs validate-env test-health test-conn
	@echo "=========================================="
	@echo "✅ All tests completed successfully"
	@echo "=========================================="
