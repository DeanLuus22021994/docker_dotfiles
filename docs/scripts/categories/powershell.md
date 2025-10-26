---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["scripts", "powershell", "windows"]
description: "PowerShell scripts organization and usage"
---
# PowerShell Scripts

## Categories

**`powershell/config/`** - Configuration and secrets management
- `apply-settings.ps1` - Apply GitHub repository settings
- `setup-secrets.ps1` - Configure GitHub secrets from .env

**`powershell/docker/`** - Docker operations
- `start-devcontainer.ps1` - Start development container

**`powershell/docs/`** - Documentation tools
- `serve-docs.ps1` - Serve MkDocs documentation locally

**`powershell/audit/`** - Testing and integration
- `test-integration.ps1` - Run integration test suite

## Usage

**Direct execution:**

```powershell
.\scripts\powershell\config\apply-settings.ps1 -ApplyAll
.\scripts\powershell\docker\start-devcontainer.ps1
```

**Via orchestrator:**

```powershell
scripts\orchestrator.ps1 validate env
scripts\orchestrator.ps1 audit code
```

## Requirements

- PowerShell 7.0+ recommended
- Windows 10/11 or PowerShell Core on Linux/macOS
- GitHub CLI (`gh`) for config scripts

See PowerShell README: `scripts/powershell/README.md`
