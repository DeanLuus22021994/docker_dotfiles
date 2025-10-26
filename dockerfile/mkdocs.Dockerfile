# ============================================================================
# MkDocs Material - Modern Multi-Stage Production Dockerfile
# ============================================================================
# Build Strategy: Compile static site during build, serve with ultra-light nginx
# Image Size: ~15MB (nginx:alpine) vs 150MB+ (Python runtime)
# Performance: Pre-built static assets, instant page loads, zero Python overhead
# ============================================================================

# ============================================================================
# Stage 1: Builder - Full Python environment for MkDocs build
# ============================================================================
FROM python:3.14-slim AS builder

LABEL stage="builder"
LABEL description="MkDocs build stage with Material theme and advanced plugins"

# Build arguments
ARG MKDOCS_VERSION=1.6.1
ARG MATERIAL_VERSION=9.5.39

# Set working directory
WORKDIR /build

# Install build dependencies (git for git-revision-date plugin)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        gcc \
        g++ \
    && rm -rf /var/lib/apt/lists/*

# Install MkDocs and comprehensive plugin suite
RUN pip install --no-cache-dir \
    # Core MkDocs
    mkdocs==${MKDOCS_VERSION} \
    mkdocs-material==${MATERIAL_VERSION} \
    \
    # Essential Plugins
    mkdocs-minify-plugin==0.8.0 \
    mkdocs-awesome-pages-plugin==2.9.3 \
    mkdocs-linkcheck==1.0.5 \
    \
    # Advanced Markdown
    pymdown-extensions==10.11.2 \
    \
    && pip cache purge

# Copy MkDocs configuration (modular YAML structure)
COPY .config/mkdocs/ /build/.config/mkdocs/

# Copy documentation source
COPY docs/ /build/docs/

# Copy assets from .config/mkdocs (not from docs/)
COPY .config/mkdocs/assets/ /build/docs/assets/

# Set git safe directory (for git plugins)
RUN git config --global --add safe.directory /build

# Build static site with optimizations
RUN mkdocs build \
    --config-file .config/mkdocs/mkdocs.yml \
    --clean \
    --site-dir /build/site

# Post-build optimizations (gzip compression)
RUN find /build/site -type f -name '*.html' -exec sed -i 's/  */ /g' {} + && \
    find /build/site -type f -name '*.js' -exec gzip -k9 {} + && \
    find /build/site -type f -name '*.css' -exec gzip -k9 {} + && \
    find /build/site -type f -name '*.html' -exec gzip -k9 {} +

# ============================================================================
# Stage 1.5: Validation - Verify built site integrity
# ============================================================================
FROM python:3.14-alpine AS validation

LABEL stage="validation"
LABEL description="Post-build validation and quality checks"

WORKDIR /validate

# Install validation dependencies (minimal Alpine packages)
RUN apk add --no-cache \
    py3-pip \
    libstdc++

# Install Python validation tools
RUN pip install --no-cache-dir \
    pyyaml==6.0.2 \
    && pip cache purge

# Copy built site from builder
COPY --from=builder /build/site /validate/site

# Copy validation scripts
COPY .config/mkdocs/scripts/validate_health.py /validate/
COPY .config/mkdocs/hooks/validate_frontmatter.py /validate/

# Run comprehensive validation suite
RUN python validate_health.py \
    --site-dir /validate/site \
    --strict \
    && echo "[$(date '+%Y-%m-%d %H:%M:%S')] Site validation passed"

# Verify critical files exist
RUN test -f /validate/site/index.html && \
    test -f /validate/site/search/search_index.json && \
    test -f /validate/site/sitemap.xml && \
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Critical files validated"

# Verify metrics were generated
RUN test -f /validate/site/metrics.json && \
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Build metrics validated"

# ============================================================================
# Stage 2: Production - Ultra-lightweight nginx server
# ============================================================================
FROM nginx:1.27-alpine AS production

LABEL maintainer="Dean Luus"
LABEL description="MkDocs Material documentation - Production static site"
LABEL version="2.0.0"

# Install envsubst for dynamic configuration
RUN apk add --no-cache gettext libintl

# Copy built site from validation stage (ensures validation passed)
COPY --from=validation /validate/site /usr/share/nginx/html

# Copy custom nginx configuration
COPY .config/mkdocs/nginx/default.conf /etc/nginx/conf.d/default.conf

# Create nginx cache directory
RUN mkdir -p /var/cache/nginx/docs && \
    chown -R nginx:nginx /var/cache/nginx/docs && \
    chown -R nginx:nginx /usr/share/nginx/html

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8000/ || exit 1

# Expose port
EXPOSE 8000

# Switch to non-root user
USER nginx

# Start nginx
CMD ["nginx", "-g", "daemon off;"]

# ============================================================================
# Stage 3: Development - Hot-reload server (optional target)
# ============================================================================
FROM python:3.14-slim AS development

LABEL stage="development"
LABEL description="MkDocs development server with live reload"

WORKDIR /docs

# Install MkDocs and plugins
RUN pip install --no-cache-dir \
    mkdocs==1.6.1 \
    mkdocs-material==9.5.39 \
    mkdocs-minify-plugin==0.8.0 \
    pymdown-extensions==10.11.2 \
    && pip cache purge

# Install git for live reload file watching
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# Note: Assets mounted from .config/mkdocs/assets at runtime

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000').read()" || exit 1

EXPOSE 8000

# Start development server with live reload
CMD ["mkdocs", "serve", \
     "--config-file", ".config/mkdocs/mkdocs.yml", \
     "--dev-addr", "0.0.0.0:8000", \
     "--livereload", \
     "--watch", ".config/mkdocs/", \
     "--watch", "docs/"]
