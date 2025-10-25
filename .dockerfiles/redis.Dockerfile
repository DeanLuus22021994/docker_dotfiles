# syntax=docker/dockerfile:1.6

FROM redis:7.2-alpine AS base

ENV DOCKER_BUILDKIT=1

# Install base packages with caching
RUN --mount=type=cache,target=/var/cache/apk,sharing=locked \
    apk add --no-cache \
    tzdata \
    && cp /usr/share/zoneinfo/Etc/UTC /etc/localtime \
    && echo "Etc/UTC" > /etc/timezone

# Create redis directories with proper permissions (redis user already exists in base image)
RUN mkdir -p /data /etc/redis && \
    chown redis:redis /data /etc/redis

# Copy custom redis configuration if needed
COPY --chown=redis:redis .dockerfiles/redis.conf /etc/redis/redis.conf

# Switch to redis user
USER redis

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD redis-cli ping || exit 1

# Expose port
EXPOSE 6379

# Default command
CMD ["redis-server", "/etc/redis/redis.conf"]