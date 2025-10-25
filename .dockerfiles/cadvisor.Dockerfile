# Docker Compose - cAdvisor Dockerfile
# Optimized cAdvisor image for container metrics

FROM gcr.io/cadvisor/cadvisor:latest

# Set environment variables
ENV ENVIRONMENT=${ENVIRONMENT:-production}

# Default command (inherited from base image)
# CMD ["--port=8080"]