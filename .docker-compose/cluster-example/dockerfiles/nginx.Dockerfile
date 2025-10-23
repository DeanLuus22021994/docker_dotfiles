# Optimized Nginx Dockerfile for cluster-example
# Lightweight and secure nginx configuration for load balancing

FROM nginx:alpine AS base

# Install security updates and curl for health checks
RUN apk add --no-cache \
  curl \
  && rm -rf /var/cache/apk/*

# nginx user already exists in nginx:alpine image

# Copy custom nginx configuration
COPY --chown=nginx:nginx dockerfiles/nginx.conf /etc/nginx/nginx.conf
COPY --chown=nginx:nginx dockerfiles/default.conf /etc/nginx/conf.d/default.conf

# Create cache directory with proper permissions
RUN mkdir -p /var/cache/nginx \
  && chown -R nginx:nginx /var/cache/nginx \
  && mkdir -p /var/log/nginx \
  && chown -R nginx:nginx /var/log/nginx \
  && touch /var/run/nginx.pid \
  && chown nginx:nginx /var/run/nginx.pid

# Switch to non-root user
USER nginx

# Health check
HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
