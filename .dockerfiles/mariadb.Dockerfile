# syntax=docker/dockerfile:1.6

FROM mariadb:11.2 AS base

ENV DOCKER_BUILDKIT=1
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=app
ENV MYSQL_USER=app
ENV MYSQL_PASSWORD=app

# Install base packages with caching
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install -y \
    tzdata \
    && cp /usr/share/zoneinfo/Etc/UTC /etc/localtime \
    && echo "Etc/UTC" > /etc/timezone \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create mysql directories with proper permissions
RUN mkdir -p /var/lib/mysql-files /var/lib/mysql-keyring /var/run/mysqld && \
    chown -R mysql:mysql /var/lib/mysql-files /var/lib/mysql-keyring /var/run/mysqld && \
    chmod 750 /var/lib/mysql-files

# Copy custom mysql configuration
COPY --chown=mysql:mysql .dockerfiles/my.cnf /etc/mysql/my.cnf
COPY --chown=mysql:mysql .dockerfiles/mariadb.cnf /etc/mysql/mariadb.cnf

# Copy initialization scripts
COPY --chown=mysql:mysql .dockerfiles/init/ /docker-entrypoint-initdb.d/

# Create health check script
RUN echo '#!/bin/bash\nmysqladmin ping -h localhost --silent' > /usr/local/bin/healthcheck && \
    chmod +x /usr/local/bin/healthcheck

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD /usr/local/bin/healthcheck || exit 1

# Expose port
EXPOSE 3306

# Default command (inherited from base image)
# CMD ["mysqld"]