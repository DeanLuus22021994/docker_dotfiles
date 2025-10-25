# PowerShell Scripts

PowerShell automation scripts organized by task (SRP principle).

## Structure

```
powershell/
├── config/                  # Configuration management
│   ├── apply-settings.ps1   # Apply VSCode settings
│   └── setup-secrets.ps1    # Setup environment secrets
├── docker/                  # Docker operations
│   └── start-devcontainer.ps1  # Start development container
├── docs/                    # Documentation tasks
│   └── serve-docs.ps1       # Serve documentation server
├── audit/                   # Auditing scripts
│   └── test-integration.ps1 # Integration tests
└── cleanup/                 # Cleanup operations (planned)
```

## Usage

### Via Orchestrator (Recommended)

```powershell
# Display help
..\orchestrator.ps1 help

# Configuration tasks
..\orchestrator.ps1 config apply-settings
..\orchestrator.ps1 config setup-secrets

# Docker tasks
..\orchestrator.ps1 docker start-devcontainer

# Documentation tasks
..\orchestrator.ps1 docs serve

# Audit tasks
..\orchestrator.ps1 audit test-integration

# Validation tasks (delegates to Python)
..\orchestrator.ps1 validate env
..\orchestrator.ps1 validate configs
```

### Direct Execution

```powershell
# Configuration
.\config\apply-settings.ps1
.\config\setup-secrets.ps1

# Docker
.\docker\start-devcontainer.ps1

# Documentation
.\docs\serve-docs.ps1

# Audit
.\audit\test-integration.ps1
```

## Scripts Reference

### config/apply-settings.ps1
**Purpose:** Apply VSCode settings from `.config/vscode/` to `.vscode/`  
**Usage:** `.\config\apply-settings.ps1`  
**Dependencies:** None

### config/setup-secrets.ps1
**Purpose:** Setup environment secrets from `.env` file  
**Usage:** `.\config\setup-secrets.ps1`  
**Dependencies:** `.env` file

### docker/start-devcontainer.ps1
**Purpose:** Start Docker development container  
**Usage:** `.\docker\start-devcontainer.ps1`  
**Dependencies:** Docker, docker-compose

### docs/serve-docs.ps1
**Purpose:** Serve Jekyll documentation  
**Usage:** `.\docs\serve-docs.ps1`  
**Dependencies:** Docker, Jekyll image

### audit/test-integration.ps1
**Purpose:** Run integration tests  
**Usage:** `.\audit\test-integration.ps1`  
**Dependencies:** Docker, test containers

## Common Patterns

### Color Output

Extracted to utility functions (consistent across scripts):

```powershell
function Write-Success { param([string]$Message) Write-Host "✓ $Message" -ForegroundColor Green }
function Write-Error-Custom { param([string]$Message) Write-Host "✗ $Message" -ForegroundColor Red }
function Write-Info { param([string]$Message) Write-Host "ℹ $Message" -ForegroundColor Blue }
function Write-Warning-Custom { param([string]$Message) Write-Host "⚠ $Message" -ForegroundColor Yellow }
```

### Error Handling

All scripts use strict mode:

```powershell
$ErrorActionPreference = 'Stop'

try {
    # Script logic
} catch {
    Write-Error-Custom "Error: $_"
    exit 1
}
```

### Path Resolution

Use `$PSScriptRoot` for relative paths:

```powershell
$ScriptRoot = $PSScriptRoot
$ConfigDir = Join-Path (Split-Path $ScriptRoot) ".config"
```

## Adding New Scripts

1. **Identify task category:** config, docker, docs, audit, cleanup
2. **Create script:**
   ```powershell
   # Header with synopsis
   <#
   .SYNOPSIS
       Brief description
   
   .DESCRIPTION
       Detailed description
   
   .EXAMPLE
       .\script-name.ps1
   #>
   
   $ErrorActionPreference = 'Stop'
   
   # Color output functions
   function Write-Success { ... }
   
   # Main logic
   try {
       # Do work
       Write-Success "Task completed"
   } catch {
       Write-Error-Custom "Task failed: $_"
       exit 1
   }
   ```

3. **Add to orchestrator:** Update `../orchestrator.ps1` switch statement
4. **Update README:** Add to scripts reference table
5. **Test:**
   ```powershell
   # Direct execution
   .\category\script-name.ps1
   
   # Via orchestrator
   ..\orchestrator.ps1 category action
   ```

## Best Practices

### Naming Convention
- Use kebab-case: `start-devcontainer.ps1`
- Action-oriented: `apply-`, `setup-`, `start-`, `test-`
- One script per task (SRP)

### Error Messages
- Explicit: Show file paths, line numbers
- Actionable: Provide fix command
- Colored: Use Write-Error-Custom, Write-Warning-Custom

### Parameters
- Use `[Parameter()]` attributes
- Validate input with `[ValidateSet()]`
- Provide help with `.SYNOPSIS`, `.DESCRIPTION`, `.EXAMPLE`

### Exit Codes
- `0` = Success
- `1` = Error
- Consistent across all scripts

## Troubleshooting

### Execution Policy Error

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Path Not Found

Ensure you're running from scripts root or use absolute paths:

```powershell
cd c:\global\docker\scripts
.\orchestrator.ps1 help
```

### Color Output Not Working

Check terminal supports ANSI colors (PowerShell 5.1+ on Windows 10+):

```powershell
$PSVersionTable.PSVersion
```

## Planned Scripts

- `cleanup/remove-old-images.ps1` - Remove old Docker images
- `cleanup/clear-volumes.ps1` - Clear unused Docker volumes
- `audit/security-scan.ps1` - Security vulnerability scan

---

**Last Updated:** 2025-10-25 (v3.0 refactor)
