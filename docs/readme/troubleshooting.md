---
date_created: "2025-10-26T18:32:25.958195+00:00"
last_updated: "2025-10-26T18:32:25.958195+00:00"
tags: ["documentation", "readme", "guide"]
description: "Documentation for troubleshooting"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- troubleshooting
- debugging
  description: Common issues and troubleshooting solutions for the cluster
  ---\n# Troubleshooting

## Port Conflicts

```bash
# Check if ports are in use
netstat -ano | findstr :8080
netstat -ano | findstr :5432
```

## Service Health Issues

```bash
# Check service logs
make logs

# Inspect specific service
docker-compose logs [service_name]

# Check health status
docker inspect <container_id> | findstr Health
```

## Database Connection

```bash
# Test database connectivity
docker-compose exec db psql -U cluster_user -d clusterdb -c "SELECT 1;"
```

## Clean Restart

```bash
# Complete cleanup and fresh start
make clean
make build
make up
```

See [maintenance guide](maintenance.md) for backup/restore procedures.
