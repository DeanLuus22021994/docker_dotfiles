# API Overview

**Express.js Docker API server for container management and monitoring.**

## Purpose

The backend API provides secure access to Docker functionality through a REST interface:

- Container status and metrics
- Service health monitoring
- Docker socket proxy integration
- Authentication and authorization

## Quick Start

```bash
cd backend
npm install
npm start
```

The API will be available at: http://localhost:3000

## Endpoints

### Health & Status

- `GET /api/health` - API health check (public)
- `GET /api/status` - System status summary

### Container Management

- `GET /api/containers` - List all containers
- `GET /api/containers/:id` - Container details
- `GET /api/containers/:id/stats` - Container statistics

### Services

- `GET /api/services` - List all services
- `GET /api/services/:id` - Service details

## Authentication

When `AUTH_ENABLED=true`, all `/api/*` endpoints require authentication:

- JWT token authentication
- Basic auth for development
- Session management

## Configuration

Key configuration files:

- **server.js** - Main Express application
- **auth.js** - Authentication middleware
- **middleware.js** - Request processing and Docker integration

## Docker Integration

The API connects to Docker via:

- **READ-ONLY socket proxy** (cluster-docker-api:2375)
- **Security**: No direct Docker socket access
- **Networks**: cluster-backend, cluster-frontend

## Development

```bash
npm run dev      # Development with nodemon
npm run test     # Run test suite
npm run lint     # ESLint validation
```

## Architecture

For detailed information, see:

- [Authentication](../security/authentication.md)
- [Docker Socket Security](../security/docker-socket/overview.md)
- [API Reference](api-reference.md)

**For production deployment, see [Production Guide](../production/api-deployment.md)**
