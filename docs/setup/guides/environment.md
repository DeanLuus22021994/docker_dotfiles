---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["setup", "environment", "configuration", "env"]
description: "Environment configuration and .env file setup"
---
# Environment Configuration

## Create .env File

```bash
cp .env.example .env
nano .env  # Or use your preferred editor
```

## Required Variables

**Domain & HTTPS:**
```bash
DOMAIN=localhost  # Or your domain
ACME_EMAIL=admin@localhost
```

**Authentication (Development):**
```bash
AUTH_ENABLED=false  # Disable for dev
JWT_SECRET=development_secret_change_in_production
```

**Database Passwords:**
```bash
DOCKER_POSTGRES_PASSWORD=postgres_dev
DOCKER_MARIADB_ROOT_PASSWORD=mariadb_root_dev
DOCKER_MARIADB_PASSWORD=mariadb_dev
DOCKER_REDIS_PASSWORD=redis_dev
DOCKER_MINIO_ROOT_PASSWORD=minio_dev
DOCKER_GRAFANA_ADMIN_PASSWORD=grafana_dev
DOCKER_JUPYTER_TOKEN=jupyter_dev
DOCKER_PGADMIN_PASSWORD=pgadmin_dev
```

**GitHub Integration (Optional):**
```bash
GITHUB_OWNER=your-username
GH_PAT=ghp_your_personal_access_token
```

## Validation

```bash
# Validate environment variables
python scripts/python/validation/validate_env.py
```

## Security Notes

- Never commit .env to version control
- Use strong passwords in production
- Generate secure JWT secrets: `openssl rand -hex 32`
- Rotate credentials regularly
