# Docker DevContainer with Buildx and Bake

A high-performance development container optimized with Docker Buildx and Bake for maximum build efficiency and caching.

## Features

- **Docker Buildx**: Advanced multi-platform builds with persistent caching
- **Docker Bake**: High-level build orchestration with parallel execution
- **Volume Mount Caching**: Persistent caches for Python, Node.js, and development tools
- **Multi-layer Optimization**: Strategic Dockerfile layering for optimal cache utilization
- **Precompilation**: Dual-phase precompilation (build-time + runtime) for instant startup
- **Multi-target Builds**: Separate targets for development, production, and CI/CD

## Quick Start

### Using Make (Recommended)

```bash
# Build development container with Bake
make buildx-bake

# Build all targets (dev, prod, ci)
make buildx-all

# Push to registry
make buildx-push REGISTRY=ghcr.io/myorg/

# Clean cache
make buildx-clean
```

### Using Build Script Directly

```bash
# Build development target
./build.sh bake dev

# Build production target
./build.sh bake prod

# Build all targets
./build.sh all

# Push to registry
./build.sh push ghcr.io/myorg/ v1.0.0
```

## Build Targets

### Development (`dev`)
- Full development environment with all tools
- Pre-installed Python and Node.js dependencies
- Precompiled bytecode and warmed caches
- GitHub Actions runner integration
- MariaDB database server

### Production (`prod`)
- Minimal production environment
- Optimized for runtime performance
- Reduced attack surface
- Production-ready configurations

### CI/CD (`ci`)
- Optimized for automated builds
- GitHub Actions cache integration
- SBOM and provenance attestations
- Registry caching enabled

## Caching Strategy

The container uses a comprehensive caching strategy:

### Build-time Caching
- **UV Cache**: Python package manager cache
- **Pip Cache**: Fallback Python package cache
- **NPM Cache**: Node.js package cache
- **MyPy Cache**: Type checking cache
- **Ruff Cache**: Linting cache

### Runtime Volume Mounts
- `docker_devcontainer_pip_cache`: Pip package cache
- `docker_devcontainer_npm_cache`: NPM package cache
- `docker_devcontainer_uv_cache`: UV package cache
- `docker_devcontainer_mypy_cache`: MyPy type checking cache
- `docker_devcontainer_ruff_cache`: Ruff linting cache
- `docker_devcontainer_pytest_cache`: Test cache
- `docker_devcontainer_precommit_cache`: Pre-commit hooks cache
- `docker_devcontainer_jupyter_cache`: Jupyter notebook cache
- `docker_devcontainer_conda_cache`: Conda environment cache

### Registry Caching
- Local cache: `/tmp/.buildx-cache`
- Registry cache: `${REGISTRY}devcontainer:cache-${TAG}`
- GitHub Actions cache: `gha` scope for CI builds

## Performance Optimizations

### Dockerfile Layer Strategy
1. **Base Dependencies**: Rarely changing system packages
2. **Language Runtimes**: Python, Node.js installations
3. **Package Managers**: UV, npm installations
4. **Application Dependencies**: Python/Node.js packages
5. **Precompilation**: Bytecode compilation and cache warming
6. **Configuration**: Final setup and user configuration

### Buildx Features
- **Multi-platform builds**: `linux/amd64` support
- **Cache mounting**: `--mount=type=cache` for persistent caches
- **Inline cache**: `BUILDKIT_INLINE_CACHE=1` for metadata caching
- **Cache export/import**: Registry and local cache backends

### Bake Configuration
- **Parallel builds**: Multiple targets built simultaneously
- **Conditional builds**: Different configurations per target
- **Variable substitution**: Registry and tag parameterization
- **Cache orchestration**: Coordinated cache management across targets

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `REGISTRY` | Container registry URL | `""` |
| `TAG` | Image tag | `"latest"` |
| `BUILDKIT_INLINE_CACHE` | Enable inline caching | `"1"` |
| `DOCKER_BUILDKIT` | Enable BuildKit | `"1"` |

## Advanced Usage

### Custom Registry
```bash
export REGISTRY=ghcr.io/myorg/
export TAG=v1.2.3
make buildx-all
make buildx-push
```

### CI/CD Integration
```yaml
- name: Build and push
  run: |
    make buildx-all REGISTRY=ghcr.io/myorg/ TAG=${{ github.sha }}
    make buildx-push
```

### Local Development
```bash
# Use local registry for testing
docker run -d -p 5000:5000 --name registry registry:2
export REGISTRY=localhost:5000/
make buildx-all
make buildx-push
```

## Troubleshooting

### Buildx Issues
```bash
# Check Buildx installation
docker buildx version

# List builders
docker buildx ls

# Inspect current builder
docker buildx inspect

# Reset builder
docker buildx rm devcontainer-builder
make buildx-bake  # Recreates builder
```

### Cache Issues
```bash
# Clear all caches
make buildx-clean
docker system prune -a

# Check cache usage
docker buildx du
```

### Performance Issues
```bash
# Enable debug logging
export BUILDKIT_PROGRESS=plain
make buildx-bake

# Check build timing
time make buildx-bake
```

## Architecture

```
.devcontainer/
├── devcontainer.json          # DevContainer configuration
├── devcontainer.dockerfile    # Multi-layer optimized Dockerfile
├── scripts/                   # Configuration scripts
│   ├── start.sh              # GitHub Actions runner
│   ├── init.sql              # MariaDB initialization
│   ├── my.cnf                # MariaDB configuration
│   └── supervisord.conf      # Process supervision
└── assets/                   # Static assets

docker-bake.hcl               # Bake configuration
build.sh                      # Build orchestration script
.dockerignore                 # Build context optimization
Makefile                      # Development tasks
```

## Contributing

1. Update `docker-bake.hcl` for new build targets
2. Modify `build.sh` for new build logic
3. Update this README for new features
4. Test builds with `make buildx-all`

## License

See repository license file.