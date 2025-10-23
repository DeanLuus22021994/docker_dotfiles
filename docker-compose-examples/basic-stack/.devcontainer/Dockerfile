FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install dependencies
RUN apt-get update && apt-get install -y \
  curl \
  wget \
  ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Default command
CMD ["sleep", "infinity"]
