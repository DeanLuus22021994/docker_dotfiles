import React from 'react'
import { LayerMetrics as ILayerMetrics } from '../../types/cluster'

interface LayerMetricsProps {
  metrics: ILayerMetrics
}

/**
 * Layer Metrics Display Component (Phase 4.6.2)
 * Shows aggregated metrics for a specific layer
 */
export const LayerMetrics: React.FC<LayerMetricsProps> = ({ metrics }) => {
  const formatBytes = (bytes: number): string => {
    if (bytes === 0) return '0 B/s'
    const k = 1024
    const sizes = ['B/s', 'KB/s', 'MB/s', 'GB/s']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`
  }

  const healthPercentage = metrics.serviceCount > 0
    ? (metrics.healthyCount / metrics.serviceCount) * 100
    : 0

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
      <div className="text-center">
        <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
          {metrics.totalCpu.toFixed(1)}%
        </div>
        <div className="text-sm text-gray-600 dark:text-gray-400">Total CPU</div>
      </div>

      <div className="text-center">
        <div className="text-2xl font-bold text-green-600 dark:text-green-400">
          {metrics.totalMemory.toFixed(1)}%
        </div>
        <div className="text-sm text-gray-600 dark:text-gray-400">Total Memory</div>
      </div>

      <div className="text-center">
        <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
          {formatBytes(metrics.totalNetworkIO)}
        </div>
        <div className="text-sm text-gray-600 dark:text-gray-400">Network I/O</div>
      </div>

      <div className="text-center">
        <div className="text-2xl font-bold text-yellow-600 dark:text-yellow-400">
          {healthPercentage.toFixed(0)}%
        </div>
        <div className="text-sm text-gray-600 dark:text-gray-400">
          Health ({metrics.healthyCount}/{metrics.serviceCount})
        </div>
      </div>
    </div>
  )
}
