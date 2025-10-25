import { ClusterMetrics as ClusterMetricsType } from '../../types/cluster'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { Activity, Database, HardDrive, Network } from 'lucide-react'
import { useState, useEffect } from 'react'

interface ClusterMetricsProps {
  metrics: ClusterMetricsType
  isLoading: boolean
}

interface TimeSeriesData {
  time: string
  value: number
}

export const ClusterMetrics = ({ metrics, isLoading }: ClusterMetricsProps) => {
  const [latencyData, setLatencyData] = useState<TimeSeriesData[]>([])

  useEffect(() => {
    // Simulate time-series data
    setLatencyData((prev: TimeSeriesData[]) => {
      const now = new Date()
      const newData = [
        ...prev,
        {
          time: now.toLocaleTimeString(),
          value: metrics.networkLatency,
        },
      ].slice(-20) // Keep last 20 data points
      return newData
    })
  }, [metrics.networkLatency])

  if (isLoading) {
    return null
  }

  return (
    <section className="space-y-4">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
        Cluster Metrics
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Services */}
        <div className="card">
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Total Services
                </p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">
                  {metrics.totalServices}
                </p>
              </div>
              <Activity className="w-10 h-10 text-primary-500 opacity-75" />
            </div>
          </div>
        </div>

        {/* Healthy Services */}
        <div className="card">
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Healthy Services
                </p>
                <p className="text-3xl font-bold text-green-600 dark:text-green-400 mt-1">
                  {metrics.healthyServices}
                </p>
              </div>
              <Database className="w-10 h-10 text-green-500 opacity-75" />
            </div>
          </div>
        </div>

        {/* Total Volumes */}
        <div className="card">
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Total Volumes
                </p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">
                  {metrics.totalVolumes}
                </p>
              </div>
              <HardDrive className="w-10 h-10 text-purple-500 opacity-75" />
            </div>
          </div>
        </div>

        {/* Network Latency */}
        <div className="card">
          <div className="card-content">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Network Latency
                </p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">
                  {metrics.networkLatency.toFixed(1)}ms
                </p>
              </div>
              <Network className="w-10 h-10 text-blue-500 opacity-75" />
            </div>
          </div>
        </div>
      </div>

      {/* Latency Chart */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Network Latency Over Time
          </h3>
        </div>
        <div className="card-content">
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={latencyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="time" stroke="#9CA3AF" />
              <YAxis stroke="#9CA3AF" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1F2937', 
                  border: 'none', 
                  borderRadius: '0.5rem',
                  color: '#F9FAFB'
                }} 
              />
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke="#3B82F6" 
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </section>
  )
}
