import { useState, useEffect } from 'react'

export interface DockerStats {
  containersRunning: number
  containersStopped: number
  containersPaused: number
  imagesCount: number
  volumesCount: number
  networksCount: number
  cpuUsage: number
  memoryUsage: number
  diskUsage: number
}

export const useDockerStats = () => {
  const [stats, setStats] = useState<DockerStats>({
    containersRunning: 0,
    containersStopped: 0,
    containersPaused: 0,
    imagesCount: 0,
    volumesCount: 14,
    networksCount: 3,
    cpuUsage: 0,
    memoryUsage: 0,
    diskUsage: 0,
  })
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        // Simulate Docker stats collection
        // In production, this would call Docker API or a backend service
        setStats({
          containersRunning: Math.floor(Math.random() * 3) + 18,
          containersStopped: Math.floor(Math.random() * 3),
          containersPaused: 0,
          imagesCount: Math.floor(Math.random() * 5) + 25,
          volumesCount: 14,
          networksCount: 3,
          cpuUsage: Math.random() * 60 + 20,
          memoryUsage: Math.random() * 40 + 40,
          diskUsage: Math.random() * 30 + 50,
        })
      } catch (error) {
        console.error('Failed to fetch Docker stats:', error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchStats()
    const interval = setInterval(fetchStats, 10000) // Update every 10 seconds

    return () => clearInterval(interval)
  }, [])

  return { stats, isLoading }
}
