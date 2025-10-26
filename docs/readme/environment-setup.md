---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["environment", "configuration", "secrets", "credentials"]
description: "Environment variables and secrets configuration guide"
---

# Environment Setup

Required before starting the stack.

## Setup Steps

1. **Copy environment template**:
```bash
cp .env.example .env
```

2. **Edit `.env` with credentials** (use strong passwords):
```bash
GITHUB_OWNER=YourUsername
GH_PAT=ghp_xxxxxxxxxxxxxxxxxxxx

# Database passwords (16+ chars, mixed case/numbers/symbols)
DOCKER_POSTGRES_PASSWORD=your_secure_password
DOCKER_MARIADB_ROOT_PASSWORD=your_secure_root_password
DOCKER_MARIADB_PASSWORD=your_secure_password

# Service credentials
DOCKER_REDIS_PASSWORD=your_redis_password
DOCKER_MINIO_ROOT_USER=minioadmin
DOCKER_MINIO_ROOT_PASSWORD=your_minio_password
DOCKER_GRAFANA_ADMIN_PASSWORD=your_grafana_password
DOCKER_JUPYTER_TOKEN=your_jupyter_token
DOCKER_PGADMIN_PASSWORD=your_pgadmin_password
```

3. **Load environment variables** (PowerShell):
```powershell
Get-Content .env | ForEach-Object {
  $var = $_.Split('=')
  [Environment]::SetEnvironmentVariable($var[0], $var[1], 'Process')
}
```

4. **Validate environment**:
```bash
python scripts/validate_env.py
make validate-env
```

**Security**: Never commit `.env` file. Use GitHub Secrets for CI/CD. Rotate passwords regularly.
