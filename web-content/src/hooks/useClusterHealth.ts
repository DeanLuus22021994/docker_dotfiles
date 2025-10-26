import { useState, useEffect } from 'react'
import { Service, LayerMetrics } from '../types/cluster'
import { getAllServices, checkServiceHealth, calculateLayerMetrics } from '../services/clusterService'
import { dockerAPI } from '../services/dockerAPI'

// Layer-specific health check intervals (Phase 4.6.1)
const LAYER_INTERVALS = {
  data: 60000,       // Data layer: 60s (changes slowly)
  services: 30000,   // Services layer: 30s (moderate changes)
  monitoring: 45000, // Monitoring layer: 45s
  compute: 30000,    // Compute layer: 30s
  network: 15000,    // Network layer: 15s (changes frequently)
}

export const useClusterHealth = () => {
  const [services, setServices] = useState<Service[]>([])
  const [layerMetrics, setLayerMetrics] = useState<Record<string, LayerMetrics>>({})
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [apiAvailable, setApiAvailable] = useState(false)

  useEffect(() => {
    const checkAPIHealth = async () => {
      try {
        await dockerAPI.checkHealth()
        setApiAvailable(true)
      } catch {
        setApiAvailable(false)
      }
    }

    checkAPIHealth()
  }, [])

  useEffect(() => {
    const layerTimers = new Map<string, number>()
    
    const checkLayerServices = async (layerId: string) => {
      try {
        const serviceConfigs = getAllServices().filter(s => s.layer === layerId)
        
        // Fetch real container data if API is available
        let containersData: any = null
        if (apiAvailable) {
          try {
            const result = await dockerAPI.getContainers()
            containersData = result.containers
          } catch (err) {
            console.warn('Failed to fetch Docker API data, falling back to simulated data:', err)
          }
        }

        const servicesWithStatus = await Promise.all(
          serviceConfigs.map(async (config) => {
            const status = await checkServiceHealth(config)
            
            // Find matching container data
            const containerData = containersData?.find((c: any) => 
              c.name.includes(config.name.toLowerCase()) || 
              config.name.toLowerCase().includes(c.name.toLowerCase())
            )

            return {
              ...config,
              status,
              metrics: {
                cpu: containerData?.cpu_percent ?? Math.random() * 100,
                memory: containerData?.memory_usage 
                  ? (containerData.memory_usage / containerData.memory_limit) * 100 
                  : Math.random() * 100,
                uptime: Math.floor(Math.random() * 86400),
                networkIO: Math.random() * 1000000, // bytes/s
              },
              replicas: containerData?.replicas ?? 1,
            }
          })
        )
        
        // Update services state by merging with existing services
        setServices(prevServices => {
          const otherLayerServices = prevServices.filter(s => s.layer !== layerId)
          const updatedServices = [...otherLayerServices, ...servicesWithStatus]
          
          // Calculate layer metrics aggregation (Phase 4.6.2)
          const metrics = calculateLayerMetrics(updatedServices)
          setLayerMetrics(metrics)
          
          return updatedServices
        })
        
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : `Failed to check ${layerId} layer health`)
      } finally {
        setIsLoading(false)
      }
    }

    // Initialize health checks for all layers with layer-specific intervals
    const initializeHealthChecks = () => {
      const layers = Object.keys(LAYER_INTERVALS) as Array<keyof typeof LAYER_INTERVALS>
      
      layers.forEach(layerId => {
        // Initial check
        checkLayerServices(layerId)
        
        // Setup interval for layer-specific polling
        const interval = setInterval(
          () => checkLayerServices(layerId),
          LAYER_INTERVALS[layerId]
        )
        
        layerTimers.set(layerId, interval)
      })
    }

    if (apiAvailable !== null) {
      initializeHealthChecks()
    }

    return () => {
      // Cleanup all layer timers
      layerTimers.forEach(timer => clearInterval(timer))
      layerTimers.clear()
    }
  }, [apiAvailable])

  return { services, layerMetrics, isLoading, error, apiAvailable }
}
