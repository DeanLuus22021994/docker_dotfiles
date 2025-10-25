# Configuration Directory

This directory contains centralized configuration files for the Modern Data Platform cluster.

## Files

### `cluster.yml`
Main cluster configuration defining all services, ports, health checks, and resource settings.

**Usage:**
- Reference for understanding cluster topology
- Source of truth for service configuration
- Template for production deployments

### `test-suite.yml`
Comprehensive end-to-end test suite configuration.

**Usage:**
- Defines all automated tests
- Infrastructure validation
- Service health checks
- Connectivity tests
- Performance benchmarks

## Integration

These configuration files are referenced by:
- `docker-compose.yml` - Service orchestration
- `Makefile` - Build and test commands
- `.devcontainer/devcontainer.json` - VS Code integration
- CI/CD pipelines (future)

## Configuration Management

### Development
```bash
# Validate configuration
docker-compose config --quiet

# Test cluster
make test-all
```

### Production
```bash
# Override settings via environment variables
export POSTGRES_MAX_CONNECTIONS=200
export REDIS_PERSISTENCE=true

# Deploy with overrides
docker-compose up -d
```

## Best Practices

1. **Never commit secrets** - Use Docker secrets or environment variables
2. **Version control** - All config files are tracked in git
3. **Documentation** - Update README when adding new config files
4. **Validation** - Always validate after changes (`make validate`)
5. **Testing** - Run test suite before deploying (`make test-all`)

## File Format

All configuration files use YAML format for consistency and readability.

## Contributing

When adding new services:
1. Update `cluster.yml` with service definition
2. Add tests to `test-suite.yml`
3. Update main `docker-compose.yml`
4. Document in this README
