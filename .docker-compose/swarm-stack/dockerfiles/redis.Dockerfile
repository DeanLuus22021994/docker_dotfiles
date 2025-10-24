# Optimized Redis Dockerfile for docker-compose stacks
# Includes persistence, monitoring, and health checks

FROM redis:7-alpine AS base

# Install additional system dependencies
RUN apk add --no-cache \
  curl \
  && rm -rf /var/cache/apk/*

# Create directories for data and logs with proper permissions
RUN mkdir -p /data \
  && mkdir -p /var/log/redis \
  && chown -R redis:redis /data \
  && chown -R redis:redis /var/log/redis

# Copy custom Redis configuration
COPY --chown=redis:redis .docker-compose/basic-stack/dockerfiles/redis.conf /etc/redis/redis.conf

# Switch to redis user
USER redis

# Health check
HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=5 \
  CMD redis-cli ping || exit 1

# Expose Redis port
EXPOSE 6379

# Default command with persistence enabled
CMD ["redis-server", "/etc/redis/redis.conf"]