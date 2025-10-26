# MariaDB Dockerfile - Production-ready MySQL-compatible database
# Separated from devcontainer for Single Responsibility Principle

FROM mariadb:11-jammy AS base

# Install runtime dependencies with cache mount
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy custom configuration
COPY --chown=mysql:mysql .config/database/mariadb.conf /etc/mysql/conf.d/custom.cnf

# Create necessary directories with proper permissions
RUN mkdir -p /var/lib/mysql /var/log/mysql \
    && chown -R mysql:mysql /var/lib/mysql /var/log/mysql

# Health check - uses environment variables from docker-compose
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD mariadb-admin ping -h localhost -u $$MYSQL_USER -p$$MYSQL_PASSWORD || exit 1

# Volume for persistence
VOLUME ["/var/lib/mysql"]

EXPOSE 3306

# Use official entrypoint
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["mariadbd"]
