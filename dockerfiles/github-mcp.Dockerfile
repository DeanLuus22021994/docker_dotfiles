# GitHub MCP Server Dockerfile
# Model Context Protocol server for GitHub integration

FROM node:22-alpine AS base

# Install runtime dependencies
RUN apk add --no-cache \
    git \
    curl \
    ca-certificates \
    bash

# Create app directory
WORKDIR /app

# Install GitHub MCP Server with cache mount
RUN --mount=type=cache,target=/root/.npm \
    npm install -g @modelcontextprotocol/server-github

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 && \
    chown -R nodejs:nodejs /app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3001/health || exit 1

USER nodejs

EXPOSE 3001

# Start the MCP server
CMD ["npx", "@modelcontextprotocol/server-github"]
