---
date_created: "2025-10-26T18:32:25.951459+00:00"
last_updated: "2025-10-26T18:32:25.951459+00:00"
tags: ["documentation", "readme", "guide"]
description: "Documentation for configuration"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- configuration
- validation
  description: Configuration management and validation procedures
  ---\n# Configuration

## Configuration Management (SSoT)

All configurations centralized in `.config/` directory:

**Cluster Configs** (`.config/cluster/`):

- `cluster.config.yml` - Master service definitions for 25+ services

**Testing Configs** (`.config/testing/`):

- `test-suite.yml` - End-to-end test suite configurations

**Jekyll Configs** (`.config/jekyll/`):

- `jekyll.config.yml` - Jekyll static site configuration
- `Gemfile` / `Gemfile.lock` - Ruby dependencies for documentation site

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

**Monitoring Configs** (`.config/monitoring/`):

- `prometheus.yml` - Metrics scraping configuration
- `alertmanager.yml` - Alert routing and grouping
- `alerts/rules.yml` - Alert rules
- `dashboards/` - Grafana dashboard definitions
- `grafana/provisioning/` - Auto-provisioning for datasources

**Traefik Configs** (`.config/traefik/`):

- `traefik.yml` - Reverse proxy configuration
- `dynamic/middlewares.yml` - Dynamic middleware definitions

**GitHub Configs** (`.config/github/`):

- `dependabot.yml` - Automated dependency updates
- `labeler.yml` - PR auto-labeling rules
- `workflows/` - Reusable workflow configurations

**Note:** Root-level config files (`.pre-commit-config.yaml`, `pytest.ini`, `pyrightconfig.json`, `.devcontainer/`) are symlinks or redirects to `.config/` for tool compatibility.

## Validation Commands

```bash
make validate-configs  # Validate all configs
make validate-env      # Validate environment variables
make validate          # Validate docker-compose
make test-all          # Run all validations
```

See [pre-commit hooks guide](pre-commit.md) for automated quality checks.
