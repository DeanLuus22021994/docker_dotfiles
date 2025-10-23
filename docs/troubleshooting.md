# Troubleshooting Guide

Common issues and their solutions for Docker Compose Examples.

## Container Issues

### Containers Won't Start

**Symptom**: Services fail to start or immediately exit

**Possible Causes**:
1. Port conflicts
2. Missing dependencies
3. Invalid configuration
4. Resource constraints

**Solutions**:

```bash
# Check logs
docker compose -f .docker-compose/basic-stack/docker-compose.yml logs <service-name>

# Check for port conflicts
sudo netstat -tulpn | grep <port-number>
# Or
lsof -i :<port-number>

# Restart Docker daemon
sudo systemctl restart docker

# Rebuild images
docker compose -f .docker-compose/basic-stack/docker-compose.yml build --no-cache

# Check disk space
docker system df
df -h
```

### Container Keeps Restarting

**Symptom**: Container status shows "Restarting"

**Solutions**:

```bash
# Check logs for errors
docker compose -f .docker-compose/basic-stack/docker-compose.yml logs --tail=100 <service-name>

# Check health check status
docker inspect <container-id> | grep -A 20 Health

# Disable auto-restart temporarily
docker update --restart=no <container-id>

# Debug interactively
docker compose -f .docker-compose/basic-stack/docker-compose.yml run --rm <service-name> bash
```

## Database Issues

### Cannot Connect to PostgreSQL

**Symptom**: Connection refused or timeout errors

**Solutions**:

```bash
# Verify database is running
docker compose -f .docker-compose/basic-stack/docker-compose.yml ps db

# Check database logs
docker compose -f .docker-compose/basic-stack/docker-compose.yml logs db

# Verify password secret exists
ls -la secrets/db_password.txt

# Test connection manually
docker compose -f .docker-compose/basic-stack/docker-compose.yml exec db psql -U user -d mydb

# Check if database initialized
docker compose -f .docker-compose/basic-stack/docker-compose.yml exec db pg_isready
```

### Database Data Lost

**Symptom**: Data disappears after restart

**Solutions**:

```bash
# Verify volume exists
docker volume ls | grep docker_examples_db_data

# Don't use -v flag when stopping
docker compose -f .docker-compose/basic-stack/docker-compose.yml down  # Good
# NOT: docker compose down -v  # Bad - removes volumes!

# Restore from backup
cat backup.sql | docker compose -f .docker-compose/basic-stack/docker-compose.yml exec -T db psql -U user mydb
```

## Network Issues

### Services Can't Communicate

**Symptom**: Service A cannot reach Service B

**Solutions**:

```bash
# Verify both services on same network
docker network inspect docker_examples_basic-stack-network

# Test connectivity
docker compose -f .docker-compose/basic-stack/docker-compose.yml exec python ping db
docker compose -f .docker-compose/basic-stack/docker-compose.yml exec python curl http://node:3000

# Check DNS resolution
docker compose -f .docker-compose/basic-stack/docker-compose.yml exec python nslookup db
```

### Port Already in Use

**Symptom**: "port is already allocated" error

**Solutions**:

```bash
# Find what's using the port
sudo lsof -i :3000
sudo netstat -tulpn | grep :3000

# Kill the process
sudo kill -9 <PID>

# Or change port in docker-compose.yml
# Change "3000:3000" to "3001:3000"
```

## Build Issues

### Build Fails with "No Space Left"

**Symptom**: Build fails with disk space errors

**Solutions**:

```bash
# Clean up Docker resources
docker system prune -af
docker volume prune -f

# Check disk space
docker system df
df -h

# Remove unused images
docker image prune -af

# Remove build cache
docker builder prune -af
```

### Build Fails with Network Timeout

**Symptom**: Cannot download packages during build

**Solutions**:

```bash
# Use Docker BuildKit with better caching
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# Retry build
docker compose -f .docker-compose/basic-stack/docker-compose.yml build --no-cache

# Check internet connection
ping google.com

# Use different package mirror (in Dockerfile)
# RUN --mount=type=cache... apt-get update
```

## Performance Issues

### Services Running Slow

**Symptom**: High CPU or memory usage

**Solutions**:

```bash
# Check resource usage
docker stats

# Increase Docker resources (Docker Desktop)
# Settings -> Resources -> Increase CPUs and Memory

# Add resource limits to docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G

# Optimize images (multi-stage builds already implemented)
```

### Database Slow Queries

**Symptom**: Slow database operations

**Solutions**:

```bash
# Connect to database
docker compose -f .docker-compose/basic-stack/docker-compose.yml exec db psql -U user -d mydb

# Check slow queries
SELECT * FROM pg_stat_activity WHERE state = 'active';

# Add indexes if needed
CREATE INDEX idx_name ON table(column);

# Increase shared_buffers (in postgresql.conf)
```

## Secret Management Issues

### Secret File Not Found

**Symptom**: "no such file or directory: /run/secrets/db_password"

**Solutions**:

```bash
# Verify secret file exists
ls -la secrets/db_password.txt

# Verify secrets configuration in docker-compose.yml
# Should have:
secrets:
  db_password:
    file: ../../secrets/db_password.txt

# Recreate containers
docker compose -f .docker-compose/basic-stack/docker-compose.yml down
docker compose -f .docker-compose/basic-stack/docker-compose.yml up -d
```

## Health Check Failures

### All Health Checks Failing

**Symptom**: Containers show "unhealthy" status

**Solutions**:

```bash
# Check health check logs
docker inspect <container-id> | grep -A 50 Health

# Test health check command manually
docker compose -f .docker-compose/basic-stack/docker-compose.yml exec <service> <health-check-command>

# Example for PostgreSQL
docker compose -f .docker-compose/basic-stack/docker-compose.yml exec db pg_isready -U user -d mydb

# Increase start_period if services take longer to start
healthcheck:
  start_period: 60s  # Increase from 40s
```

## Environment Variable Issues

### Environment Variables Not Set

**Symptom**: Application cannot find configuration

**Solutions**:

```bash
# Verify .env file exists and is loaded
cat .env

# Check environment variables in container
docker compose -f .docker-compose/basic-stack/docker-compose.yml exec <service> env

# Ensure .env file is in same directory as docker-compose.yml
# Or explicitly specify:
docker compose --env-file .env.development -f .docker-compose/basic-stack/docker-compose.yml up
```

## Volume Permission Issues

### Permission Denied Errors

**Symptom**: Cannot write to mounted volumes

**Solutions**:

```bash
# Check volume ownership
docker compose -f .docker-compose/basic-stack/docker-compose.yml exec <service> ls -la /path/to/volume

# Fix permissions
docker compose -f .docker-compose/basic-stack/docker-compose.yml exec <service> chown -R app:app /path/to/volume

# Or run container as root temporarily (not recommended for production)
user: root
```

## Docker Compose Version Issues

### Unsupported Compose File Format

**Symptom**: "version is obsolete" or similar errors

**Solutions**:

```bash
# Check Docker Compose version
docker compose version

# Update Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Or use Docker Compose V2 syntax (no version field)
# Modern docker-compose.yml files don't need version field
```

## Getting More Help

### Useful Commands for Debugging

```bash
# Full system information
docker info
docker version

# Inspect container
docker inspect <container-id>

# Container processes
docker top <container-id>

# Resource usage
docker stats

# Network details
docker network inspect <network-name>

# Volume details
docker volume inspect <volume-name>
```

### Where to Get Help

1. Check logs: `docker compose logs`
2. Review this troubleshooting guide
3. Check GitHub Issues: https://github.com/DeanLuus22021994/docker_dotfiles/issues
4. Docker documentation: https://docs.docker.com
5. Stack Overflow: https://stackoverflow.com/questions/tagged/docker-compose

## Common Error Messages

| Error Message | Likely Cause | Solution |
|---------------|--------------|----------|
| "Cannot connect to Docker daemon" | Docker not running | `sudo systemctl start docker` |
| "Conflict. The container name is already in use" | Container already exists | `docker rm <container>` or use `docker compose down` |
| "No space left on device" | Disk full | `docker system prune -af` |
| "port is already allocated" | Port conflict | Change port or stop other service |
| "manifest unknown" | Image not found | Check image name and tag |
| "network not found" | Network deleted or not created | `docker compose up` creates networks |
| "volume in use" | Volume mounted elsewhere | `docker volume rm` with force |
