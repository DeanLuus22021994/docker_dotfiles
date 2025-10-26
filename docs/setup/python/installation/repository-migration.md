---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["python", "migration", "version-update", "repository"]
description: "Updating repository from Python 3.14 to 3.13"
---
# Repository Migration (3.14 → 3.13)

Update repository references from Python 3.14.0 to 3.13.1.

## Files to Update (37 references)

**CI/CD:**
- `.github/workflows/validate.yml` (3 references)

**Configuration:**
- `pyproject.toml` (2 references)
- `.pre-commit-config.yaml` (1 reference)
- `.docker-compose/cluster.config.yml` (1 reference)

**Containerization:**
- `.devcontainer/devcontainer.dockerfile` (6 references)

**Documentation:**
- `README.md` (7 references)
- `AGENT.md` (4 references)
- `docs/python-setup-troubleshooting.md` (6 references)
- `TODO.md` (3 references)
- Scripts documentation (various)

## Search Command

```powershell
# Find all Python 3.14 references
rg "3\.14\.0|Python 3\.14|python-3\.14|py314|Python314" --type-add 'config:*.{yml,yaml,toml,md,txt}' -t config
```

## Update Process

1. **Search and Review**
```powershell
rg "3\.14" -l  # List files
rg "3\.14" -A 2 -B 2  # Show context
```

2. **Manual Updates** (recommended for accuracy):
   - Version strings: `3.14.0` → `3.13.1`
   - Docker tags: `python:3.14` → `python:3.13`
   - Actions versions: `python-version: 3.14` → `python-version: 3.13`

3. **Verify Changes**
```powershell
# Check no 3.14 references remain
rg "3\.14" --type-add 'config:*.{yml,yaml,toml,md}' -t config

# Validate Python version
python --version  # Should show 3.13.x
```

4. **Test Repository**
```bash
# Run validation
python scripts/orchestrator.py validate env
python scripts/orchestrator.py validate configs

# Run tests
pytest

# Build Docker images
docker-compose build
```

## Commit Message

```
chore: migrate from Python 3.14.0 to 3.13.1

- Update all references across 37 files
- Modify CI/CD workflows, Dockerfiles, configs
- Update documentation and scripts
- Reason: Python 3.14.0 Windows Installer issues

Refs: docs/setup/python/installation/issue-overview.md
```
