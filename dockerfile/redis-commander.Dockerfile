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

USER node

# Expose Redis Commander port
EXPOSE 8081

# Start Redis Commander
CMD ["redis-commander", \
     "--redis-host", "cluster-redis", \
     "--redis-port", "6379", \
     "--redis-db", "0", \
     "--http-auth-username", "admin", \
     "--http-auth-password", "admin"]
