import { Service } from '../../types/cluster'

/**
 * Development Layer Services
 * Developer tools, database admin, and testing utilities
 * Mirrors docker-compose.yml development services
 */
export const DEVELOPMENT_SERVICES: Omit<Service, 'status' | 'metrics'>[] = [
  {
    id: 'buildkit',
    name: 'BuildKit',
    category: 'development',
    port: 1234,
    description: 'Docker build engine with cache optimization (cluster-buildkit)',
    icon: '🔨',
  },
  {
    id: 'localstack',
    name: 'LocalStack',
    category: 'development',
    url: 'http://localhost:4566',
    port: 4566,
    healthEndpoint: 'http://localhost:4566/_localstack/health',
    description: 'Local AWS cloud emulation (cluster-localstack)',
    icon: '☁️',
  },
  {
    id: 'mailhog',
    name: 'MailHog',
    category: 'development',
    url: 'http://localhost:8025',
    port: 8025,
    healthEndpoint: 'http://localhost:8025',
    description: 'Email testing and capture (cluster-mailhog)',
    icon: '📧',
  },
  {
    id: 'pgadmin',
    name: 'pgAdmin',
    category: 'development',
    url: 'http://localhost:5050',
    port: 5050,
    healthEndpoint: 'http://localhost:5050/misc/ping',
    description: 'Database administration tool (cluster-pgadmin)',
    icon: '🗄️',
  },
  {
    id: 'redis-commander',
    name: 'Redis Commander',
    category: 'development',
    url: 'http://localhost:8081',
    port: 8081,
    healthEndpoint: 'http://localhost:8081',
    description: 'Redis data browser and management (cluster-redis-commander)',
    icon: '🎮',
  },
]
