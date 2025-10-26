---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["organization", "structure", "files", "directories"]
description: "File organization patterns and volume mount strategies"
---

# File Organization

## Volume Mounts

```yaml
# Example: nginx loadbalancer
volumes:
  - ./.config/nginx/loadbalancer.conf:/etc/nginx/nginx.conf:ro

# Example: PostgreSQL
volumes:
  - ./.config/database/postgresql.conf:/etc/postgresql/postgresql.conf:ro
```

## Dockerfile COPY

```dockerfile
# Example: MariaDB
COPY --chown=mysql:mysql .config/database/mariadb.conf /etc/mysql/conf.d/custom.cnf

# Example: nginx
COPY --chown=nginx:nginx .config/nginx/main.conf /etc/nginx/nginx.conf
```

## VSCode Configuration

**Team Settings (Tracked)**:
- `.vscode/settings.json` - YAML schemas, Copilot enabled
- Shared across team, committed to repo

**Personal Settings (Gitignored)**:
- `.vscode/settings.local.json` - AI model preferences
- Local only, added to `.gitignore`

See [security guidelines](agent-security.md) for credential management.
