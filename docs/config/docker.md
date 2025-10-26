---
date_created: "2025-10-26T18:32:25.942834+00:00"
last_updated: "2025-10-26T18:32:25.942834+00:00"
tags: ['documentation', 'configuration', 'setup', 'docker']
description: "Documentation for docker"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- docker
- documentation
description: Documentation for docker in config
---\n# Docker Configuration

This directory contains Docker-specific configuration files for local development and production deployments.

## Files

### `daemon.json`
Docker daemon configuration - **for reference only**.

**Location to apply:**
- **Linux**: `/etc/docker/daemon.json`
- **Windows (WSL2)**: `%USERPROFILE%\.docker\daemon.json` or WSL: `/etc/docker/daemon.json`
- **macOS**: `~/.docker/daemon.json`

**Key settings:**
- BuildKit enabled by default
- JSON file logging with 30MB rotation (3×10MB)
- Overlay2 storage driver
- Custom network pools to avoid conflicts
- 20GB build cache

**Apply changes:**
```bash
# Linux/macOS
sudo systemctl restart docker

# Windows Docker Desktop
# Restart Docker Desktop from system tray
```

### `buildkitd.toml`
BuildKit daemon configuration for the `cluster-buildkit` service.

**Usage:** Mounted into the BuildKit container via docker-compose.yml

**Key Features:**
- **10GB cache** with 3-day retention
- **Multi-platform support**: amd64, arm64
- **OCI workers** with rootless execution
- **Garbage collection**: Automatic cleanup of old build cache
- **Build history**: 7-day retention with max 50 records

**Cache Settings:**
```toml
[worker.oci]
  max-parallelism = 4
  
[[worker.oci.gcpolicy]]
  keepBytes = 10737418240  # 10GB
  keepDuration = 259200    # 3 days
  filters = [ "type==source.local", "type==exec.cachemount", "type==source.git.checkout"]
```

**Platform Support:**
```toml
platforms = ["linux/amd64", "linux/arm64"]
```

**Validation:**
```bash
# Check if mounted correctly
docker exec cluster-buildkit cat /etc/buildkit/buildkitd.toml

# View cache usage
docker exec cluster-buildkit buildctl debug workers
```

### `compose.override.example.yml`
Template for local docker-compose overrides.

**Setup:**
```bash
# Copy to root (file is gitignored)
cp .config/docker/compose.override.example.yml docker-compose.override.yml

# Edit for your local environment
# Changes ports, volumes, environment variables, etc.
```

**Usage:**
- Automatically loaded by `docker-compose` commands
- Overrides/extends main `docker-compose.yml`
- Never committed (in `.gitignore`)

## Quick Start for New Developers

### 1. Configure Docker Daemon (Optional)
```bash
# Linux
sudo cp .config/docker/daemon.json /etc/docker/daemon.json
sudo systemctl restart docker

# Windows/macOS
# Manually copy settings to Docker Desktop preferences
```

### 2. Set Up BuildKit (Optional)
```bash
# BuildKit is pre-configured in the cluster-buildkit service
# No manual setup required - just use docker-compose

# To verify BuildKit service
docker-compose ps cluster-buildkit
```

### 3. Create Local Overrides
```bash
# Copy template
cp .config/docker/compose.override.example.yml docker-compose.override.yml

# Customize for your environment
# Example: Change ports, add debug volumes, etc.
```

### 4. Verify Configuration
```bash
# Check Docker daemon config
docker info | grep -i buildkit

# Validate compose files
docker-compose config --quiet

# Test build with BuildKit
docker-compose build cluster-docker-api
```

## Best Practices

### For Local Development
1. **Use overrides file** - Keep local changes in `docker-compose.override.yml`
2. **Port conflicts** - Override ports in your local file
3. **Hot reload** - Mount local code directories
4. **Debug mode** - Enable verbose logging
5. **Resource limits** - Adjust based on your machine

### For Production
1. **Apply daemon.json** - Consistent logging and limits
2. **Enable BuildKit** - Faster builds and better caching
3. **No overrides** - Use only main `docker-compose.yml`
4. **Secrets** - Always use Docker secrets, never env vars
5. **Health checks** - Verify all services are healthy

## Troubleshooting

### BuildKit not enabled
```bash
# Check if BuildKit is active
docker buildx version

# Enable BuildKit
export DOCKER_BUILDKIT=1
```

### Port conflicts
```bash
# Check what's using ports
netstat -ano | findstr ":5432"  # Windows
lsof -i :5432                    # Linux/macOS

# Override in docker-compose.override.yml
```

### Disk space issues
```bash
# Clean up Docker
docker system prune -a --volumes

# Check disk usage
docker system df
```

### Permission errors (Linux)
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Fix daemon.json permissions
sudo chmod 644 /etc/docker/daemon.json
```

## References

- [Docker Daemon Configuration](https://docs.docker.com/engine/reference/commandline/dockerd/#daemon-configuration-file)
- [BuildKit Configuration](https://github.com/moby/buildkit/blob/master/docs/buildkitd.toml.md)
- [Docker Compose Override](https://docs.docker.com/compose/extends/)
