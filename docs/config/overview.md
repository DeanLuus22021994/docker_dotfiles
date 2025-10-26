---
date_created: "2025-10-26T18:32:25.943866+00:00"
last_updated: "2025-10-26T18:32:25.943866+00:00"
tags: ['documentation', 'configuration', 'setup']
description: "Documentation for overview"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- overview
- documentation
description: Documentation for overview in config
---\n# .config - Single Source of Truth

All configuration files for the Docker cluster stack, strictly organized according to Docker and GitHub standards.

## 📁 Directory Structure

```
.config/
├── README.md                    # This file
├── cluster/                     # Cluster configuration
│   └── cluster.config.yml       # Master service definitions
├── testing/                     # Test configurations
│   └── test-suite.yml           # E2E test configurations
├── jekyll/                      # Jekyll documentation site
│   ├── jekyll.config.yml        # Jekyll site configuration
│   ├── Gemfile                  # Ruby dependencies for Jekyll
│   └── Gemfile.lock             # Locked Ruby versions
├── docker/                      # Docker-specific configurations
│   ├── README.md                # Docker config guide
│   ├── daemon.json              # Daemon config reference
│   ├── buildkit.toml            # BuildKit optimization
│   └── compose.override.example.yml  # Local overrides template
├── github/                      # GitHub automation
│   ├── README.md                # GitHub workflows guide
│   ├── dependabot.yml           # Auto dependency updates
│   ├── labeler.yml              # PR auto-labeling
│   └── workflows/
│       └── labeler.yml          # Labeler action
└── monitoring/                  # Complete monitoring stack
    ├── prometheus.yml           # Scrape configs
    ├── alertmanager.yml         # Alert routing
    ├── alerts/
    │   └── rules.yml            # 25 alert rules
    ├── dashboards/              # 4 Grafana dashboards
    │   ├── containers.json
    │   ├── host.json
    │   ├── postgresql.json
    │   └── redis.json
    └── grafana/
        ├── README.md
        └── provisioning/        # Auto-provisioning
            ├── dashboards/
            │   └── dashboards.yml
            └── datasources/
                └── prometheus.yml
```

## 🎯 Purpose

This directory serves as the **single source of truth** for all configuration, following these principles:

1. **Centralization** - All YAML configs in one location
2. **Standardization** - Docker & GitHub naming conventions
3. **Documentation** - Comprehensive READMEs in each subdirectory
4. **Automation** - Dependabot, PR labeling, provisioning
5. **Portability** - Complete setup for new developers
6. **Validation** - All configs validated before commit

## 📄 Core Configuration Files

### `cluster/cluster.config.yml`

Master service definitions: 25+ services, ports, health checks, resources, volumes, network.

### `testing/test-suite.yml`

E2E test definitions: infrastructure validation, service health checks, connectivity tests.

### `jekyll/`

Jekyll static site configuration and Ruby dependencies:
- **jekyll.config.yml**: Theme (Cayman), plugins, collections, navigation, build settings
- **Gemfile/Gemfile.lock**: Ruby dependencies (github-pages, jekyll-seo-tag, jekyll-sitemap, jekyll-feed, webrick)

### `docker/` Directory
- **daemon.json**: Docker Engine reference config (BuildKit, logging, storage)
- **buildkit.toml**: Build optimization (cache, mirrors, platforms)
- **compose.override.example.yml**: Local development overrides template
- **README.md**: Complete Docker setup guide

### `github/` Directory
- **dependabot.yml**: Weekly dependency updates (Docker, Python, npm, Actions)
- **labeler.yml**: Auto-label PRs by file changes (10+ labels)
- **workflows/labeler.yml**: GitHub Action for PR labeling
- **README.md**: Complete GitHub automation guide

### `monitoring/` Directory
- **prometheus.yml**: 8 scrape targets, 15s intervals
- **alertmanager.yml**: Email routing, severity grouping, inhibition rules
- **alerts/rules.yml**: 25 alert rules across 4 categories
- **dashboards/**: 4 Grafana JSON dashboards (containers, host, PostgreSQL, Redis)
- **grafana/provisioning/**: Auto-provisioning for datasources and dashboards

## 🔄 Configuration Hierarchy

```
1. .config/*.yml → Source of truth (documented)
2. docker-compose.yml → Implementation (references .config)
3. docker-compose.override.yml → Local overrides (gitignored)
4. .env → Runtime secrets (gitignored)
```

## ✅ Validation

```bash
# Validate all configs
make validate-config

# Validate docker-compose
docker-compose config --quiet

# Validate YAML syntax
yamllint .config/**/*.yml
```

## � New Developer Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/DeanLuus22021994/docker_dotfiles.git
cd docker_dotfiles

# Install GitHub CLI (automated workflows)
gh auth login

# Copy local overrides template
cp .config/docker/compose.override.example.yml docker-compose.override.yml
```

### 2. Configure Docker (Optional)
```bash
# Linux: Copy daemon config
sudo cp .config/docker/daemon.json /etc/docker/daemon.json
sudo systemctl restart docker

# Windows/macOS: Use Docker Desktop settings GUI

# Enable BuildKit
export DOCKER_BUILDKIT=1
export BUILDKIT_CONFIG=$PWD/.config/docker/buildkit.toml
```

### 3. Start Stack
```bash
# Generate secrets
make secrets

# Start services
docker-compose up -d

# Verify health
docker-compose ps
```

### 4. Access Services
- **Documentation**: http://localhost:4000 (Jekyll)
- **Dashboard**: http://localhost:3000
- **Grafana**: http://localhost:3002
- **Prometheus**: http://localhost:9090

## �📝 Making Changes

1. Update `.config` files (source of truth)
2. Update implementation (docker-compose.yml)
3. Validate: `make validate`
4. Test: `make test-all`
5. Document in commit message

## 🔒 Security

**Never commit**: Secrets, passwords, API tokens, `.env` files  
**Always commit**: Templates, defaults, documentation

## 📊 Standards Compliance

**Docker**: `cluster-<service>`, `cluster_<volume>`, `cluster-network`  
**GitHub**: YAML format, Dependabot, branch protection  
**YAML**: 2-space indent, comments, anchors, sorted keys

---

**Version**: 3.0.0 | **Updated**: 2025-10-25 | **License**: MIT | **Status**: Production Ready
