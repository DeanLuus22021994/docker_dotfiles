import { Network, ArrowRight, Circle } from 'lucide-react'
import clsx from 'clsx'

const CONNECTIONS = [
  { from: 'Load Balancer', to: 'Web Server 1', port: 80, status: 'active' as const },
  { from: 'Load Balancer', to: 'Web Server 2', port: 80, status: 'active' as const },
  { from: 'Load Balancer', to: 'Web Server 3', port: 80, status: 'active' as const },
  { from: 'Web Servers', to: 'PostgreSQL', port: 5432, status: 'active' as const },
  { from: 'Web Servers', to: 'MariaDB', port: 3306, status: 'active' as const },
  { from: 'Web Servers', to: 'Redis', port: 6379, status: 'active' as const },
  { from: 'Web Servers', to: 'MinIO', port: 9000, status: 'active' as const },
  { from: 'Prometheus', to: 'All Services', port: 9090, status: 'active' as const },
]

export const NetworkTopology = () => {
  return (
    <section className="card">
      <div className="card-header">
        <div className="flex items-center space-x-3">
          <Network className="w-6 h-6 text-blue-500" />
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">
            Network Topology
          </h2>
        </div>
      </div>
      <div className="card-content">
        <div className="space-y-3">
          {CONNECTIONS.map((conn, idx) => (
            <div
              key={idx}
              className="flex items-center space-x-3 p-3 rounded-lg bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            >
              <Circle
                className={clsx(
                  'w-2 h-2 fill-current',
                  conn.status === 'active' ? 'text-green-500' : 'text-gray-400'
                )}
              />
              <div className="flex-1 flex items-center justify-between text-sm">
                <span className="font-medium text-gray-900 dark:text-white">
                  {conn.from}
                </span>
                <ArrowRight className="w-4 h-4 text-gray-400 mx-2" />
                <span className="font-medium text-gray-900 dark:text-white">
                  {conn.to}
                </span>
              </div>
              <span className="text-xs px-2 py-1 rounded bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 font-mono">
                :{conn.port}
              </span>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
