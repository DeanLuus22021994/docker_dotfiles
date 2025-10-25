# Makefile for Docker Cluster Implementation
# Turn-key modern data platform with GPU support

.PHONY: help build up down logs ps restart clean validate dev test-all test-health test-connectivity

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
	@echo "Testing:"
	@echo "  make test-all    - Run all tests"
	@echo "  make test-health - Check service health"
	@echo "  make test-conn   - Test connectivity"
	@echo ""
	@echo "Maintenance:"
	@echo "  make validate    - Validate configuration"
	@echo "  make clean       - Clean resources"

build:
	@echo "Building all images with BuildKit..."
	@docker-compose build

up:
	@echo "Starting production cluster..."
	@docker-compose up -d loadbalancer cluster-web1 cluster-web2 cluster-web3 cluster-postgres cluster-redis cluster-mariadb cluster-github-mcp cluster-jupyter cluster-minio cluster-grafana cluster-prometheus

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
	@echo "Validating configuration..."
	@docker-compose config > /dev/null
	@echo "Configuration valid"

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

test-all: validate test-health test-conn
	@echo "All tests completed"
