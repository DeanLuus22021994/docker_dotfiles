---
started: 2025-01-15
completed: 2025-01-15
author: AI Assistant
version: 3.0
status: active
description: Enterprise-grade basic Docker Compose stack with security enhancements, Redis caching, and comprehensive testing
tags: [docker, compose, basic-stack, nodejs, python314, postgres, redis, security, enterprise]
---

# Basic Stack - Enterprise Edition

## Overview

The basic stack provides a complete development environment with enterprise-grade security features, Redis caching, and comprehensive testing capabilities. This is the recommended starting point for development and testing.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Node.js       │    │   Python        │    │  PostgreSQL     │    │     Redis       │
│   (Frontend)    │◄──►│   (FastAPI)     │◄──►│   (Database)    │    │   (Cache)      │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │    │   Port: 6379   │
│                 │    │                 │    │                 │    │                 │
│ • React/Vite    │    │ • REST API      │    │ • Persistent     │    │ • Session store │
│ • Hot reload    │    │ • Security MW   │    │ • Health checks │    │ • Rate limiting │
│ • Development   │    │ • Input validation│    │ • Named volumes │    │ • Health checks │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Services

### Node.js Service
- **Technology**: Node.js 22 with Vite
- **Port**: 3000
- **Features**: Modern React development with hot reload
- **Health Check**: HTTP endpoint availability

### Python Service (FastAPI)
- **Technology**: Python 3.14+ with FastAPI and Uvicorn
- **Port**: 8000
- **Security Features**:
  - API key authentication
  - Rate limiting with Redis
  - CORS protection
  - Security headers
  - Input validation with Pydantic
- **Endpoints**:
  - `GET /health` - Health check
  - `GET /api/status` - API status
  - `POST /api/inventory` - Inventory management
  - `GET /api/link-check` - Link validation

### PostgreSQL Database
- **Technology**: PostgreSQL 15+
- **Port**: 5432
- **Features**:
  - Persistent data storage
  - Named volumes (`docker_examples_db_data`)
  - Health checks with `pg_isready`
  - Docker secrets for password management

### Redis Cache
- **Technology**: Redis 7+
- **Port**: 6379
- **Features**:
  - High-performance caching
  - Session storage
  - Rate limiting data
  - Health checks with `redis-cli ping`
  - Named volumes (`docker_examples_redis_data`)

## Quick Start

### Prerequisites
- Docker Engine 24.0+
- Docker Compose V2
- Python 3.14+ (for validation)
- 4GB RAM minimum

### Setup and Run
```bash
# Navigate to basic stack directory
cd .docker-compose/basic-stack

# Validate configuration
docker compose config

# Start services
docker compose up -d

# View logs
docker compose logs -f

# Check health
docker compose ps
```

### Access Services
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432 (from host)
- **Redis**: localhost:6379 (from host)

## Security Configuration

### API Authentication
```bash
# Generate API key
openssl rand -hex 32

# Configure in environment
echo "API_KEY=your_generated_key" >> .env

# Test authentication
curl -H "X-API-Key: your_key" http://localhost:8000/api/status
```

### Environment Variables
Create a `.env` file in the project root:
```bash
# Database
POSTGRES_DB=mydb
POSTGRES_USER=user

# Security
API_KEY=your_secure_api_key
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
CORS_ORIGINS=http://localhost:3000
SECURITY_HEADERS_ENABLED=true
INPUT_VALIDATION_ENABLED=true

# External APIs (optional)
GITHUB_TOKEN=your_github_token
```

## Development Workflow

### Running Tests
```bash
# Run Python tests
docker compose -f ../mcp/python_utils/docker-compose.yml run --rm test

# Run with coverage
docker compose -f ../mcp/python_utils/docker-compose.yml run --rm test-coverage
```

### Database Operations
```bash
# Connect to database
docker compose exec db psql -U user -d mydb

# Run migrations (if applicable)
docker compose exec python alembic upgrade head

# Backup database
docker compose exec db pg_dump -U user mydb > backup.sql
```

### Debugging
```bash
# View all logs
docker compose logs -f

# View specific service logs
docker compose logs -f python

# Access service shell
docker compose exec python bash

# Check resource usage
docker stats
```

## Health Checks

All services include comprehensive health checks:

| Service | Check Command | Interval | Timeout | Retries |
|---------|---------------|----------|---------|---------|
| **node** | `curl -f http://localhost:3000` | 30s | 10s | 3 |
| **python** | `python -c "import sys; sys.exit(0)"` | 30s | 10s | 3 |
| **db** | `pg_isready -U user -d mydb` | 30s | 10s | 3 |
| **redis** | `redis-cli ping` | 30s | 10s | 3 |

## Volumes and Data Persistence

### Named Volumes
- `docker_examples_db_data` - PostgreSQL data
- `docker_examples_db_logs` - PostgreSQL logs
- `docker_examples_redis_data` - Redis data

### Backup Strategy
```bash
# Backup database
docker run --rm -v docker_examples_db_data:/data \
  -v $(pwd):/backup ubuntu \
  tar czf /backup/db_backup_$(date +%Y%m%d).tar.gz /data

# Backup Redis (if persistent)
docker run --rm -v docker_examples_redis_data:/data \
  -v $(pwd):/backup ubuntu \
  tar czf /backup/redis_backup_$(date +%Y%m%d).tar.gz /data
```

## Networking

Services communicate over the `docker_examples_basic-stack-network`:
- **Internal DNS**: Services can reach each other by service name
- **Port Exposure**: Only necessary ports exposed to host
- **Isolation**: Services isolated from other Docker networks

## Troubleshooting

### Common Issues

**Services won't start**:
```bash
# Check for port conflicts
netstat -tulpn | grep -E ':3000|:8000|:5432|:6379'

# Validate configuration
docker compose config

# Check Docker resources
docker system df
```

**Database connection fails**:
```bash
# Verify database is running
docker compose ps db

# Check database logs
docker compose logs db

# Test connection
docker compose exec db pg_isready -U user -d mydb
```

**API authentication fails**:
```bash
# Verify API key configuration
docker compose exec python env | grep API_KEY

# Check security middleware logs
docker compose logs python | grep -i auth
```

See [troubleshooting.md](../../docs/troubleshooting.md) for detailed solutions.

## Performance Optimization

### Resource Limits
```yaml
# In docker-compose.yml
services:
  python:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### Build Optimization
- Multi-stage Docker builds
- Layer caching with BuildKit
- Dependency optimization

## Production Considerations

### Security Hardening
- Use strong, randomly generated passwords
- Enable all security middleware features
- Configure proper CORS origins
- Use Docker secrets in production

### Monitoring
- Implement centralized logging
- Set up metrics collection
- Configure alerting for health check failures

### Scaling
For production workloads, consider:
- Cluster example with load balancing
- Swarm stack for orchestration
- External Redis cluster
- Database read replicas

## Recent Updates

### Version 3.0 - Enterprise Security
- ✅ **Redis Integration**: Added Redis caching service
- ✅ **Security Middleware**: API authentication, rate limiting, CORS
- ✅ **Input Validation**: Pydantic model validation
- ✅ **Health Checks**: Comprehensive service monitoring
- ✅ **Documentation**: Updated for enterprise features

### Version 2.2 - Python 3.14
- ✅ Python 3.14 with performance optimizations
- ✅ Enhanced testing capabilities
- ✅ Build caching improvements

### Version 2.1 - Multi-Service Architecture
- ✅ Node.js frontend integration
- ✅ PostgreSQL persistence
- ✅ Named volume management
