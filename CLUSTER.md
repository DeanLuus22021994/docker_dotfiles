# Modern Data Platform v2.0 - Complete Cluster Overview

## 🎯 Cluster Dashboard

**Access**: http://localhost:3000

The integrated React dashboard provides real-time monitoring of all 20 services in the cluster.

### Quick Start

**Development Mode** (with hot reload):
```bash
cd web-content
npm install
npm run dev
```

**Production Mode** (Docker):
```bash
docker-compose up -d cluster-dashboard
```

## 📊 Cluster Services (20 Total)

### Infrastructure Layer (4 Services)
- **Load Balancer** (`:8080`) - Nginx load balancer distributing across 3 web servers
- **Web Server 1-3** - Nginx web servers serving static content

### Database Layer (2 Services)
- **PostgreSQL** (`:5432`) - Primary relational database
- **MariaDB** (`:3306`) - MySQL-compatible database

### Cache & Storage Layer (2 Services)
- **Redis** (`:6379`) - In-memory cache with persistence
- **MinIO** (`:9000`, `:9001`) - S3-compatible object storage

### Compute Layer (3 Services)
- **Jupyter Lab** (`:8888`) - GPU-accelerated ML notebooks
- **GitHub MCP** - Model Context Protocol for GitHub
- **k9s** - Kubernetes CLI management

### Monitoring Layer (2 Services)
- **Grafana** (`:3002`) - Monitoring dashboards
- **Prometheus** (`:9090`) - Metrics collection

### Development Tools (6 Services)
- **BuildKit** (`:1234`) - Docker build optimization
- **LocalStack** (`:4566`) - Local AWS cloud
- **MailHog** (`:8025`) - Email testing
- **pgAdmin** (`:5050`) - Database admin
- **Redis Commander** (`:8081`) - Redis management
- **Cluster Dashboard** (`:3000`) - This monitoring UI

### DevContainer (1 Service)
- **DevContainer** - Development environment (profile: dev)

## 🚀 Deployment

### Full Cluster Deployment
```bash
# Start all services
docker-compose up -d

# Include DevContainer
docker-compose --profile dev up -d

# View status
docker-compose ps

# View logs
docker-compose logs -f cluster-dashboard
```

### Dashboard Only
```bash
# Start dashboard with dependencies
docker-compose up -d cluster-dashboard

# Rebuild dashboard after code changes
docker-compose build cluster-dashboard
docker-compose up -d cluster-dashboard
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      cluster-network                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌─────────────────────────────┐     │
│  │ Load Balancer│─────▶│  Web1 │ Web2 │ Web3          │     │
│  │   (:8080)    │      └─────────────────────────────┘     │
│  └──────────────┘                                            │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Dashboard (:3000) - React Monitoring UI              │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────┬─────────────┬─────────────┐               │
│  │ PostgreSQL  │  MariaDB    │   Redis     │               │
│  │  (:5432)    │  (:3306)    │  (:6379)    │               │
│  └─────────────┴─────────────┴─────────────┘               │
│                                                               │
│  ┌─────────────┬─────────────┬─────────────┐               │
│  │  MinIO      │  Jupyter    │  Grafana    │               │
│  │  (:9000)    │  (:8888)    │  (:3002)    │               │
│  └─────────────┴─────────────┴─────────────┘               │
│                                                               │
│  ┌─────────────┬─────────────┬─────────────┐               │
│  │ Prometheus  │ LocalStack  │  MailHog    │               │
│  │  (:9090)    │  (:4566)    │  (:8025)    │               │
│  └─────────────┴─────────────┴─────────────┘               │
│                                                               │
│  ┌─────────────┬─────────────┬─────────────┐               │
│  │  pgAdmin    │   Redis     │  BuildKit   │               │
│  │  (:5050)    │ Commander   │  (:1234)    │               │
│  │             │  (:8081)    │             │               │
│  └─────────────┴─────────────┴─────────────┘               │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Volumes (14 Total)

- `cluster_postgres_data` - PostgreSQL database
- `cluster_redis_data` - Redis persistence
- `cluster_mariadb_data` - MariaDB database
- `cluster_mariadb_logs` - MariaDB logs
- `cluster_jupyter_data` - Jupyter notebooks
- `cluster_minio_data` - Object storage
- `cluster_grafana_data` - Grafana dashboards
- `cluster_prometheus_data` - Metrics storage
- `cluster_k9s_config` - k9s configuration
- `cluster_github_mcp_data` - MCP server data
- `cluster_mcp_data` - Additional MCP data
- `cluster_buildkit_data` - Build cache
- `cluster_localstack_data` - LocalStack state
- `cluster_pgadmin_data` - pgAdmin config

## 🌐 Network

**Name**: `cluster-network`
**Driver**: bridge
**Purpose**: Isolated network for all cluster services

## 🎨 Dashboard Features

### Real-time Monitoring
- Service health status (healthy/degraded/unhealthy)
- CPU and memory metrics per service
- Network latency tracking
- Docker infrastructure stats

### Visualizations
- System health overview with health score
- Live metrics charts (Recharts)
- Volume usage progress bars
- Network topology diagram

### UI Features
- Dark/light mode with auto-detection
- Responsive design (mobile/tablet/desktop)
- Quick service access links
- Real-time updates (15-30s intervals)

## 🔧 Technology Stack

### Dashboard
- React 18.3 + TypeScript 5.7
- Vite 6.0 (build tool)
- Tailwind CSS 3.4 (styling)
- Recharts 2.13 (charts)
- Lucide React (icons)

### Infrastructure
- Docker Compose (orchestration)
- Nginx Alpine (web servers)
- Multi-stage builds (optimization)

## 📝 Configuration Files

```
docker-compose.yml          # Main cluster definition
web-content/
  ├── Dockerfile           # Dashboard production build
  ├── nginx.conf           # Production Nginx config
  ├── vite.config.ts       # Vite build config
  ├── tailwind.config.js   # Tailwind customization
  ├── tsconfig.json        # TypeScript config
  └── src/
      ├── services/clusterService.ts  # Service definitions
      ├── hooks/                      # React hooks
      └── components/                 # UI components
```

## 🔐 Default Credentials

**PostgreSQL**
- User: `cluster_user`
- Password: `changeme`
- Database: `clusterdb`

**MariaDB**
- Root Password: `changeme`
- User: `cluster_user`
- Password: `changeme`
- Database: `clusterdb`

**Grafana**
- Username: `admin`
- Password: `admin`

**MinIO**
- User: `minioadmin`
- Password: `minioadmin`

**Jupyter**
- Token: `changeme`

**pgAdmin**
- Email: `admin@cluster.local`
- Password: `admin`

⚠️ **Change these in production!**

## 🚦 Health Checks

All services have health checks configured:
- Interval: 30s
- Timeout: 10s
- Retries: 3
- Start period: 20-60s (varies by service)

Dashboard monitors these endpoints and displays status.

## 🔍 Troubleshooting

### Dashboard Not Loading
```bash
# Check if running
docker-compose ps cluster-dashboard

# View logs
docker-compose logs cluster-dashboard

# Rebuild
docker-compose build cluster-dashboard
docker-compose up -d cluster-dashboard
```

### Service Unreachable
```bash
# Check network
docker network inspect cluster-network

# Check service health
docker-compose ps

# View specific service logs
docker-compose logs <service-name>
```

### Development Mode Issues
```bash
cd web-content

# Clean install
rm -rf node_modules package-lock.json
npm install

# Type check
npm run type-check

# Start dev server
npm run dev
```

## 📊 Performance

### Resource Usage (Approximate)
- **Total Containers**: 20
- **Total Volumes**: 14
- **Network**: 1 bridge network
- **Memory**: ~8-12 GB (all services)
- **CPU**: Variable based on load
- **Disk**: ~20-30 GB (with data)

### Dashboard Performance
- Initial load: < 2s
- Hot reload: < 100ms (dev mode)
- Health checks: 30s interval
- Metrics refresh: 15s interval
- Docker stats: 10s interval

## 🎯 Next Steps

1. **Access Dashboard**: http://localhost:3000
2. **Verify Services**: Check all 20 services are healthy
3. **Explore Features**: Dark mode, metrics, topology
4. **Customize**: Edit `src/services/clusterService.ts`
5. **Monitor**: Use Grafana and Prometheus for deep metrics

## 📚 Documentation

- `README.md` - Dashboard overview and features
- `QUICKSTART.md` - Quick start guide
- `INSTALL.md` - Detailed installation and troubleshooting
- `TODO.md` - Project roadmap

## 🤝 Integration

The dashboard is fully integrated into the cluster:
- Connected to `cluster-network`
- Depends on key services (DBs, load balancer)
- Health checks all services
- Single `docker-compose.yml` management
- No separate deployment scripts needed

**Everything runs from the root docker-compose.yml file.**
