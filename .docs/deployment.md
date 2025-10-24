---
started: 2025-10-24
completed: 2025-10-24
author: AI Assistant
version: 1.0
status: active
description: Step-by-step deployment guide for Docker Compose Examples across all environments
tags: [docker, compose, deployment, environments, production]
---

# Docker Compose Examples - Deployment Guide

## Prerequisites
- Docker Engine 24.0+ with Compose V2
- Python 3.14+ (for validation)
- 4GB RAM, 8GB disk space
- Git for cloning

## Quick Start
```bash
git clone https://github.com/DeanLuus22021994/docker_dotfiles.git
cd docker_dotfiles
echo "your_secure_password" > secrets/db_password.txt
cp .env.development .env
./setup-python-mcp.sh
```

## Stack Deployment

### Basic Stack (Development)
```bash
docker compose -f .compose/basic-stack/docker-compose.yml up -d
# Frontend: http://localhost:3000, API: http://localhost:8000, MCP: http://localhost:8001
```

### Cluster Example (Load Balancing)
```bash
docker compose -f .compose/cluster-example/docker-compose.yml up -d
docker compose -f .compose/cluster-example/docker-compose.yml up -d --scale python=3
# Frontend: http://localhost:3000, API: http://localhost:8080 (nginx)
```

### Swarm Stack (Production)
```bash
docker swarm init
docker stack deploy -c .compose/swarm-stack/docker-compose.yml docker_examples
docker service scale docker_examples_python=5
```

## Environment Configuration

### Security Setup
```bash
openssl rand -hex 32  # Generate API key
# Configure in .env: API_KEY, RATE_LIMIT_REQUESTS, CORS_ORIGINS
```

### Database Configuration
```bash
# PostgreSQL: POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD_FILE
# Redis: REDIS_URL=redis://redis:6379 (auto-configured)
```

## Validation & Testing

### Automated Validation
```bash
python .compose/validate_stacks.py
docker compose -f .compose/mcp/docker-compose.yml run --rm test
```

### Health Checks
```bash
docker compose -f .compose/basic-stack/docker-compose.yml ps
docker compose -f .compose/basic-stack/docker-compose.yml logs -f
```

## Production Deployment

### Monitoring Setup
```bash
docker compose -f .compose/monitoring/docker-compose.yml up -d
# Prometheus: http://localhost:9090, Grafana: http://localhost:3001
```

## Troubleshooting

### Common Issues
#### Port Conflicts
```bash
netstat -tulpn | grep :3000
# Stop conflicting services or change ports in docker-compose.yml
```

#### Permission Issues
```bash
sudo chown -R 1001:1001 volumes/
docker compose -f .compose/basic-stack/docker-compose.yml down -v
```

#### Memory Issues
```bash
docker system df
docker system prune -f
```

#### Logs & Debugging
```bash
docker compose -f .compose/basic-stack/docker-compose.yml logs
docker compose -f .compose/basic-stack/docker-compose.yml logs -f python
docker compose -f .compose/basic-stack/docker-compose.yml exec python bash
```

## Maintenance

### Updates
```bash
docker compose -f .compose/basic-stack/docker-compose.yml pull
docker compose -f .compose/basic-stack/docker-compose.yml up -d
```

### Cleanup
```bash
docker compose -f .compose/basic-stack/docker-compose.yml down
docker compose -f .compose/basic-stack/docker-compose.yml down -v  # WARNING: destroys data
docker system prune -f
```

## Support
- Issues: GitHub repository issues
- Documentation: See .docs/ directory
- Logs: Use `docker logs` for debugging
- Health: Check service health endpoints
