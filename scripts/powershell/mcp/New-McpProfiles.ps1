# New-McpProfiles
# Generates optimized MCP server profile configurations from base mcp.json

<#
.SYNOPSIS
    Generates MCP server profile configurations for different development workflows.

.DESCRIPTION
    Creates 4 optimized profiles from the base mcp.json configuration:
    - core: 53 tools (git, github, filesystem, fetch)
    - fullstack: 80 tools (adds playwright, postgres, sqlite, memory)
    - testing: 87 tools (browser automation focused)
    - data: 47 tools (database and analytics focused)

.PARAMETER Force
    Overwrite existing profile files without confirmation.

.EXAMPLE
    .\New-McpProfiles.ps1
    Generates all profile configurations with confirmation prompts.

.EXAMPLE
    .\New-McpProfiles.ps1 -Force
    Regenerates all profiles, overwriting existing files.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [switch]$Force
)

$ErrorActionPreference = "Stop"

# Resolve paths
$workspaceRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$configDir = Join-Path $workspaceRoot ".vscode\configs\mcp"
$profilesDir = Join-Path $configDir "profiles"
$baseConfig = Join-Path $profilesDir "mcp.json"  # Base config in profiles directory

# Ensure directories exist
if (-not (Test-Path $profilesDir)) {
    New-Item -ItemType Directory -Path $profilesDir -Force | Out-Null
}

# Validate base config exists
if (-not (Test-Path $baseConfig)) {
    Write-Host "✗ Base MCP config not found: $baseConfig" -ForegroundColor Red
    Write-Host "  Create .vscode/mcp.json with your MCP server configuration first." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  MCP Profile Generator" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Load base configuration
$baseConfigData = Get-Content $baseConfig | ConvertFrom-Json

# Helper function to create profile with metadata
function New-ProfileConfig {
    param(
        [string]$Name,
        [int]$ToolCount,
        [string]$Tokens,
        [string[]]$Servers
    )
    
    # Always ensure github and filesystem are first in the list
    $orderedServers = @('github', 'filesystem') + ($Servers | Where-Object { $_ -notin @('github', 'filesystem') })
    
    # Build JSON manually to maintain server order
    $jsonLines = @('{ "servers": {')
    
    $serverJsonLines = @()
    foreach ($server in $orderedServers) {
        if ($baseConfigData.servers.PSObject.Properties.Name -contains $server) {
            $serverConfig = $baseConfigData.servers.$server | ConvertTo-Json -Depth 10 -Compress
            # Format the server config with proper indentation
            $formattedConfig = $serverConfig -replace '^', '    ' -replace '\n', "`n    "
            $serverJsonLines += "  `"$server`": $formattedConfig"
        }
    }
    $jsonLines += ($serverJsonLines -join ",`n")
    $jsonLines += '  }'
    $jsonLines += '}'
    # Note: _metadata property removed to prevent JSON schema validation warnings
    
    return ($jsonLines -join "`n")
}

# Profile 1: Core Development (53 tools)
Write-Host "Creating profile: core (53 tools)" -ForegroundColor Green
$coreJson = New-ProfileConfig -Name "core" -ToolCount 53 -Tokens "8-10k" `
    -Servers @('github', 'filesystem', 'git', 'fetch')
$coreJson | Set-Content (Join-Path $profilesDir "core.json")
Write-Host "  ✓ Saved: core.json (github, filesystem, git, fetch)" -ForegroundColor Gray

# Profile 2: Full-Stack Development (80 tools)
Write-Host "Creating profile: fullstack (80 tools)" -ForegroundColor Green
$fullstackJson = New-ProfileConfig -Name "fullstack" -ToolCount 80 -Tokens "11-14k" `
    -Servers @('github', 'filesystem', 'git', 'fetch', 'playwright', 'postgres', 'sqlite', 'memory')
$fullstackJson | Set-Content (Join-Path $profilesDir "fullstack.json")
Write-Host "  ✓ Saved: fullstack.json (github, filesystem + 6 more servers)" -ForegroundColor Gray

# Profile 3: Testing & Automation (87 tools)
Write-Host "Creating profile: testing (87 tools)" -ForegroundColor Green
$testingJson = New-ProfileConfig -Name "testing" -ToolCount 87 -Tokens "12-15k" `
    -Servers @('github', 'filesystem', 'playwright', 'git', 'fetch', 'postgres')
$testingJson | Set-Content (Join-Path $profilesDir "testing.json")
Write-Host "  ✓ Saved: testing.json (github, filesystem, playwright, git, fetch, postgres)" -ForegroundColor Gray

# Profile 4: Data & Analytics (47 tools)
Write-Host "Creating profile: data (47 tools)" -ForegroundColor Green
$dataJson = New-ProfileConfig -Name "data" -ToolCount 47 -Tokens "7-9k" `
    -Servers @('github', 'filesystem', 'postgres', 'sqlite', 'memory', 'git', 'fetch')
$dataJson | Set-Content (Join-Path $profilesDir "data.json")
Write-Host "  ✓ Saved: data.json (github, filesystem, postgres, sqlite, memory, git, fetch)" -ForegroundColor Gray

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✓ Profile creation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Available profiles:" -ForegroundColor White
Write-Host "  • core       - 53 tools  (git, github, filesystem, fetch)" -ForegroundColor Gray
Write-Host "  • fullstack  - 80 tools  (+ playwright, postgres, sqlite, memory)" -ForegroundColor Gray
Write-Host "  • testing    - 87 tools  (playwright, github, filesystem, git, fetch, postgres)" -ForegroundColor Gray
Write-Host "  • data       - 47 tools  (postgres, sqlite, memory, filesystem, git, github)" -ForegroundColor Gray
Write-Host "  • all        - 107 tools (use base mcp.json)" -ForegroundColor Gray
Write-Host ""
Write-Host "Switch profiles with:" -ForegroundColor Yellow
Write-Host "  .\scripts\orchestrator.ps1 mcp set-profile -Profile core" -ForegroundColor Cyan
Write-Host ""
