# Custom Dockerfiles for Basic Stack

This directory contains optimized Dockerfiles for the basic-stack Docker Compose example. These custom Dockerfiles provide several advantages over the default images:

## Benefits

### 🚀 Performance Optimizations

- **Multi-stage builds**: Separate stages for dependencies, building, and runtime to minimize image size
- **Layer caching**: Optimized Docker layers for faster rebuilds
- **Named volume mounts**: Persistent volumes for `node_modules`, Python virtual environments, and pip cache

### 🔒 Security Enhancements

- **Non-root users**: Services run as non-privileged users
- **Minimal attack surface**: Only essential packages installed
- **Health checks**: Built-in health monitoring for all services

### 📦 Dependency Management

- **Pre-installed dependencies**: Dependencies installed during build, not runtime
- **Virtual environments**: Isolated Python environments
- **Optimized caching**: Dependencies cached in separate layers

### 🏥 Reliability Improvements

- **Health checks**: Integrated health monitoring
- **Proper configuration**: Optimized PostgreSQL configuration
- **Error handling**: Better error detection and recovery

## Services

### Node.js Service (`node.Dockerfile`)

- **Base image**: Node.js 20 Alpine
- **Multi-stage build**: base → deps → dev-deps → builder → runner
- **Features**:
  - System dependencies pre-installed
  - Production and development dependencies separated
  - Health check endpoint
  - Non-root user execution

### Python Service (`python.Dockerfile`)

- **Base image**: Python 3.14 slim
- **Multi-stage build**: base → deps → runner
- **Features**:
  - Virtual environment isolation
  - System dependencies for Python packages
  - Health check validation
  - Non-root user execution

### PostgreSQL Service (`postgres.Dockerfile`)

- **Base image**: PostgreSQL 13 Alpine
- **Features**:
  - Custom configuration file
  - Performance monitoring (pg_stat_statements)
  - Optimized memory settings
  - Health check integration

## Usage

The Docker Compose file automatically uses these custom Dockerfiles. To build and run:

```bash
# Build custom images
docker-compose build

# Start services
docker-compose up

# Or run in background
docker-compose up -d
```

## Development Workflow

### First Build

- Dependencies are installed during build
- May take longer due to dependency installation
- Subsequent builds are much faster

### Subsequent Builds

- Named volumes cache dependencies
- Only source code changes trigger rebuilds
- Virtual environments persist between builds

### Volume Management

```bash
# Clear all volumes (fresh start)
docker-compose down -v

# Clear specific volumes
docker volume rm basic-stack_node_modules
docker volume rm basic-stack_python_venv
docker volume rm basic-stack_python_cache
```

## Configuration

### PostgreSQL
Custom configuration in `postgresql.conf` includes:

- Performance optimizations
- Monitoring settings
- Security enhancements
- Logging configuration

### Environment Variables
All environment variables remain the same as the original configuration.

## Troubleshooting

### Build Issues

- Ensure Docker has sufficient resources
- Check network connectivity for package downloads
- Verify volume permissions

### Runtime Issues

- Check health status: `docker-compose ps`
- View logs: `docker-compose logs [service]`
- Verify volume mounts: `docker volume ls`

### Performance Issues

- Monitor resource usage: `docker stats`
- Check health endpoints
- Review PostgreSQL configuration

## Migration from Default Images

The custom Dockerfiles are drop-in replacements for the default images. No changes to docker-compose.yml are required beyond the build context updates.
