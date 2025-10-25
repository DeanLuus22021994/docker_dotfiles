# Docker Compose - Grafana Dockerfile
# Optimized Grafana image with custom configuration

FROM grafana/grafana:latest

# Set environment variables
ENV ENVIRONMENT=${ENVIRONMENT:-production}

# Copy custom configuration if needed
# COPY config/grafana.ini /etc/grafana/grafana.ini

# Install additional plugins if needed
# RUN grafana-cli plugins install redis-datasource

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000/api/health || exit 1

# Default user (inherited from base image)
# USER grafana