# Redis Dockerfile - High-performance in-memory data store
# Multi-stage build for optimized production image

FROM redis:7-alpine AS base

# Install runtime dependencies
RUN apk add --no-cache \
    ca-certificates \
    tzdata

# Create redis user and directories
RUN mkdir -p /data \
    && chown -R redis:redis /data

# Custom Redis configuration
FROM base AS production

# Create config directory
RUN mkdir -p /usr/local/etc/redis \
    && chown -R redis:redis /usr/local/etc/redis

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD redis-cli ping || exit 1

# Switch to redis user
USER redis

# Expose Redis port
EXPOSE 6379

# Volume for persistence
VOLUME ["/data"]

# Start Redis with custom config or default
CMD ["redis-server", "--appendonly", "yes", "--requirepass", "changeme"]
