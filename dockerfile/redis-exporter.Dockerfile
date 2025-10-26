# Redis Exporter Dockerfile - Prometheus exporter for Redis metrics
# Built on Alpine to add curl for health checks

FROM alpine:latest AS base

# Install runtime dependencies
RUN apk add --no-cache \
    ca-certificates \
    curl \
    && addgroup -g 59121 -S redis_exporter \
    && adduser -S -u 59121 -G redis_exporter redis_exporter

# Download and install redis_exporter binary
ARG VERSION=v1.55.0
ARG ARCH=amd64
RUN wget -q https://github.com/oliver006/redis_exporter/releases/download/${VERSION}/redis_exporter-${VERSION}.linux-${ARCH}.tar.gz \
    && tar xzf redis_exporter-${VERSION}.linux-${ARCH}.tar.gz \
    && mv redis_exporter-${VERSION}.linux-${ARCH}/redis_exporter /usr/local/bin/redis_exporter \
    && chmod +x /usr/local/bin/redis_exporter \
    && rm -rf redis_exporter-*

# Health check using curl
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:9121/metrics || exit 1

USER redis_exporter

# Expose metrics port
EXPOSE 9121

# Start redis_exporter
ENTRYPOINT ["/usr/local/bin/redis_exporter"]
