// Docker API Proxy service for real-time container metrics
const API_BASE_URL = 'http://localhost:3001/api'

export interface ContainerStats {
  name: string
  state: string
  status: string
  health?: string
  cpu_percent?: number
  memory_usage?: number
  memory_limit?: number
  network_rx?: number
  network_tx?: number
}

export interface SystemInfo {
  containers: number
  containers_running: number
  containers_paused: number
  containers_stopped: number
  images: number
  cpus: number
  memory_total: number
  docker_version: string
  os: string
  architecture: string
}

export interface AggregateStats {
  total_containers: number
  running_containers: number
  total_cpu_percent: number
  total_memory_usage: number
  total_network_rx: number
  total_network_tx: number
}

class DockerAPIService {
  private baseURL: string
  private retryCount: number
  private retryDelay: number

  constructor(baseURL: string = API_BASE_URL, retryCount: number = 3, retryDelay: number = 1000) {
    this.baseURL = baseURL
    this.retryCount = retryCount
    this.retryDelay = retryDelay
  }

  private async fetchWithRetry<T>(url: string, retries: number = this.retryCount): Promise<T> {
    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(10000), // 10 second timeout
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return data as T
    } catch (error) {
      if (retries > 0) {
        await new Promise(resolve => setTimeout(resolve, this.retryDelay))
        return this.fetchWithRetry<T>(url, retries - 1)
      }
      throw error
    }
  }

  async getContainers(): Promise<{ containers: ContainerStats[]; timestamp: string }> {
    return this.fetchWithRetry(`${this.baseURL}/containers`)
  }

  async getContainerStats(containerId: string): Promise<any> {
    return this.fetchWithRetry(`${this.baseURL}/containers/${containerId}/stats`)
  }

  async getSystemInfo(): Promise<SystemInfo> {
    return this.fetchWithRetry(`${this.baseURL}/system/info`)
  }

  async getAggregateStats(): Promise<AggregateStats> {
    return this.fetchWithRetry(`${this.baseURL}/stats/aggregate`)
  }

  async checkHealth(): Promise<{ status: string; timestamp: string }> {
    return this.fetchWithRetry(`http://localhost:3001/health`)
  }
}

export const dockerAPI = new DockerAPIService()
