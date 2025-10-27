# Configuration Directory Index

**Central reference for all configuration files across the cluster.**

For detailed configuration documentation, see [`docs/config/`](../docs/config/)

## Directories

- **cluster/** - Cluster-wide configuration and service inventory
- **database/** - PostgreSQL and MariaDB production configurations  
- **devcontainer/** - VS Code development environment configuration
- **docker/** - Docker daemon and BuildKit configuration
- **git/** - Pre-commit hooks and Git LFS configuration
- **github/** - GitHub Actions workflows and repository automation
- **markdownlint/** - Markdown documentation standards and linting
- **mkdocs/** - Documentation site configuration
- **monitoring/** - Prometheus, Alertmanager, and observability configuration
- **nginx/** - Load balancer and reverse proxy configuration
- **python/** - Python tooling configuration (pytest, ruff, mypy)
- **services/** - Service-specific configurations (pgAdmin, MinIO, Redis Commander)
- **testing/** - Test automation and validation configuration
- **traefik/** - Reverse proxy and ingress configuration
- **frontend/** - Frontend build configurations and web server settings

## Usage

```bash
# Validate all configurations
docker-compose config --quiet

# View detailed configuration guide for specific area
ls .config/[directory]/README.md
```

**For detailed configuration guides, see individual README files in each subdirectory.**