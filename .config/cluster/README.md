---
date_created: '2025-10-27T02:37:41Z'
last_updated: '2025-10-27T02:37:41Z'
tags: [cluster, configuration, infrastructure]
description: 'Cluster-wide configuration and service inventory'
---

# Cluster Configuration

Central cluster configuration and service inventory.

## 📁 Files

### `cluster.config.yml`
**Master cluster configuration** - Complete infrastructure documentation.

**Contents**:
- 31 services inventory
- 6-network architecture (5-tier + legacy)
- 18 persistent volumes
- Security configuration (secrets, hardening)
- GPU support settings
- Docker Desktop beta features
- BuildKit configuration
- Cluster statistics

**Version**: 3.0.0 (updated 2025-10-27)

---

## 🚀 Quick Reference

### Service Count by Category

- **Security**: 2 (socket-proxy, pre-commit)
- **Frontend**: 1 (loadbalancer)
- **Backend**: 4 (web1/2/3, docker-api)
- **Data**: 3 (postgres, mariadb, redis)
- **Observability**: 8 (prometheus, grafana, alertmanager, exporters)
- **Management**: 5 (buildkit, jupyter, k9s, github-mcp, dashboard)
- **Cloud/Storage**: 2 (minio, localstack)
- **Development**: 3 (mailhog, pgadmin, redis-commander)
- **Documentation**: 1 (mkdocs)

### Network Architecture

1. **cluster-frontend** (172.20.0.0/24) - Public-facing
2. **cluster-backend** (172.20.1.0/24) - Application tier
3. **cluster-data** (172.20.2.0/24) - Database tier (internal-only)
4. **cluster-observability** (172.20.3.0/24) - Monitoring
5. **cluster-management** (172.20.4.0/24) - Management tools
6. **cluster-network** (172.20.5.0/24) - Legacy (migrating)

---

## 📚 Usage

This file serves as:
- Service inventory documentation
- Network architecture reference
- Volume and storage overview
- Security configuration documentation
- Infrastructure planning guide

**Note**: This is a documentation file, not executed by Docker Compose.
