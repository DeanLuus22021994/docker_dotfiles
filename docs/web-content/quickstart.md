---
date_created: "2025-10-26T18:32:25.960163+00:00"
last_updated: "2025-10-26T18:32:25.960163+00:00"
tags: ["documentation", "web-content", "architecture"]
description: "Documentation for quickstart"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- web-content
- quickstart
- documentation
  description: Documentation for quickstart in web-content
  ---\n# Cluster Dashboard - Quick Start

## Development Mode (Hot Reload)

```bash
cd web-content
npm install
npm run dev
```

Dashboard will be available at: http://localhost:3000

## Production Mode (Docker)

The dashboard is automatically built and deployed as part of the main cluster:

```bash
# From project root
docker-compose up -d cluster-dashboard

# View logs
docker-compose logs -f cluster-dashboard

# Rebuild after changes
docker-compose build cluster-dashboard
docker-compose up -d cluster-dashboard
```

Dashboard will be available at: http://localhost:3000

## Features

- **Real-time Monitoring**: 20+ services tracked with health status
- **System Health**: Overall cluster health with metrics
- **Docker Stats**: Container, image, volume, and network tracking
- **Resource Usage**: CPU, Memory, and Disk visualization
- **Service Grid**: Individual service cards with quick access
- **Volume Status**: Storage usage across all volumes
- **Network Topology**: Service connection mapping
- **Dark Mode**: Automatic theme switching

## Architecture

- **Frontend**: React 18 + TypeScript + Vite 6
- **Styling**: Tailwind CSS v3
- **Charts**: Recharts for data visualization
- **Icons**: Lucide React
- **Build**: Multi-stage Docker build with Nginx
- **Integration**: Part of main docker-compose.yml cluster

## Monitored Services

All 20 cluster services are pre-configured:

- Load Balancer + 3 Web Servers
- PostgreSQL, MariaDB, Redis
- MinIO, Jupyter Lab
- Grafana, Prometheus
- BuildKit, LocalStack, MailHog
- pgAdmin, Redis Commander
- GitHub MCP, k9s

## Service Integration

The dashboard is connected to the cluster network and can:

- Check health endpoints of all services
- Display real-time metrics
- Show Docker infrastructure stats
- Visualize network topology

## Configuration

Service definitions are in:

- `src/services/clusterService.ts` - Service configuration
- `src/hooks/useClusterHealth.ts` - Health check polling (30s)
- `src/hooks/useClusterMetrics.ts` - Metrics updates (15s)
- `src/hooks/useDockerStats.ts` - Docker stats (10s)

## Tech Stack

- React 18.3.1
- TypeScript 5.7.2
- Vite 6.0.1
- Tailwind CSS 3.4.15
- Recharts 2.13.3
- Lucide React 0.453.0

## Build Output

Production build includes:

- Minified JS/CSS bundles
- Code splitting (react-vendor, charts, icons)
- Optimized images and assets
- Source maps for debugging
- Gzip compression via Nginx
- Health check endpoint at `/health`

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Notes

- No authentication (designed for internal use)
- Health checks use no-cors mode
- All services use container names for networking
- Dashboard connects to cluster-network bridge
