import { Service } from '../../types/cluster'
import { ExternalLink, Circle } from 'lucide-react'
import clsx from 'clsx'

interface ServiceCardProps {
  service: Service
}

export const ServiceCard = ({ service }: ServiceCardProps) => {
  const statusColor = {
    healthy: 'text-green-500',
    degraded: 'text-yellow-500',
    unhealthy: 'text-red-500',
    unknown: 'text-gray-500',
  }[service.status]

  const statusBg = {
    healthy: 'bg-green-100 dark:bg-green-900/30',
    degraded: 'bg-yellow-100 dark:bg-yellow-900/30',
    unhealthy: 'bg-red-100 dark:bg-red-900/30',
    unknown: 'bg-gray-100 dark:bg-gray-900/30',
  }[service.status]

  return (
    <div className="card hover:shadow-md transition-shadow">
      <div className="card-content space-y-4">
        {/* Header */}
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-3">
            <span className="text-3xl">{service.icon}</span>
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white">
                {service.name}
              </h3>
              {service.port && (
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Port {service.port}
                </p>
              )}
            </div>
          </div>
          <Circle className={clsx('w-3 h-3 fill-current', statusColor)} />
        </div>

        {/* Description */}
        <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
          {service.description}
        </p>

        {/* Metrics */}
        {service.metrics && (
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className={clsx('p-2 rounded', statusBg)}>
              <p className="text-gray-500 dark:text-gray-400">CPU</p>
              <p className="font-semibold text-gray-900 dark:text-white">
                {service.metrics.cpu.toFixed(1)}%
              </p>
            </div>
            <div className={clsx('p-2 rounded', statusBg)}>
              <p className="text-gray-500 dark:text-gray-400">Memory</p>
              <p className="font-semibold text-gray-900 dark:text-white">
                {service.metrics.memory.toFixed(1)}%
              </p>
            </div>
          </div>
        )}

        {/* Action */}
        {service.url && (
          <a
            href={service.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-center space-x-2 w-full px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg transition-colors text-sm font-medium"
          >
            <span>Open</span>
            <ExternalLink className="w-4 h-4" />
          </a>
        )}
      </div>
    </div>
  )
}
