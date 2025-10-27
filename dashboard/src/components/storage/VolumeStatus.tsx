import { HardDrive, Database } from 'lucide-react'

const VOLUMES = [
  { name: 'postgres_data', service: 'PostgreSQL', size: '2.4 GB', usage: 45 },
  { name: 'mariadb_data', service: 'MariaDB', size: '1.8 GB', usage: 32 },
  { name: 'redis_data', service: 'Redis', size: '512 MB', usage: 18 },
  { name: 'minio_data', service: 'MinIO', size: '5.2 GB', usage: 67 },
  { name: 'grafana_data', service: 'Grafana', size: '256 MB', usage: 25 },
  { name: 'prometheus_data', service: 'Prometheus', size: '3.1 GB', usage: 52 },
]

export const VolumeStatus = () => {
  return (
    <section className="card">
      <div className="card-header">
        <div className="flex items-center space-x-3">
          <HardDrive className="w-6 h-6 text-purple-500" />
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">
            Volume Status
          </h2>
        </div>
      </div>
      <div className="card-content">
        <div className="space-y-4">
          {VOLUMES.map((volume) => (
            <div key={volume.name} className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center space-x-2">
                  <Database className="w-4 h-4 text-gray-500" />
                  <span className="font-medium text-gray-900 dark:text-white">
                    {volume.name}
                  </span>
                  <span className="text-gray-500 dark:text-gray-400">
                    ({volume.service})
                  </span>
                </div>
                <span className="text-gray-600 dark:text-gray-400">
                  {volume.size}
                </span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="flex-1 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-purple-500 to-blue-500 transition-all duration-300"
                    style={{ width: `${volume.usage}%` }}
                  />
                </div>
                <span className="text-xs font-medium text-gray-600 dark:text-gray-400 min-w-[3rem] text-right">
                  {volume.usage}%
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
