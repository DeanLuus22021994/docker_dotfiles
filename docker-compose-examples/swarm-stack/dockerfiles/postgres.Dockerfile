# Optimized PostgreSQL Dockerfile for swarm-stack
# Includes performance monitoring and Swarm manager optimizations

FROM postgres:13-alpine AS base

# Install additional system dependencies
RUN apk add --no-cache \
  curl \
  && rm -rf /var/cache/apk/*

# Create directories for logs and data with proper permissions
RUN mkdir -p /var/log/postgresql \
  && chown -R postgres:postgres /var/log/postgresql \
  && mkdir -p /var/lib/postgresql/data \
  && chown -R postgres:postgres /var/lib/postgresql/data

# Copy custom configuration
COPY --chown=postgres:postgres docker-compose-examples/swarm-stack/dockerfiles/postgresql.conf /etc/postgresql/postgresql.conf

# Switch to postgres user
USER postgres

# Health check optimized for Swarm (less frequent for manager node)
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD pg_isready -U user -d mydb || exit 1

# Expose PostgreSQL port
EXPOSE 5432

# Default command with performance monitoring
CMD ["postgres", \
  "-c", "config_file=/etc/postgresql/postgresql.conf", \
  "-c", "shared_preload_libraries=pg_stat_statements", \
  "-c", "pg_stat_statements.track=all"]
