---
date_created: "2025-10-26T18:32:25.954818+00:00"
last_updated: "2025-10-26T18:32:25.954818+00:00"
tags: ["documentation", "readme", "guide"]
description: "Documentation for overview"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- overview
- architecture
  description: Overview of the Modern Data Platform Docker cluster
  ---\n# Modern Data Platform - Overview

[![Docker](https://img.shields.io/badge/Docker-24.0%2B-blue)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-V2-blue)](https://docs.docker.com/compose/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GPU](https://img.shields.io/badge/CUDA-12.2-green)](https://developer.nvidia.com/cuda-toolkit)

A turn-key modern data platform featuring GPU-accelerated Jupyter, load-balanced web services, dual databases (PostgreSQL + MariaDB), Redis cache, S3-compatible storage (MinIO), GitHub MCP integration, production-grade monitoring with Grafana/Prometheus, and complete local development stack.

## Quick Start

```bash
# Clone and navigate
git clone <repository-url>
cd docker

# Build and start cluster
make build
make up

# Verify deployment
curl http://localhost:8080/
make ps

# For development with VS Code
make dev  # Starts cluster + devcontainer
```

See [installation guide](installation.md) for detailed setup.
