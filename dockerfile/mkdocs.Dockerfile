# Multi-stage build for optimized MkDocs production images
# Target: <20MB final image with all bleeding-edge features

# Build stage - full Python environment
FROM python:3.12-alpine as builder

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    build-base \
    git

# Set working directory
WORKDIR /build

# Copy dependency files
COPY pyproject.toml ./
COPY .config/mkdocs ./config/

# Install Python dependencies in virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:"

# Install core dependencies for docs
RUN pip install --no-cache-dir \
    mkdocs==1.6.0 \
    mkdocs-material==9.6.22 \
    mkdocs-awesome-pages-plugin==2.9.3 \
    pydantic==2.9.2 \
    pyyaml==6.0.2 \
    jinja2==3.1.4 \
    psutil==6.1.0 \
    requests==2.32.3

# Copy documentation source
COPY docs ./docs/
COPY mkdocs.yml ./

# Build static site
RUN mkdocs build --clean --strict

# Production stage - minimal runtime
FROM nginx:alpine as production

# Install minimal runtime dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:"

# Copy built site
COPY --from=builder /build/site /usr/share/nginx/html

# Copy nginx configuration
COPY .config/mkdocs/nginx.conf /etc/nginx/nginx.conf

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:80/ || exit 1

# Create non-root user
RUN addgroup -g 1001 -S mkdocs && \
    adduser -S -D -H -u 1001 -h /usr/share/nginx/html -s /sbin/nologin -G mkdocs -g mkdocs mkdocs

# Set ownership
RUN chown -R mkdocs:mkdocs /usr/share/nginx/html

# Switch to non-root user
USER mkdocs

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]

# Development stage - with hot reload
FROM python:3.12-alpine as development

# Install development dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    build-base \
    git \
    nodejs \
    npm

WORKDIR /docs

# Copy dependency files
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir \
    mkdocs==1.6.0 \
    mkdocs-material==9.6.22 \
    mkdocs-awesome-pages-plugin==2.9.3 \
    pydantic==2.9.2 \
    rich==13.9.4 \
    inquirer==3.4.0 \
    pyyaml==6.0.2 \
    jinja2==3.1.4 \
    psutil==6.1.0 \
    requests==2.32.3 \
    watchdog[watchmedo]==5.0.3

# Install Node.js dependencies for Mermaid
RUN npm install -g mermaid@10.9.1

# Create development user
RUN addgroup -g 1001 -S mkdocs && \
    adduser -S -D -H -u 1001 -h /docs -s /bin/sh -G mkdocs -g mkdocs mkdocs

# Set ownership
RUN chown -R mkdocs:mkdocs /docs

# Switch to non-root user
USER mkdocs

# Expose port for development server
EXPOSE 8000

# Default command for development
CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8000", "--livereload"]
