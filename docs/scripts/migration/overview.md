---
date_created: "2025-10-26T18:32:25.986866+00:00"
last_updated: "2025-10-26T18:32:25.986866+00:00"
tags: ["documentation", "scripts", "automation"]
description: "Documentation for overview"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- scripts
- migration
- overview
  description: Scripts migration guide overview for v3.0.0 restructure
  ---\n# Scripts Migration Overview

Migration from flat scripts structure to organized SRP/DRY structure (v3.0.0, 2025-10-25).

## What Changed

**Old:** All scripts in `scripts/` root (9 files, no organization)

**New:** Organized by language and purpose:

```
scripts/
├── orchestrator.{ps1,sh,py}  # Unified task execution
├── powershell/               # PowerShell scripts by category
│   ├── config/               # apply-settings, setup-secrets
│   ├── docker/               # start-devcontainer
│   ├── docs/                 # serve-docs
│   └── audit/                # test-integration
├── python/                   # Python modules
│   ├── validation/           # validate_env, validate_configs
│   ├── audit/                # code_quality, dependencies
│   └── utils/                # Shared utilities (DRY)
└── bash/                     # Bash scripts by category
    ├── docker/               # start-devcontainer
    └── docs/                 # serve-docs
```

## Migration Approaches

**Option 1: Orchestrators (Recommended)**

```powershell
python scripts/orchestrator.py validate env
scripts/orchestrator.ps1 audit code
```

**Option 2: Update Paths**

```powershell
# Old: python scripts/validate_env.py
# New: python scripts/python/validation/validate_env.py
```

## Breaking Changes

- Old paths no longer work (removed)
- Python imports need updating
- CI/CD pipelines require path updates

**No backward compatibility** - clean break for better organization.
