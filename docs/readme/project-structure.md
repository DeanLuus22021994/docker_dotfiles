---
date_created: "2025-10-26T18:32:25.956506+00:00"
last_updated: "2025-10-26T18:32:25.956506+00:00"
tags: ['documentation', 'readme', 'guide']
description: "Documentation for project structure"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- architecture
description: Project directory structure and file organization
---\n# Project Structure

```
docker/
├── .config/                    # Centralized configuration (SSoT)
│   ├── web/                    # Web dashboard configs (Vite, TypeScript, ESLint, etc.)
│   ├── python/                 # Python tool configs (pytest, pyright)
│   ├── git/                    # Git tool configs (pre-commit)
│   ├── devcontainer/           # DevContainer configuration
│   ├── nginx/                  # Nginx configs
│   ├── database/               # PostgreSQL and MariaDB configs
│   ├── services/               # Service-specific configs
│   ├── docker/                 # Docker daemon configs
│   └── monitoring/             # Prometheus, Grafana
├── .devcontainer/              # Symlink to .config/devcontainer/
├── .github/                    # GitHub configuration
│   ├── copilot-instructions.md # Copilot coding standards
│   ├── TODO.md                 # Implementation tracking
│   └── workflows/              # CI/CD pipelines
├── .vscode/                    # VS Code team settings
├── dockerfile/                 # All Dockerfiles (SSoT - 20 services)
│   ├── web-dashboard.Dockerfile    # React monitoring dashboard
│   ├── devcontainer.Dockerfile     # Development container
│   ├── postgres.Dockerfile         # PostgreSQL database
│   ├── redis.Dockerfile            # Redis cache
│   ├── nginx.Dockerfile            # Load balancer
│   └── [15 more services...]       # See complete list below
├── scripts/                    # Automation scripts
│   ├── orchestrator.py         # Python orchestrator
│   ├── powershell/             # PowerShell scripts
│   ├── python/                 # Python scripts
│   └── bash/                   # Bash scripts
├── web-content/                # React dashboard source code
├── api/                        # Express.js API server
├── docker-compose.yml          # 26-service orchestration
└── Makefile                    # Build + test + validate
```

See [configuration guide](configuration.md) for config details.
