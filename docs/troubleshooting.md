# Troubleshooting Guide

Common issues and solutions for the Docker cluster implementation.

## Service Issues

### Services Won't Start

```bash
# Check logs
make logs

# Validate configuration
make validate

# Check service health
docker-compose ps
```

### Port Conflicts

```bash
# Windows
netstat -ano | findstr :8080
netstat -ano | findstr :5432

# Linux/Mac
lsof -i :8080
lsof -i :5432

# Solution: Stop conflicting service or change ports in docker-compose.yml
```

### Container Exits Immediately

```bash
# Check container logs
docker-compose logs <service_name>

# Check exit code
docker-compose ps

# Restart service
docker-compose restart <service_name>
```

## Database Issues

### Cannot Connect to Database

```bash
# Test connection
docker-compose exec db psql -U cluster_user -d clusterdb -c "SELECT 1;"

# Check database is running
docker-compose ps db

# Check logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Database Performance Issues

```bash
# Check connections
docker-compose exec db psql -U cluster_user -d clusterdb -c "SELECT count(*) FROM pg_stat_activity;"

# Check database size
docker-compose exec db psql -U cluster_user -d clusterdb -c "SELECT pg_size_pretty(pg_database_size('clusterdb'));"

# Vacuum database
docker-compose exec db psql -U cluster_user -d clusterdb -c "VACUUM ANALYZE;"
```

## Load Balancer Issues

### Load Balancer Not Distributing Traffic

```bash
# Check upstream servers
docker-compose exec loadbalancer cat /etc/nginx/conf.d/default.conf

# Check nginx logs
docker-compose logs loadbalancer

# Test each web server directly
docker-compose exec web1 curl localhost
docker-compose exec web2 curl localhost
docker-compose exec web3 curl localhost
```

### 502 Bad Gateway

```bash
# Check if web servers are healthy
docker-compose ps

# Check web server logs
docker-compose logs web1 web2 web3

# Restart web servers
docker-compose restart web1 web2 web3
```

## DevContainer Issues

### DevContainer Won't Start

```bash
# Check Docker is running
docker ps

# Rebuild devcontainer
docker-compose build devcontainer

# Start with logs
docker-compose --profile dev up devcontainer
```

### VS Code Extensions Not Loading

```bash
# Check volume
docker volume ls | grep vscode

# Remove and recreate
docker volume rm cluster_vscode_extensions
# Reopen in container
```

## Performance Issues

### High CPU Usage

```bash
# Check resource usage
docker stats

# Identify problematic container
docker stats --no-stream | sort -k3 -rh

# Add resource limits in docker-compose.yml
```

### High Memory Usage

```bash
# Check memory
docker stats --format "table {{.Name}}\t{{.MemUsage}}"

# Clear Docker cache
docker system prune -a
```

### Slow Build Times

```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Use cache
make build  # without --no-cache

# Check disk space
docker system df
```

## Network Issues

### Cannot Access Services

```bash
# Check port forwarding
docker-compose port loadbalancer 80

# Check firewall
# Windows: Check Windows Firewall
# Linux: sudo iptables -L

# Test from inside network
docker-compose exec loadbalancer curl http://web1
```

### Services Can't Communicate

```bash
# Check network
docker network ls
docker network inspect cluster-network

# Restart networking
docker-compose down
docker-compose up -d
```

## Volume Issues

### Data Not Persisting

```bash
# Check volumes
docker volume ls | grep cluster

# Inspect volume
docker volume inspect cluster_db_data

# Backup before cleanup
make clean
```

### Volume Permission Issues

```bash
# Check permissions
docker-compose exec db ls -la /var/lib/postgresql/data

# Fix permissions (if needed)
docker-compose exec -u root db chown -R postgres:postgres /var/lib/postgresql/data
```

## Build Issues

### Build Fails

```bash
# Check BuildKit
docker buildx version

# Build with verbose output
docker-compose build --progress=plain

# Clean build
make clean
make build --no-cache
```

### Image Pull Fails

```bash
# Check internet connection
ping google.com

# Check Docker Hub status
curl https://status.docker.com/

# Use mirror (if available)
# Edit /etc/docker/daemon.json
```

## Common Solutions

### Complete Reset

```bash
# Stop everything
docker-compose down -v --remove-orphans

# Clean Docker system
docker system prune -a -f
docker volume prune -f

# Rebuild
make build
make up
```

### Check Configuration

```bash
# Validate compose file
make validate

# Check Docker version
docker --version
docker-compose version

# Check system resources
docker system df
```

### Enable Debug Logging

Add to `docker-compose.yml`:

```yaml
services:
  <service_name>:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Getting Help

1. Check logs: `make logs`
2. Validate config: `make validate`
3. Review docs: `docs/architecture.md`
4. Check GitHub issues
5. Run health checks: `make ps`

## Diagnostic Commands

```bash
# Full system check
docker info
docker-compose ps
docker-compose logs --tail=50
docker stats --no-stream
docker system df

# Network diagnostic
docker network ls
docker network inspect cluster-network

# Volume diagnostic  
docker volume ls
docker volume inspect cluster_db_data
```
