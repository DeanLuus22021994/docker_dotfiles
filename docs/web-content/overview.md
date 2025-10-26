---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["web-content", "overview", "documentation"]
description: "Documentation for overview in web-content"
---
# Cluster Dashboard

A comprehensive React-based monitoring dashboard for the Modern Data Platform v2.0, providing real-time cluster status, service health monitoring, and system metrics visualization.

## 🚀 Features

- **Real-time Service Monitoring** - Track 20+ services including databases, caches, load balancers, and monitoring tools
- **System Health Overview** - At-a-glance cluster health with color-coded status indicators
- **Cluster Metrics** - Live metrics tracking for services, volumes, and network latency
- **Volume Status** - Monitor Docker volume usage across all services
- **Network Topology** - Visualize service connections and network architecture
- **Dark Mode** - Full dark/light theme support with system preference detection
- **Responsive Design** - Optimized for desktop and mobile viewing

## 🛠️ Tech Stack

- **React 18** - Modern React with hooks and concurrent features
- **TypeScript** - Type-safe development
- **Vite 6** - Lightning-fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Recharts** - Composable charting library for metrics visualization
- **Lucide React** - Beautiful, consistent icon set

## 📦 Installation

### Development Mode (Recommended)
```bash
cd web-content
npm install
npm run dev
```

### Production Mode (Docker)
The dashboard is integrated into the main cluster docker-compose.yml:
```bash
docker-compose up -d cluster-dashboard
```

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

## 🔧 Development

```bash
# Type checking
npm run type-check

# Lint code
npm run lint
```

## 🌐 Services Monitored

### Infrastructure (4)
- Load Balancer (Nginx)
- Web Server 1-3 (Nginx)

### Databases (2)
- PostgreSQL 13
- MariaDB 11

### Cache & Storage (2)
- Redis 7
- MinIO (S3-compatible)

### Compute (3)
- Jupyter Lab (GPU-accelerated)
- GitHub MCP
- k9s

### Monitoring (2)
- Grafana
- Prometheus

### Development Tools (7)
- BuildKit
- LocalStack
- MailHog
- pgAdmin
- Redis Commander
- And more...

## 📊 Dashboard Sections

### System Health
- Overall cluster health status
- Health score percentage
- Healthy/degraded/unhealthy service counts

### Cluster Metrics
- Total services count
- Healthy services count
- Volume statistics
- Real-time network latency graph

### Service Grid
- Individual service cards with:
  - Status indicators
  - CPU and memory metrics
  - Quick access links
  - Port information

### Volume Status
- Docker volume usage tracking
- Storage allocation per service
- Visual progress bars

### Network Topology
- Service connection mapping
- Port information
- Connection status indicators

## 🎨 Customization

The dashboard is highly customizable through:

- **Tailwind Config** - Modify colors, spacing, and theme in `tailwind.config.js`
- **Service Configuration** - Update service list in `src/services/layers/` (organized by cluster layer)
- **Metrics** - Adjust polling intervals in hooks (`src/hooks/`)

### Adding New Services

Services are organized into architectural layers matching docker-compose.yml:
1. Choose layer: `infrastructure`, `data`, `compute`, `monitoring`, or `development`
2. Edit corresponding file in `src/services/layers/`
3. Add service configuration with container name
4. Service automatically appears in dashboard

See `src/services/layers/README.md` for detailed architecture documentation.

## 🚦 Health Check Endpoints

The dashboard performs health checks on services with exposed endpoints:
- Load Balancer: `http://localhost:8080`
- PostgreSQL: Port 5432
- MariaDB: Port 3306
- Redis: Port 6379
- MinIO: `http://localhost:9000/minio/health/live`
- Grafana: `http://localhost:3002/api/health`
- Prometheus: `http://localhost:9090/-/healthy`

## 📝 Configuration

### Environment Variables
No environment variables required - all configuration is in code for simplicity.

### Service Polling
- Health checks: Every 30 seconds
- Metrics updates: Every 15 seconds

## 🔐 Security Notes

- Dashboard runs on port 3000 by default
- No authentication implemented (intended for local/private network use)
- All health checks use `no-cors` mode for cross-origin requests

## 📱 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## 🤝 Contributing

This dashboard is part of the Modern Data Platform v2.0 project. To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

Part of the Modern Data Platform v2.0 project.

## 🙏 Acknowledgments

Built with modern React patterns and best practices, leveraging:
- Vite for blazing-fast development
- TypeScript for type safety
- Tailwind CSS for rapid UI development
- Recharts for beautiful data visualization
