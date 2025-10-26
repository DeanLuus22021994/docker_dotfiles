import React, { useState, useEffect } from 'react'
import { Service } from '../../types/cluster'

interface LayerGroupProps {
  layerId: string
  layerName: string
  services: Service[]
  children: React.ReactNode
}

/**
 * Chevron icon components (simple SVG)
 */
const ChevronDownIcon: React.FC<{ className?: string }> = ({ className }) => (
  <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
  </svg>
)

const ChevronUpIcon: React.FC<{ className?: string }> = ({ className }) => (
  <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
  </svg>
)

/**
 * Collapsible Layer Group Component (Phase 4.6.3)
 * Allows expanding/collapsing layer sections with persistent state
 */
export const LayerGroup: React.FC<LayerGroupProps> = ({
  layerId,
  layerName,
  services,
  children,
}) => {
  const [isExpanded, setIsExpanded] = useState<boolean>(() => {
    // Load collapsed state from localStorage
    const saved = localStorage.getItem(`layer-${layerId}-expanded`)
    return saved !== null ? saved === 'true' : true // Default to expanded
  })

  useEffect(() => {
    // Save collapsed state to localStorage
    localStorage.setItem(`layer-${layerId}-expanded`, isExpanded.toString())
  }, [layerId, isExpanded])

  const toggleExpanded = () => {
    setIsExpanded(!isExpanded)
  }

  const healthyCount = services.filter(s => s.status === 'healthy').length
  const totalCount = services.length
  const healthPercentage = totalCount > 0 ? (healthyCount / totalCount) * 100 : 0

  const healthColor =
    healthPercentage === 100 ? 'text-green-600 dark:text-green-400' :
    healthPercentage >= 70 ? 'text-yellow-600 dark:text-yellow-400' :
    'text-red-600 dark:text-red-400'

  return (
    <div className="mb-6 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
      {/* Header - Clickable to expand/collapse */}
      <button
        onClick={toggleExpanded}
        className="w-full flex items-center justify-between p-4 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
      >
        <div className="flex items-center gap-3">
          {/* Chevron icon */}
          {isExpanded ? (
            <ChevronUpIcon className="w-5 h-5 text-gray-600 dark:text-gray-400" />
          ) : (
            <ChevronDownIcon className="w-5 h-5 text-gray-600 dark:text-gray-400" />
          )}

          {/* Layer name */}
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            {layerName}
          </h3>

          {/* Service count badge */}
          <span className="px-2 py-1 text-xs font-medium bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded">
            {totalCount} {totalCount === 1 ? 'service' : 'services'}
          </span>
        </div>

        {/* Health indicator */}
        <div className={`text-sm font-medium ${healthColor}`}>
          {healthyCount}/{totalCount} healthy
        </div>
      </button>

      {/* Content - With smooth animation */}
      <div
        className={`transition-all duration-300 ease-in-out overflow-hidden ${
          isExpanded ? 'max-h-[10000px] opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        <div className="p-4 bg-white dark:bg-gray-900">
          {children}
        </div>
      </div>
    </div>
  )
}

interface LayerGroupContainerProps {
  children: React.ReactNode
}

/**
 * Container for multiple layer groups with expand/collapse all controls
 */
export const LayerGroupContainer: React.FC<LayerGroupContainerProps> = ({ children }) => {
  const handleExpandAll = () => {
    // Find all layer groups and expand them
    const layerIds = ['data', 'services', 'monitoring', 'compute', 'network']
    layerIds.forEach(id => {
      localStorage.setItem(`layer-${id}-expanded`, 'true')
    })
    // Force re-render by dispatching a custom event
    window.dispatchEvent(new Event('layerExpansionChanged'))
  }

  const handleCollapseAll = () => {
    // Find all layer groups and collapse them
    const layerIds = ['data', 'services', 'monitoring', 'compute', 'network']
    layerIds.forEach(id => {
      localStorage.setItem(`layer-${id}-expanded`, 'false')
    })
    // Force re-render by dispatching a custom event
    window.dispatchEvent(new Event('layerExpansionChanged'))
  }

  return (
    <div>
      {/* Controls */}
      <div className="flex gap-2 mb-4">
        <button
          onClick={handleExpandAll}
          className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          Expand All
        </button>
        <button
          onClick={handleCollapseAll}
          className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          Collapse All
        </button>
      </div>

      {/* Layer groups */}
      {children}
    </div>
  )
}
