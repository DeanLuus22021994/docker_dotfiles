---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["pre-commit", "hooks", "automation", "quality", "validation"]
description: "Pre-commit hooks for automated code quality and validation"
---

# Pre-commit Hooks

Pre-commit hooks run automatically in the `cluster-pre-commit` container service.

## Enabled Hooks

- YAML/JSON syntax validation
- Secrets detection (detect-secrets)
- docker-compose validation
- Python formatting (Black, Ruff)
- Trailing whitespace, end-of-file fixer

## Usage

```bash
# Pre-commit runs automatically in dev profile
make dev

# Manual run (if needed)
docker-compose run --rm cluster-pre-commit

# Or install locally
pre-commit install
pre-commit run --all-files
```

**Configuration**: See `.pre-commit-config.yaml`

## Scaling

Scale web servers dynamically:
```bash
docker-compose up -d --scale cluster-web1=5 --scale cluster-web2=5 --scale cluster-web3=5
```

See [troubleshooting guide](troubleshooting.md) for common issues.
