# Environment Variables - Docker Compose Examples

This directory contains environment variable files for different deployment environments and configurations.

## Structure

```
.env/
├── .env.development    # Development environment variables
├── .env.docker         # Docker-specific environment variables
├── .env.example        # Template/example environment variables
└── .env.production     # Production environment variables
```

## Usage

### Development
```bash
# Load development environment
export $(cat .env/.env.development | xargs)

# Or use with docker-compose
docker-compose --env-file .env/.env.development up
```

### Production
```bash
# Load production environment
export $(cat .env/.env.production | xargs)

# Or use with docker-compose
docker-compose --env-file .env/.env.production up
```

### Docker Environment
```bash
# Docker-specific variables
export $(cat .env/.env.docker | xargs)
```

## Environment Variable Naming Convention

- `DOCKER_EXAMPLES_*` - Docker Compose specific variables
- `POSTGRES_*` - PostgreSQL database configuration
- `REDIS_*` - Redis configuration
- `API_*` - API configuration
- `DEBUG` - Debug mode toggle
- `LOG_LEVEL` - Logging level

## Security Notes

- Never commit actual secrets to version control
- Use `.env.example` as a template for required variables
- Actual environment files should be git-ignored if they contain sensitive data
- Use environment variable substitution in docker-compose.yml files

## CI/CD Integration

These environment files can be used with:
- GitHub Actions (via repository secrets)
- Docker Compose `--env-file` flag
- Kubernetes ConfigMaps/Secrets
- AWS Systems Manager Parameter Store
- Azure Key Vault

## Example docker-compose usage

```yaml
services:
  app:
    env_file:
      - .env/.env.production
    environment:
      - ADDITIONAL_VAR=value
```</content>
<parameter name="filePath">c:\global\docker\.env\README.md