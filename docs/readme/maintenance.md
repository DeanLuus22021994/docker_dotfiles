---
date_created: "2025-10-26T18:32:25.954276+00:00"
last_updated: "2025-10-26T18:32:25.954276+00:00"
tags: ['documentation', 'readme', 'guide']
description: "Documentation for maintenance"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- documentation
description: Maintenance procedures including backup, restore, and updates
---\n# Maintenance

## Backup Database

```bash
docker-compose exec db pg_dump -U cluster_user clusterdb > backup.sql
```

## Restore Database

```bash
docker-compose exec -T db psql -U cluster_user -d clusterdb < backup.sql
```

## Update Images

```bash
make build --no-cache
make restart
```

## Security & Performance

**Security Features:**
- Non-root user execution in all containers
- Secret management for sensitive data
- Read-only volumes where applicable
- Network isolation with bridge networking
- Regular security updates via base images
- Minimal attack surface with Alpine Linux

**Performance Optimizations:**
- BuildKit caching for fast builds
- Optimized multi-stage Dockerfiles
- Named volumes for persistent data
- Nginx caching for improved response times
- PostgreSQL tuning for optimal performance
- Resource limits and health checks
