import { useState, useEffect } from 'react'
import { Service } from '../types/cluster'
import { getAllServices, checkServiceHealth } from '../services/clusterService'
import { dockerAPI } from '../services/dockerAPI'

export const useClusterHealth = () => {
  const [services, setServices] = useState<Service[]>([])
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
    const checkAllServices = async () => {
      try {
        const serviceConfigs = getAllServices()
        
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
              },
            }
          })
        )
        setServices(servicesWithStatus)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to check cluster health')
      } finally {
        setIsLoading(false)
      }
    }

    checkAllServices()
    const interval = setInterval(checkAllServices, 30000) // Check every 30 seconds

    return () => clearInterval(interval)
  }, [apiAvailable])

  return { services, isLoading, error, apiAvailable }
}
