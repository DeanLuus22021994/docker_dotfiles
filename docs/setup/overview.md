---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["setup", "overview", "documentation"]
description: "Documentation for overview in setup"
---
# Setup Guide - Docker Compose Stack

This guide will help you configure the environment and GitHub secrets for the docker_dotfiles project.

## Prerequisites

- Docker Desktop with Docker Compose
- GitHub CLI (`gh`) installed and authenticated
- PowerShell 7+ (Windows) or bash (Linux/macOS)

## Quick Setup

### 1. Configure Environment Variables

The `.env` file has been created from `.env.example`. You need to edit it with your actual credentials:

```powershell
# Edit .env file with your preferred editor
notepad .env
# OR
code .env
```

**Required Variables:**
- `GITHUB_OWNER`: Your GitHub username (e.g., DeanLuus22021994)
- `GH_PAT`: GitHub Personal Access Token with `repo` and `workflow` scopes
- `DOCKER_POSTGRES_PASSWORD`: Strong password for PostgreSQL
- `DOCKER_MARIADB_ROOT_PASSWORD`: Strong root password for MariaDB
- `DOCKER_MARIADB_PASSWORD`: Strong user password for MariaDB
- `DOCKER_REDIS_PASSWORD`: Strong password for Redis
- `DOCKER_MINIO_ROOT_USER`: Admin username for MinIO (min 3 chars)
- `DOCKER_MINIO_ROOT_PASSWORD`: Admin password for MinIO (min 8 chars)
- `DOCKER_GRAFANA_ADMIN_PASSWORD`: Admin password for Grafana
- `DOCKER_JUPYTER_TOKEN`: Token for Jupyter notebook access
- `DOCKER_PGADMIN_PASSWORD`: Password for pgAdmin interface

**Security Best Practices:**
- Use strong passwords (16+ characters, mix of letters/numbers/symbols)
- Never commit `.env` file (already in `.gitignore`)
- Use a password manager to generate and store credentials
- Rotate credentials periodically

### 2. Set Up GitHub Secrets

Use the provided PowerShell script to set up GitHub secrets from your `.env` file:

```powershell
# Set GitHub secrets (reads from .env)
.\scripts\setup_secrets.ps1 -SetGitHubSecrets

# Load environment variables into current session
.\scripts\setup_secrets.ps1 -LoadEnvVars

# Run all validations
.\scripts\setup_secrets.ps1 -ValidateAll

# Or do everything at once
.\scripts\setup_secrets.ps1 -SetGitHubSecrets -LoadEnvVars -ValidateAll
```

**Manual Setup (if script fails):**

```powershell
# Load .env variables into current session
Get-Content .env | ForEach-Object {
    if ($_ -and -not $_.StartsWith("#")) {
        $var = $_.Split("=", 2)
        [Environment]::SetEnvironmentVariable($var[0], $var[1], 'Process')
    }
}

# Set GitHub secrets manually
gh secret set GH_PAT --repo DeanLuus22021994/docker_dotfiles
gh secret set DOCKER_POSTGRES_PASSWORD --repo DeanLuus22021994/docker_dotfiles
gh secret set DOCKER_MARIADB_ROOT_PASSWORD --repo DeanLuus22021994/docker_dotfiles
gh secret set DOCKER_MARIADB_PASSWORD --repo DeanLuus22021994/docker_dotfiles
gh secret set DOCKER_REDIS_PASSWORD --repo DeanLuus22021994/docker_dotfiles
gh secret set DOCKER_MINIO_ROOT_USER --repo DeanLuus22021994/docker_dotfiles
gh secret set DOCKER_MINIO_ROOT_PASSWORD --repo DeanLuus22021994/docker_dotfiles
gh secret set DOCKER_GRAFANA_ADMIN_PASSWORD --repo DeanLuus22021994/docker_dotfiles
gh secret set DOCKER_JUPYTER_TOKEN --repo DeanLuus22021994/docker_dotfiles
gh secret set DOCKER_PGADMIN_PASSWORD --repo DeanLuus22021994/docker_dotfiles
```

### 3. Validate Configuration

```powershell
# Validate environment variables
make validate-env
# OR
python scripts/validate_env.py

# Validate configuration files
make validate-configs
# OR
python scripts/validate_configs.py

# Validate docker-compose syntax
make validate
# OR
docker-compose config --quiet

# Run all validations
make test-all
```

### 4. Self-Hosted Runner Setup

All workflows have been configured to use `runs-on: self-hosted`. To use GitHub Actions, you need to set up a self-hosted runner:

**Option 1: Docker-based Runner (Recommended)**
```powershell
# Pull the GitHub Actions runner image
docker pull myoung34/github-runner:latest

# Run the runner container
docker run -d --restart always \
  --name github-runner \
  -e RUNNER_NAME="docker-stack-runner" \
  -e RUNNER_WORKDIR="/tmp/github-runner" \
  -e RUNNER_SCOPE="repo" \
  -e REPO_URL="https://github.com/DeanLuus22021994/docker_dotfiles" \
  -e ACCESS_TOKEN="${GH_PAT}" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /tmp/github-runner:/tmp/github-runner \
  myoung34/github-runner:latest
```

**Option 2: Native Runner**
1. Go to: https://github.com/DeanLuus22021994/docker_dotfiles/settings/actions/runners/new
2. Follow GitHub's instructions to download and configure the runner
3. Start the runner service

**Verify Runner:**
```powershell
gh api repos/DeanLuus22021994/docker_dotfiles/actions/runners
```

### 5. Start the Stack

```powershell
# Start production stack
make up
# OR
docker-compose up -d

# Start development stack (includes devcontainer and pre-commit)
make dev
# OR
docker-compose --profile dev up -d

# Check service status
make ps
# OR
docker-compose ps
```

### 6. Access Services

Once the stack is running, access services at:

| Service | URL | Credentials |
|---------|-----|-------------|
| **Web Dashboard** | http://localhost:5173 | N/A |
| **API Proxy** | http://localhost:3001 | N/A |
| **Grafana** | http://localhost:3000 | admin / `$DOCKER_GRAFANA_ADMIN_PASSWORD` |
| **pgAdmin** | http://localhost:5050 | admin@admin.com / `$DOCKER_PGADMIN_PASSWORD` |
| **Redis Commander** | http://localhost:8081 | N/A |
| **MinIO Console** | http://localhost:9001 | `$DOCKER_MINIO_ROOT_USER` / `$DOCKER_MINIO_ROOT_PASSWORD` |
| **Jupyter** | http://localhost:8888 | Token: `$DOCKER_JUPYTER_TOKEN` |
| **Prometheus** | http://localhost:9090 | N/A |
| **MailHog** | http://localhost:8025 | N/A |

## Troubleshooting

### Environment Variables Not Loading

**Windows PowerShell:**
```powershell
Get-Content .env | ForEach-Object {
    if ($_ -and -not $_.StartsWith("#")) {
        $var = $_.Split("=", 2)
        [Environment]::SetEnvironmentVariable($var[0], $var[1], 'Process')
    }
}
```

**Linux/macOS:**
```bash
export $(cat .env | xargs)
```

### Docker Compose Validation Fails

```powershell
# Check for syntax errors
docker-compose config

# Validate with loaded environment
.\scripts\setup_secrets.ps1 -LoadEnvVars
docker-compose config --quiet
```

### GitHub Secrets Not Set

```powershell
# List current secrets
gh secret list --repo DeanLuus22021994/docker_dotfiles

# Re-run setup script
.\scripts\setup_secrets.ps1 -SetGitHubSecrets
```

### Self-Hosted Runner Not Working

```powershell
# Check runner status
gh api repos/DeanLuus22021994/docker_dotfiles/actions/runners

# If using Docker runner, check container
docker ps -a | Select-String github-runner
docker logs github-runner

# Restart runner
docker restart github-runner
```

### Pre-commit Hooks Failing

```powershell
# Run pre-commit manually
docker-compose run --rm cluster-pre-commit

# Or install locally
pip install pre-commit==3.6.0
pre-commit run --all-files
```

## Next Steps

1. **Customize Services**: Edit `docker-compose.yml` to enable/disable services
2. **Configure Monitoring**: Set up Grafana dashboards (templates in `.config/monitoring/grafana/`)
3. **Set Up Backups**: Configure automated backups for databases
4. **Review Security**: Audit secrets, rotate credentials, enable HTTPS
5. **Scale Services**: Use `docker-compose scale` to add replicas

## Additional Resources

- [README.md](README.md) - Main project documentation
- [.github/TODO.md](.github/TODO.md) - Project status and roadmap
- [.config/docker/README.md](.config/docker/README.md) - Docker configuration details
- [AGENT.md](AGENT.md) - AI agent development guide

## Support

For issues or questions:
- Create an issue: https://github.com/DeanLuus22021994/docker_dotfiles/issues
- Check existing issues: https://github.com/DeanLuus22021994/docker_dotfiles/issues?q=is%3Aissue
