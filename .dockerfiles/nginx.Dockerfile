# syntax=docker/dockerfile:1.6

FROM nginx:1.25-alpine AS base

ENV DOCKER_BUILDKIT=1
ENV NGINX_ENVSUBST_TEMPLATE_DIR=/etc/nginx/templates
ENV NGINX_ENVSUBST_OUTPUT_DIR=/etc/nginx/conf.d

# Install base packages with caching
RUN --mount=type=cache,target=/var/cache/apk,sharing=locked \
    apk add --no-cache \
    tzdata \
    openssl \
    curl \
    && cp /usr/share/zoneinfo/Etc/UTC /etc/localtime \
    && echo "Etc/UTC" > /etc/timezone

# Create nginx directories with proper permissions
RUN mkdir -p /var/cache/nginx /var/log/nginx /etc/nginx/ssl /etc/nginx/templates && \
    chown -R nginx:nginx /var/cache/nginx /var/log/nginx /etc/nginx/ssl /etc/nginx/templates && \
    touch /var/run/nginx.pid && \
    chown nginx:nginx /var/run/nginx.pid

# Copy nginx configuration templates
COPY --chown=nginx:nginx .dockerfiles/nginx.conf /etc/nginx/nginx.conf
COPY --chown=nginx:nginx .dockerfiles/conf.d/ /etc/nginx/conf.d/
COPY --chown=nginx:nginx .dockerfiles/templates/ /etc/nginx/templates/

# Copy static assets if any
COPY --chown=nginx:nginx .dockerfiles/static/ /usr/share/nginx/html/

# Switch to nginx user
USER nginx

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Expose ports
EXPOSE 80 443

# Default command
CMD ["nginx", "-g", "daemon off;"]