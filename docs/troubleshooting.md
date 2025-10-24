---
started: 2025-10-24
completed: 2025-10-24
author: AI Assistant
version: 1.0
status: active
description: Common issues and solutions for Docker Compose deployment
tags: [docker, compose, troubleshooting, debugging, errors]
---

# Docker Compose - Troubleshooting Guide

## Container Issues

### Containers Won't Start
```bash
# Check logs
docker compose -f .compose/basic-stack/docker-compose.yml logs <service-name>

# Check port conflicts
netstat -tulpn | grep :3000

# Restart Docker daemon
sudo systemctl restart docker

# Check disk space
docker system df
```

### Container Keeps Restarting
```bash
# Check logs for errors
docker compose -f .compose/basic-stack/docker-compose.yml logs --tail=100 <service-name>

# Check health status
docker inspect <container-id> | grep -A 20 Health

# Debug interactively
docker compose -f .compose/basic-stack/docker-compose.yml run --rm <service-name> bash
```

## Database Issues

### Cannot Connect to PostgreSQL
```bash
# Verify database is running
docker compose -f .compose/basic-stack/docker-compose.yml ps db

# Check database logs
docker compose -f .compose/basic-stack/docker-compose.yml logs db

# Test connection manually
docker compose -f .compose/basic-stack/docker-compose.yml exec db psql -U user -d mydb

# Check if database initialized
docker compose -f .compose/basic-stack/docker-compose.yml exec db pg_isready
```

### Database Data Lost
```bash
# Verify volume exists
docker volume ls | grep docker_db_data

# Don't use -v flag when stopping
docker compose -f .compose/basic-stack/docker-compose.yml down  # Good

# Restore from backup
cat backup.sql | docker compose -f .compose/basic-stack/docker-compose.yml exec -T db psql -U user mydb
```

## Network Issues

### Services Can't Communicate
```bash
# Test connectivity
docker compose -f .compose/basic-stack/docker-compose.yml exec python ping db

# Check DNS resolution
docker compose -f .compose/basic-stack/docker-compose.yml exec python nslookup db

# Verify network
docker network inspect docker_basic-stack-network
```

### Port Already in Use
```bash
# Find what's using the port
lsof -i :3000

# Kill the process
kill -9 <PID>

# Or change port in docker-compose.yml
# Change "3000:3000" to "3001:3000"
```

## Build Issues

### Build Fails with "No Space Left"
```bash
# Clean up Docker resources
docker system prune -af

# Check disk space
docker system df

# Remove build cache
docker builder prune -af
```

### Build Fails with Network Timeout
```bash
# Use BuildKit
export DOCKER_BUILDKIT=1

# Retry build
docker compose -f .compose/basic-stack/docker-compose.yml build --no-cache

# Check internet connection
ping google.com
```

## Common Error Messages

| Error Message | Likely Cause | Solution |
|---------------|--------------|----------|
| "Cannot connect to Docker daemon" | Docker not running | `sudo systemctl start docker` |
| "port is already allocated" | Port conflict | Change port or stop other service |
| "No space left on device" | Disk full | `docker system prune -af` |
| "network not found" | Network deleted | `docker compose up` creates networks |

### Support Resources
- **Logs**: `docker compose logs`
- **GitHub Issues**: Repository issues page
- **Docker Docs**: https://docs.docker.com
- **Stack Overflow**: Search for docker-compose tag
