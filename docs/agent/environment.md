---
date_created: "2025-10-26T18:32:25.938405+00:00"
last_updated: "2025-10-26T18:32:25.938405+00:00"
tags: ["documentation", "agent", "development"]
description: "Documentation for environment"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- environment
- secrets
- authentication
  description: Environment variables naming conventions and setup procedures
  ---\n# Environment Variables

## Naming Convention

- **Prefix**: All service secrets use `DOCKER_` prefix
- **Examples**: `DOCKER_POSTGRES_PASSWORD`, `DOCKER_MARIADB_ROOT_PASSWORD`
- **Source**: GitHub Secrets (CI/CD) or host environment (local dev)

## Setup

```powershell
# Copy template
Copy-Item .env.example .env

# Edit with credentials
code .env

# Load variables
Get-Content .env | ForEach-Object {
  $var = $_.Split('=')
  [Environment]::SetEnvironmentVariable($var[0], $var[1], 'Process')
}

# Validate
python scripts/validate_env.py
```

## Required Variables

- `GITHUB_OWNER`, `GH_PAT`
- `DOCKER_POSTGRES_PASSWORD`
- `DOCKER_MARIADB_ROOT_PASSWORD`, `DOCKER_MARIADB_PASSWORD`
- `DOCKER_REDIS_PASSWORD`
- `DOCKER_MINIO_ROOT_USER`, `DOCKER_MINIO_ROOT_PASSWORD`
- `DOCKER_GRAFANA_ADMIN_PASSWORD`
- `DOCKER_JUPYTER_TOKEN`
- `DOCKER_PGADMIN_PASSWORD`

See [code quality guide](agent-code-quality.md) for validation procedures.
