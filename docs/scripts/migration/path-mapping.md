---
date_created: "2025-10-26T18:32:25.987433+00:00"
last_updated: "2025-10-26T18:32:25.987433+00:00"
tags: ['documentation', 'scripts', 'automation']
description: "Documentation for path mapping"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- scripts
- migration
- documentation
description: Complete path mapping for scripts migration
---\n# Scripts Path Mapping

Complete mapping from old to new paths.

## File Migrations

| Old Path | New Path | Status |
|----------|----------|--------|
| `scripts/validate_env.py` | `scripts/python/validation/validate_env.py` | ✅ Migrated |
| `scripts/validate_configs.py` | `scripts/python/validation/validate_configs.py` | ✅ Migrated |
| `scripts/apply-settings.ps1` | `scripts/powershell/config/apply-settings.ps1` | ✅ Migrated |
| `scripts/setup_secrets.ps1` | `scripts/powershell/config/setup-secrets.ps1` | ✅ Migrated |
| `scripts/start_devcontainer.ps1` | `scripts/powershell/docker/start-devcontainer.ps1` | ✅ Migrated |
| `scripts/serve_docs.ps1` | `scripts/powershell/docs/serve-docs.ps1` | ✅ Migrated |
| `scripts/test_integration.ps1` | `scripts/powershell/audit/test-integration.ps1` | ✅ Migrated |
| `scripts/start_devcontainer.sh` | `scripts/bash/docker/start-devcontainer.sh` | ✅ Migrated |
| `scripts/serve_docs.sh` | `scripts/bash/docs/serve-docs.sh` | ✅ Migrated |

## Quick Reference

**Python Validation:**
- `validate_env.py` → `python/validation/validate_env.py`
- `validate_configs.py` → `python/validation/validate_configs.py`

**PowerShell Config:**
- `apply-settings.ps1` → `powershell/config/apply-settings.ps1`
- `setup_secrets.ps1` → `powershell/config/setup-secrets.ps1`

**Docker Scripts:**
- `start_devcontainer.{ps1,sh}` → `{powershell,bash}/docker/start-devcontainer.{ps1,sh}`

**Documentation:**
- `serve_docs.{ps1,sh}` → `{powershell,bash}/docs/serve-docs.{ps1,sh}`

**Audit:**
- `test_integration.ps1` → `powershell/audit/test-integration.ps1`
