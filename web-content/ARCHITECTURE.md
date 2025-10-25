# Cluster Dashboard - Architecture Overview

## 🏗️ Project Organization

The dashboard is organized into **modular layers** that mirror the cluster architecture defined in `docker-compose.yml`. This alignment ensures maintainability and makes the codebase easier to understand.

### Directory Structure

```
web-content/
├── src/
│   ├── components/          # React UI components (organized by feature)
│   │   ├── docker/          # Docker infrastructure stats
│   │   ├── health/          # System health overview
│   │   ├── layout/          # Header, navigation
│   │   ├── metrics/         # Cluster metrics and charts
│   │   ├── network/         # Network topology visualization
│   │   ├── services/        # Service grid and cards
│   │   └── storage/         # Volume status
│   │
│   ├── hooks/               # Custom React hooks
│   │   ├── useClusterHealth.ts   # Service health polling (30s)
│   │   ├── useClusterMetrics.ts  # Metrics aggregation (15s)
│   │   └── useDockerStats.ts     # Docker stats polling (10s)
│   │
│   ├── services/            # Service configuration and utilities
│   │   ├── layers/          # 🔥 Modular service definitions by cluster layer
│   │   │   ├── infrastructure.ts  # Load balancer + web servers
│   │   │   ├── data.ts           # Databases, cache, storage
│   │   │   ├── compute.ts        # ML/GPU, AI integration
│   │   │   ├── monitoring.ts     # Grafana, Prometheus
│   │   │   ├── development.ts    # Developer tools
│   │   │   └── README.md         # Layer architecture docs
│   │   └── clusterService.ts     # Service registry + health checks
│   │
│   ├── types/               # TypeScript type definitions
│   │   └── cluster.ts       # Service, metrics, network types
│   │
│   ├── App.tsx              # Main application component
│   ├── main.tsx             # React entry point
│   └── index.css            # Global styles + Tailwind
│
├── Dockerfile               # Multi-stage production build
├── nginx.conf              # Production Nginx configuration
├── package.json            # Dependencies and scripts
├── vite.config.ts          # Vite build configuration
├── tailwind.config.js      # Tailwind CSS customization
├── tsconfig.json           # TypeScript configuration
├── dev.ps1                 # Development server launcher
└── README.md               # User documentation
```

## 🎯 Key Architecture Principles

### 1. Layer-Based Service Organization
Services are split across 5 modules that correspond to cluster architectural layers:

```typescript
// src/services/clusterService.ts
const SERVICES_CONFIG = [
  ...INFRASTRUCTURE_SERVICES,  // Load balancer + web servers
  ...DATA_SERVICES,           // DBs, cache, storage
  ...COMPUTE_SERVICES,        // ML/GPU, AI workloads
  ...MONITORING_SERVICES,     // Grafana, Prometheus
  ...DEVELOPMENT_SERVICES,    // Dev tools, admin panels
]
```

**Benefits:**
- Matches `docker-compose.yml` structure
- Easy to add/remove services within a layer
- Clear separation of concerns
- Self-documenting code organization

### 2. Component-Driven Architecture
React components are organized by **feature**, not technical type:

```
components/
├── docker/       # DockerStats.tsx - Container/image/volume stats
├── health/       # SystemHealth.tsx - Overall cluster status
├── metrics/      # ClusterMetrics.tsx - Metrics + charts
├── network/      # NetworkTopology.tsx - Connection visualization
├── services/     # ServiceGrid + ServiceCard - Service display
└── storage/      # VolumeStatus.tsx - Volume usage tracking
```

Each feature directory is **self-contained** with all related logic.

### 3. Custom Hooks for Data Fetching
Three hooks manage real-time data at different intervals:

| Hook | Purpose | Interval | Data |
|------|---------|----------|------|
| `useClusterHealth` | Service health checks | 30s | Status, CPU, memory per service |
| `useClusterMetrics` | Cluster-wide metrics | 15s | Total services, volumes, latency |
| `useDockerStats` | Docker infrastructure | 10s | Containers, images, resource usage |

**Why multiple intervals?**
- Health checks are "expensive" (network calls to 20 services)
- Metrics are aggregated (lighter weight)
- Docker stats are local (fastest to fetch)

### 4. TypeScript Type Safety
All types are centralized in `src/types/cluster.ts`:

```typescript
export type ServiceStatus = 'healthy' | 'degraded' | 'unhealthy' | 'unknown'
export type ServiceCategory = 'load-balancer' | 'web' | 'database' | ...

export interface Service {
  id: string
  name: string
  category: ServiceCategory
  status: ServiceStatus
  url?: string
  port?: number
  healthEndpoint?: string
  description: string
  icon: string
  metrics?: ServiceMetrics
}
```

## 🔄 Data Flow

### Service Health Monitoring

```
useClusterHealth (30s)
   ↓
getAllServices() → Returns 20 service configs from layers
   ↓
checkServiceHealth() → Fetch each health endpoint
   ↓
Add random metrics (CPU, memory, uptime)
   ↓
Update services state
   ↓
SystemHealth + ServiceGrid components render
```

### Cluster Metrics

```
useClusterMetrics (15s)
   ↓
Calculate:
  - totalServices: 20
  - healthyServices: Count from useClusterHealth
  - totalVolumes: 14
  - networkLatency: Simulated
   ↓
Update metrics state
   ↓
ClusterMetrics component renders charts
```

### Docker Infrastructure

```
useDockerStats (10s)
   ↓
Simulate Docker API calls:
  - containersRunning: 18-20
  - imagesCount: 25-30
  - volumesCount: 14
  - cpuUsage, memoryUsage, diskUsage
   ↓
Update stats state
   ↓
DockerStats component renders cards + progress bars
```

## 🎨 UI Component Hierarchy

```
App.tsx
├── Header (dark mode toggle)
├── SystemHealth (overall status)
├── ClusterMetrics (metrics + chart)
├── DockerStats (infrastructure stats)
├── ServiceGrid
│   └── ServiceCard (x20 services)
├── VolumeStatus (6 volumes)
└── NetworkTopology (8 connections)
```

## 📦 Build & Deployment

### Development Mode
```bash
npm run dev  # Vite dev server on port 3000
```
- Hot module replacement
- Fast refresh
- TypeScript checking

### Production Mode
```bash
npm run build  # Creates dist/ folder
```
Multi-stage Docker build:
1. **Builder stage**: Node 22 Alpine + npm install + vite build
2. **Production stage**: Nginx Alpine + copy dist/ + health check

### Docker Integration
```yaml
# docker-compose.yml
cluster-dashboard:
  build: ./web-content
  ports: ["3000:80"]
  networks: [cluster-network]
  healthcheck: /health endpoint
```

## 🔍 Health Check Implementation

### Service Health
```typescript
// src/services/clusterService.ts
export const checkServiceHealth = async (service) => {
  try {
    await fetch(service.healthEndpoint, {
      mode: 'no-cors',  // Avoid CORS preflight
      cache: 'no-cache',
    })
    return 'healthy'
  } catch {
    return 'unhealthy'
  }
}
```

**Why no-cors?**
- Services don't have CORS headers configured
- We only need to know if service responds
- Actual response body not needed

### Docker Health
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1
```

## 🎯 Future-Proof Design

### Adding New Services
1. Determine layer (infrastructure/data/compute/monitoring/development)
2. Add to corresponding `layers/*.ts` file
3. Automatically included in registry
4. Component renders new service card

### Adding New Layers
1. Create `layers/my-new-layer.ts`
2. Export `MY_NEW_LAYER_SERVICES` array
3. Import in `clusterService.ts`
4. Add to `SERVICES_CONFIG` spread

### Modifying Health Checks
- Update `checkServiceHealth()` in `clusterService.ts`
- All services use same logic (consistency)

### Adjusting Polling Intervals
- Edit hooks in `src/hooks/`
- Independent intervals per data type

## 📊 Performance Considerations

### Code Splitting
```typescript
// vite.config.ts
manualChunks: {
  'react-vendor': ['react', 'react-dom'],
  'charts': ['recharts'],
  'icons': ['lucide-react'],
}
```

### Optimizations
- React 18 concurrent features
- Memoization where needed
- Efficient re-renders via proper state management
- Lazy loading for future expansion

## 🔐 Security Notes

### Current State (Development)
- No authentication (internal use)
- Direct service access URLs
- Exposed port information

### Production Recommendations
1. Add authentication layer (OAuth/JWT)
2. Use reverse proxy for service access
3. Implement rate limiting
4. Enable HTTPS
5. Restrict network access

## 📚 Documentation Structure

| File | Purpose |
|------|---------|
| `README.md` | User-facing feature overview |
| `ARCHITECTURE.md` | **(This file)** Technical architecture |
| `QUICKSTART.md` | Quick start guide |
| `INSTALL.md` | Detailed installation |
| `IMPLEMENTATION.md` | Implementation summary |
| `src/services/layers/README.md` | Service layer architecture |

## 🎓 Learning Path

### New Developers
1. Read `QUICKSTART.md` - Get running fast
2. Read this `ARCHITECTURE.md` - Understand structure
3. Explore `src/services/layers/` - See service organization
4. Look at `src/hooks/` - Understand data fetching
5. Browse `src/components/` - See UI implementation

### Contributing
1. Identify which layer your change affects
2. Follow existing patterns in that layer
3. Update types if needed
4. Test with `npm run dev`
5. Verify production build with Docker

## ✅ Quality Checklist

- [x] TypeScript strict mode enabled
- [x] All errors resolved
- [x] ESLint configured
- [x] Modular architecture
- [x] Type-safe throughout
- [x] Production-ready Docker build
- [x] Health checks implemented
- [x] Real-time updates
- [x] Responsive design
- [x] Dark mode support
- [x] Comprehensive documentation

## 🚀 Next Steps

See `TODO.md` for planned enhancements and roadmap.
