---
date_created: "2025-10-26T18:32:25.936236+00:00"
last_updated: "2025-10-26T18:32:25.936236+00:00"
tags: ["documentation", "agent", "development"]
description: "Documentation for code quality"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- validation
- testing
  description: Code quality standards and validation procedures
  ---\n# Code Quality

## Pre-commit Hooks (Automated)

- Runs as `cluster-pre-commit` container service (dev profile)
- Auto-installs hooks on devcontainer startup
- Blocks commits on errors (no warnings)
- Checks: YAML/JSON syntax, secrets detection, docker-compose validation

## Manual Validation

```powershell
# Environment variables
python scripts/validate_env.py

# Docker Compose syntax
docker-compose config --quiet

# Nginx configs
docker run --rm -v "${PWD}/.config/nginx:/etc/nginx:ro" nginx:alpine nginx -t

# All configs
python scripts/validate_configs.py
```

## Error Messages

- **Explicit**: Show exact file path, line number
- **Actionable**: Provide fix command or example
- **Unambiguous**: No vague errors, clear root cause

See [Docker stack guide](docker-stack.md) for service management.
