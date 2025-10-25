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
  status: ServiceStatus
  url?: string
  port?: number
  healthEndpoint?: string
  description: string
  icon: string
  metrics?: ServiceMetrics
}

export interface ServiceMetrics {
  cpu: number
  memory: number
  uptime: number
  requests?: number
  latency?: number
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
