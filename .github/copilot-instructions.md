# Copilot Instructions for Docker Dotfiles Project

## Project Overview
This is a Docker Compose multi-stack environment for React Scuba with:
- **Python 3.14** with UV package manager (free-threaded execution enabled)
- **Node.js 22** with React 18 + Vite
- **PostgreSQL/MariaDB** databases
- **Multi-stage Docker builds** with BuildKit optimization
- **Health checks** and **secrets management**

## Directory Structure
- `.docker-compose/` - All Docker Compose stacks (hidden directory with dot prefix)
- `.docker-compose/basic-stack/` - Basic development stack
- `.docker-compose/cluster-example/` - Multi-container cluster setup
- `.docker-compose/swarm-stack/` - Docker Swarm configuration
- `.docker-compose/mcp/python_utils/` - Python utilities with MCP compliance
- `.docker-compose/github-actions-runner/` - Self-hosted GitHub Actions runner
- `.devcontainer/` - VS Code Dev Container configuration
- `.github/` - GitHub workflows and TODO list

## Code Standards

### Docker Compose
- **DO NOT** use `version:` field (deprecated in modern Docker Compose)
- Use dot-prefix for hidden directories (`.docker-compose`)
- Use secrets management for credentials (never hardcode passwords)
- Standardize volume naming: `react_scuba_<service>_<type>`
- Use consistent health check timings:
  - `interval: 30s`
  - `timeout: 10s`
  - `retries: 3`
  - `start_period: 40s`

### Python
- Target Python 3.14 (`py314`)
- Use UV for package management
- Follow PEP 8 with Black formatter (line length: 88)
- Type hints required (mypy strict mode)
- Use Ruff for linting

### Node.js
- Use Node.js 22 LTS
- Install with `npm install --legacy-peer-deps`
- Use Vite for development server

### File Naming
- Hidden directories: `.docker-compose`, `.github`, `.devcontainer`
- Docker files: `docker-compose.yml`, `docker-compose.dev.yml`
- Dockerfiles: `<service>.Dockerfile` in `dockerfiles/` subdirectory

## When Making Changes

### Docker Compose Files
1. Remove deprecated `version` field if present
2. Update all related stacks (basic, cluster, swarm)
3. Test with: `docker-compose -f <path> config --quiet`
4. Build test: `docker-compose -f <path> build`

### Python Code
1. Update type hints for all functions
2. Run: `ruff check .` and `mypy .`
3. Format with: `black .` and `isort .`
4. Test with: `pytest tests/ -v`

### Documentation
1. Update README.md if adding new features
2. Check `.github/TODO.md` for active tasks
3. Document breaking changes in comments

## Security
- Use Docker secrets for sensitive data
- Never commit `.env` files (only `.env.example`)
- Scan images with Trivy before deployment
- Use non-root users in containers

## Common Commands
```bash
# Validate all stacks
python .docker-compose/validate_stacks.py

# Build specific stack
docker-compose -f .docker-compose/basic-stack/docker-compose.yml build

# Run with dev overrides
docker-compose -f .docker-compose/basic-stack/docker-compose.yml \
  -f .docker-compose/basic-stack/docker-compose.dev.yml up

# Clean up
docker system prune -f
```

## Performance Optimization
- Use multi-stage builds
- Leverage BuildKit caching
- Use named volumes for persistent data
- Enable health checks for all services
- Use `--cached` mount option for volumes in dev