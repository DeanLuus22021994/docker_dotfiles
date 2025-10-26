// Service Type Definitions
export type ServiceStatus = 'healthy' | 'degraded' | 'unhealthy' | 'unknown'

export type ServiceCategory = 
  | 'load-balancer'
  | 'web'
  | 'database'
  | 'cache'
  | 'storage'
  | 'compute'
  | 'monitoring'
  | 'development'

export interface Service {
  id: string
  name: string
  category: ServiceCategory
  layer: string // Layer identifier (data, services, monitoring, compute, network)
  status: ServiceStatus
  url?: string
  port?: number
  healthEndpoint?: string
  description: string
  icon: string
  metrics?: ServiceMetrics
  replicas?: number // Current replica count (Phase 4.6.5)
}

export interface ServiceMetrics {
  cpu: number
  memory: number
  uptime: number
  networkIO?: number // Network I/O in bytes/s (Phase 4.6.2)
  requests?: number
  latency?: number
}

// Layer Metrics (Phase 4.6.2)
export interface LayerMetrics {
  layer: string
  totalCpu: number
  totalMemory: number
  totalNetworkIO: number
  serviceCount: number
  healthyCount: number
  unhealthyCount: number
}

// Cluster Metrics
export interface ClusterMetrics {
  totalServices: number
  healthyServices: number
  totalVolumes: number
  networkLatency: number
  timestamp: number
}

// Volume Type
export interface Volume {
  name: string
  driver: string
  size: string
  mountPath: string
  service: string
}

// Network Type
export interface NetworkConnection {
  from: string
  to: string
  protocol: string
  port: number
  status: 'active' | 'idle'
}

// Layer Dependencies (Phase 4.6.4)
export interface LayerDependency {
  from: string
  to: string
  type: 'requires' | 'uses' | 'monitors'
}

