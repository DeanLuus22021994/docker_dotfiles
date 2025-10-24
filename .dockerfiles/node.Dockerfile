# Optimized Node.js Dockerfile with Buildx/Bake caching
# Generated: 2025-10-25
# Description: Multi-stage Node.js application with advanced caching
# Build args:
#   - ENVIRONMENT: development|production (default: development)

# Base stage with system dependencies
FROM node:22-alpine AS base

# Build arguments
ARG ENVIRONMENT=development

# Set environment variables
ENV NODE_ENV=${ENVIRONMENT}

# Set work directory
WORKDIR /app

# Dependencies stage for caching
FROM base AS deps

# Copy package files for dependency installation
COPY package*.json ./

# Install dependencies based on environment
RUN if [ "$ENVIRONMENT" = "development" ]; then \
        npm ci; \
    else \
        npm ci --only=production && npm cache clean --force; \
    fi

# Application stage
FROM base AS app

# Copy dependencies from deps stage
COPY --from=deps /app .

# Copy package files
COPY package*.json ./

# Copy application code
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Change ownership
RUN chown -R nextjs:nodejs /app
USER nextjs

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1

# Expose port
EXPOSE 3000

# Run application based on environment
CMD if [ "$ENVIRONMENT" = "development" ]; then \
        npm run dev; \
    else \
        npm start; \
    fi