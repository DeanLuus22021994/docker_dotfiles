import { Service } from '../../types/cluster'

/**
 * Data Layer Services
 * Databases, cache, and object storage
 * Mirrors docker-compose.yml data persistence services
 */
export const DATA_SERVICES: Omit<Service, 'status' | 'metrics'>[] = [
  // Databases
  {
    id: 'postgres',
    name: 'PostgreSQL',
    category: 'database',
    port: 5432,
    healthEndpoint: 'http://localhost:5432',
    description: 'PostgreSQL 13 relational database (cluster-postgres)',
    icon: '🐘',
  },
  {
    id: 'mariadb',
    name: 'MariaDB',
    category: 'database',
    port: 3306,
    healthEndpoint: 'http://localhost:3306',
    description: 'MariaDB 11 MySQL-compatible database (cluster-mariadb)',
    icon: '🐬',
  },
  
  // Cache
  {
    id: 'redis',
    name: 'Redis',
    category: 'cache',
    port: 6379,
    healthEndpoint: 'http://localhost:6379',
    description: 'Redis 7 in-memory cache with persistence (cluster-redis)',
    icon: '⚡',
  },
  
  // Object Storage
  {
    id: 'minio',
    name: 'MinIO',
    category: 'storage',
    url: 'http://localhost:9001',
    port: 9000,
    healthEndpoint: 'http://localhost:9000/minio/health/live',
    description: 'S3-compatible object storage (cluster-minio)',
    icon: '🪣',
  },
]
