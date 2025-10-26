import { Service, ServiceStatus, LayerMetrics } from '../types/cluster'
import { INFRASTRUCTURE_SERVICES } from './layers/infrastructure'
import { DATA_SERVICES } from './layers/data'
import { COMPUTE_SERVICES } from './layers/compute'
import { MONITORING_SERVICES } from './layers/monitoring'
import { DEVELOPMENT_SERVICES } from './layers/development'

/**
 * Cluster Service Registry
 * Organized by architectural layers to mirror docker-compose.yml structure
 * Aligns with Modern Data Platform v2.0 cluster architecture
 */
const SERVICES_CONFIG: Omit<Service, 'status' | 'metrics'>[] = [
  ...INFRASTRUCTURE_SERVICES,
  ...DATA_SERVICES,
  ...COMPUTE_SERVICES,
  ...MONITORING_SERVICES,
  ...DEVELOPMENT_SERVICES,
]

export const checkServiceHealth = async (service: Omit<Service, 'status' | 'metrics'>): Promise<ServiceStatus> => {
  if (!service.healthEndpoint) {
    return 'unknown'
  }

  try {
    await fetch(service.healthEndpoint, {
      method: 'GET',
      mode: 'no-cors',
      cache: 'no-cache',
    })
    
    // In no-cors mode, we can't read the response, but we can detect network errors
    return 'healthy'
  } catch (error) {
    // If fetch fails, service might still be starting or unreachable
    return 'unhealthy'
  }
}

export const getAllServices = (): Omit<Service, 'status' | 'metrics'>[] => {
  return SERVICES_CONFIG
}

export const getServicesByCategory = (category: string): Omit<Service, 'status' | 'metrics'>[] => {
  return SERVICES_CONFIG.filter(service => service.category === category)
}

/**
 * Calculate aggregated metrics per layer (Phase 4.6.2)
 * Aggregates CPU, memory, network I/O, and service counts by layer
 */
export const calculateLayerMetrics = (services: Service[]): Record<string, LayerMetrics> => {
  const layerMap = new Map<string, LayerMetrics>()

  services.forEach(service => {
    const layer = service.layer
    const existing = layerMap.get(layer)

    if (!existing) {
      layerMap.set(layer, {
        layer,
        totalCpu: service.metrics?.cpu || 0,
        totalMemory: service.metrics?.memory || 0,
        totalNetworkIO: service.metrics?.networkIO || 0,
        serviceCount: 1,
        healthyCount: service.status === 'healthy' ? 1 : 0,
        unhealthyCount: service.status === 'unhealthy' ? 1 : 0,
      })
    } else {
      layerMap.set(layer, {
        ...existing,
        totalCpu: existing.totalCpu + (service.metrics?.cpu || 0),
        totalMemory: existing.totalMemory + (service.metrics?.memory || 0),
        totalNetworkIO: existing.totalNetworkIO + (service.metrics?.networkIO || 0),
        serviceCount: existing.serviceCount + 1,
        healthyCount: existing.healthyCount + (service.status === 'healthy' ? 1 : 0),
        unhealthyCount: existing.unhealthyCount + (service.status === 'unhealthy' ? 1 : 0),
      })
    }
  })

  return Object.fromEntries(layerMap)
}

/**
 * Get layer metrics by ID (Phase 4.6.2)
 */
export const getLayerMetrics = (services: Service[], layerId: string): LayerMetrics | null => {
  const layerServices = services.filter(s => s.layer === layerId)
  if (layerServices.length === 0) return null

  const metrics = calculateLayerMetrics(layerServices)
  return metrics[layerId] || null
}

