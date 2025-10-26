---
date_created: "2025-10-26T18:32:25.945695+00:00"
last_updated: "2025-10-26T18:32:25.945695+00:00"
tags: ['documentation']
description: "Documentation for getting started"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- installation
- setup
- quickstart
description: Getting started guides for new users
---\n# Getting Started

Quick links to begin using the platform:

- [Project Overview](../../README.md) - Features and introduction
- [Prerequisites](../../docs/readme/prerequisites.md) - System requirements
- [Installation](../../docs/readme/installation.md) - Setup instructions
- [Environment Setup](../../docs/readme/environment-setup.md) - Configure credentials
- [Quickstart](../../web-content/QUICKSTART.md) - 5-minute guide
- [Production Deployment](../production/overview.md) - Production setup

## Quick Commands

```bash
# Clone and start
git clone <repository-url>
cd docker && make build && make up

# Verify
curl http://localhost:8080/
make ps
```

See [usage guide](../../docs/readme/usage.md) for all commands.
