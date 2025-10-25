# Docker Secrets - Environment Variable Driven

This directory implements **industry-standard, environment variable driven secrets management** for Docker Compose services.

## 🔒 Security Standards

- **Environment Variables**: All secrets are environment variable driven
- **Safe to Commit**: No sensitive data committed to version control
- **Industry Standard**: Follows 12-factor app methodology
- **CI/CD Compatible**: Works with GitHub Actions, Jenkins, and other CI/CD systems

## 📁 Directory Structure

```
.secrets/
├── .env.template          # Environment variable template (committed)
├── secrets.env           # Environment variables file (NOT committed)
├── .gitignore           # Ensures secrets.env is ignored
└── README.md            # This documentation (committed)
```

## 🚀 Setup Instructions

### 1. Copy Environment Template
```bash
cp .secrets/.env.template .secrets/secrets.env
```

### 2. Configure Environment Variables
Edit `.secrets/secrets.env` with your actual values:

```bash
# Database Configuration
docker_DB_PASSWORD=your_secure_database_password_here
docker_DB_USER=postgres_user
docker_DB_NAME=docker_db

# API Security
docker_API_KEY=your_api_key_here
docker_JWT_SECRET=your_jwt_secret_here

# External Services
docker_GITHUB_TOKEN=your_github_token_here
docker_REDIS_PASSWORD=your_redis_password_here
```

### 3. Load Environment Variables
```bash
# Development
export $(cat .secrets/secrets.env | xargs)

# Production (use your deployment system's secret management)
# Example: GitHub Actions, Kubernetes secrets, AWS Secrets Manager, etc.
```

## 🔧 Environment Variable Standards

### Naming Convention
```
docker_[COMPONENT]_[SECRET_TYPE]
```

**Examples:**
- `docker_DB_PASSWORD` - Database password
- `docker_API_KEY` - API authentication key
- `docker_JWT_SECRET` - JWT signing secret
- `docker_GITHUB_TOKEN` - GitHub API token

### Security Requirements
- **Minimum Length**: 32 characters for passwords, 64 for secrets
- **Complexity**: Mix of uppercase, lowercase, numbers, symbols
- **Rotation**: Regular rotation of secrets (90 days recommended)
- **No Hardcoding**: Never hardcode secrets in application code

## 🐳 Docker Compose Integration

### Environment Variable Loading
```yaml
# docker-compose.yml
services:
  postgres:
    environment:
      POSTGRES_PASSWORD: ${docker_DB_PASSWORD}
      POSTGRES_USER: ${docker_DB_USER}
      POSTGRES_DB: ${docker_DB_NAME}

  python:
    environment:
      API_KEY: ${docker_API_KEY}
      JWT_SECRET: ${docker_JWT_SECRET}
      GITHUB_TOKEN: ${docker_GITHUB_TOKEN}
```

### Docker Secrets (Alternative)
```yaml
# For enhanced security in production
secrets:
  db_password:
    environment: "docker_DB_PASSWORD"

services:
  postgres:
    secrets:
      - db_password
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
```

## 🔐 Security Best Practices

### Development Environment
```bash
# Use simple passwords for local development
docker_DB_PASSWORD=dev_password_123
docker_API_KEY=dev_api_key_456
```

### Production Environment
```bash
# Use strong, randomly generated secrets
docker_DB_PASSWORD=$(openssl rand -base64 32)
docker_API_KEY=$(openssl rand -hex 32)
docker_JWT_SECRET=$(openssl rand -base64 64)
```

### CI/CD Integration
```yaml
# .github/workflows/deploy.yml
env:
  docker_DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
  docker_API_KEY: ${{ secrets.API_KEY }}
  docker_JWT_SECRET: ${{ secrets.JWT_SECRET }}
```

## 🛠️ Utility Scripts

### Generate Secure Secrets
```bash
# Generate database password
echo "docker_DB_PASSWORD=$(openssl rand -base64 32)" >> .secrets/secrets.env

# Generate API key
echo "docker_API_KEY=$(openssl rand -hex 32)" >> .secrets/secrets.env

# Generate JWT secret
echo "docker_JWT_SECRET=$(openssl rand -base64 64)" >> .secrets/secrets.env
```

### Validate Environment Setup
```bash
# Check if all required variables are set
required_vars="docker_DB_PASSWORD docker_API_KEY"
for var in $required_vars; do
  if [ -z "${!var}" ]; then
    echo "ERROR: $var is not set"
    exit 1
  fi
done
echo "All required secrets are configured"
```

## 📋 Migration from Legacy Secrets

### From File-Based Secrets
If migrating from file-based secrets in `secrets/` directory:

1. **Extract values** from existing secret files
2. **Create environment variables** in `.secrets/secrets.env`
3. **Update docker-compose.yml** to use environment variables
4. **Remove old secrets/** directory**
5. **Update .gitignore** to include `.secrets/secrets.env`

### Legacy to New Format
```bash
# Old: secrets/db_password.txt
cat secrets/db_password.txt

# New: .secrets/secrets.env
echo "docker_DB_PASSWORD=$(cat secrets/db_password.txt)" >> .secrets/secrets.env
```

## 🔍 Verification

### Check Environment Variables
```bash
# Verify variables are loaded
env | grep docker_

# Test database connection
docker compose exec postgres psql -U ${docker_DB_USER} -d ${docker_DB_NAME}
```

### Security Audit
```bash
# Check for hardcoded secrets
grep -r "password\|secret\|key" --exclude-dir=.git --exclude-dir=.secrets .

# Verify .gitignore excludes secrets
cat .gitignore | grep secrets.env
```

## 📚 References

- [12-Factor App Methodology](https://12factor.net/config)
- [OWASP Secrets Management](https://owasp.org/www-project-cheat-sheets/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [Docker Secrets Best Practices](https://docs.docker.com/engine/swarm/secrets/)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)</content>
<parameter name="filePath">c:\global\docker\.secrets\README.md