import { Service } from '../../types/cluster'
import { CheckCircle2, XCircle, AlertCircle, Loader2 } from 'lucide-react'
import clsx from 'clsx'

interface SystemHealthProps {
  services: Service[]
  isLoading: boolean
  error: string | null
}

export const SystemHealth = ({ services, isLoading, error }: SystemHealthProps) => {
  if (isLoading) {
    return (
      <section className="card">
        <div className="card-content flex items-center justify-center py-8">
          <Loader2 className="w-8 h-8 animate-spin text-primary-500" />
        </div>
      </section>
    )
  }

  if (error) {
    return (
      <section className="card border-red-200 dark:border-red-900">
        <div className="card-content">
          <div className="flex items-center space-x-3 text-red-600 dark:text-red-400">
            <XCircle className="w-6 h-6" />
            <span className="font-semibold">Error: {error}</span>
          </div>
        </div>
      </section>
    )
  }

  const healthyCount = services.filter((s) => s.status === 'healthy').length
  const degradedCount = services.filter((s) => s.status === 'degraded').length
  const unhealthyCount = services.filter((s) => s.status === 'unhealthy').length
  const healthPercentage = Math.round((healthyCount / services.length) * 100)

  const overallStatus = unhealthyCount > 0 ? 'critical' : degradedCount > 0 ? 'warning' : 'healthy'

  return (
    <section className="card">
      <div className="card-header">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            System Health
          </h2>
          <div className="flex items-center space-x-2">
            {overallStatus === 'healthy' && (
              <CheckCircle2 className="w-6 h-6 text-green-500" />
            )}
            {overallStatus === 'warning' && (
              <AlertCircle className="w-6 h-6 text-yellow-500" />
            )}
            {overallStatus === 'critical' && (
              <XCircle className="w-6 h-6 text-red-500" />
            )}
            <span
              className={clsx(
                'text-lg font-semibold',
                overallStatus === 'healthy' && 'text-green-600 dark:text-green-400',
                overallStatus === 'warning' && 'text-yellow-600 dark:text-yellow-400',
                overallStatus === 'critical' && 'text-red-600 dark:text-red-400'
              )}
            >
              {overallStatus === 'healthy' && 'All Systems Operational'}
              {overallStatus === 'warning' && 'Some Issues Detected'}
              {overallStatus === 'critical' && 'Critical Issues'}
            </span>
          </div>
        </div>
      </div>
      <div className="card-content">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {/* Health Percentage */}
          <div className="text-center">
            <div className="text-4xl font-bold text-primary-600 dark:text-primary-400">
              {healthPercentage}%
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Health Score
            </div>
          </div>

          {/* Healthy Services */}
          <div className="text-center">
            <div className="text-4xl font-bold text-green-600 dark:text-green-400">
              {healthyCount}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Healthy
            </div>
          </div>

          {/* Degraded Services */}
          <div className="text-center">
            <div className="text-4xl font-bold text-yellow-600 dark:text-yellow-400">
              {degradedCount}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Degraded
            </div>
          </div>

          {/* Unhealthy Services */}
          <div className="text-center">
            <div className="text-4xl font-bold text-red-600 dark:text-red-400">
              {unhealthyCount}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Unhealthy
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
