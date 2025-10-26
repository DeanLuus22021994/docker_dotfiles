# Set-McpProfile
# Switches the active MCP server configuration profile

<#
.SYNOPSIS
    Switches the active MCP server profile configuration.

.DESCRIPTION
    Copies a profile configuration from .vscode/profiles/ to .vscode/mcp.json.
    Backs up the current configuration before switching.
    Requires VS Code restart to apply changes.

.PARAMETER Profile
    Profile name to activate: core, fullstack, testing, data, or all

.PARAMETER NoBackup
    Skip backup of current mcp.json

.EXAMPLE
    .\Set-McpProfile.ps1 -Profile core
    Switches to core development profile (53 tools).

.EXAMPLE
    .\Set-McpProfile.ps1 -Profile fullstack -NoBackup
    Switches to fullstack profile without backing up current config.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("core", "fullstack", "testing", "data", "all")]
    [string]$Profile,
    
    [Parameter(Mandatory=$false)]
    [switch]$NoBackup
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# Profile definitions
$profiles = @{
    "core" = @{
        file = "core.json"
        description = "Core Development (53 tools: github, filesystem, git, fetch)"
        toolCount = 53
        tokens = "8-10k"
    }
    "fullstack" = @{
        file = "fullstack.json"
        description = "Full-Stack Development (80 tools: github, filesystem + 6 servers)"
        toolCount = 80
        tokens = "11-14k"
    }
    "testing" = @{
        file = "testing.json"
        description = "Testing & Automation (87 tools: github, filesystem, playwright, git, fetch, postgres)"
        toolCount = 87
        tokens = "12-15k"
    }
    "data" = @{
        file = "data.json"
        description = "Data & Analytics (47 tools: github, filesystem, postgres, sqlite, memory, git, fetch)"
        toolCount = 47
        tokens = "7-9k"
    }
    "all" = @{
        file = "../../mcp.json"  # Reference to existing base config
        description = "All Servers (107 tools: complete configuration)"
        toolCount = 107
        tokens = "15-20k"
    }
}

$workspaceRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$profilesDir = Join-Path $workspaceRoot ".vscode\profiles"
$sourceFile = Join-Path $profilesDir $profiles[$Profile].file
$targetFile = Join-Path $workspaceRoot ".vscode\mcp.json"

# Handle "all" profile (already at target location)
if ($Profile -eq "all") {
    Write-Host ""
    Write-Host "ℹ Already using 'all' profile (base mcp.json)" -ForegroundColor Cyan
    Write-Host "  Description: $($profiles[$Profile].description)" -ForegroundColor Gray
    Write-Host "  Tool Count: $($profiles[$Profile].toolCount)" -ForegroundColor Gray
    Write-Host "  Estimated Tokens: $($profiles[$Profile].tokens)" -ForegroundColor Gray
    Write-Host ""
    exit 0
}

# Validate source file exists
if (-not (Test-Path $sourceFile)) {
    Write-Host "✗ Profile configuration not found: $sourceFile" -ForegroundColor Red
    Write-Host ""
    Write-Host "Available profiles:"
    foreach ($key in $profiles.Keys | Sort-Object) {
        $prof = $profiles[$key]
        if ($key -ne "all") {
            $profFile = Join-Path $profilesDir $prof.file
            $exists = Test-Path $profFile
            $status = if ($exists) { "✓" } else { "✗" }
            $color = if ($exists) { "Green" } else { "Red" }
            Write-Host "  $status $key - $($prof.description)" -ForegroundColor $color
        }
    }
    Write-Host ""
    Write-Host "Run to generate profiles:" -ForegroundColor Yellow
    Write-Host "  .\scripts\orchestrator.ps1 mcp new-profiles" -ForegroundColor Cyan
    exit 1
}

# Backup current config if it exists and not disabled
if ((Test-Path $targetFile) -and -not $NoBackup) {
    $backupFile = Join-Path $workspaceRoot ".vscode\mcp.backup.json"
    Copy-Item $targetFile $backupFile -Force
    Write-Host "ℹ Backed up current config to: mcp.backup.json" -ForegroundColor Cyan
}

# Switch profile
Copy-Item $sourceFile $targetFile -Force

Write-Host ""
Write-Host "✓ Switched to '$Profile' profile" -ForegroundColor Green
Write-Host "  Description: $($profiles[$Profile].description)" -ForegroundColor Gray
Write-Host "  Tool Count: $($profiles[$Profile].toolCount)" -ForegroundColor Gray
Write-Host "  Estimated Tokens: $($profiles[$Profile].tokens)" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠ IMPORTANT: Restart VS Code Insiders to apply changes" -ForegroundColor Yellow
Write-Host ""
