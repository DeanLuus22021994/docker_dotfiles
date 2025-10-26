---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["services", "endpoints", "access", "urls", "ports"]
description: "Service endpoints and access credentials for all cluster services"
---

# Service Access

## Web Services

- **Load Balancer**: http://localhost:8080 (Web UI)
- **MailHog**: http://localhost:8025 (Email testing UI, SMTP: 1025)
- **pgAdmin**: http://localhost:5050 (admin@example.com/admin)
- **Redis Commander**: http://localhost:8082 (admin/admin)

## Databases

- **PostgreSQL**: localhost:5432 (User: cluster_user, DB: clusterdb)
- **MariaDB**: localhost:3306 (User: cluster_user, DB: clusterdb)
- **Redis**: localhost:6379 (Password: changeme)

## Data & ML

- **Jupyter Lab**: http://localhost:8888 (Token: changeme, GPU-enabled)
- **MinIO Console**: http://localhost:9001 (Admin/Admin)
- **MinIO API**: localhost:9000 (S3-compatible)

## Monitoring & Tools

- **Grafana**: http://localhost:3002 (Admin/Admin)
- **Prometheus**: http://localhost:9090 (Metrics)
- **BuildKit**: localhost:1234 (Build daemon)
- **LocalStack**: http://localhost:4566 (AWS emulation)
- **GitHub MCP**: stdio-based (Node.js integration)

See [configuration guide](configuration.md) for customization.
