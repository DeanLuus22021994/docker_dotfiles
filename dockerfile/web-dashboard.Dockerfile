FROM node:22-alpine AS builder

WORKDIR /app

# Copy package files from web-content
COPY web-content/package*.json ./

# Install dependencies with cache mount for faster rebuilds
RUN --mount=type=cache,target=/root/.npm \
    npm install --legacy-peer-deps

# Copy all config files from .config/web (extended by web-content configs)
COPY .config/web/tsconfig.json ../.config/web/tsconfig.json
COPY .config/web/postcss.config.js ../.config/web/postcss.config.js
COPY .config/web/tailwind.config.js ../.config/web/tailwind.config.js

# Copy web-content source
COPY web-content/ .

# Build with precompilation
RUN npm run build

# Production stage with nginx
FROM nginx:alpine AS production

# Install curl for health check
RUN apk add --no-cache curl

# Copy custom nginx config from central .config location
COPY .config/web/nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost/ || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
