---
date_created: '2025-10-27T02:35:03Z'
last_updated: '2025-10-27T02:35:03Z'
tags: [configuration, index, documentation]
description: 'Master index of all configuration files in the .config directory'
---

# Configuration Directory Index

**Complete inventory of all configuration files for the Docker Modern Data Platform.**

This index serves as the central reference for all configuration files across the cluster. Each subdirectory contains specialized configuration for different aspects of the infrastructure.

---

## 📊 Quick Stats

- **Total Directories**: 15
- **Configuration Files**: 50+
- **Services Configured**: 31
- **Networks**: 6 (5-tier segmentation + legacy)
- **Volumes**: 18 persistent volumes
- **Secrets**: 6 Docker secrets
- **Total Storage**: ~1.2 GB

---

## �� Directory Structure

### 1. **cluster/** - Cluster-Wide Configuration
**Purpose**: Central cluster configuration and service inventory

| File | Description | Type |
|------|-------------|------|
| `cluster.config.yml` | Master cluster configuration (31 services, 6 networks, 18 volumes) | YAML |

**Key Features**:
- 5-tier network segmentation (frontend, backend, data, observability, management)
- Docker secrets management (6 credentials)
- Security hardening (READ-ONLY socket proxy, no-new-privileges)
- GPU support (Jupyter, Model Runner)
- Beta features (Docker AI, MCP, Wasm)
- BuildKit v0.25.1 (250GB cache, multi-platform)

**Documentation**: See README in directory (if exists)

---

### 2. **database/** - Database Configuration
**Purpose**: PostgreSQL and MariaDB production configurations

| File | Description | Type |
|------|-------------|------|
| `postgresql.conf` | PostgreSQL 16+ config (200 connections, 256MB buffers, WAL replication) | Properties |
| `mariadb.conf` | MariaDB 11+ config (UTF-8MB4, 256MB InnoDB, binary logging) | Properties |
| `README.md` | Database configuration guide | Markdown |

**Key Features**:
- Performance monitoring (pg_stat_statements, performance_schema)
- Replication ready (WAL level: replica, binary logging)
- Security (SCRAM-SHA-256, Docker secrets integration)
- Autovacuum tuning, slow query logging

**Networks**: `cluster-data` (internal-only), `cluster-backend`

---

### 3. **devcontainer/** - VS Code Dev Container
**Purpose**: Development environment configuration

| File | Description | Type |
|------|-------------|------|
| `devcontainer.json` | VS Code devcontainer with Python 3.14, Node 22, CUDA, Docker-in-Docker | JSON |

**Key Features**:
- Python 3.14.0 + Node.js 22
- NVIDIA CUDA support
- Docker-in-Docker
- 29 services auto-started
- Port forwarding for all services
- GitHub Copilot integration

**Host Requirements**: 4 CPUs, 4GB RAM, 8GB storage, optional GPU

---

### 4. **docker/** - Docker Engine Configuration
**Purpose**: Docker daemon and BuildKit configuration

| File | Description | Type |
|------|-------------|------|
| `daemon.json` | Docker Engine config (250GB cache, GPU runtime, experimental features) | JSON |
| `buildkitd.toml` | BuildKit daemon (250GB cache, 7 platforms, 50 parallelism) | TOML |
| `compose.override.example.yml` | Local development overrides template (GPU, Wasm, AI examples) | YAML |
| `README.md` | Comprehensive Docker configuration guide | Markdown |

**Beta Features**:
- Docker AI ("Ask Gordon")
- MCP Toolkit
- Wasm Support (containerd)
- Docker Model Runner (GPU inference, port 12434)
- Docker Extensions

**BuildKit Platforms**: amd64, arm64, riscv64, ppc64le, s390x, arm/v7, arm/v6

---

### 5. **git/** - Git Configuration
**Purpose**: Pre-commit hooks and Git automation

| File | Description | Type |
|------|-------------|------|
| `.pre-commit-config.yaml` | Pre-commit hooks (Black, Ruff, Pyright, YAML linting, Markdown) | YAML |

**Key Features**:
- Python formatting (Black, Ruff)
- Type checking (Pyright, Mypy)
- YAML/JSON/TOML linting
- Markdown linting (markdownlint-cli2)
- Secrets detection (detect-secrets)
- Trailing whitespace/EOF fixes

**Cache**: 608.4 MB persistent volume (`pre-commit-cache`)

---

### 6. **github/** - GitHub Configuration
**Purpose**: Repository settings, workflows, and automation

| File | Description | Type |
|------|-------------|------|
| `repository.yml` | Repository settings (security, features, branch protection) | YAML |
| `branch-protection.yml` | Branch protection rules | YAML |
| `code-security.yml` | Security scanning configuration | YAML |
| `dependabot.yml` | Dependency updates automation | YAML |
| `labeler.yml` | Auto-labeling configuration | YAML |
| `actions.yml` | GitHub Actions workflow configuration | YAML |
| `secrets.yml` | Repository secrets inventory | YAML |
| `project-v4.0.yml` | GitHub Projects configuration | YAML |
| `workflows/` | GitHub Actions workflow files | Directory |

**Security Features**:
- Dependabot (Docker, npm, pip, GitHub Actions)
- Code scanning (CodeQL)
- Secret scanning
- Branch protection (required reviews, status checks)

---

### 7. **markdownlint/** - Markdown Linting
**Purpose**: Markdown style enforcement

| File | Description | Type |
|------|-------------|------|
| `markdownlint.json` | Markdownlint configuration (MD013 disabled, MD033 allowed) | JSON |

**Rules**: 40+ markdown linting rules configured

---

### 8. **mkdocs/** - Documentation Site
**Purpose**: MkDocs Material documentation generation

| File/Directory | Description | Type |
|----------------|-------------|------|
| `mkdocs.yml` | Main MkDocs configuration | YAML |
| `base.yml` | Base configuration (merged) | YAML |
| `navigation.yml` | Site navigation structure | YAML |
| `theme.yml` | Material theme configuration | YAML |
| `plugins.yml` | MkDocs plugins configuration | YAML |
| `markdown.yml` | Markdown extensions configuration | YAML |
| `requirements.txt` | Python dependencies | Text |
| `README.md` | MkDocs comprehensive guide | Markdown |
| `overrides/` | Custom template overrides | Directory |
| `hooks/` | MkDocs build hooks | Directory |
| `assets/` | Static assets | Directory |

**Key Features**:
- Material theme with custom branding
- Multi-stage Docker builds
- 600+ document coverage
- Search, social cards, Git integration
- Custom CSS/JS overrides
- Auto-generated navigation

---

### 9. **monitoring/** - Observability Stack
**Purpose**: Prometheus, Grafana, Alertmanager configuration

| File/Directory | Description | Type |
|----------------|-------------|------|
| `prometheus.yml` | Prometheus scrape configs (9 targets, 15s interval) | YAML |
| `alertmanager.yml` | Alert routing and notifications | YAML |
| `alerts/` | Prometheus alert rules | Directory |
| `dashboards/` | Grafana dashboard definitions | Directory |
| `grafana/` | Grafana provisioning configs | Directory |

**Monitored Services**:
- Prometheus self-monitoring
- Grafana
- cAdvisor (container metrics)
- PostgreSQL exporter
- Redis exporter
- Node exporter (host metrics)

**Alerting**:
- Email notifications via MailHog
- Critical alerts (5m repeat)
- Warning alerts (1h repeat)
- Inhibition rules

**Network**: `cluster-observability`

---

### 10. **nginx/** - Web Server Configuration
**Purpose**: NGINX load balancer and web server configs

| File | Description | Type |
|------|-------------|------|
| `loadbalancer.conf` | Load balancer config (round-robin to web1/web2/web3) | Properties |
| `default.conf` | Default NGINX configuration | Properties |
| `main.conf` | Main NGINX configuration | Properties |

**Features**:
- Round-robin load balancing
- Health check endpoint (`/health`)
- Proxy headers (X-Real-IP, X-Forwarded-For)
- Custom server identifier

**Networks**: `cluster-frontend`, `cluster-backend`

---

### 11. **python/** - Python Configuration
**Purpose**: Python tooling configuration

| File | Description | Type |
|------|-------------|------|
| `pyrightconfig.json` | Pyright type checker config (Python 3.14, basic mode) | JSON |
| `pytest.ini` | Pytest configuration | INI |

**Features**:
- Python 3.14 compatibility
- Type checking (basic mode)
- Custom paths (scripts, tests, .config/mkdocs)
- Strict module handling

---

### 12. **services/** - Service-Specific Configuration
**Purpose**: Individual service configurations

| File | Description | Type |
|------|-------------|------|
| `pgadmin-servers.json` | pgAdmin server connections (PostgreSQL, MariaDB) | JSON |
| `localstack-init.sh` | LocalStack initialization script | Shell |

**pgAdmin Servers**:
1. PostgreSQL Cluster (cluster-postgres:5432)
2. MariaDB Cluster (cluster-mariadb:3306)

---

### 13. **testing/** - Test Configuration
**Purpose**: Test suite and validation configuration

| File | Description | Type |
|------|-------------|------|
| `test-suite.yml` | End-to-end test definitions (infrastructure, services, connectivity) | YAML |

**Test Categories**:
- Infrastructure (Docker Compose, networks)
- Service health checks (11 services)
- Connectivity tests (inter-service communication)
- DevContainer integration
- Performance benchmarks

---

### 14. **traefik/** - Reverse Proxy Configuration
**Purpose**: Traefik edge router configuration

| File/Directory | Description | Type |
|----------------|-------------|------|
| `traefik.yml` | Traefik v3.2 config (HTTPS, Let's Encrypt, metrics) | YAML |
| `dynamic/` | Dynamic configuration (middlewares, routes) | Directory |

**Key Features**:
- HTTPS with Let's Encrypt
- HTTP to HTTPS redirect
- Docker service discovery
- Prometheus metrics
- Security headers middleware
- Rate limiting

**Entry Points**:
- `web` (port 80, redirects to HTTPS)
- `websecure` (port 443, TLS)
- `traefik` (port 8080, dashboard)

---

### 15. **web/** - Frontend Configuration
**Purpose**: Web application build and development configuration

| File | Description | Type |
|------|-------------|------|
| `vite.config.ts` | Vite build configuration | TypeScript |
| `tsconfig.json` | TypeScript compiler configuration | JSON |
| `tailwind.config.js` | Tailwind CSS configuration | JavaScript |
| `postcss.config.js` | PostCSS configuration | JavaScript |
| `.eslintrc.cjs` | ESLint configuration | CommonJS |
| `nginx.conf` | Production NGINX configuration | Properties |

**Tech Stack**:
- Vite (build tool)
- TypeScript
- Tailwind CSS
- PostCSS
- ESLint

---

## 🔍 Configuration Search Guide

### By Service Type

**Databases**:
- PostgreSQL: `.config/database/postgresql.conf`
- MariaDB: `.config/database/mariadb.conf`
- Redis: See `docker-compose.yml` (secrets-based)

**Monitoring**:
- Prometheus: `.config/monitoring/prometheus.yml`
- Grafana: `.config/monitoring/grafana/`
- Alertmanager: `.config/monitoring/alertmanager.yml`

**Web Servers**:
- Load Balancer: `.config/nginx/loadbalancer.conf`
- Traefik: `.config/traefik/traefik.yml`

**Development**:
- DevContainer: `.config/devcontainer/devcontainer.json`
- Docker: `.config/docker/daemon.json`
- Pre-commit: `.config/git/.pre-commit-config.yaml`

**Documentation**:
- MkDocs: `.config/mkdocs/mkdocs.yml`
- Markdown Linting: `.config/markdownlint/markdownlint.json`

---

## 🚀 Quick Commands

### Validate All Configurations

```powershell
# Docker Compose
docker-compose config --quiet

# BuildKit
docker exec cluster-buildkit cat /etc/buildkit/buildkitd.toml

# PostgreSQL
docker exec cluster-postgres psql -U cluster_user -d clusterdb -c \"SHOW config_file;\"

# MkDocs
docker exec cluster-docs mkdocs --version
```

### Edit Configurations

```powershell
# Use VS Code with proper syntax highlighting
code .config/docker/daemon.json
code .config/monitoring/prometheus.yml
code .config/mkdocs/mkdocs.yml

# Or edit in devcontainer for full linting
devcontainer open .
```

---

## 📚 Related Documentation

- **Main README**: `../README.md` - Project overview
- **Docker Configuration**: `.config/docker/README.md` - Docker daemon and BuildKit guide
- **Database Configuration**: `.config/database/README.md` - Database tuning guide
- **MkDocs Guide**: `.config/mkdocs/README.md` - Documentation site setup
- **Agent Workflow**: `../AGENT.md` - AI-optimized development patterns

---

## 🔐 Security Considerations

### Secrets Management

**Never commit these files**:
- `.secrets/*.txt` - Docker secrets (gitignored)
- `docker-compose.override.yml` - Local overrides (gitignored)
- `.env` files - Environment variables (gitignored)

**Secrets Location**:
- Docker secrets: `.secrets/` directory
- Mounted at: `/run/secrets/` in containers
- Used by: PostgreSQL, MariaDB, Redis

### Configuration Files with Sensitive Data

**Review before committing**:
- `daemon.json` - No secrets, but contains infrastructure details
- `prometheus.yml` - Scrape targets expose internal architecture
- `traefik.yml` - Domain names and certificate email

---

## 📝 Maintenance Guidelines

### When Adding New Services

1. **Update** `cluster.config.yml` with service details
2. **Assign** to appropriate network tier
3. **Add** monitoring to `prometheus.yml` if applicable
4. **Update** this INDEX.md with new configuration files
5. **Document** in service-specific README

### When Modifying Configurations

1. **Test** changes in `docker-compose.override.yml` first
2. **Validate** with `docker-compose config --quiet`
3. **Update** relevant README files
4. **Update** `last_updated` timestamp in this INDEX.md
5. **Document** breaking changes

### Regular Maintenance Tasks

- **Monthly**: Review cache usage (BuildKit, pre-commit)
- **Quarterly**: Update BuildKit version
- **Quarterly**: Review and update dependency versions
- **Bi-annually**: Audit security configurations
- **Annually**: Review and optimize database configurations

---

## 🆘 Troubleshooting

### Configuration Not Applied

```powershell
# Rebuild services after config changes
docker-compose up -d --force-recreate <service-name>

# Check if config file is mounted
docker inspect <container-name> | Select-String -Pattern \"Mounts\"

# Verify config inside container
docker exec <container-name> cat /path/to/config
```

### Validation Errors

```powershell
# YAML validation
docker-compose config --quiet

# JSON validation
Get-Content .config/docker/daemon.json | ConvertFrom-Json

# TOML validation
docker exec cluster-buildkit cat /etc/buildkit/buildkitd.toml
```

---

## 📅 Last Updated

**Date**: 2025-10-27  
**Version**: 3.0.0  
**Total Files Indexed**: 50+  
**Cluster Services**: 31  
**Networks**: 6  
**Volumes**: 18  

---

**For detailed configuration guides, see individual README files in each subdirectory.**
