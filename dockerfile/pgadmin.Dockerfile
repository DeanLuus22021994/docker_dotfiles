# pgAdmin Dockerfile - PostgreSQL administration tool
# Web-based database management for PostgreSQL and MariaDB

FROM dpage/pgadmin4:latest

# Install additional database tools
USER root

RUN apk add --no-cache \
    postgresql-client \
    mariadb-client \
    curl \
    bash

# Create pgadmin directories with proper ownership
# pgAdmin container runs as UID 5050 by default
RUN mkdir -p /var/lib/pgadmin/storage \
    && mkdir -p /var/lib/pgadmin/sessions \
    && chown -R 5050:5050 /var/lib/pgadmin

# Copy server definitions
COPY .config/services/pgadmin-servers.json /pgadmin4/servers.json

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:80/misc/ping || exit 1

USER 5050

# Expose pgAdmin port
EXPOSE 80

# Volume for persistence
VOLUME ["/var/lib/pgadmin"]

# Start pgAdmin
ENTRYPOINT ["/entrypoint.sh"]
