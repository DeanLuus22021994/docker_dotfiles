# Docker Compose - Promtail Dockerfile
# Optimized Promtail image for log shipping

FROM grafana/promtail:latest

# Set environment variables
ENV ENVIRONMENT=${ENVIRONMENT:-production}

# Copy custom configuration if needed
# COPY config/promtail-config.yml /etc/promtail/promtail-config.yml

# Default command (inherited from base image)
# CMD ["-config.file=/etc/promtail/promtail-config.yml"]