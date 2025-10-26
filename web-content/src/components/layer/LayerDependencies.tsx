import React, { useRef } from 'react'
import { LayerDependency } from '../../types/cluster'

interface LayerDependenciesProps {
  dependencies?: LayerDependency[]
}

// Default layer dependencies (Phase 4.6.4)
const DEFAULT_DEPENDENCIES: LayerDependency[] = [
  { from: 'network', to: 'services', type: 'requires' },
  { from: 'services', to: 'data', type: 'uses' },
  { from: 'services', to: 'compute', type: 'uses' },
  { from: 'monitoring', to: 'services', type: 'monitors' },
  { from: 'monitoring', to: 'data', type: 'monitors' },
  { from: 'monitoring', to: 'compute', type: 'monitors' },
  { from: 'monitoring', to: 'network', type: 'monitors' },
]

const LAYER_LABELS: Record<string, string> = {
  network: 'Network Layer',
  services: 'Services Layer',
  data: 'Data Layer',
  compute: 'Compute Layer',
  monitoring: 'Monitoring Layer',
}

const LAYER_COLORS: Record<string, string> = {
  network: '#3b82f6', // blue
  services: '#10b981', // green
  data: '#f59e0b', // amber
  compute: '#8b5cf6', // purple
  monitoring: '#ef4444', // red
}

/**
 * Layer Dependencies Visualization Component (Phase 4.6.4)
 * Uses SVG to show dependency tree between layers
 */
export const LayerDependencies: React.FC<LayerDependenciesProps> = ({
  dependencies = DEFAULT_DEPENDENCIES,
}) => {
  const containerRef = useRef<HTMLDivElement>(null)
  const [highlightedPath, setHighlightedPath] = React.useState<string | null>(null)

  // Layer positions (arranged vertically)
  const layerPositions: Record<string, { x: number; y: number }> = {
    network: { x: 250, y: 50 },
    services: { x: 250, y: 150 },
    data: { x: 150, y: 250 },
    compute: { x: 350, y: 250 },
    monitoring: { x: 250, y: 350 },
  }

  const handleLayerHover = (layerId: string | null) => {
    setHighlightedPath(layerId)
  }

  // Get dependencies for a specific layer
  const getLayerDependencies = (layerId: string): LayerDependency[] => {
    return dependencies.filter(d => d.from === layerId || d.to === layerId)
  }

  return (
    <div ref={containerRef} className="bg-white dark:bg-gray-900 rounded-lg p-6">
      <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
        Layer Dependencies
      </h3>

      <svg
        width="500"
        height="400"
        viewBox="0 0 500 400"
        className="mx-auto"
      >
        {/* Draw dependency arrows */}
        {dependencies.map((dep, index) => {
          const from = layerPositions[dep.from]
          const to = layerPositions[dep.to]
          
          if (!from || !to) return null

          const isHighlighted = 
            highlightedPath === dep.from || 
            highlightedPath === dep.to

          const arrowColor = 
            dep.type === 'requires' ? '#3b82f6' :
            dep.type === 'uses' ? '#10b981' :
            '#ef4444'

          const opacity = highlightedPath === null || isHighlighted ? 1 : 0.2

          return (
            <g key={index}>
              {/* Arrow line */}
              <line
                x1={from.x}
                y1={from.y + 30}
                x2={to.x}
                y2={to.y - 30}
                stroke={arrowColor}
                strokeWidth={isHighlighted ? 3 : 2}
                strokeOpacity={opacity}
                markerEnd={`url(#arrowhead-${dep.type})`}
              />
            </g>
          )
        })}

        {/* Arrowhead markers */}
        <defs>
          <marker
            id="arrowhead-requires"
            markerWidth="10"
            markerHeight="10"
            refX="5"
            refY="5"
            orient="auto"
          >
            <polygon points="0,0 10,5 0,10" fill="#3b82f6" />
          </marker>
          <marker
            id="arrowhead-uses"
            markerWidth="10"
            markerHeight="10"
            refX="5"
            refY="5"
            orient="auto"
          >
            <polygon points="0,0 10,5 0,10" fill="#10b981" />
          </marker>
          <marker
            id="arrowhead-monitors"
            markerWidth="10"
            markerHeight="10"
            refX="5"
            refY="5"
            orient="auto"
          >
            <polygon points="0,0 10,5 0,10" fill="#ef4444" />
          </marker>
        </defs>

        {/* Draw layer nodes */}
        {Object.entries(layerPositions).map(([layerId, pos]) => {
          const isHighlighted = highlightedPath === layerId
          const opacity = highlightedPath === null || isHighlighted ? 1 : 0.3

          return (
            <g
              key={layerId}
              onMouseEnter={() => handleLayerHover(layerId)}
              onMouseLeave={() => handleLayerHover(null)}
              style={{ cursor: 'pointer' }}
            >
              {/* Circle */}
              <circle
                cx={pos.x}
                cy={pos.y}
                r={30}
                fill={LAYER_COLORS[layerId]}
                fillOpacity={opacity}
                stroke="#fff"
                strokeWidth={2}
              />
              
              {/* Label */}
              <text
                x={pos.x}
                y={pos.y + 5}
                textAnchor="middle"
                fontSize="12"
                fontWeight="bold"
                fill="#fff"
              >
                {layerId.toUpperCase()}
              </text>
            </g>
          )
        })}
      </svg>

      {/* Legend */}
      <div className="mt-6 space-y-2">
        <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">
          Dependency Types:
        </h4>
        <div className="flex flex-wrap gap-4 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-4 h-1 bg-blue-500"></div>
            <span className="text-gray-600 dark:text-gray-400">Requires</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-1 bg-green-500"></div>
            <span className="text-gray-600 dark:text-gray-400">Uses</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-1 bg-red-500"></div>
            <span className="text-gray-600 dark:text-gray-400">Monitors</span>
          </div>
        </div>
      </div>

      {/* Hover info */}
      {highlightedPath && (
        <div className="mt-4 p-3 bg-gray-100 dark:bg-gray-800 rounded">
          <h4 className="font-medium text-gray-900 dark:text-white mb-2">
            {LAYER_LABELS[highlightedPath]}
          </h4>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            <p className="mb-1">
              <strong>Dependencies:</strong>{' '}
              {getLayerDependencies(highlightedPath).length} connections
            </p>
            <ul className="list-disc list-inside space-y-1">
              {getLayerDependencies(highlightedPath).map((dep, i) => (
                <li key={i}>
                  {dep.from === highlightedPath
                    ? `${dep.type} ${LAYER_LABELS[dep.to]}`
                    : `Required by ${LAYER_LABELS[dep.from]}`}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}
