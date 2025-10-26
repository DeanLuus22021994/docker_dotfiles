---
date_created: "2025-10-26T18:32:25.937688+00:00"
last_updated: "2025-10-26T18:32:25.937688+00:00"
tags: ["documentation", "agent", "development", "docker"]
description: "Documentation for docker stack"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- docker
- docker-compose
- compose
  description: Docker stack services and management commands
  ---\n# Docker Stack

## Services (25+)

- **Databases**: PostgreSQL, MariaDB, Redis
- **Storage**: MinIO (S3-compatible)
- **Monitoring**: Prometheus, Grafana, Alertmanager
- **Development**: Jupyter, pgAdmin, Redis Commander
- **Infrastructure**: nginx loadbalancer, BuildKit, LocalStack
- **DevContainer**: Python 3.14.0 + Node 22

## Profiles

- **Default**: Production services (databases, monitoring, web servers)
- **dev**: Includes devcontainer, pre-commit, docs server
- **docs**: GitHub Pages Jekyll server

## Commands

```powershell
# Production stack
docker-compose up -d

# Development stack (includes devcontainer and pre-commit)
docker-compose --profile dev up -d

# View logs
docker-compose logs -f [service]

# Restart service
docker-compose restart [service]

# Stop all
docker-compose down
```

See [file organization guide](file-organization.md) for config locations.
