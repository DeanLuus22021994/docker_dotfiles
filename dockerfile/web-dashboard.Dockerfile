FROM node:22-alpine AS builder

WORKDIR /app

# Copy package files from dashboard
COPY dashboard/package*.json ./

# Install dependencies with cache mount for faster rebuilds
RUN --mount=type=cache,target=/root/.npm \
    npm install --legacy-peer-deps

# Copy all config files from frontend (extended by dashboard configs)
COPY frontend/tsconfig.json ../frontend/tsconfig.json
COPY frontend/postcss.config.js ../frontend/postcss.config.js
COPY frontend/tailwind.config.js ../frontend/tailwind.config.js

# Copy dashboard source
COPY dashboard/ .

# Build with precompilation
RUN npm run build

# Production stage with nginx
FROM nginx:alpine AS production

# Install curl for health check
RUN apk add --no-cache curl

# Copy custom nginx config from frontend location
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost/ || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
