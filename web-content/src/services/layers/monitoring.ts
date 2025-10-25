import { Service } from '../../types/cluster'

/**
 * Monitoring Layer Services
 * Observability, metrics, and dashboards
 * Mirrors docker-compose.yml monitoring services
 */
export const MONITORING_SERVICES: Omit<Service, 'status' | 'metrics'>[] = [
  {
    id: 'grafana',
    name: 'Grafana',
    category: 'monitoring',
    url: 'http://localhost:3002',
    port: 3002,
    healthEndpoint: 'http://localhost:3002/api/health',
    description: 'Monitoring dashboards and visualization (cluster-grafana)',
    icon: '📊',
  },
  {
    id: 'prometheus',
    name: 'Prometheus',
    category: 'monitoring',
    url: 'http://localhost:9090',
    port: 9090,
    healthEndpoint: 'http://localhost:9090/-/healthy',
    description: 'Metrics collection and alerting (cluster-prometheus)',
    icon: '📈',
  },
]
