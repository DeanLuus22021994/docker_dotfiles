# Redis Commander Dockerfile - Redis web management
# Web-based UI for browsing and managing Redis data

FROM rediscommander/redis-commander:latest

# Install additional tools
USER root

RUN apk add --no-cache \
    curl \
    bash \
    redis

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -f http://localhost:8081 || exit 1

# Run as root (base image default)
# USER directive removed - base image handles user switching

# Expose Redis Commander port
EXPOSE 8081

# Start Redis Commander - base image has its own entrypoint
# Remove explicit CMD to use base image default
