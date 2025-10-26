---
date_created: "2025-10-26T18:32:25.950834+00:00"
last_updated: "2025-10-26T18:32:25.950834+00:00"
tags: ["documentation", "readme", "guide"]
description: "Documentation for architecture"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- architecture
  description: System architecture and component overview of the Docker cluster
  ---\n# Architecture

```
Internet → Load Balancer (nginx:8080)
            ↓
    ┌───────┼───────┐
   Web1   Web2   Web3
    ↓       ↓      ↓
┌─────────────────────────────┐
│   Data & Processing Layer   │
├─────────────────────────────┤
│ PostgreSQL:5432             │
│ MariaDB:3306                │
│ Redis:6379 (Cache)          │
│ MinIO:9000 (S3 Storage)     │
│ Jupyter:8888 (GPU/ML)       │
│ GitHub MCP (AI Context)     │
├─────────────────────────────┤
│   Monitoring & Ops          │
│ Grafana:3002 | Prometheus   │
│ k9s (K8s CLI)               │
└─────────────────────────────┘
```

## Components

- **Load Balancer**: Nginx-based load balancer distributing traffic across web servers
- **Web Servers**: 3 nginx instances serving static content with round-robin distribution
- **Database**: PostgreSQL 16 + MariaDB 11 with persistent storage and health monitoring
- **Networking**: Isolated bridge network for secure internal communication
- **Storage**: Named volumes for database persistence and nginx caching

See [features](features.md) for detailed capabilities.
