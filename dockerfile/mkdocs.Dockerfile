# syntax=docker/dockerfile:1.7

ARG PYTHON_VERSION=3.12
ARG MKDOCS_VERSION=1.6.1
ARG MATERIAL_VERSION=9.6.22
ARG AWESOME_PAGES_VERSION=2.9.3

# ---------------------------------------------------------------------------
# Base Python stage with shared tooling
# ---------------------------------------------------------------------------
FROM python:${PYTHON_VERSION}-alpine AS python-base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

RUN apk add --no-cache \
    build-base \
    brotli \
    ca-certificates \
    git \
    libffi-dev \
    openssl-dev \
    zlib-dev && \
    python -m venv "$VIRTUAL_ENV"

# ---------------------------------------------------------------------------
# Builder stage - install dependencies, build site, run validation
# ---------------------------------------------------------------------------
FROM python-base AS builder

ARG MKDOCS_VERSION
ARG MATERIAL_VERSION
ARG AWESOME_PAGES_VERSION

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install \
    "mkdocs==${MKDOCS_VERSION}" \
    "mkdocs-material==${MATERIAL_VERSION}" \
    "mkdocs-awesome-pages-plugin==${AWESOME_PAGES_VERSION}" \
    mkdocs-minify-plugin>=0.8 \
    mkdocs-git-revision-date-localized-plugin>=1.2 \
    mkdocs-git-authors-plugin>=0.7 \
    mkdocs-redirects>=1.2 \
    mkdocs-include-markdown-plugin>=6.0 \
    mkdocs-glightbox>=0.4 \
    pymdown-extensions>=10.8 \
    pydantic>=2.9 \
    rich>=13.9 \
    inquirer>=3.4 \
    jinja2>=3.1 \
    pyyaml>=6.0 \
    psutil>=6.1 \
    requests>=2.32 \
    python-frontmatter>=1.1 \
    brotli

WORKDIR /workspace

COPY docs ./docs
COPY .config/mkdocs ./.config/mkdocs

# Build the documentation site with strict validation
RUN mkdocs build --config-file .config/mkdocs/mkdocs.yml --strict --clean

# Capture build metrics before compression
RUN mkdir -p /build/artifacts && \
    python .config/mkdocs/build/build_metrics.py \
        --docs-dir docs \
        --site-dir .config/mkdocs/site \
        --output /build/artifacts/metrics.json

# Run post-build health validation
RUN python .config/mkdocs/build/validate_health.py \
        --site-dir .config/mkdocs/site \
        --output /build/artifacts/health-report.json

# Pre-compress static assets for optimal delivery
RUN python - <<'PY'
from pathlib import Path
import gzip
import brotli

site_dir = Path('.config/mkdocs/site')
compressible_suffixes = {'.html', '.css', '.js', '.json', '.xml', '.svg'}

for file_path in site_dir.rglob('*'):
    if not file_path.is_file() or file_path.suffix.lower() not in compressible_suffixes:
        continue

    data = file_path.read_bytes()

    gz_path = file_path.with_suffix(file_path.suffix + '.gz')
    with gzip.open(gz_path, 'wb', compresslevel=9) as gz_file:
        gz_file.write(data)

    br_quality = 11
    mode = brotli.MODE_TEXT if file_path.suffix.lower() in {'.html', '.css', '.js'} else brotli.MODE_GENERIC
    br_path = file_path.with_suffix(file_path.suffix + '.br')
    br_path.write_bytes(brotli.compress(data, quality=br_quality, mode=mode))
PY

# Stage final site artifacts for production image
RUN mkdir -p /build/site/health && \
    cp -a .config/mkdocs/site/. /build/site && \
    cp /build/artifacts/metrics.json /build/site/metrics.json && \
    cp /build/artifacts/health-report.json /build/site/health/health-report.json

# ---------------------------------------------------------------------------
# Production stage - lightweight nginx runtime (<20MB target)
# ---------------------------------------------------------------------------
FROM nginx:1.27-alpine AS production

# Copy static site and metadata produced by builder
COPY --from=builder /build/site /usr/share/nginx/html

# Harden permissions for non-root runtime
RUN addgroup -S mkdocs && adduser -S mkdocs -G mkdocs && \
    chown -R mkdocs:mkdocs /usr/share/nginx/html

# Provide tuned nginx configuration for static assets
COPY .config/mkdocs/nginx.conf /etc/nginx/nginx.conf

# Configure health checks for deployment environments
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/health/health-report.json || exit 1

USER mkdocs

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

# ---------------------------------------------------------------------------
# Development stage - live reload environment
# ---------------------------------------------------------------------------
FROM python-base AS development

ARG MKDOCS_VERSION
ARG MATERIAL_VERSION
ARG AWESOME_PAGES_VERSION

RUN apk add --no-cache nodejs npm

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install \
    "mkdocs==${MKDOCS_VERSION}" \
    "mkdocs-material==${MATERIAL_VERSION}" \
    "mkdocs-awesome-pages-plugin==${AWESOME_PAGES_VERSION}" \
    mkdocs-minify-plugin>=0.8 \
    mkdocs-git-revision-date-localized-plugin>=1.2 \
    mkdocs-git-authors-plugin>=0.7 \
    mkdocs-redirects>=1.2 \
    mkdocs-include-markdown-plugin>=6.0 \
    mkdocs-glightbox>=0.4 \
    pymdown-extensions>=10.8 \
    rich>=13.9 \
    inquirer>=3.4 \
    jinja2>=3.1 \
    pyyaml>=6.0 \
    watchdog[watchmedo]>=5.0 \
    python-frontmatter>=1.1

RUN --mount=type=cache,target=/root/.npm npm install --global mermaid@10.9.1

RUN addgroup -S mkdocs && adduser -S mkdocs -G mkdocs

WORKDIR /docs

COPY --chown=mkdocs:mkdocs docs ./docs
COPY --chown=mkdocs:mkdocs .config/mkdocs ./.config/mkdocs

USER mkdocs

EXPOSE 8000

CMD ["mkdocs", "serve", "--config-file", ".config/mkdocs/mkdocs.yml", "--dev-addr=0.0.0.0:8000", "--livereload"]
