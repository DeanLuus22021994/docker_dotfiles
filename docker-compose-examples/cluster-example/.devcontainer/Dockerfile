FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install dependencies for VS Code server and nginx
RUN apt-get update && apt-get install -y \
  curl \
  wget \
  ca-certificates \
  nginx \
  && rm -rf /var/lib/apt/lists/*

# Set up VS Code server
ENV VSCODE_AGENT_FOLDER=/tmp/vscode-remote
RUN mkdir -p ${VSCODE_AGENT_FOLDER}

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose ports
EXPOSE 80 8000

# Default command - run nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
