import { useState, useEffect } from 'react'
import { Service } from '../types/cluster'
import { getAllServices, checkServiceHealth } from '../services/clusterService'

export const useClusterHealth = () => {
  const [services, setServices] = useState<Service[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const checkAllServices = async () => {
      try {
        const serviceConfigs = getAllServices()
        const servicesWithStatus = await Promise.all(
          serviceConfigs.map(async (config) => {
            const status = await checkServiceHealth(config)
            return {
              ...config,
              status,
              metrics: {
                cpu: Math.random() * 100,
                memory: Math.random() * 100,
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
  }, [])

  return { services, isLoading, error }
}
