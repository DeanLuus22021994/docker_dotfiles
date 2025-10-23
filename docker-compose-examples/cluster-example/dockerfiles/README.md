---
started: 2025-10-22
completed: 2025-10-22
author: AI Assistant
version: 1.0
status: active
description: Load-balanced cluster configuration with multiple nginx web servers
tags: [docker, compose, cluster, load-balancer, nginx]
---

# [`CLUSTER-EXAMPLE-001`](#cluster-example-001) Cluster Example

## [`UAT-2025-10-22T21:33:19Z`](#uat-2025-10-22t21-33-19z) User Acceptance Testing - 2025-10-22T21:33:19Z ✅ PASSED

### Test Results Summary

- **Configuration**: ✅ PASSED - Docker Compose validated
- **Services**: ✅ PASSED - Load balancer + 6 services healthy
- **Load Balancing**: ✅ PASSED - Nginx distributing traffic
- **Health Checks**: ✅ PASSED - All services monitored

### Service Status

| Service | Status | Health | Ports |
|---------|--------|--------|-------|
| **loadbalancer** | ✅ Running | Healthy | 8080 |
| **web1-3** | ✅ Running | Healthy | 80 |
| **node** | ✅ Running | Healthy | 3000 |
| **python** | ✅ Running | Healthy | 8000 |
| **db** | ✅ Running | Healthy | 5432 |

### Architecture

```
Internet → Load Balancer (nginx:8080)
                     ↓
          ┌─────────┼─────────┐
          │         │         │
        Web1      Web2      Web3
       (nginx)   (nginx)   (nginx)
                     ↓
                Shared Services
            ┌─────────┼─────────┐
            │         │         │
          Node     Python      DB
        (React)  (FastAPI)  (PostgreSQL)
```

<a id="fr-cluster-example-001-functional-requirements"></a>

## [`FR-CLUSTER-EXAMPLE-001`](#fr-cluster-example-001-functional-requirements) Functional Requirements

- Nginx load balancer with upstream routing
- Multiple web server replicas
- Service health monitoring
- Round-robin load distribution

### [`FR-CLUSTER-EXAMPLE-001`] Validation Criteria

```bash
docker-compose config
curl -f http://localhost:8080/
```

<a id="uac-cluster-example-001-user-acceptance-criteria"></a>

## [`UAC-CLUSTER-EXAMPLE-001`](#uac-cluster-example-001-user-acceptance-criteria) User Acceptance Criteria

- Load balancer distributes requests
- All web servers respond
- Services remain healthy under load
- No service failures

### [`UAC-CLUSTER-EXAMPLE-001`] Validation Criteria

```bash
docker-compose up -d
curl http://localhost:8080/ | grep -c "web" | grep -q "3"
```

<a id="blk-cluster-example-001-blockers"></a>

## [`BLK-CLUSTER-EXAMPLE-001`](#blk-cluster-example-001-blockers) Blockers

- Port 8080 conflicts
- Insufficient memory for replicas
- Network connectivity issues

### [`BLK-CLUSTER-EXAMPLE-001`] Validation Criteria

```bash
lsof -i :8080 || echo "Port available"
docker system df
```

<a id="lnk-cluster-example-001-links"></a>

## [`LNK-CLUSTER-EXAMPLE-001`](#lnk-cluster-example-001-links) Links

- [Testing Protocol](../../TESTING.md)
- [Main README](../../README.md)
- [Changelog](../../CHANGELOG.md)
- [MCP Utilities](../../mcp/README.md)
