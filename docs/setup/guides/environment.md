---
date_created: "2025-10-26T18:32:25.970487+00:00"
last_updated: "2025-10-26T18:32:25.970487+00:00"
tags: ['documentation', 'setup', 'installation']
description: "Documentation for environment"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- setup
- environment
- configuration
description: Environment configuration and .env file setup
---\n# Environment Configuration

## Configuration Approach

**Local Development**: Single `.env` file (created from template)  
**CI/CD Pipeline**: GitHub repository secrets (already configured)  
**Naming Convention**: All service passwords use `DOCKER_` prefix

## Verify GitHub Secrets (CI/CD)

Check configured secrets for CI/CD pipelines:
```bash
gh secret list --repo DeanLuus22021994/docker_dotfiles
```

Current secrets configured:
- ✓ `DOCKER_POSTGRES_PASSWORD`
- ✓ `DOCKER_MARIADB_ROOT_PASSWORD`
- ✓ `DOCKER_MARIADB_PASSWORD`
- ✓ `DOCKER_REDIS_PASSWORD`
- ✓ `DOCKER_MINIO_ROOT_USER`
- ✓ `DOCKER_MINIO_ROOT_PASSWORD`
- ✓ `DOCKER_GRAFANA_ADMIN_PASSWORD`
- ✓ `DOCKER_JUPYTER_TOKEN`
- ✓ `DOCKER_PGADMIN_PASSWORD`
- ✓ `GH_PAT`
- ✓ `DOCKER_ACCESS_TOKEN`
- ✓ `CODECOV_TOKEN`

## Create Local .env File

For local development, copy the template:
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

- **Never commit** `.env` to version control (gitignored by `.env.*` pattern)
- **Single source**: Use `.env.example` as the only template (no separate dev/prod files)
- **CI/CD secrets**: Managed via GitHub repository secrets (use `gh secret` commands)
- **Strong passwords**: Use minimum 16 characters in production
- **Generate JWT secrets**: `openssl rand -hex 32` or `node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"`
- **Rotate regularly**: Change credentials periodically, especially after team changes

## Environment Variable Management

**Add new secret to GitHub**:
```bash
gh secret set SECRET_NAME --repo DeanLuus22021994/docker_dotfiles
```

**Update existing secret**:
```bash
gh secret set SECRET_NAME --repo DeanLuus22021994/docker_dotfiles
```

**Remove secret**:
```bash
gh secret remove SECRET_NAME --repo DeanLuus22021994/docker_dotfiles
```
