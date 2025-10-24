# Docker Compose - Prometheus Dockerfile
# Optimized Prometheus image with custom configuration

FROM prom/prometheus:latest

# Set environment variables
ENV ENVIRONMENT=${ENVIRONMENT:-production}

# Copy custom configuration if needed
# COPY config/prometheus.yml /etc/prometheus/prometheus.yml

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:9090/-/healthy || exit 1

# Default command (inherited from base image)
# CMD ["--config.file=/etc/prometheus/prometheus.yml", "--storage.tsdb.path=/prometheus"]