# Docker API Proxy - Dockerfile
FROM node:22-alpine

# Install curl for health checks
RUN apk add --no-cache curl

# Set working directory
WORKDIR /app

# Copy package files (including lock file)
COPY api/package.json api/package-lock.json ./

# Install dependencies
RUN npm ci --omit=dev && \
    npm cache clean --force

# Copy application code
COPY api/server.js ./

# For Docker Desktop, socket permissions require root access
# Since socket is mounted read-only, this is acceptable
# Create app directory with proper permissions
RUN chown -R node:node /app

# Note: Running as root for Docker socket access
# Socket is mounted read-only for security

# Expose port
EXPOSE 3001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=10s \
  CMD curl -f http://localhost:3001/health || exit 1

# Start server
CMD ["node", "server.js"]
