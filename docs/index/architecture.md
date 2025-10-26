---
date_created: "2025-10-26T18:32:25.945017+00:00"
last_updated: "2025-10-26T18:32:25.945017+00:00"
tags: ["documentation"]
description: "Documentation for architecture"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- architecture
  description: Architecture and design documentation index
  ---\n# Architecture

System design and component documentation:

- [Overview](../../docs/readme/architecture.md) - High-level architecture
- [Web Dashboard](../../web-content/architecture/overview.md) - Frontend architecture
- [Features](../../docs/readme/features.md) - Complete feature set
- [Project Structure](../../docs/readme/project-structure.md) - Directory organization
- [API Documentation](../../api/overview.md) - API server design

## Layers

The platform is organized into five architectural layers:

- **Data Layer** - PostgreSQL, MariaDB, Redis, MinIO
- **Services Layer** - API server, web dashboard
- **Monitoring Layer** - Grafana, Prometheus
- **Compute Layer** - Jupyter notebooks
- **Network Layer** - Nginx, Traefik reverse proxy

See [web architecture](../../web-content/architecture/layers.md) for details.
