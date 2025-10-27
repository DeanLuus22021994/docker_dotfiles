# Docker Cluster Status Report
**Generated:** 2025-10-27 02:03:25
**Total Containers Running:** 29

## Container Overview by Category

### 🗄️ Database Services (3 containers)
| Container | Memory Used | Memory Limit | CPU % | Volume Size | Purpose |
|-----------|-------------|--------------|-------|-------------|---------|
| cluster-postgres | 18.37 MiB | 4 GiB | 4.87% | 49.62 MB | PostgreSQL relational database |
| cluster-redis | 8.47 MiB | 2 GiB | 4.12% | 264 B | Redis in-memory cache/database |
| cluster-mariadb | 300.8 MiB | 4 GiB | 3.86% | 152.7 MB data, 3.4 KB logs | MariaDB relational database |

### 📊 Monitoring & Observability (8 containers)
| Container | Memory Used | Memory Limit | CPU % | Volume Size | Purpose |
|-----------|-------------|--------------|-------|-------------|---------|
| cluster-prometheus | 57.87 MiB | 2 GiB | 2.35% | 99.53 MB | Metrics collection & alerting |
| cluster-grafana | 93.4 MiB | 1 GiB | 0.23% | 40.69 MB | Metrics visualization dashboards |
| cluster-alertmanager | 17.5 MiB | 256 MiB | 3.85% | 578 B | Alert routing & management |
| cluster-cadvisor | 43.72 MiB | 512 MiB | 0.87% | N/A | Container resource monitoring |
| cluster-node-exporter | 15.7 MiB | 128 MiB | 0.00% | N/A | Host metrics exporter |
| cluster-postgres-exporter | 9.53 MiB | 256 MiB | 0.00% | N/A | PostgreSQL metrics exporter |
| cluster-redis-exporter | 14.01 MiB | 256 MiB | 0.00% | N/A | Redis metrics exporter |
| cluster-redis-commander | 17.86 MiB | 256 MiB | 0.13% | N/A | Redis web UI |

### 🌐 Web & Load Balancing (4 containers)
| Container | Memory Used | Memory Limit | CPU % | Volume Size | Purpose |
|-----------|-------------|--------------|-------|-------------|---------|
| cluster-loadbalancer | 2.58 MiB | 256 MiB | 0.00% | N/A | NGINX load balancer (frontend) |
| cluster-web1 | 13.29 MiB | 128 MiB | 0.00% | N/A | Backend web server 1 |
| cluster-web2 | 13.38 MiB | 128 MiB | 3.63% | N/A | Backend web server 2 |
| cluster-web3 | 13.36 MiB | 128 MiB | 0.00% | N/A | Backend web server 3 |

### 🛠️ Development & DevOps (6 containers)
| Container | Memory Used | Memory Limit | CPU % | Volume Size | Purpose |
|-----------|-------------|--------------|-------|-------------|---------|
| cluster-devcontainer | 384 KiB | 4 GiB | 0.00% | N/A | VS Code dev environment |
| cluster-buildkit | 8.81 MiB | 4 GiB | 0.00% | 114.7 KB | Docker BuildKit daemon |
| cluster-pre-commit | 490.9 MiB | 512 MiB | 98.07% | 608.4 MB | Git pre-commit hooks (active) |
| cluster-k9s | 488 KiB | 512 MiB | 0.00% | 0 B | Kubernetes CLI management |
| cluster-jupyter | 73.47 MiB | 8 GiB | 3.81% | 0 B | Jupyter notebook environment |
| cluster-pgadmin | 211 MiB | 512 MiB | 0.03% | 176.1 KB | PostgreSQL admin interface |

### 🔐 Security & Infrastructure (3 containers)
| Container | Memory Used | Memory Limit | CPU % | Volume Size | Purpose |
|-----------|-------------|--------------|-------|-------------|---------|
| cluster-docker-socket-proxy | 15.45 MiB | 128 MiB | 0.00% | N/A | Secure Docker API proxy (READ-ONLY) |
| cluster-docker-api | 27.78 MiB | 512 MiB | 0.02% | N/A | Docker API service |
| cluster-dashboard | 13.31 MiB | 256 MiB | 0.00% | N/A | Cluster dashboard UI |

### ☁️ Cloud Services & Storage (3 containers)
| Container | Memory Used | Memory Limit | CPU % | Volume Size | Purpose |
|-----------|-------------|--------------|-------|-------------|---------|
| cluster-localstack | 89.05 MiB | 2 GiB | 0.04% | 21.04 KB | AWS service emulation |
| cluster-minio | 87.84 MiB | 2 GiB | 0.00% | 18.51 KB | S3-compatible object storage |
| cluster-mailhog | 4.62 MiB | 256 MiB | 4.52% | N/A | Email testing service |

### 🤖 AI & Integration (2 containers)
| Container | Memory Used | Memory Limit | CPU % | Volume Size | Purpose |
|-----------|-------------|--------------|-------|-------------|---------|
| cluster-github-mcp | 12.07 MiB | 512 MiB | 0.98% | 0 B | GitHub Model Context Protocol |
| cluster-gpu-node | 17.06 MiB | 512 MiB | 0.00% | N/A | GPU resource node |

## Network Segmentation Architecture

### 🌐 cluster-frontend (172.20.0.0/24)
- **Purpose:** Public-facing services
- **Services:** cluster-loadbalancer, cluster-dashboard

### 🔧 cluster-backend (172.20.1.0/24)
- **Purpose:** Application services
- **Services:** cluster-web1, cluster-web2, cluster-web3, cluster-loadbalancer (bridge)

### 🗄️ cluster-data (172.20.2.0/24) - INTERNAL ONLY
- **Purpose:** Database and cache services (no external access)
- **Services:** cluster-postgres, cluster-redis, cluster-mariadb

### 📊 cluster-observability (172.20.3.0/24)
- **Purpose:** Monitoring and logging
- **Services:** cluster-prometheus, cluster-grafana, cluster-alertmanager

### 🛠️ cluster-management (172.20.4.0/24)
- **Purpose:** DevOps tools
- **Services:** cluster-buildkit, cluster-pre-commit, cluster-docker-socket-proxy

### 🔄 cluster-network (legacy)
- **Purpose:** Backward compatibility
- **Status:** Being phased out

## Security Hardening Applied

✅ **Network Segmentation:** 5-tier isolation with internal-only data network
✅ **Docker Socket Protection:** READ-ONLY proxy with least-privilege API access
✅ **Secrets Management:** 6 credentials migrated to Docker secrets
✅ **Security Options:** no-new-privileges applied to 5 services
✅ **Read-only Filesystems:** Applied to loadbalancer and dashboard with tmpfs
✅ **Web Service Isolation:** Backend services on isolated network segment

## Volume Storage Summary

**Total Persistent Storage:** ~1.2 GB

### Largest Volumes:
- pre-commit-cache: 608.4 MB (hook environments)
- mariadb_data: 152.7 MB
- prometheus_data: 99.53 MB
- postgres_data: 49.62 MB
- grafana_data: 40.69 MB
- mkdocs_site: 6.99 MB

### Active Secrets (File-based):
- postgres_user, postgres_password
- redis_password
- mariadb_root_password, mariadb_password, mariadb_user

## Resource Utilization

**High Activity:**
- cluster-pre-commit: 98.07% CPU (actively running hooks)
- cluster-mailhog: 4.52% CPU
- cluster-postgres: 4.87% CPU
- cluster-redis: 4.12% CPU
- cluster-mariadb: 3.86% CPU
- cluster-alertmanager: 3.85% CPU
- cluster-jupyter: 3.81% CPU
- cluster-web2: 3.63% CPU

**Memory Pressure:**
- cluster-pre-commit: 95.87% (490.9 MiB / 512 MiB)
- cluster-pgadmin: 41.21% (211 MiB / 512 MiB)
- cluster-node-exporter: 12.26% (15.7 MiB / 128 MiB)
- cluster-docker-socket-proxy: 12.07% (15.45 MiB / 128 MiB)
- cluster-web1/2/3: ~10.4% each (13 MiB / 128 MiB)

## Notes

- Pre-commit container is actively running hook installations (first-time setup)
- All health checks passing for critical services
- Network segmentation provides defense-in-depth security
- Docker socket access controlled through secure proxy
- Database services using persistent volumes for data durability
- Monitoring stack (Prometheus/Grafana) fully operational with 99.53 MB of metrics data
