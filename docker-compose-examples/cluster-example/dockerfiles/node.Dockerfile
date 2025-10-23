# Multi-stage Node.js Dockerfile for cluster-example
# Optimized for cluster deployment with load balancing

FROM node:20-alpine AS base
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
  curl \
  && rm -rf /var/cache/apk/*

# Create non-root user
RUN addgroup -g 1001 -S nodejs \
  && adduser -S -D -H -u 1001 -h /app -s /sbin/nologin -G nodejs -g nodejs nodejs

FROM base AS deps
# Copy package files
COPY --chown=nodejs:nodejs package*.json ./
# Skip prepare scripts during Docker build
ENV npm_config_ignore_scripts=true
# Install production dependencies only
RUN npm install --only=production --legacy-peer-deps \
  && npm cache clean --force

FROM deps AS dev-deps
# Install all dependencies (including dev)
RUN npm install --legacy-peer-deps \
  && npm cache clean --force

FROM dev-deps AS builder
# Copy source code
COPY --chown=nodejs:nodejs . .
# Build application if needed
RUN npm run build --if-present

FROM base AS runner
# Copy dependencies from deps stage
COPY --from=deps --chown=nodejs:nodejs /app/node_modules ./node_modules
# Copy built application
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/public ./public
COPY --from=builder --chown=nodejs:nodejs /app/package*.json ./
COPY --from=builder --chown=nodejs:nodejs /app/server.js* ./

# Switch to non-root user
USER nodejs

# Environment variables for cluster
ENV NODE_ENV=production
ENV PORT=3000
ENV HOST=0.0.0.0

# Health check
HEALTHCHECK --interval=15s --timeout=5s --start-period=45s --retries=5 \
  CMD curl -f http://localhost:3000/health || exit 1

EXPOSE 3000

# Default command (can be overridden in docker-compose)
CMD ["npm", "start"]
