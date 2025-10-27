---
date_created: "2025-10-27T00:00:00Z"
last_updated: "2025-10-27T00:00:00Z"
tags: ["dashboard", "installation", "guide"]
description: "Dashboard installation reference"
---

# Dashboard Installation

**This guide has been split for better maintainability.**

For dashboard setup information, see:

- [Installation Guide](installation-guide.md) - Step-by-step setup
- [Development Setup](development-setup.md) - Local development
- [Production Deployment](production-deployment.md) - Docker deployment
- [Configuration](configuration.md) - Environment settings

For architecture details, see the `architecture/` directory.

## Quick Start

### Windows

```cmd
# Install dependencies
install.bat

# Start development server
start.bat
```

### PowerShell/Linux/Mac

```bash
# Install dependencies
npm install --legacy-peer-deps

# Start development server
npm run dev
```

The dashboard will be available at: **http://localhost:3000**

## Docker Integration

To serve this dashboard through the docker-compose stack, you can:

### Option 1: Development Mode (Recommended for development)

```bash
cd web-content
npm run dev
```

### Option 2: Production Build

```bash
# Build production assets
npm run build

# Preview production build
npm run preview
```

### Option 3: Nginx Container (Production)

```yaml
# Add to docker-compose.yml
web-dashboard:
  image: nginx:alpine
  container_name: cluster-dashboard
  volumes:
    - ./web-content/dist:/usr/share/nginx/html:ro
    - ./web-content/nginx.conf:/etc/nginx/conf.d/default.conf:ro
  ports:
    - "3000:80"
  networks:
    - platform_network
  healthcheck:
    test:
      ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/"]
    interval: 30s
    timeout: 10s
    retries: 3
  restart: unless-stopped
```

## Available Scripts

### `npm run dev`

Starts the development server with hot-reload at http://localhost:3000

### `npm run build`

Creates an optimized production build in the `dist/` directory

### `npm run preview`

Preview the production build locally

### `npm run lint`

Run ESLint to check code quality

### `npm run type-check`

Run TypeScript compiler to check for type errors

## Troubleshooting

### Dependencies Installation Issues

If you encounter issues with `npm install`:

1. **Clear cache and retry:**

   ```bash
   npm cache clean --force
   rm -rf node_modules package-lock.json
   npm install --legacy-peer-deps
   ```

2. **Node version:**
   Ensure you're using Node.js 18 or higher:

   ```bash
   node --version
   ```

3. **Permission issues:**
   On Windows, run as Administrator
   On Linux/Mac, don't use sudo with npm

### Port Already in Use

If port 3000 is already in use, you can change it in `vite.config.ts`:

```ts
server: {
  port: 3001, // Change to any available port
}
```

### CORS Issues

If services aren't reachable for health checks, ensure:

- Services are running on expected ports
- No firewall blocking localhost connections
- Docker containers are using `network_mode: host` or proper port mapping

### Build Errors

If you encounter TypeScript or build errors:

```bash
# Clean build artifacts
rm -rf dist

# Rebuild
npm run type-check
npm run build
```

## Customization

### Adding New Services

Edit `src/services/clusterService.ts` and add your service to `SERVICES_CONFIG`:

```typescript
{
  id: 'my-service',
  name: 'My Service',
  category: 'web',
  port: 8080,
  healthEndpoint: 'http://localhost:8080/health',
  description: 'My custom service',
  icon: '🚀',
}
```

### Changing Polling Intervals

Edit hook files in `src/hooks/`:

- Health checks: `useClusterHealth.ts` (line 30000 ms)
- Metrics: `useClusterMetrics.ts` (line 15000 ms)

### Styling

Modify `tailwind.config.js` for theme customization:

```js
theme: {
  extend: {
    colors: {
      primary: {
        /* your colors */
      }
    }
  }
}
```

## Production Deployment

### Build for Production

```bash
npm run build
```

This creates optimized files in `dist/` with:

- Minified JavaScript
- Optimized CSS
- Source maps for debugging
- Code splitting for faster loading

### Serve with Nginx

```bash
# Copy dist/ contents to nginx html directory
cp -r dist/* /usr/share/nginx/html/
```

Or use the docker-compose integration (Option 3 above).

## Performance Notes

- Health checks use `no-cors` mode to avoid CORS preflight requests
- Metrics update every 15 seconds to reduce server load
- Service health checks every 30 seconds
- Chart data limited to last 20 points to prevent memory leaks
- Code splitting reduces initial bundle size

## Browser Support

Requires a modern browser with:

- ES2022 support
- CSS Grid
- Flexbox
- fetch API

Recommended browsers:

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Security Considerations

**⚠️ Important:** This dashboard is designed for local/internal use and includes:

- No authentication
- Direct service access URLs
- Exposed port information

For production deployments:

1. Add authentication layer (OAuth, JWT, etc.)
2. Use reverse proxy for service access
3. Implement rate limiting
4. Use HTTPS
5. Restrict network access

## Support

For issues or questions:

1. Check this guide first
2. Review browser console for errors
3. Check service health endpoints manually
4. Verify Docker containers are running

## License

Part of the Modern Data Platform v2.0 project.
