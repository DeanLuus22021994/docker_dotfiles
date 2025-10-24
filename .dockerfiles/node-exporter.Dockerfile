# Docker Compose - Node Exporter Dockerfile
# Optimized Node Exporter image for system metrics

FROM prom/node-exporter:latest

# Set environment variables
ENV ENVIRONMENT=${ENVIRONMENT:-production}

# Default command (inherited from base image)
# CMD ["--path.rootfs=/host"]