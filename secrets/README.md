# Docker Secrets Directory

This directory contains sensitive credentials used by Docker Compose services.

## ⚠️ Security Notice

**NEVER commit actual secret files to version control!**

All files in this directory (except `.secrets.example` and this `README.md`) are excluded via `.gitignore`.

## Setup Instructions

1. Copy `.secrets.example` and review the format
2. Create individual secret files for your services:
   - `db_password.txt` - PostgreSQL database password
   - `redis_password.txt` - Redis password (if needed)
   - `api_key.txt` - External API keys (if needed)

3. Add one secret value per file (plain text, no newlines at the end)

## Example: Database Password

Create `db_password.txt`:
```
MySecureP@ssw0rd123!
```

## Usage in Docker Compose

Secrets are referenced in `docker-compose.yml`:

```yaml
secrets:
  db_password:
    file: ./secrets/db_password.txt

services:
  postgres:
    secrets:
      - db_password
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
```

## Development vs Production

- **Development**: Use simple passwords in `db_password.txt` for local testing
- **Production**: Use strong, randomly generated passwords
- **CI/CD**: Inject secrets via environment variables or secret management systems

## Generating Secure Passwords

```bash
# Generate a random password (Linux/Mac)
openssl rand -base64 32

# Or use Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Files in This Directory

- `.secrets.example` - Template showing secret file format (committed to git)
- `README.md` - This file (committed to git)
- `db_password.txt` - Database password (NOT in git, created by you)
- `*.txt` - Other secret files (NOT in git, created by you)
