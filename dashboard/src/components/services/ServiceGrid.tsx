import { useState, useEffect } from 'react'
import { Service, LayerMetrics } from '../../types/cluster'
import { ServiceCard } from './ServiceCard'
import { Loader2, ChevronDown, ChevronRight } from 'lucide-react'

interface ServiceGridProps {
  services: Service[]
  layerMetrics?: Record<string, LayerMetrics>
  isLoading: boolean
}

// Phase 4.6.3: Layer color coding and display names
const LAYER_CONFIG: Record<string, { name: string; color: string; bgColor: string }> = {
  infrastructure: {
    name: 'Infrastructure Layer',
    color: 'text-blue-600',
    bgColor: 'bg-blue-50 dark:bg-blue-900/20',
  },
  data: {
    name: 'Data Layer',
    color: 'text-orange-600',
    bgColor: 'bg-orange-50 dark:bg-orange-900/20',
  },
  compute: {
    name: 'Compute Layer',
    color: 'text-purple-600',
    bgColor: 'bg-purple-50 dark:bg-purple-900/20',
  },
  monitoring: {
    name: 'Monitoring Layer',
    color: 'text-red-600',
    bgColor: 'bg-red-50 dark:bg-red-900/20',
  },
  development: {
    name: 'Development Layer',
    color: 'text-green-600',
    bgColor: 'bg-green-50 dark:bg-green-900/20',
  },
}

export const ServiceGrid = ({ services, layerMetrics, isLoading }: ServiceGridProps) => {
  // Phase 4.6.3: Layer collapsed state (persisted to localStorage)
  const [collapsedLayers, setCollapsedLayers] = useState<Record<string, boolean>>(() => {
    const stored = localStorage.getItem('collapsedLayers')
    return stored ? JSON.parse(stored) : {}
  })

  useEffect(() => {
    localStorage.setItem('collapsedLayers', JSON.stringify(collapsedLayers))
  }, [collapsedLayers])

  const toggleLayer = (layer: string) => {
    setCollapsedLayers((prev) => ({ ...prev, [layer]: !prev[layer] }))
  }

  const expandAll = () => setCollapsedLayers({})
  const collapseAll = () => {
    const allLayers = Object.keys(LAYER_CONFIG)
    setCollapsedLayers(Object.fromEntries(allLayers.map((l) => [l, true])))
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-primary-500" />
      </div>
    )
  }

  // Group services by layer
  const servicesByLayer = services.reduce<Record<string, Service[]>>((acc, service) => {
    const layerKey = service.layer ?? 'unassigned'
    const bucket = acc[layerKey] ?? []
    if (!acc[layerKey]) {
      acc[layerKey] = bucket
    }
    bucket.push(service)
    return acc
  }, {})

  return (
    <section className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Services by Layer</h2>
        <div className="flex gap-2">
          <button
            onClick={expandAll}
            className="px-3 py-1 text-sm bg-gray-100 dark:bg-gray-700 rounded hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          >
            Expand All
          </button>
          <button
            onClick={collapseAll}
            className="px-3 py-1 text-sm bg-gray-100 dark:bg-gray-700 rounded hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          >
            Collapse All
          </button>
        </div>
      </div>

      {Object.entries(servicesByLayer).map(([layer, layerServices]) => {
        const isCollapsed = collapsedLayers[layer]
        const config = LAYER_CONFIG[layer] || { name: layer, color: 'text-gray-600', bgColor: 'bg-gray-50' }
        const metrics = layerMetrics?.[layer]

        return (
          <div key={layer} className="space-y-3">
            {/* Phase 4.6.3: Collapsible layer header */}
            <div
              onClick={() => toggleLayer(layer)}
              className={`${config.bgColor} rounded-lg p-4 cursor-pointer hover:shadow-md transition-all`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  {isCollapsed ? (
                    <ChevronRight className="w-5 h-5" />
                  ) : (
                    <ChevronDown className="w-5 h-5" />
                  )}
                  <h3 className={`text-xl font-semibold ${config.color}`}>
                    {config.name}
                  </h3>
                  <span className="text-sm text-gray-500">
                    ({layerServices.length} services)
                  </span>
                </div>
                {/* Phase 4.6.2: Layer metrics display */}
                {metrics && (
                  <div className="flex gap-6 text-sm">
                    <div>
                      <span className="text-gray-500">CPU:</span>{' '}
                      <span className="font-medium">{metrics.avgCpu.toFixed(1)}%</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Memory:</span>{' '}
                      <span className="font-medium">{metrics.avgMemory.toFixed(1)}%</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Health:</span>{' '}
                      <span className="font-medium">
                        {metrics.healthyCount}/{metrics.serviceCount}
                      </span>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Phase 4.6.3: Animated expand/collapse */}
            {!isCollapsed && (
              <div
                className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 animate-in fade-in slide-in-from-top-2 duration-200"
              >
                {layerServices.map((service) => (
                  <ServiceCard key={service.id} service={service} />
                ))}
              </div>
            )}
          </div>
        )
      })}
    </section>
  )
}
