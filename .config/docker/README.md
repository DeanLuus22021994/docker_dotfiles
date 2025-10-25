# Docker Configuration

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

### `buildkit.toml`
BuildKit-specific configuration for optimized builds.

**Usage:**
```bash
# Set environment variable before building
export BUILDKIT_CONFIG=$PWD/.config/docker/buildkit.toml
docker-compose build
```

**Features:**
- 512MB cache retention
- 48-hour cache duration
- Docker Hub mirror (gcr.io)
- OCI worker enabled

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
# Add to ~/.bashrc or ~/.zshrc
export BUILDKIT_CONFIG=/path/to/docker_dotfiles/.config/docker/buildkit.toml
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1
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
