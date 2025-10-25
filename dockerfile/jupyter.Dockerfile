# Jupyter Lab Dockerfile - Data science environment with GPU support
# Based on official Jupyter Docker Stacks

FROM jupyter/tensorflow-notebook:latest

USER root

# Install additional system dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y \
    postgresql-client \
    redis-tools \
    curl \
    wget \
    git \
    vim

# Install Python packages for data science and ML
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install \
    psycopg2-binary \
    redis \
    sqlalchemy \
    pandas \
    numpy \
    scikit-learn \
    matplotlib \
    seaborn \
    plotly \
    jupyterlab-git \
    jupyterlab-lsp \
    python-lsp-server

# Install PyTorch for additional ML frameworks
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install \
    torch \
    torchvision \
    torchaudio \
    --index-url https://download.pytorch.org/whl/cu118

# Configure Jupyter Lab
RUN jupyter labextension install @jupyterlab/git

# Create work directory
RUN mkdir -p /home/jovyan/work \
    && chown -R jovyan:users /home/jovyan/work

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8888/api || exit 1

# Switch back to jovyan user
USER jovyan

WORKDIR /home/jovyan/work

# Expose Jupyter port
EXPOSE 8888

# Start Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
