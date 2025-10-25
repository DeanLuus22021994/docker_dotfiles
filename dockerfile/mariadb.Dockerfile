# MariaDB Dockerfile - Production-ready MySQL-compatible database
# Separated from devcontainer for Single Responsibility Principle

FROM mariadb:11-jammy

ENV MARIADB_ROOT_PASSWORD=changeme
ENV MARIADB_DATABASE=clusterdb
ENV MARIADB_USER=cluster_user
ENV MARIADB_PASSWORD=changeme
ENV MARIADB_AUTO_UPGRADE=1

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy custom configuration
COPY --chown=mysql:mysql dockerfile/configs/mariadb.conf /etc/mysql/conf.d/custom.cnf

# Create necessary directories with proper permissions
RUN mkdir -p /var/lib/mysql /var/log/mysql \
    && chown -R mysql:mysql /var/lib/mysql /var/log/mysql

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD mariadb-admin ping -h localhost -u root -p${MARIADB_ROOT_PASSWORD} || exit 1

# Volume for persistence
VOLUME ["/var/lib/mysql"]

EXPOSE 3306

# Use official entrypoint
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["mariadbd"]
