# MCP Python Utils Dockerfiles

This directory contains optimized Dockerfiles for the MCP Python utilities stack. These custom Dockerfiles provide Python 3.14-specific optimizations with comprehensive build caching and testing capabilities.

## Benefits

### 🚀 **Python 3.14 Optimizations**

- **Free-threaded execution**: True parallelism with concurrent interpreters
- **Enhanced pathlib**: Direct file operations with improved performance
- **Build caching**: Multi-layer caching for pip, pytest, mypy, and ruff
- **Virtual environment isolation**: Persistent Python environments

### 🔒 **Security & Reliability**

- **Non-root user execution**: Services run as unprivileged users
- **Health checks**: Built-in monitoring for service availability
- **Resource optimization**: Memory and CPU efficient configurations
- **Dependency isolation**: Virtual environments prevent conflicts

### 📦 **Development & Testing**

- **Comprehensive caching**: Separate caches for all Python tools
- **Test runner service**: Dedicated container for running tests
- **Coverage reporting**: HTML and terminal coverage reports
- **Hot reloading**: Cached volumes for instant rebuilds

### 🏥 **MCP Integration**

- **Model Context Protocol**: Server implementation for AI assistants
- **API endpoints**: RESTful interfaces for utility functions
- **Concurrent processing**: Multi-threaded link checking and analysis
- **Component inventory**: Automated React component analysis

## Services

### Python Service (`python.Dockerfile`)

- **Base image**: Python 3.14 slim
- **Multi-stage build**: base → deps → runner
- **Features**:
  - System dependencies for PostgreSQL, Redis, Docker
  - Virtual environment with pip caching
  - MCP server with FastAPI backend
  - Health checks and monitoring
  - Non-root user execution

### Test Runner Service

- **Dedicated testing container**: Isolated test execution
- **Coverage reporting**: HTML and terminal output
- **Cache persistence**: pytest, mypy, ruff caches
- **Dependency sharing**: Reuses main service virtual environment

## Architecture

```
MCP Python Utils Stack
├── Python Service (FastAPI/MCP Server)
│   ├── API Endpoints (/api/*)
│   ├── Link Checker Utilities
│   ├── Component Inventory Analysis
│   └── Document Processing
└── Test Runner (Optional)
    ├── Unit Tests
    ├── Integration Tests
    └── Coverage Reports
```

## Usage

### Development Mode

```bash
# Start MCP server
docker-compose up python

# Run tests
docker-compose --profile test up test-runner

# Or run both
docker-compose --profile test up
```

### Production Mode

```bash
# Build optimized images
docker-compose build

# Start services
docker-compose up -d

# Check health
docker-compose ps
```

## Volume Management

### Named Volumes for Caching

- **react_scuba_python_venv**: Python virtual environment
- **python_cache**: pip package cache
- **python_pytest_cache**: pytest cache
- **python_mypy_cache**: mypy cache
- **python_ruff_cache**: ruff cache
- **test_coverage**: coverage report output

### Cache Benefits

- **Instant rebuilds**: Dependencies cached between builds
- **Cross-stack reuse**: Volumes shared with other stacks
- **Persistent state**: Virtual environments survive container restarts
- **Performance optimization**: <30 second rebuilds after initial setup

## Configuration

### Environment Variables

```bash
# Python optimizations
PYTHONOPTIMIZE=1
PYTHONDONTWRITEBYTECODE=1

# Application settings
HOST=0.0.0.0
PORT=8000
PYTHONPATH=/app/python_utils:/app

# Development
PYTHONUNBUFFERED=1
```

### Health Checks

- **Interval**: 15 seconds
- **Timeout**: 5 seconds
- **Retries**: 5 attempts
- **Start period**: 20 seconds

## Testing Integration

### Test Runner Features

- **pytest execution**: Comprehensive test suite
- **Coverage reporting**: HTML and terminal output
- **Cache persistence**: Faster subsequent test runs
- **Dependency isolation**: Separate from main service

### Coverage Reports

```bash
# View HTML coverage
open htmlcov/index.html

# Terminal summary
docker-compose --profile test logs test-runner
```

## MCP Server Endpoints

### API Endpoints

- `GET /health`: Service health check
- `POST /api/links/check`: Batch link validation
- `POST /api/components/inventory`: Component analysis
- `POST /api/docs/process`: Document processing

### MCP Protocol

- **Tool registration**: Dynamic tool discovery
- **Concurrent execution**: Multi-threaded processing
- **Error handling**: Comprehensive error responses
- **Logging**: Structured JSON logging

## Troubleshooting

### Build Issues

- **Cache conflicts**: Clear volumes with `docker-compose down -v`
- **Permission errors**: Ensure proper user permissions
- **Network issues**: Check Docker network connectivity

### Runtime Issues

- **Port conflicts**: Verify port availability (8001)
- **Health check failures**: Check logs with `docker-compose logs`
- **Memory issues**: Monitor with `docker stats`

### Testing Issues

- **Test failures**: Check test-runner logs
- **Coverage errors**: Verify source code paths
- **Cache issues**: Clear test caches if corrupted

## Integration with Other Stacks

### Volume Sharing

The MCP Python utils stack shares named volumes with other stacks:

- **react_scuba_python_venv**: Shared with basic-stack, cluster-example, swarm-stack
- **python_cache**: Shared pip cache across all Python services
- **python_*_cache**: Tool-specific caches for development efficiency

### Cross-Stack Dependencies

- **Database connectivity**: Can connect to PostgreSQL from other stacks
- **API consumption**: Other services can call MCP endpoints
- **Shared utilities**: Common Python utilities available to all stacks

## Performance Optimization

### Build Time Improvements

- **BuildKit**: Advanced Docker build features
- **Layer caching**: Dependencies cached in separate layers
- **Multi-stage builds**: Optimized image sizes
- **Named volumes**: Persistent caches between builds

### Runtime Optimizations

- **Python 3.14 features**: Free-threaded execution
- **Virtual environments**: Isolated dependency management
- **Resource limits**: Appropriate memory and CPU allocation
- **Health monitoring**: Proactive issue detection

## Migration Notes

This stack provides enhanced MCP capabilities with Python 3.14 optimizations. The dockerfiles are designed for integration with the broader React Scuba ecosystem while maintaining backward compatibility.
</content>
<parameter name="filePath">c:\react_scuba_runner\react-scuba\docker-compose-examples\mcp\python_utils\dockerfiles\README.md
