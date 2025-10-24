# Consolidated Node.js Dockerfile
# Generated: 2025-10-24
# Description: Multi-purpose Node.js application with configurable environments
# Build args:
#   - ENVIRONMENT: development|production (default: development)

FROM node:22-alpine

# Build arguments
ARG ENVIRONMENT=development

# Set environment variables
ENV NODE_ENV=${ENVIRONMENT}

# Set work directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies based on environment
RUN if [ "$ENVIRONMENT" = "development" ]; then \
        npm install; \
    else \
        npm ci --only=production && npm cache clean --force; \
    fi

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