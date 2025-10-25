# Pre-commit hooks container for code quality enforcement
FROM python:3.13-slim

LABEL maintainer="DeanLuus22021994"
LABEL description="Pre-commit hooks automation with strict error enforcement"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python tools
RUN pip install --no-cache-dir \
    pre-commit==3.6.0 \
    yamllint==1.33.0 \
    detect-secrets==1.4.0 \
    black==23.12.1 \
    ruff==0.1.9

# Set working directory
WORKDIR /workspace

# Default command: install hooks and run all checks
CMD ["sh", "-c", "pre-commit install && pre-commit run --all-files"]
