---
date_created: "2025-10-26T18:32:25.998895+00:00"
last_updated: "2025-10-26T18:32:25.998895+00:00"
tags: ["documentation", "configuration", "setup"]
description: "Documentation for security"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- security
- secrets
  description: GitHub security features configuration and setup
  ---\n# GitHub Security Configuration

Code scanning, secret detection, and dependency review configuration.

## Security Features

**File:** `.config/github/code-security.yml`

Enabled features (all FREE for public repos):

- CodeQL analysis (Python, JavaScript, TypeScript)
- Secret scanning with push protection
- Dependabot alerts and security updates
- Dependency review for PRs
- Container scanning (Trivy)

## GitHub Secrets

**File:** `.config/github/secrets.yml`

**Required Secrets (11 total):**

- `GH_PAT` - GitHub Personal Access Token
- `DOCKER_POSTGRES_PASSWORD` - PostgreSQL password
- `DOCKER_MARIADB_ROOT_PASSWORD` - MariaDB root password
- `DOCKER_MARIADB_PASSWORD` - MariaDB user password
- `DOCKER_REDIS_PASSWORD` - Redis password
- `DOCKER_MINIO_ROOT_USER` - MinIO root username
- `DOCKER_MINIO_ROOT_PASSWORD` - MinIO root password
- `DOCKER_GRAFANA_ADMIN_PASSWORD` - Grafana admin password
- `DOCKER_JUPYTER_TOKEN` - Jupyter notebook token
- `DOCKER_PGADMIN_PASSWORD` - pgAdmin password
- `DOCKER_NGINX_HTPASSWD` - Nginx auth credentials

**Setup:**

```powershell
# Edit .env with credentials
notepad .env

# Set all secrets
.\scripts\setup_secrets.ps1 -SetGitHubSecrets

# Verify
gh secret list
```

## Enable Security Scanning

```powershell
# Via GitHub UI
Start-Process "https://github.com/DeanLuus22021994/docker_dotfiles/settings/security_analysis"
```

Enable all features in Security & analysis section.

**Cost:** FREE (GitHub Advanced Security included for public repos)
