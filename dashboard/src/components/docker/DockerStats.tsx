import { useDockerStats } from '../../hooks/useDockerStats'
import { Container, Image, HardDrive, Network, Cpu, MemoryStick, Database } from 'lucide-react'

export const DockerStats = () => {
  const { stats, isLoading } = useDockerStats()

  if (isLoading) {
    return null
  }

  const statCards = [
    {
      icon: Container,
      label: 'Running Containers',
      value: stats.containersRunning,
      total: stats.containersRunning + stats.containersStopped,
      color: 'text-green-500',
      bgColor: 'bg-green-100 dark:bg-green-900/30',
    },
    {
      icon: Image,
      label: 'Docker Images',
      value: stats.imagesCount,
      color: 'text-blue-500',
      bgColor: 'bg-blue-100 dark:bg-blue-900/30',
    },
    {
      icon: Database,
      label: 'Volumes',
      value: stats.volumesCount,
      color: 'text-purple-500',
      bgColor: 'bg-purple-100 dark:bg-purple-900/30',
    },
    {
      icon: Network,
      label: 'Networks',
      value: stats.networksCount,
      color: 'text-cyan-500',
      bgColor: 'bg-cyan-100 dark:bg-cyan-900/30',
    },
  ]

  const resourceCards = [
    {
      icon: Cpu,
      label: 'CPU Usage',
      value: `${stats.cpuUsage.toFixed(1)}%`,
      progress: stats.cpuUsage,
      color: 'text-orange-500',
      progressColor: 'from-orange-500 to-red-500',
    },
    {
      icon: MemoryStick,
      label: 'Memory Usage',
      value: `${stats.memoryUsage.toFixed(1)}%`,
      progress: stats.memoryUsage,
      color: 'text-blue-500',
      progressColor: 'from-blue-500 to-purple-500',
    },
    {
      icon: HardDrive,
      label: 'Disk Usage',
      value: `${stats.diskUsage.toFixed(1)}%`,
      progress: stats.diskUsage,
      color: 'text-green-500',
      progressColor: 'from-green-500 to-teal-500',
    },
  ]

  return (
    <section className="space-y-4">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
        Docker Infrastructure
      </h2>

      {/* Container Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((stat) => {
          const Icon = stat.icon
          return (
            <div key={stat.label} className="card">
              <div className="card-content">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {stat.label}
                    </p>
                    <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">
                      {stat.value}
                      {stat.total && (
                        <span className="text-lg text-gray-500 dark:text-gray-400">
                          /{stat.total}
                        </span>
                      )}
                    </p>
                  </div>
                  <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                    <Icon className={`w-6 h-6 ${stat.color}`} />
                  </div>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Resource Usage */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {resourceCards.map((resource) => {
          const Icon = resource.icon
          return (
            <div key={resource.label} className="card">
              <div className="card-content space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <Icon className={`w-5 h-5 ${resource.color}`} />
                    <span className="text-sm font-medium text-gray-900 dark:text-white">
                      {resource.label}
                    </span>
                  </div>
                  <span className="text-lg font-bold text-gray-900 dark:text-white">
                    {resource.value}
                  </span>
                </div>
                <div className="relative h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                  <div
                    className={`absolute top-0 left-0 h-full bg-gradient-to-r ${resource.progressColor} transition-all duration-500`}
                    style={{ width: `${resource.progress}%` }}
                  />
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </section>
  )
}
