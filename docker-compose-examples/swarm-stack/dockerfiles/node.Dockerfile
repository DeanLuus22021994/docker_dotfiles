# Simplified Node.js Dockerfile for swarm-stack
# Optimized for Docker Swarm deployment with resource constraints

FROM node:20-alpine AS base
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
  curl \
  && rm -rf /var/cache/apk/*

# Create non-root user
RUN addgroup -g 1001 -S nodejs \
  && adduser -S -D -H -u 1001 -h /app -s /sbin/nologin -G nodejs -g nodejs nodejs

# Copy package files
COPY --chown=nodejs:nodejs package*.json ./

# Skip prepare scripts during Docker build
ENV npm_config_ignore_scripts=true

# Install all dependencies
RUN npm install --legacy-peer-deps \
  && npm cache clean --force

# Copy source code
COPY --chown=nodejs:nodejs . .

# Build application if needed
RUN npm run build --if-present

# Install a simple static file server for production
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Default command (can be overridden in docker-compose)
CMD ["serve", "-s", "dist", "-l", "3000"]
