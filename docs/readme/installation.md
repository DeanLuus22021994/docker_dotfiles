---
date_created: "2025-10-26T18:32:25.953769+00:00"
last_updated: "2025-10-26T18:32:25.953769+00:00"
tags: ['documentation', 'readme', 'guide']
description: "Documentation for installation"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- installation
- deployment
- setup
description: Installation and deployment guide for production and development
---\n# Installation

## Production Deployment

```bash
# Clone repository
git clone <repository-url>
cd docker

# Build and start
make build
make up

# Verify
make ps
curl http://localhost:8080/
```

## Development with VS Code

1. **Open in VS Code**:
```bash
code .
```

2. **Open in DevContainer**:
   - Press `F1` or `Ctrl+Shift+P`
   - Select "Dev Containers: Reopen in Container"
   - Wait for container build and initialization

3. **Development environment includes**:
   - Full cluster access (load balancer, web servers, database)
   - Python 3.14.0 with UV package manager
   - Node.js 22 with npm
   - Docker-in-Docker for managing cluster
   - VS Code extensions pre-installed

See [usage guide](usage.md) for available commands.
