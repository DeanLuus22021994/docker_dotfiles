# Docker Configuration Overview

**Central Docker configuration reference for local development and production.**

## Configuration Files

- **daemon.json** - Docker Engine configuration (BuildKit, experimental features)
- **buildkitd.toml** - BuildKit daemon configuration for cluster-buildkit service
- **compose.override.example.yml** - Local development overrides template

## Key Features

- BuildKit v0.25.1 with multi-platform support (7 architectures)
- 250GB build cache with optimization
- Beta features: Docker AI, MCP Toolkit, Wasm Support, Model Runner
- GPU support for ML workloads (RTX consumer-grade GPU)
- Network isolation (172.20.0.0/16 custom pools)

## Quick Setup

### Linux/macOS

```bash
# Copy daemon configuration
sudo cp .config/docker/daemon.json /etc/docker/daemon.json
sudo systemctl restart docker
```

### Windows (WSL2)

```cmd
# Copy to Windows Docker Desktop
copy .config\docker\daemon.json %USERPROFILE%\.docker\daemon.json
# Restart Docker Desktop from system tray
```

## Detailed Configuration

For specific configuration details, see:

- [Docker Daemon Configuration](daemon-config.md)
- [BuildKit Configuration](buildkit-config.md)
- [Compose Overrides](compose-overrides.md)
- [Beta Features Setup](beta-features.md)

## Validation

```bash
# Validate configuration
docker system info | grep -E "(BuildKit|Experimental|Storage Driver)"

# Check build cache
docker buildx du

# Verify multi-platform support
docker buildx ls
```

**For troubleshooting, see [Docker Troubleshooting](../troubleshooting/docker.md)**
