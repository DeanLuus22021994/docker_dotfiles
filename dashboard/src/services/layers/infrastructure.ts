import { Service } from '../../types/cluster'

/**
 * Infrastructure Layer Services
 * Load balancing and web server fleet
 * Mirrors docker-compose.yml infrastructure services
 */
export const INFRASTRUCTURE_SERVICES: Omit<Service, 'status' | 'metrics'>[] = [
  {
    id: 'loadbalancer',
    name: 'Load Balancer',
    category: 'load-balancer',
    layer: 'infrastructure',
    url: 'http://localhost:8080',
    port: 8080,
    healthEndpoint: 'http://localhost:8080/health',
    description: 'Nginx load balancer distributing traffic across 3 web servers',
    icon: '🔀',
  },
  {
    id: 'web1',
    name: 'Web Server 1',
    category: 'web',
    layer: 'infrastructure',
    description: 'Nginx web server instance 1 (cluster-web1)',
    icon: '🌐',
  },
  {
    id: 'web2',
    name: 'Web Server 2',
    category: 'web',
    layer: 'infrastructure',
    description: 'Nginx web server instance 2 (cluster-web2)',
    icon: '🌐',
  },
  {
    id: 'web3',
    name: 'Web Server 3',
    category: 'web',
    layer: 'infrastructure',
    description: 'Nginx web server instance 3 (cluster-web3)',
    icon: '🌐',
  },
]
