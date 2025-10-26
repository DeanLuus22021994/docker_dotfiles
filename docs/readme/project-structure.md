---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["structure", "organization", "directories", "files"]
description: "Project directory structure and file organization"
---

# Project Structure

```
docker/
├── .config/                    # Centralized configuration (SSoT)
│   ├── nginx/                  # Nginx configs
│   ├── database/               # PostgreSQL and MariaDB configs
│   ├── services/               # Service-specific configs
│   ├── docker/                 # Docker daemon configs
│   └── monitoring/             # Prometheus, Grafana
├── .devcontainer/              # VS Code devcontainer config
├── .github/                    # GitHub configuration
│   ├── copilot-instructions.md # Copilot coding standards
│   ├── TODO.md                 # Implementation tracking
│   └── workflows/              # CI/CD pipelines
├── .vscode/                    # VS Code team settings
├── dockerfile/                 # Dockerfile definitions (SRP)
├── scripts/                    # Automation scripts
│   ├── orchestrator.py         # Python orchestrator
│   ├── powershell/             # PowerShell scripts
│   ├── python/                 # Python scripts
│   └── bash/                   # Bash scripts
├── web-content/                # Static web content
├── docker-compose.yml          # 26-service orchestration
└── Makefile                    # Build + test + validate
```

See [configuration guide](configuration.md) for config details.
