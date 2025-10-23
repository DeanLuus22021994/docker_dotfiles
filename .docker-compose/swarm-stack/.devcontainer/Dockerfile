FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install dependencies for VS Code server
RUN apt-get update && apt-get install -y \
  curl \
  wget \
  ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Set up VS Code server
ENV VSCODE_AGENT_FOLDER=/tmp/vscode-remote
RUN mkdir -p ${VSCODE_AGENT_FOLDER}

# Expose port for VS Code server
EXPOSE 8000

# Default command
CMD ["sleep", "infinity"]
