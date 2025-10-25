import { useState, useEffect } from 'react'
import { ClusterMetrics } from '../types/cluster'

export const useClusterMetrics = () => {
  const [metrics, setMetrics] = useState<ClusterMetrics>({
    totalServices: 20,
    healthyServices: 0,
    totalVolumes: 14,
    networkLatency: 0,
    timestamp: Date.now(),
  })
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        // Simulate metrics collection
        setMetrics({
          totalServices: 20,
          healthyServices: Math.floor(Math.random() * 20) + 15,
          totalVolumes: 14,
          networkLatency: Math.random() * 10,
          timestamp: Date.now(),
        })
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

  return { metrics, isLoading }
}
