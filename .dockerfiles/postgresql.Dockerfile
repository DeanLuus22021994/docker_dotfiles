# syntax=docker/dockerfile:1.6

FROM postgres:16-alpine AS base

ENV DOCKER_BUILDKIT=1
ENV POSTGRES_DB=app
ENV POSTGRES_USER=app
ENV POSTGRES_PASSWORD=app
ENV PGDATA=/var/lib/postgresql/data/pgdata

# Install base packages with caching
RUN --mount=type=cache,target=/var/cache/apk,sharing=locked \
    apk add --no-cache \
    tzdata \
    && cp /usr/share/zoneinfo/Etc/UTC /etc/localtime \
    && echo "Etc/UTC" > /etc/timezone

# Create postgres directories with proper permissions
RUN mkdir -p /var/lib/postgresql/data /var/run/postgresql && \
    chown -R postgres:postgres /var/lib/postgresql/data /var/run/postgresql && \
    chmod 700 /var/lib/postgresql/data

# Copy custom postgresql configuration
COPY --chown=postgres:postgres .dockerfiles/postgresql.conf /usr/local/share/postgresql/postgresql.conf.sample
COPY --chown=postgres:postgres .dockerfiles/pg_hba.conf /usr/local/share/postgresql/pg_hba.conf.sample

# Copy initialization scripts
COPY --chown=postgres:postgres .dockerfiles/init/ /docker-entrypoint-initdb.d/

# Create health check script
RUN echo '#!/bin/bash\npg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}' > /usr/local/bin/healthcheck && \
    chmod +x /usr/local/bin/healthcheck

# Switch to postgres user
USER postgres

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD /usr/local/bin/healthcheck || exit 1

# Expose port
EXPOSE 5432

# Default command (inherited from base image)
# CMD ["postgres"]