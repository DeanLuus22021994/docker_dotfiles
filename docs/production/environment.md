---
date_created: "2025-10-26T18:32:25.947784+00:00"
last_updated: "2025-10-26T18:32:25.947784+00:00"
tags: ["documentation", "production", "deployment"]
description: "Documentation for environment"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- production
- environment
- configuration
- secrets
  description: Production environment configuration and secrets management
  ---\n# Environment Configuration

## Create Production .env

```bash
cp .env.example .env
nano .env
```

## Required Changes

**Domain & HTTPS:**

```bash
DOMAIN=your-domain.com
ACME_EMAIL=admin@your-domain.com
```

**Authentication:**

```bash
AUTH_ENABLED=true
JWT_SECRET=$(node -e "console.log(require('crypto').randomBytes(32).toString('hex'))")
JWT_EXPIRES_IN=8h
JWT_REFRESH_EXPIRES_IN=7d
CORS_ORIGIN=https://your-domain.com
NODE_ENV=production
```

**Database Passwords:**

```bash
DOCKER_POSTGRES_PASSWORD=$(openssl rand -base64 32)
DOCKER_MARIADB_ROOT_PASSWORD=$(openssl rand -base64 32)
DOCKER_MARIADB_PASSWORD=$(openssl rand -base64 32)
DOCKER_REDIS_PASSWORD=$(openssl rand -base64 32)
DOCKER_MINIO_ROOT_PASSWORD=$(openssl rand -base64 32)
DOCKER_GRAFANA_ADMIN_PASSWORD=$(openssl rand -base64 32)
DOCKER_JUPYTER_TOKEN=$(openssl rand -base64 32)
DOCKER_PGADMIN_PASSWORD=$(openssl rand -base64 32)
```

## Automated Setup

```bash
# Generate all passwords automatically
python scripts/powershell/config/setup-secrets.ps1
```

**Important:** Never commit .env to version control. Add to .gitignore.
