import { useState, useEffect } from 'react'
import { ClusterMetrics } from '../types/cluster'
import { dockerAPI } from '../services/dockerAPI'

export const useClusterMetrics = () => {
  const [metrics, setMetrics] = useState<ClusterMetrics>({
    totalServices: 20,
    healthyServices: 0,
    totalVolumes: 14,
    networkLatency: 0,
    timestamp: Date.now(),
  })
  const [isLoading, setIsLoading] = useState(true)
  const [apiAvailable, setApiAvailable] = useState(false)

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        // Try to fetch real metrics from Docker API
        try {
          const systemInfo = await dockerAPI.getSystemInfo()

          setMetrics({
            totalServices: systemInfo.containers,
            healthyServices: systemInfo.containers_running,
            totalVolumes: 14, // Keep static for now, would need separate API call
            networkLatency: Math.random() * 10, // Calculated from network stats in future
            timestamp: Date.now(),
          })

          setApiAvailable(true)
        } catch (apiError) {
          // Fallback to simulated data if API fails
          console.warn('Docker API unavailable, using simulated metrics:', apiError)
          setApiAvailable(false)

          setMetrics({
            totalServices: 20,
            healthyServices: Math.floor(Math.random() * 20) + 15,
            totalVolumes: 14,
            networkLatency: Math.random() * 10,
            timestamp: Date.now(),
          })
        }
      } catch (error) {
        console.error('Failed to fetch metrics:', error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchMetrics()
    const interval = setInterval(fetchMetrics, 15000) // Update every 15 seconds

    return () => clearInterval(interval)
  }, [])

  return { metrics, isLoading, apiAvailable }
}
