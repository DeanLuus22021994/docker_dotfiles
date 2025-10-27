---
date_created: '2025-10-27T02:37:39Z'
last_updated: '2025-10-27T02:37:39Z'
tags: [testing, validation, e2e, configuration]
description: 'Test suite configuration for cluster validation'
---

# Testing Configuration

End-to-end test suite for cluster infrastructure validation.

## 📁 Files

### `test-suite.yml`
**Comprehensive test definitions** for all cluster components.

**Test Categories**:

1. **Infrastructure Tests**
   - Docker Compose validation
   - Network existence checks

2. **Service Health Tests** (11 services)
   - Load Balancer (HTTP)
   - PostgreSQL (pg_isready)
   - MariaDB (mariadb-admin ping)
   - Redis (redis-cli ping)
   - Jupyter Lab (HTTP API)
   - MinIO (HTTP health)
   - Grafana (HTTP API)
   - Prometheus (HTTP health)

3. **Connectivity Tests**
   - Web → PostgreSQL (TCP 5432)
   - Web → Redis (TCP 6379)
   - Web → MariaDB (TCP 3306)

4. **DevContainer Tests**
   - Container running check
   - Network access validation
   - Database connectivity

5. **Performance Tests**
   - Load balancer response time (<500ms)
   - Database query performance

---

## 🚀 Quick Start

### Run All Tests

```powershell
# TODO: Implement test runner script
# For now, run tests manually:

# Infrastructure
docker-compose config --quiet

# Service health
curl http://localhost:8080
docker exec cluster-postgres pg_isready -U cluster_user
docker exec cluster-redis redis-cli ping

# Connectivity
docker exec cluster-web1 nc -zv cluster-postgres 5432
```

---

## 🎯 Best Practices

✅ **Run tests before deployment** - Catch issues early  
✅ **Monitor test execution time** - Detect performance regressions  
✅ **Automate in CI/CD** - Continuous validation  
✅ **Add tests for new services** - Maintain coverage  

---

## 📚 References

- [Docker Healthcheck Documentation](https://docs.docker.com/engine/reference/builder/#healthcheck)
