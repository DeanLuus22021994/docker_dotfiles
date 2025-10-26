# ==============================================================================
# MkDocs Documentation - Optimized Production Image
# ==============================================================================
# Multi-stage build for minimal final image (<20MB target)
# Includes: Material theme, plugins, health validation
# ==============================================================================

# Stage 1: Builder - Install dependencies and build docs
FROM python:3.14-slim AS builder

# Set working directory
WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy only dependency files first (layer caching)
COPY pyproject.toml ./
COPY .config/mkdocs/ ./.config/mkdocs/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    mkdocs-material>=9.5.39 \
    pydantic>=2.9 \
    pyyaml>=6.0 \
    psutil

# Copy documentation source
COPY docs/ ./docs/
COPY mkdocs.yml ./.config/mkdocs/mkdocs.yml

# Build documentation site
RUN cd .config/mkdocs && mkdocs build --strict

# Run health validation
RUN python .config/mkdocs/build/validate_health.py \
    --site-dir .config/mkdocs/site \
    --output /build/health-report.json

# ==============================================================================
# Stage 2: Nginx - Serve static site
# ==============================================================================
FROM nginx:alpine AS runtime

# Remove default nginx content
RUN rm -rf /usr/share/nginx/html/*

# Copy built documentation from builder
COPY --from=builder /build/.config/mkdocs/site /usr/share/nginx/html

# Copy health report for monitoring
COPY --from=builder /build/health-report.json /usr/share/nginx/html/health/

# Copy custom nginx configuration
COPY .config/mkdocs/nginx/docs.conf /etc/nginx/conf.d/default.conf

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health/ || exit 1

# Expose port
EXPOSE 8080

# Add non-root user
RUN addgroup -g 1001 -S docs && \
    adduser -u 1001 -S docs -G docs && \
    chown -R docs:docs /usr/share/nginx/html /var/cache/nginx /var/run

USER docs

# Labels
LABEL maintainer="Dean Luus"
LABEL description="Optimized MkDocs documentation site"
LABEL version="1.0.0"

CMD ["nginx", "-g", "daemon off;"]
