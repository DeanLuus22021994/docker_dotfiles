---
started: 2025-01-15
completed: 2025-01-15
author: AI Assistant
version: 3.0
status: active
description: Enterprise-grade Docker Compose examples with security enhancements, Redis caching, and comprehensive testing
tags: [docker, compose, examples, security, redis, enterprise, python314, fastapi]
---

# Docker Compose Examples - Enterprise Edition

## Overview

A comprehensive collection of Docker Compose configurations demonstrating enterprise-grade application deployment patterns with advanced security, caching, and monitoring capabilities.

## Architecture Features

### Core Services
- **Python FastAPI** (3.14+): REST API with enterprise security middleware
- **Node.js** (22+): Modern frontend with Vite
- **PostgreSQL** (15+): Primary relational database
- **Redis** (7+): High-performance caching and session management

### Security Enhancements
- API key authentication with configurable keys
- Rate limiting with Redis-backed storage
- CORS protection with configurable origins
- Security headers (HSTS, CSP, X-Frame-Options)
- Input validation with Pydantic models
- Request correlation ID tracking

### Enterprise Features
- Health checks with configurable intervals
- Named volumes for data persistence
- Docker secrets for credential management
- Comprehensive logging and monitoring
- Multi-stack deployment patterns

## Available Stacks

### 1. Basic Stack (`basic-stack/`)
**Purpose**: Development and testing environment
**Services**: Python, Node.js, PostgreSQL, Redis
**Use Case**: Local development, unit testing, CI/CD pipelines

### 2. Cluster Example (`cluster-example/`)
**Purpose**: Load-balanced multi-instance deployment
**Services**: 3x Python replicas, Node.js, PostgreSQL, Redis, Nginx
**Use Case**: Testing horizontal scaling, load balancing

### 3. Swarm Stack (`swarm-stack/`)
**Purpose**: Production orchestration with Docker Swarm
**Services**: Replicated services with overlay networking
**Use Case**: Production deployments, service discovery

### 4. MCP Python Utils (`mcp/python_utils/`)
**Purpose**: Testing and validation utilities
**Services**: Python testing environment with comprehensive tooling
**Use Case**: Automated testing, code quality validation

## Quick Start

### Prerequisites
- Docker Engine 24.0+
- Docker Compose V2
- Python 3.14+
- 4GB RAM minimum

### Setup
```bash
# Clone repository
git clone <repository-url>
cd docker-compose-examples

# Configure secrets
echo "your_db_password" > secrets/db_password.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start basic stack
docker compose -f .docker-compose/basic-stack/docker-compose.yml up -d

# Access services
# Frontend: http://localhost:3000
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Security Configuration

### API Authentication
```bash
# Generate secure API key
openssl rand -hex 32

# Configure in .env
API_KEY=your_generated_key_here

# Use in requests
curl -H "X-API-Key: your_key" http://localhost:8000/api/status
```

### Rate Limiting
```bash
# Configure limits in .env
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

### CORS Setup
```bash
# Configure allowed origins
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

## Validation & Testing

### Automated Validation
```bash
# Validate all stack configurations
python .docker-compose/validate_stacks.py

# Run comprehensive tests
docker compose -f .docker-compose/mcp/python_utils/docker-compose.yml run --rm test
```

### Health Checks
All services include health checks with enterprise-grade monitoring:
- **Interval**: 30s
- **Timeout**: 10s
- **Retries**: 3
- **Start Period**: 40s

## Development Workflow

### Local Development
```bash
# Start development stack
docker compose -f .docker-compose/basic-stack/docker-compose.yml up

# View logs
docker compose -f .docker-compose/basic-stack/docker-compose.yml logs -f

# Run tests
docker compose -f .docker-compose/mcp/python_utils/docker-compose.yml run --rm test
```

### Production Deployment
```bash
# Use Swarm stack for production
docker stack deploy -c .docker-compose/swarm-stack/docker-compose.yml docker_examples

# Scale services
docker service scale docker_examples_python=5
```

## Documentation

- [Architecture Overview](../docs/architecture.md)
- [Deployment Guide](../docs/deployment.md)
- [Troubleshooting](../docs/troubleshooting.md)
- [API Documentation](http://localhost:8000/docs) (when running)

## Recent Updates

### Version 3.0 - Enterprise Security (Current)
- ✅ **Security Enhancements**: API authentication, rate limiting, CORS, security headers
- ✅ **Redis Integration**: All stacks now include Redis caching services
- ✅ **Input Validation**: Comprehensive Pydantic model validation
- ✅ **Mock Removal**: Eliminated all mock implementations for production readiness
- ✅ **Documentation**: Updated all docs to reflect current enterprise architecture

### Version 2.2 - Python 3.14 Support
- ✅ Python 3.14 with free-threaded execution
- ✅ Enhanced caching and build optimization
- ✅ Comprehensive testing integration

### Version 2.1 - Multi-Stack Architecture
- ✅ Basic, cluster, and swarm deployment patterns
- ✅ Named volumes for data persistence
- ✅ Health checks and monitoring

## Contributing

1. Follow conventional commit standards
2. Update documentation for any architecture changes
3. Include tests for new features
4. Validate all stacks before submitting PRs

## Support

- [Issues](https://github.com/your-repo/issues)
- [Documentation](../docs/)
- [Troubleshooting Guide](../docs/troubleshooting.md)
