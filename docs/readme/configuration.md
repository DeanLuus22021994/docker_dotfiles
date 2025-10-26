---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["configuration", "settings", "validation", "pre-commit"]
description: "Configuration management and validation procedures"
---

# Configuration

## Configuration Management (SSoT)

All configurations centralized in `.config/` directory:

**Web Configs** (`.config/web/`):
- `nginx.conf` - React web dashboard nginx settings
- `vite.config.ts` - Vite build configuration
- `tsconfig.json` - TypeScript compiler options
- `.eslintrc.cjs` - ESLint rules
- `postcss.config.js` - PostCSS plugins
- `tailwind.config.js` - Tailwind CSS theme

**Python Configs** (`.config/python/`):
- `pytest.ini` - Pytest additional settings
- `pyrightconfig.json` - Pyright type checking rules

**Git Configs** (`.config/git/`):
- `.pre-commit-config.yaml` - Pre-commit hooks

**DevContainer** (`.config/devcontainer/`):
- `devcontainer.json` - VS Code DevContainer settings

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

**Note:** Root-level config files (`.pre-commit-config.yaml`, `pytest.ini`, `pyrightconfig.json`, `.devcontainer/`) are symlinks or redirects to `.config/` for tool compatibility.

## Validation Commands

```bash
make validate-configs  # Validate all configs
make validate-env      # Validate environment variables
make validate          # Validate docker-compose
make test-all          # Run all validations
```

See [pre-commit hooks guide](pre-commit.md) for automated quality checks.
