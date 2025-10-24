# syntax=docker/dockerfile:1.6

FROM nvidia/cuda:12.2.0-base-ubuntu22.04 AS base

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV DOCKER_BUILDKIT=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/home/vscode/.local/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install tzdata first (rarely changes)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install -y tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install base system packages (infrequently changes)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install -y \
    apt-utils \
    curl \
    wget \
    unzip \
    lsb-release \
    tree \
    vim \
    jq \
    ca-certificates \
    gnupg \
    software-properties-common \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install GitHub CLI (stable dependency)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update \
    && apt-get install -y gh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3.14 (dependency that changes occasionally)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y python3.14 python3.14-venv python3.14-dev \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.14 1 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.14 1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install UV (Python package manager)
RUN --mount=type=cache,target=/root/.cache/uv \
    curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv \
    && chmod +x /usr/local/bin/uv

# Install Node.js and npm
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user with sudo access
RUN groupadd -r vscode && useradd -m -s /bin/bash -g vscode vscode \
    && mkdir -p /etc/sudoers.d \
    && echo 'vscode ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode \
    && mkdir -p /workspaces \
    && chown vscode:vscode /workspaces \
    && mkdir -p /home/vscode/.cache/pip \
    && mkdir -p /home/vscode/.npm \
    && mkdir -p /home/vscode/.cache/uv \
    && mkdir -p /home/vscode/.mypy_cache \
    && mkdir -p /home/vscode/.cache/ruff \
    && mkdir -p /home/vscode/.pytest_cache \
    && mkdir -p /home/vscode/.cache/pre-commit \
    && mkdir -p /home/vscode/.jupyter \
    && mkdir -p /home/vscode/.conda/envs \
    && chown -R vscode:vscode /home/vscode

# Switch to vscode user for dependency installation
USER vscode
WORKDIR /home/vscode
ENV PATH="/home/vscode/.local/bin:$PATH"

# Copy Python project files for dependency installation
COPY --chown=vscode:vscode pyproject.toml uv.lock* ./

# Pre-install Python dependencies with caching
RUN --mount=type=cache,target=/home/vscode/.cache/uv,id=uv-cache \
    --mount=type=cache,target=/home/vscode/.cache/pip,id=pip-cache \
    uv sync --extra dev --frozen-lockfile || uv sync --extra dev || true

# Install dev tools directly to avoid dependency conflicts (ultra-optimized)
RUN --mount=type=cache,target=/home/vscode/.cache/pip,id=pip-cache \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python && \
    PIP_CACHE_DIR=/home/vscode/.cache/pip PIP_NO_CACHE_DIR=1 python -m pip install --user --only-binary=all black>=23.11.0 ruff>=0.1.0 mypy>=1.7.0 isort>=5.12.0 pre-commit>=3.5.0

# Precompile Python bytecode for both venv and user packages (optimized)
RUN python -m compileall -b -o 0 /home/vscode/.venv && \
    python -m compileall -b -o 0 /home/vscode/.local/lib/python3.14/site-packages && \
    find /home/vscode/.local/lib/python3.14/site-packages -name "*.py" -exec python -m py_compile {} \; && \
    python -c "import black; print('Black imported successfully')" && \
    python -m py_compile /home/vscode/.local/lib/python3.14/site-packages/black/__init__.py 2>/dev/null || true

# Pre-install Node.js global packages with caching (optimized)
RUN --mount=type=cache,target=/home/vscode/.npm,id=npm-cache \
    npm config set cache /home/vscode/.npm && \
    npm install -g --prefer-offline --no-audit yarn typescript @types/node eslint prettier || true

# Pre-warm all development tool caches in parallel (optimized)
RUN --mount=type=cache,target=/home/vscode/.mypy_cache,id=mypy-cache \
    --mount=type=cache,target=/home/vscode/.cache/ruff,id=ruff-cache \
    --mount=type=cache,target=/home/vscode/.cache/black,id=black-cache \
    --mount=type=cache,target=/home/vscode/.cache/isort,id=isort-cache \
    echo -e "# test file for cache warming\nimport os\nprint('hello')" > /tmp/test.py && \
    mypy --cache-dir /home/vscode/.mypy_cache --no-error-summary /tmp/test.py || true && \
    ruff check --cache-dir /home/vscode/.cache/ruff /tmp/test.py || true && \
    PYTHONOPTIMIZE=1 black /tmp/test.py || true && \
    isort /tmp/test.py || true && \
    rm /tmp/test.py

# Final performance optimization: strip debug symbols, optimize binaries, and clean up
RUN find /home/vscode/.local/lib/python3.14/site-packages -name "*.so" -exec strip {} \; 2>/dev/null || true && \
    find /home/vscode/.local/lib/python3.14/site-packages -name "__pycache__" -type d -exec rm -rf {} \; 2>/dev/null || true && \
    find /home/vscode/.venv -name "__pycache__" -type d -exec rm -rf {} \; 2>/dev/null || true

# Switch back to root for final setup
USER root

# Set default command
CMD ["sleep", "infinity"]
