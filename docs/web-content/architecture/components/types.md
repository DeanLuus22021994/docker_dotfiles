---
date_created: "2025-10-26T18:32:25.963360+00:00"
last_updated: "2025-10-26T18:32:25.963360+00:00"
tags: ['documentation', 'web-content', 'architecture']
description: "Documentation for types"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- web-content
- architecture
- typescript
description: TypeScript type system and type definitions
---\n# Type System

## Type Definitions (`src/types/`)

**`cluster.ts`**
- ClusterHealth, ClusterMetrics, ClusterStatus interfaces
- Service health types
- Node status types

**Additional Type Files**
- Container types (ContainerStats, ContainerInfo)
- Network types (NetworkTopology, NetworkNode)
- Volume types (VolumeStatus, VolumeUsage)
- Metrics types (MetricData, MetricSeries)

## Type Safety Benefits

1. **Compile-Time Errors** - Catch bugs before runtime
2. **IntelliSense** - Auto-complete and documentation
3. **Refactoring Safety** - Type errors guide changes
4. **Self-Documenting** - Types serve as documentation

## Example Type Definition

```typescript
export interface ClusterHealth {
  status: 'healthy' | 'degraded' | 'unhealthy';
  score: number; // 0-100
  services: ServiceHealth[];
  lastUpdated: Date;
}

export interface ServiceHealth {
  name: string;
  status: 'running' | 'stopped' | 'error';
  cpu: number;
  memory: number;
}
```

## Type Conventions

- Interface for object shapes
- Type alias for unions/intersections
- Enums for fixed sets of values
- Readonly for immutable data
