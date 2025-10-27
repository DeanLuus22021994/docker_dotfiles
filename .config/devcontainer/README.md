---
date_created: '2025-10-27T02:37:41Z'
last_updated: '2025-10-27T02:37:41Z'
tags: [devcontainer, vscode, development]
description: 'VS Code development container configuration'
---

# DevContainer Configuration

VS Code development container with full cluster access.

## 📁 Files

### `devcontainer.json`
**VS Code devcontainer configuration**.

**Features**:
- Python 3.14.0
- Node.js 22
- NVIDIA CUDA support
- Docker-in-Docker
- 29 services auto-started

**Host Requirements**:
- 4 CPUs
- 4GB RAM
- 8GB storage
- GPU optional

**Port Forwarding**: All cluster services (8080, 5432, 3306, 6379, etc.)

**VS Code Extensions**:
- GitHub Copilot
- Docker
- Python
- YAML
- ESLint

---

## 🚀 Quick Start

### Open in DevContainer

```powershell
# From VS Code
# Command Palette → Dev Containers: Reopen in Container

# Or using CLI
devcontainer open .
```

### Access Services

All services are automatically port-forwarded:
- Load Balancer: http://localhost:8080
- PostgreSQL: localhost:5432
- Grafana: http://localhost:3002
- Jupyter: http://localhost:8888

---

## 📚 References

- [Dev Containers Documentation](https://containers.dev/)
- [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)
