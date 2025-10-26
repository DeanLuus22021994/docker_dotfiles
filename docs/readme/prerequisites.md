---
date_created: "2025-10-26T18:32:25.955953+00:00"
last_updated: "2025-10-26T18:32:25.955953+00:00"
tags: ['documentation', 'readme', 'guide']
description: "Documentation for prerequisites"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- setup
description: System requirements and prerequisites for running the Docker cluster
---\n# Prerequisites

- **Python 3.14.0+** (see [Python setup guide](python-setup.md))
- Docker Engine 24.0+ with BuildKit enabled
- Docker Compose V2
- 8GB RAM minimum (16GB recommended for Jupyter GPU workloads)
- NVIDIA GPU + drivers (optional, for Jupyter CUDA acceleration)
- Ports: 8080, 5432, 3306, 6379, 8888, 9000, 9001, 3002, 9090
- Windows: WSL2 with Docker Desktop | Linux: Docker Engine | macOS: Docker Desktop

## Required Ports

| Port | Service |
|------|---------|
| 8080 | Load Balancer |
| 5432 | PostgreSQL |
| 3306 | MariaDB |
| 6379 | Redis |
| 8888 | Jupyter Lab |
| 9000/9001 | MinIO |
| 3002 | Grafana |
| 9090 | Prometheus |

See [environment setup](environment-setup.md) for configuration details.
