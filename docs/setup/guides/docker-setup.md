---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["setup", "docker", "containers", "services"]
description: "Docker setup and service deployment"
---
# Docker Setup

## Build Images

```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build api nginx
```

## Start Services

```bash
# Start all services (detached)
docker-compose up -d

# Start specific services
docker-compose up -d postgres redis

# View logs
docker-compose logs -f

# Follow specific service logs
docker-compose logs -f api
```

## Verify Deployment

```bash
# Check service status
docker-compose ps

# Check service health
docker-compose exec api curl http://localhost:3000/health

# Access services
# - Dashboard: http://localhost
# - API: http://localhost:3000
# - Grafana: http://localhost:3001
# - Prometheus: http://localhost:9090
```

## Manage Services

```bash
# Stop all services
docker-compose stop

# Stop specific service
docker-compose stop api

# Restart service
docker-compose restart api

# Remove all containers
docker-compose down

# Remove with volumes
docker-compose down -v
```

## Troubleshooting

- Port conflicts: Check if ports already in use
- Build failures: Clear cache with `docker-compose build --no-cache`
- Network issues: Restart Docker daemon
