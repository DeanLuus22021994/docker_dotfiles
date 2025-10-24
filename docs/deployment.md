# Deployment Guide

This guide provides step-by-step instructions for deploying Docker Compose Examples in different environments.

## Prerequisites

- Docker Engine 24.0+ with Compose V2
- Git
- Python 3.14+ (for validation scripts)
- At least 4GB RAM available for Docker
- 8GB free disk space
- Redis service (included in all stacks)
- PostgreSQL database (included in all stacks)

## Environment Setup

### 1. Clone Repository

```bash
git clone https://github.com/DeanLuus22021994/docker_dotfiles.git
cd docker_dotfiles
```

### 2. Configure Secrets

```bash
# Create secrets directory (if not exists)
mkdir -p secrets

# Create database password
echo "your_secure_password_here" > secrets/db_password.txt

# Ensure secrets are not tracked by git
ls secrets/db_password.txt  # Should exist but not be in git status
```

### 3. Choose Environment Configuration

Copy the appropriate environment file:

```bash
# For development
cp .env.development .env

# For production
cp .env.production .env
# Edit .env and replace placeholder values with actual credentials

# For Docker testing
cp .env.docker .env
```

### 4. Configure Security Settings

Edit the `.env` file to configure security features:

```bash
# Security Configuration
API_KEY=your_secure_api_key_here
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
SECURITY_HEADERS_ENABLED=true
INPUT_VALIDATION_ENABLED=true
```

## Security Configuration

### API Key Authentication

1. Generate a secure API key:
```bash
openssl rand -hex 32
```

2. Add to your `.env` file:
```bash
API_KEY=your_generated_api_key_here
```

3. Include API key in requests:
```bash
curl -H "X-API-Key: your_api_key" http://localhost:8000/api/status
```

### Rate Limiting

Configure rate limits in `.env`:
```bash
# Requests per window (seconds)
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

### CORS Configuration

Configure allowed origins:
```bash
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### Security Headers

Enable security headers (enabled by default):
```bash
SECURITY_HEADERS_ENABLED=true
```

### Option 1: Basic Stack (Development)

Best for: Local development, testing, single developer

```bash
# Validate configuration
python .docker-compose/validate_stacks.py

# Start services
docker compose -f .docker-compose/basic-stack/docker-compose.yml up -d

# View logs
docker compose -f .docker-compose/basic-stack/docker-compose.yml logs -f

# Access services
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - PostgreSQL: localhost:5432
```

### Option 2: Cluster Example (Production-like)

Best for: Testing load balancing, multi-instance setups

```bash
# Build images
docker compose -f .docker-compose/cluster-example/docker-compose.yml build

# Start cluster
docker compose -f .docker-compose/cluster-example/docker-compose.yml up -d

# Scale services
docker compose -f .docker-compose/cluster-example/docker-compose.yml up -d --scale web1=3

# Access via load balancer
# - Load Balancer: http://localhost:8080
```

### Option 3: Swarm Stack (Production)

Best for: Production deployments with orchestration

```bash
# Initialize Docker Swarm (if not already)
docker swarm init

# Deploy stack
docker stack deploy -c .docker-compose/swarm-stack/docker-compose.yml docker_examples

# View services
docker service ls

# Scale a service
docker service scale docker_examples_python=5

# View service logs
docker service logs docker_examples_python

# Remove stack
docker stack rm docker_examples
```

## Post-Deployment Verification

### 1. Check Service Health

```bash
# Basic stack
docker compose -f .docker-compose/basic-stack/docker-compose.yml ps

# All services should show "healthy" or "running"
```

### 2. Test Database Connection

```bash
# Connect to PostgreSQL
docker compose -f .docker-compose/basic-stack/docker-compose.yml exec db psql -U user -d mydb

# Run test query
SELECT version();
```

### 3. Test API Endpoint

```bash
# Health check
curl http://localhost:8000/health

# API endpoint
curl http://localhost:8000/api/status
```

### 4. Test Frontend

Open browser to http://localhost:3000 and verify application loads

## Updating Deployment

### Update Services

```bash
# Pull latest code
git pull origin main

# Rebuild images
docker compose -f .docker-compose/basic-stack/docker-compose.yml build --no-cache

# Restart services
docker compose -f .docker-compose/basic-stack/docker-compose.yml up -d
```

### Rolling Updates (Swarm)

```bash
# Update service with zero downtime
docker service update --image docker_examples_python:latest docker_examples_python
```

## Backup and Restore

### Backup Database

```bash
# Create backup
docker compose -f .docker-compose/basic-stack/docker-compose.yml exec db pg_dump -U user mydb > backup.sql

# Or use volume backup
docker run --rm -v docker_examples_db_data:/data -v $(pwd):/backup ubuntu tar czf /backup/db_backup.tar.gz /data
```

### Restore Database

```bash
# From SQL dump
cat backup.sql | docker compose -f .docker-compose/basic-stack/docker-compose.yml exec -T db psql -U user mydb

# From volume backup
docker run --rm -v docker_examples_db_data:/data -v $(pwd):/backup ubuntu tar xzf /backup/db_backup.tar.gz -C /
```

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for common issues and solutions.

## Monitoring

### View Resource Usage

```bash
# Container stats
docker stats

# Disk usage
docker system df
```

### View Logs

```bash
# All services
docker compose -f .docker-compose/basic-stack/docker-compose.yml logs -f

# Specific service
docker compose -f .docker-compose/basic-stack/docker-compose.yml logs -f python

# Last 100 lines
docker compose -f .docker-compose/basic-stack/docker-compose.yml logs --tail=100
```

## Cleanup

### Stop Services

```bash
# Stop and keep data
docker compose -f .docker-compose/basic-stack/docker-compose.yml stop

# Stop and remove containers (keep volumes)
docker compose -f .docker-compose/basic-stack/docker-compose.yml down

# Stop and remove everything including volumes
docker compose -f .docker-compose/basic-stack/docker-compose.yml down -v
```

### Clean Docker System

```bash
# Using Makefile
make clean

# Manual cleanup
docker system prune -af
docker volume prune -f
```

## Security Considerations

1. **Always use Docker secrets** for sensitive data
2. **Never commit** `.env` files or `secrets/` directory
3. **Use strong passwords** in production
4. **Limit exposed ports** in production
5. **Keep Docker and images updated**
6. **Run containers as non-root** (already configured)
7. **Use read-only filesystems** where possible
8. **Enable Docker Content Trust** in production

## Production Checklist

- [ ] All secrets configured with strong passwords
- [ ] Environment variables set correctly
- [ ] Backups configured and tested
- [ ] Monitoring and alerting in place
- [ ] SSL/TLS certificates configured (if using HTTPS)
- [ ] Firewall rules configured
- [ ] Log rotation configured
- [ ] Resource limits set on containers
- [ ] Health checks verified
- [ ] Disaster recovery plan documented
