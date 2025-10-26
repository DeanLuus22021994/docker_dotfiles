---
date_created: "2025-10-26T18:32:25.971744+00:00"
last_updated: "2025-10-26T18:32:25.971744+00:00"
tags: ["documentation", "setup", "installation"]
description: "Documentation for prerequisites"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- setup
- installation
  description: Software prerequisites and system requirements
  ---\n# Prerequisites

## Required Software

**Docker 24.0+**

```bash
# Verify installation
docker --version
docker-compose --version
```

**Python 3.14+**

```bash
# Install via UV
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.14
```

**Node.js 22+ LTS**

```bash
# Verify installation
node --version
npm --version
```

**Git 2.40+**

```bash
git --version
```

## System Requirements

- **OS:** Windows 10/11, Ubuntu 22.04+, macOS 12+
- **RAM:** 8GB minimum, 16GB recommended
- **Storage:** 20GB free disk space (50GB for production)
- **CPU:** 4 cores minimum, 8 cores recommended
- **Network:** Internet connection for image downloads

## Optional Tools

- **GitHub CLI** (`gh`) - For repository management
- **Make** - For Makefile commands
- **VS Code** - Recommended IDE with extensions

## Firewall Configuration

Open ports for local development:

- 80/443 - HTTP/HTTPS (Traefik)
- 3000 - API server
- 5432 - PostgreSQL
- 3306 - MariaDB
- 6379 - Redis
- 9000 - MinIO
- 3001 - Grafana
- 9090 - Prometheus
