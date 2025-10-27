import React, { useState } from 'react'
import { Service } from '../../types/cluster'
import { dockerAPI } from '../../services/dockerAPI'

interface ServiceScaleControlsProps {
  service: Service
  onScaled?: (replicas: number) => void
}

/**
 * Service Scaling Controls Component (Phase 4.6.5)
 * Adds +/- buttons to scale service replicas
 * Requires authentication (AUTH_ENABLED=true)
 */
export const ServiceScaleControls: React.FC<ServiceScaleControlsProps> = ({
  service,
  onScaled,
}) => {
  const [replicas, setReplicas] = useState(service.replicas || 1)
  const [isScaling, setIsScaling] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Services that don't support scaling (singletons)
  const NON_SCALABLE_SERVICES = [
    'postgres',
    'mariadb',
    'redis',
    'grafana',
    'prometheus',
    'nginx',
    'traefik',
  ]

  const isScalable = !NON_SCALABLE_SERVICES.includes(service.name.toLowerCase())
  const minReplicas = 1
  const maxReplicas = 10

  const handleScale = async (newReplicas: number) => {
    if (newReplicas < minReplicas || newReplicas > maxReplicas) {
      return
    }

    setIsScaling(true)
    setError(null)

    try {
      await dockerAPI.scaleService(service.id, newReplicas)
      setReplicas(newReplicas)
      onScaled?.(newReplicas)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to scale service')
      console.error('Scale error:', err)
    } finally {
      setIsScaling(false)
    }
  }

  const handleIncrement = () => {
    if (replicas < maxReplicas) {
      handleScale(replicas + 1)
    }
  }

  const handleDecrement = () => {
    if (replicas > minReplicas) {
      handleScale(replicas - 1)
    }
  }

  if (!isScalable) {
    return (
      <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
        <span className="px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded">
          1 replica
        </span>
        <span className="text-xs">(not scalable)</span>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-2">
      {/* Scale controls */}
      <div className="flex items-center gap-2">
        <button
          onClick={handleDecrement}
          disabled={isScaling || replicas <= minReplicas}
          className="w-8 h-8 flex items-center justify-center rounded bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 hover:bg-red-200 dark:hover:bg-red-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          title="Decrease replicas"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 12H4" />
          </svg>
        </button>

        <div className="flex flex-col items-center min-w-[60px]">
          <span className="text-lg font-semibold text-gray-900 dark:text-white">
            {replicas}
          </span>
          <span className="text-xs text-gray-500 dark:text-gray-400">
            {replicas === 1 ? 'replica' : 'replicas'}
          </span>
        </div>

        <button
          onClick={handleIncrement}
          disabled={isScaling || replicas >= maxReplicas}
          className="w-8 h-8 flex items-center justify-center rounded bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 hover:bg-green-200 dark:hover:bg-green-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          title="Increase replicas"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
        </button>
      </div>

      {/* Status */}
      {isScaling && (
        <div className="text-xs text-blue-600 dark:text-blue-400 text-center">
          Scaling...
        </div>
      )}

      {/* Error message */}
      {error && (
        <div className="text-xs text-red-600 dark:text-red-400 text-center">
          {error}
        </div>
      )}

      {/* Limits info */}
      <div className="text-xs text-gray-500 dark:text-gray-400 text-center">
        Limits: {minReplicas}-{maxReplicas}
      </div>
    </div>
  )
}

/**
 * Confirmation Dialog for Scaling Operations
 */
interface ScaleConfirmDialogProps {
  isOpen: boolean
  serviceName: string
  currentReplicas: number
  newReplicas: number
  onConfirm: () => void
  onCancel: () => void
}

export const ScaleConfirmDialog: React.FC<ScaleConfirmDialogProps> = ({
  isOpen,
  serviceName,
  currentReplicas,
  newReplicas,
  onConfirm,
  onCancel,
}) => {
  if (!isOpen) return null

  const isScalingUp = newReplicas > currentReplicas

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white dark:bg-gray-900 rounded-lg p-6 max-w-md w-full shadow-xl">
        <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
          Confirm Service Scaling
        </h3>

        <p className="text-gray-700 dark:text-gray-300 mb-4">
          {isScalingUp ? 'Scale up' : 'Scale down'} <strong>{serviceName}</strong> from{' '}
          <strong>{currentReplicas}</strong> to <strong>{newReplicas}</strong> replicas?
        </p>

        {isScalingUp && (
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
            ⚠️ Scaling up will create additional containers and consume more resources.
          </p>
        )}

        {!isScalingUp && (
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
            ⚠️ Scaling down will remove containers. Ensure no active connections will be lost.
          </p>
        )}

        <div className="flex gap-3 justify-end">
          <button
            onClick={onCancel}
            className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-200 dark:bg-gray-800 rounded hover:bg-gray-300 dark:hover:bg-gray-700 transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            className={`px-4 py-2 text-sm font-medium text-white rounded transition-colors ${
              isScalingUp
                ? 'bg-green-600 hover:bg-green-700'
                : 'bg-red-600 hover:bg-red-700'
            }`}
          >
            Confirm
          </button>
        </div>
      </div>
    </div>
  )
}
