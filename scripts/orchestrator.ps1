#!/usr/bin/env pwsh
<#
.SYNOPSIS
    PowerShell Orchestrator for Docker Infrastructure Scripts

.DESCRIPTION
    Central orchestrator for all PowerShell-based automation scripts.
    Delegates tasks to specialized scripts organized by function (SRP).

.PARAMETER Task
    Task to execute: config, docker, docs, audit, cleanup, validate

.PARAMETER Action
    Specific action within the task category

.EXAMPLE
    .\orchestrator.ps1 -Task config -Action apply-settings
    .\orchestrator.ps1 -Task docker -Action start-devcontainer
    .\orchestrator.ps1 -Task docs -Action serve
    .\orchestrator.ps1 -Task audit -Action test-integration

.NOTES
    Organization: Tasks organized by SRP (Single Responsibility Principle)
    Location: scripts/powershell/[task]/[action].ps1
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [ValidateSet('config', 'docker', 'docs', 'audit', 'cleanup', 'validate', 'mcp', 'help')]
    [string]$Task,

    [Parameter(Mandatory=$false, Position=1)]
    [string]$Action,
    
    [Parameter(Mandatory=$false)]
    [string]$Profile
)

$ErrorActionPreference = 'Stop'
$ScriptRoot = $PSScriptRoot

# Color output functions
function Write-Success { param([string]$Message) Write-Host "✓ $Message" -ForegroundColor Green }
function Write-Error-Custom { param([string]$Message) Write-Host "✗ $Message" -ForegroundColor Red }
function Write-Info { param([string]$Message) Write-Host "ℹ $Message" -ForegroundColor Blue }
function Write-Warning-Custom { param([string]$Message) Write-Host "⚠ $Message" -ForegroundColor Yellow }

# Display help
function Show-Help {
    Write-Host "`n=== PowerShell Orchestrator ===" -ForegroundColor Cyan
    Write-Host "`nAvailable Tasks:`n"
    
    Write-Host "config" -ForegroundColor Yellow
    Write-Host "  apply-settings    Apply VSCode settings"
    Write-Host "  setup-secrets     Setup environment secrets"
    
    Write-Host "`ndocker" -ForegroundColor Yellow
    Write-Host "  start-devcontainer Start development container"
    
    Write-Host "`ndocs" -ForegroundColor Yellow
    Write-Host "  serve             Serve documentation"
    
    Write-Host "`naudit" -ForegroundColor Yellow
    Write-Host "  test-integration  Run integration tests"
    
    Write-Host "`nvalidate" -ForegroundColor Yellow
    Write-Host "  env               Validate environment variables (uses Python)"
    Write-Host "  configs           Validate configuration files (uses Python)"
    
    Write-Host "`nmcp" -ForegroundColor Yellow
    Write-Host "  new-profiles      Generate MCP profile configurations"
    Write-Host "  set-profile       Switch active MCP profile (-Profile <name>)"
    Write-Host "  get-profile       Show current active profile"
    Write-Host "  test-servers      Health check all MCP servers"
    Write-Host "  compare-profiles  Compare two profiles"
    Write-Host "  test-profiles     Run comprehensive profile tests"
    
    Write-Host "`nExamples:"
    Write-Host "  .\orchestrator.ps1 config apply-settings" -ForegroundColor Gray
    Write-Host "  .\orchestrator.ps1 mcp set-profile -Profile core" -ForegroundColor Gray
    Write-Host "  .\orchestrator.ps1 mcp test-servers" -ForegroundColor Gray
    Write-Host ""
}

# Execute task
function Invoke-Task {
    param([string]$Task, [string]$Action)
    
    switch ($Task) {
        'config' {
            switch ($Action) {
                'apply-settings' {
                    $script = Join-Path $ScriptRoot "powershell\config\apply-settings.ps1"
                    if (Test-Path $script) {
                        Write-Info "Applying VSCode settings..."
                        & $script
                    } else {
                        Write-Error-Custom "Script not found: $script"
                        exit 1
                    }
                }
                'setup-secrets' {
                    $script = Join-Path $ScriptRoot "powershell\config\setup-secrets.ps1"
                    if (Test-Path $script) {
                        Write-Info "Setting up secrets..."
                        & $script
                    } else {
                        Write-Error-Custom "Script not found: $script"
                        exit 1
                    }
                }
                default {
                    Write-Error-Custom "Unknown config action: $Action"
                    Write-Info "Available: apply-settings, setup-secrets"
                    exit 1
                }
            }
        }
        
        'docker' {
            switch ($Action) {
                'start-devcontainer' {
                    $script = Join-Path $ScriptRoot "powershell\docker\start-devcontainer.ps1"
                    if (Test-Path $script) {
                        Write-Info "Starting devcontainer..."
                        & $script
                    } else {
                        Write-Error-Custom "Script not found: $script"
                        exit 1
                    }
                }
                default {
                    Write-Error-Custom "Unknown docker action: $Action"
                    Write-Info "Available: start-devcontainer"
                    exit 1
                }
            }
        }
        
        'docs' {
            switch ($Action) {
                'serve' {
                    $script = Join-Path $ScriptRoot "powershell\docs\serve-docs.ps1"
                    if (Test-Path $script) {
                        Write-Info "Starting documentation server..."
                        & $script
                    } else {
                        Write-Error-Custom "Script not found: $script"
                        exit 1
                    }
                }
                default {
                    Write-Error-Custom "Unknown docs action: $Action"
                    Write-Info "Available: serve"
                    exit 1
                }
            }
        }
        
        'audit' {
            switch ($Action) {
                'test-integration' {
                    $script = Join-Path $ScriptRoot "powershell\audit\test-integration.ps1"
                    if (Test-Path $script) {
                        Write-Info "Running integration tests..."
                        & $script
                    } else {
                        Write-Error-Custom "Script not found: $script"
                        exit 1
                    }
                }
                default {
                    Write-Error-Custom "Unknown audit action: $Action"
                    Write-Info "Available: test-integration"
                    exit 1
                }
            }
        }
        
        'validate' {
            switch ($Action) {
                'env' {
                    $script = Join-Path $ScriptRoot "python\validation\validate_env.py"
                    if (Test-Path $script) {
                        Write-Info "Validating environment variables..."
                        python $script
                    } else {
                        Write-Error-Custom "Script not found: $script"
                        exit 1
                    }
                }
                'configs' {
                    $script = Join-Path $ScriptRoot "python\validation\validate_configs.py"
                    if (Test-Path $script) {
                        Write-Info "Validating configuration files..."
                        python $script
                    } else {
                        Write-Error-Custom "Script not found: $script"
                        exit 1
                    }
                }
                default {
                    Write-Error-Custom "Unknown validate action: $Action"
                    Write-Info "Available: env, configs"
                    exit 1
                }
            }
        }
        
        'mcp' {
            switch ($Action) {
                'new-profiles' {
                    $script = Join-Path $ScriptRoot "powershell\mcp\New-McpProfiles.ps1"
                    if (Test-Path $script) {
                        Write-Info "Generating MCP profiles..."
                        & $script
                    } else {
                        Write-Error-Custom "Script not found: $script"
                        exit 1
                    }
                }
                'set-profile' {
                    if ([string]::IsNullOrEmpty($Profile)) {
                        Write-Error-Custom "Profile parameter required: -Profile <core|fullstack|testing|data|all>"
                        exit 1
                    }
                    $script = Join-Path $ScriptRoot "powershell\mcp\Set-McpProfile.ps1"
                    if (Test-Path $script) {
                        Write-Info "Switching to $Profile profile..."
                        & $script -Profile $Profile
                    } else {
                        Write-Error-Custom "Script not found: $script"
                        exit 1
                    }
                }
                'get-profile' {
                    $script = Join-Path $ScriptRoot "powershell\mcp\Get-McpProfile.ps1"
                    if (Test-Path $script) {
                        & $script
                    } else {
                        Write-Error-Custom "Script not found: $script"
                        exit 1
                    }
                }
                'test-servers' {
                    $script = Join-Path $ScriptRoot "powershell\mcp\Test-McpServers.ps1"
                    if (Test-Path $script) {
                        Write-Info "Testing MCP servers..."
                        & $script
                    } else {
                        Write-Error-Custom "Script not found: $script"
                        exit 1
                    }
                }
                'compare-profiles' {
                    $script = Join-Path $ScriptRoot "powershell\mcp\Compare-McpProfiles.ps1"
                    if (Test-Path $script) {
                        & $script
                    } else {
                        Write-Error-Custom "Script not found: $script"
                        exit 1
                    }
                }
                'test-profiles' {
                    $script = Join-Path $ScriptRoot "powershell\mcp\Test-McpProfileGeneration.ps1"
                    if (Test-Path $script) {
                        Write-Info "Running profile generation tests..."
                        & $script
                    } else {
                        Write-Error-Custom "Script not found: $script"
                        exit 1
                    }
                }
                default {
                    Write-Error-Custom "Unknown mcp action: $Action"
                    Write-Info "Available: new-profiles, set-profile, get-profile, test-servers, compare-profiles, test-profiles"
                    exit 1
                }
            }
        }
        
        'help' {
            Show-Help
            exit 0
        }
        
        default {
            Write-Error-Custom "Unknown task: $Task"
            Show-Help
            exit 1
        }
    }
}

# Main execution
if ($Task -eq 'help' -or [string]::IsNullOrEmpty($Action)) {
    Show-Help
    exit 0
}

try {
    Invoke-Task -Task $Task -Action $Action
    Write-Success "Task completed: $Task $Action"
} catch {
    Write-Error-Custom "Task failed: $_"
    exit 1
}
