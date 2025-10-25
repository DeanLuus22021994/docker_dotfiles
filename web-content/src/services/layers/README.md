# Service Layer Architecture

This directory contains modular service definitions organized by cluster architectural layers. Each module corresponds to a layer in the docker-compose.yml cluster architecture.

## Structure

```
layers/
├── infrastructure.ts  # Load balancer + web server fleet
├── data.ts           # Databases, cache, object storage
├── compute.ts        # ML/GPU workloads, AI integration
├── monitoring.ts     # Observability and metrics
└── development.ts    # Developer tools and admin panels
```

## Design Principles

### 1. **Alignment with Cluster Architecture**
Each layer mirrors the organization of services in `docker-compose.yml`:
- **Infrastructure Layer**: `loadbalancer`, `cluster-web1/2/3`
- **Data Layer**: `cluster-postgres`, `cluster-mariadb`, `cluster-redis`, `cluster-minio`
- **Compute Layer**: `cluster-jupyter`, `cluster-github-mcp`, `cluster-k9s`
- **Monitoring Layer**: `cluster-grafana`, `cluster-prometheus`
- **Development Layer**: `cluster-buildkit`, `cluster-localstack`, `cluster-mailhog`, `cluster-pgadmin`, `cluster-redis-commander`

### 2. **Modular Service Definitions**
Each layer exports a typed array of service configurations:
```typescript
export const DATA_SERVICES: Omit<Service, 'status' | 'metrics'>[] = [...]
```

### 3. **Container Name Documentation**
Service descriptions include actual container names from docker-compose.yml for easy reference:
```typescript
description: 'PostgreSQL 13 relational database (cluster-postgres)'
```

### 4. **Single Responsibility**
Each module manages only services in its architectural layer, making it easy to:
- Add/remove services within a layer
- Update layer-specific configurations
- Understand cluster topology at a glance

## Adding New Services

### Step 1: Determine Layer
Identify which architectural layer your service belongs to:
- Infrastructure: Load balancing, web serving
- Data: Persistence, caching, storage
- Compute: Processing, ML, AI workloads
- Monitoring: Metrics, dashboards, alerting
- Development: Tools, admin panels, testing

### Step 2: Add to Layer Module
Edit the corresponding file (e.g., `data.ts`):
```typescript
{
  id: 'my-database',
  name: 'My Database',
  category: 'database',
  port: 5433,
  healthEndpoint: 'http://localhost:5433',
  description: 'My custom database (cluster-my-database)',
  icon: '🗄️',
}
```

### Step 3: Verify Registry
The service is automatically included via `clusterService.ts` registry:
```typescript
const SERVICES_CONFIG = [
  ...INFRASTRUCTURE_SERVICES,
  ...DATA_SERVICES,  // Your service is included here
  ...COMPUTE_SERVICES,
  ...MONITORING_SERVICES,
  ...DEVELOPMENT_SERVICES,
]
```

## Service Configuration Schema

```typescript
{
  id: string               // Unique identifier (lowercase-hyphenated)
  name: string             // Display name
  category: ServiceCategory // 'load-balancer' | 'web' | 'database' | 'cache' | ...
  url?: string             // Optional public URL
  port?: number            // Exposed port
  healthEndpoint?: string  // Health check endpoint
  description: string      // User-facing description (include container name)
  icon: string             // Emoji icon
}
```

## Benefits

### 🎯 **Maintainability**
- Clear separation of concerns
- Easy to locate and update services
- Reduced cognitive load when making changes

### 🔍 **Discoverability**
- Service organization matches cluster architecture
- Container names documented in descriptions
- Layer purpose explicit in module name

### 🚀 **Scalability**
- Add entire new layers without touching existing code
- Scale individual layers independently
- Future-proof for cluster growth

### 📖 **Documentation**
- Self-documenting structure
- Clear mapping to docker-compose.yml
- Architecture visible in code organization

## Integration Points

### clusterService.ts
Main service registry that aggregates all layers:
```typescript
import { INFRASTRUCTURE_SERVICES } from './layers/infrastructure'
import { DATA_SERVICES } from './layers/data'
// ... other imports

const SERVICES_CONFIG = [
  ...INFRASTRUCTURE_SERVICES,
  ...DATA_SERVICES,
  ...COMPUTE_SERVICES,
  ...MONITORING_SERVICES,
  ...DEVELOPMENT_SERVICES,
]
```

### Service Grid Component
Automatically displays services grouped by their layers:
```typescript
<ServiceGrid services={services} />
```

### Health Monitoring
All layer services are monitored via `useClusterHealth` hook:
```typescript
const { services, isLoading, error } = useClusterHealth()
```

## Layer Details

### Infrastructure Layer (4 services)
**Purpose**: Traffic distribution and web serving  
**Services**: Load Balancer, Web Servers 1-3  
**Key Ports**: 8080 (LB)

### Data Layer (4 services)
**Purpose**: Data persistence and caching  
**Services**: PostgreSQL, MariaDB, Redis, MinIO  
**Key Ports**: 5432, 3306, 6379, 9000/9001

### Compute Layer (3 services)
**Purpose**: Processing and AI workloads  
**Services**: Jupyter Lab, GitHub MCP, k9s  
**Key Ports**: 8888 (Jupyter)

### Monitoring Layer (2 services)
**Purpose**: Observability and metrics  
**Services**: Grafana, Prometheus  
**Key Ports**: 3002 (Grafana), 9090 (Prometheus)

### Development Layer (5 services)
**Purpose**: Developer tools and utilities  
**Services**: BuildKit, LocalStack, MailHog, pgAdmin, Redis Commander  
**Key Ports**: 1234, 4566, 8025, 5050, 8081

## Migration Notes

### Before (Monolithic)
All 18 services in single array in `clusterService.ts` - difficult to navigate and maintain.

### After (Modular)
Services split across 5 layer modules - matches cluster architecture, easy to extend.

## Related Files

- `../../types/cluster.ts` - TypeScript type definitions
- `../clusterService.ts` - Service registry and health check logic
- `../../hooks/useClusterHealth.ts` - Health monitoring hook
- `../../components/services/ServiceGrid.tsx` - Service display component

## Future Enhancements

1. **Layer-specific health checks** - Different polling intervals per layer
2. **Layer metrics aggregation** - Per-layer resource usage stats
3. **Visual layer grouping** - Collapsed/expanded sections in UI
4. **Layer dependencies** - Explicit dependency trees (e.g., Web → Data)
5. **Layer scaling** - UI controls to scale services within a layer
