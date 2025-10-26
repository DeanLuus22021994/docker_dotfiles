// Docker API Proxy service for real-time container metrics
const API_BASE_URL = 'http://localhost:3001/api'

// Authentication token storage
let authToken: string | null = null

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

export interface LoginResponse {
  success: boolean
  accessToken: string
  refreshToken: string
  expiresIn: string
  user: {
    username: string
    role: string
  }
}

export interface AuthError {
  error: string
  message: string
  details?: any[]
}

class DockerAPIService {
  private baseURL: string
  private retryCount: number
  private retryDelay: number

  constructor(baseURL: string = API_BASE_URL, retryCount: number = 3, retryDelay: number = 1000) {
    this.baseURL = baseURL
    this.retryCount = retryCount
    this.retryDelay = retryDelay
    
    // Load token from localStorage on initialization
    this.loadToken()
  }

  /**
   * Load authentication token from localStorage
   */
  private loadToken(): void {
    const stored = localStorage.getItem('auth_token')
    if (stored) {
      authToken = stored
    }
  }

  /**
   * Save authentication token to localStorage
   */
  private saveToken(token: string): void {
    authToken = token
    localStorage.setItem('auth_token', token)
  }

  /**
   * Clear authentication token
   */
  private clearToken(): void {
    authToken = null
    localStorage.removeItem('auth_token')
    localStorage.removeItem('refresh_token')
  }

  /**
   * Get current authentication token
   */
  getToken(): string | null {
    return authToken
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return authToken !== null
  }

  private async fetchWithRetry<T>(url: string, retries: number = this.retryCount): Promise<T> {
    try {
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      }

      // Add authentication token if available
      if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`
      }

      const response = await fetch(url, {
        method: 'GET',
        headers,
        signal: AbortSignal.timeout(10000), // 10 second timeout
      })

      // Handle 401 Unauthorized - token expired or invalid
      if (response.status === 401) {
        this.clearToken()
        throw new Error('Authentication required')
      }

      // Handle 429 Too Many Requests - rate limit exceeded
      if (response.status === 429) {
        const data = await response.json()
        throw new Error(`Rate limit exceeded. ${data.message || 'Please try again later.'}`)
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return data as T
    } catch (error) {
      if (retries > 0 && (error as Error).message !== 'Authentication required') {
        await new Promise(resolve => setTimeout(resolve, this.retryDelay))
        return this.fetchWithRetry<T>(url, retries - 1)
      }
      throw error
    }
  }

  /**
   * Login with username and password
   */
  async login(username: string, password: string): Promise<LoginResponse> {
    try {
      const response = await fetch('http://localhost:3001/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      })

      if (!response.ok) {
        const error: AuthError = await response.json()
        throw new Error(error.message || 'Login failed')
      }

      const data: LoginResponse = await response.json()
      
      // Save tokens
      this.saveToken(data.accessToken)
      localStorage.setItem('refresh_token', data.refreshToken)
      
      return data
    } catch (error) {
      throw error
    }
  }

  /**
   * Logout and clear tokens
   */
  async logout(): Promise<void> {
    try {
      await fetch('http://localhost:3001/auth/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${authToken}`,
        },
      })
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      this.clearToken()
    }
  }

  /**
   * Refresh access token using refresh token
   */
  async refreshToken(): Promise<string> {
    const refreshToken = localStorage.getItem('refresh_token')
    if (!refreshToken) {
      throw new Error('No refresh token available')
    }

    try {
      const response = await fetch('http://localhost:3001/auth/refresh', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refreshToken }),
      })

      if (!response.ok) {
        this.clearToken()
        throw new Error('Token refresh failed')
      }

      const data = await response.json()
      this.saveToken(data.accessToken)
      
      return data.accessToken
    } catch (error) {
      this.clearToken()
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
