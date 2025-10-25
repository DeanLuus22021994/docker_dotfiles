import { Service, ServiceStatus } from '../types/cluster'
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
