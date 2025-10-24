# Docker Compose - Loki Dockerfile
# Optimized Loki image for log aggregation

FROM grafana/loki:latest

# Set environment variables
ENV ENVIRONMENT=${ENVIRONMENT:-production}

# Copy custom configuration if needed
# COPY config/loki-config.yml /etc/loki/loki-config.yml

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3100/ready || exit 1

# Default command (inherited from base image)
# CMD ["-config.file=/etc/loki/loki-config.yml"]