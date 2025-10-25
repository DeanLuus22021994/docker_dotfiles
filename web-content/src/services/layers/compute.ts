import { Service } from '../../types/cluster'

/**
 * Compute Layer Services
 * ML/GPU workloads and AI integration
 * Mirrors docker-compose.yml compute services
 */
export const COMPUTE_SERVICES: Omit<Service, 'status' | 'metrics'>[] = [
  {
    id: 'jupyter',
    name: 'Jupyter Lab',
    category: 'compute',
    url: 'http://localhost:8888',
    port: 8888,
    healthEndpoint: 'http://localhost:8888/api',
    description: 'GPU-accelerated ML notebooks with CUDA 12.2 (cluster-jupyter)',
    icon: '🧪',
  },
  {
    id: 'github-mcp',
    name: 'GitHub MCP',
    category: 'compute',
    description: 'Model Context Protocol server for GitHub integration (cluster-github-mcp)',
    icon: '🐙',
  },
  {
    id: 'k9s',
    name: 'k9s',
    category: 'compute',
    description: 'Kubernetes CLI management UI (cluster-k9s)',
    icon: '☸️',
  },
]
