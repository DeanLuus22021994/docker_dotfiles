FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV PYTHONUNBUFFERED=1
ENV NODE_ENV=development

# Install system dependencies with cache mount
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y \
    tzdata \
    curl \
    wget \
    git \
    gnupg \
    software-properties-common \
    build-essential \
    ca-certificates \
    sudo \
    postgresql-client \
    redis-tools

# Python layer - install Python 3.14 and UV
RUN add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y \
        python3.14 \
        python3.14-venv \
        python3.14-dev \
        python3.14-distutils \
        python3-pip \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.14 1 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.14 1 \
    && python3 -m pip install --upgrade pip setuptools wheel \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install UV (fast Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv \
    && chmod +x /usr/local/bin/uv

# Node.js layer - install Node.js 22
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    --mount=type=cache,target=/root/.npm \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest

# Install kubectl for k8s management
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl \
    && rm kubectl

# Create non-root user with sudo access
RUN useradd -m -s /bin/bash -u 1000 vscode \
    && echo 'vscode ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode \
    && mkdir -p /workspaces \
    && chown -R vscode:vscode /workspaces

# Setup user directories
RUN mkdir -p /home/vscode/.cache/pip \
    && mkdir -p /home/vscode/.npm \
    && mkdir -p /home/vscode/.local/bin \
    && chown -R vscode:vscode /home/vscode

# Install common Python packages with cache mount
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install \
    jupyter \
    jupyterlab \
    ipython \
    pandas \
    numpy \
    psycopg2-binary \
    redis \
    requests

USER vscode
WORKDIR /workspaces/docker

# Default command
CMD ["sleep", "infinity"]
