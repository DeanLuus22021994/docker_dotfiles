import { useState, useEffect } from 'react'
import { Header } from './components/layout/Header'
import { ServiceGrid } from './components/services/ServiceGrid'
import { ClusterMetrics } from './components/metrics/ClusterMetrics'
import { SystemHealth } from './components/health/SystemHealth'
import { VolumeStatus } from './components/storage/VolumeStatus'
import { NetworkTopology } from './components/network/NetworkTopology'
import { DockerStats } from './components/docker/DockerStats'
import { useClusterHealth } from './hooks/useClusterHealth'
import { useClusterMetrics } from './hooks/useClusterMetrics'

function App() {
  const [darkMode, setDarkMode] = useState(false)
  const { services, isLoading: healthLoading, error: healthError } = useClusterHealth()
  const { metrics, isLoading: metricsLoading } = useClusterMetrics()

  useEffect(() => {
    // Check system preference
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      setDarkMode(true)
    }
  }, [])

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [darkMode])

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 transition-colors">
      <Header darkMode={darkMode} onToggleDarkMode={() => setDarkMode(!darkMode)} />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* System Health Overview */}
        <SystemHealth 
          services={services} 
          isLoading={healthLoading} 
          error={healthError}
        />

        {/* Cluster Metrics */}
        <ClusterMetrics 
          metrics={metrics} 
          isLoading={metricsLoading}
        />

        {/* Docker Infrastructure */}
        <DockerStats />

        {/* Service Grid */}
        <ServiceGrid 
          services={services} 
          isLoading={healthLoading}
        />

        {/* Storage & Network */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <VolumeStatus />
          <NetworkTopology />
        </div>
      </main>

      {/* Footer */}
      <footer className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 mt-16 border-t border-gray-200 dark:border-gray-800">
        <div className="text-center text-sm text-gray-600 dark:text-gray-400">
          <p>Modern Data Platform v2.0 • 20 Services • Fully Provisioned</p>
          <p className="mt-2">Built with React 18, TypeScript, Tailwind CSS, Vite 6</p>
        </div>
      </footer>
    </div>
  )
}

export default App
