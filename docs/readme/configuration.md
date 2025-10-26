---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["configuration", "settings", "validation", "pre-commit"]
description: "Configuration management and validation procedures"
---

# Configuration

## Configuration Management (SSoT)

All configurations centralized in `.config/` directory:

**Nginx Configs** (`.config/nginx/`):
- `loadbalancer.conf` - Load balancer routing
- `main.conf` - Worker processes, gzip, security headers
- `default.conf` - Static content, API endpoints

**Database Configs** (`.config/database/`):
- `postgresql.conf` - max_connections: 200, shared_buffers: 256MB
- `mariadb.conf` - utf8mb4, innodb_buffer_pool: 256MB

**Service Configs** (`.config/services/`):
- `pgadmin-servers.json` - Pre-configured connections
- `localstack-init.sh` - S3 buckets, DynamoDB tables

**Docker Configs** (`.config/docker/`):
- `buildkitd.toml` - 10GB cache, 3-day retention

## Validation Commands

```bash
make validate-configs  # Validate all configs
make validate-env      # Validate environment variables
make validate          # Validate docker-compose
make test-all          # Run all validations
```

See [pre-commit hooks guide](pre-commit.md) for automated quality checks.
