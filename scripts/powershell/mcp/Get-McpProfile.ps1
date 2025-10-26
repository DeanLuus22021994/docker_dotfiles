# Get-McpProfile
# Displays the currently active MCP server profile

<#
.SYNOPSIS
    Shows the currently active MCP server profile configuration.

.DESCRIPTION
    Reads .vscode/mcp.json and displays:
    - Active profile name (from metadata if available)
    - Enabled servers
    - Tool count
    - Token usage estimate
    - Last generation timestamp

.PARAMETER Detailed
    Show detailed information about each enabled server.

.EXAMPLE
    .\Get-McpProfile.ps1
    Shows basic profile information.

.EXAMPLE
    .\Get-McpProfile.ps1 -Detailed
    Shows detailed information including server configurations.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [switch]$Detailed
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$workspaceRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$configFile = Join-Path $workspaceRoot ".vscode\mcp.json"

# Validate config exists
if (-not (Test-Path $configFile)) {
    Write-Host "✗ MCP config not found: $configFile" -ForegroundColor Red
    Write-Host "  No active MCP profile configured." -ForegroundColor Yellow
    exit 1
}

# Load configuration
try {
    $config = Get-Content $configFile | ConvertFrom-Json
} catch {
    Write-Host "✗ Failed to parse MCP config: $_" -ForegroundColor Red
    exit 1
}

# Extract information
$metadata = if ($config.PSObject.Properties.Name -contains '_metadata') { $config._metadata } else { $null }
$servers = $config.servers.PSObject.Properties.Name
$serverCount = $servers.Count

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ACTIVE MCP PROFILE" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

if ($metadata) {
    Write-Host "Profile Name:      " -NoNewline
    Write-Host $metadata.profile_name -ForegroundColor Green
    Write-Host "Tool Count:        " -NoNewline
    Write-Host $metadata.tool_count -ForegroundColor Cyan
    Write-Host "Estimated Tokens:  " -NoNewline
    Write-Host $metadata.estimated_tokens -ForegroundColor Cyan
    Write-Host "Last Generated:    " -NoNewline
    Write-Host $metadata.last_generated -ForegroundColor Gray
    Write-Host "Servers Enabled:   " -NoNewline
    Write-Host $serverCount -ForegroundColor Cyan
} else {
    Write-Host "Profile Name:      " -NoNewline
    Write-Host "custom" -ForegroundColor Yellow -NoNewline
    Write-Host " (no metadata)" -ForegroundColor Gray
    Write-Host "Servers Enabled:   " -NoNewline
    Write-Host $serverCount -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Enabled Servers:" -ForegroundColor White

foreach ($server in $servers | Sort-Object) {
    $serverConfig = $config.servers.$server
    $command = $serverConfig.command
    $runtime = if ($command -eq 'npx') { 'Node.js' } elseif ($command -eq 'uvx') { 'Python' } else { $command }
    
    Write-Host "  • " -NoNewline -ForegroundColor Gray
    Write-Host $server.PadRight(15) -NoNewline -ForegroundColor Green
    Write-Host " ($runtime)" -ForegroundColor Gray
    
    if ($Detailed) {
        $argsList = $serverConfig.args -join ' '
        Write-Host "    Command: $command $argsList" -ForegroundColor DarkGray
        if ($serverConfig.env) {
            $envVars = ($serverConfig.env.PSObject.Properties.Name) -join ', '
            Write-Host "    Env: $envVars" -ForegroundColor DarkGray
        }
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Show available profiles hint
Write-Host "Switch profiles with:" -ForegroundColor Yellow
Write-Host "  .\scripts\orchestrator.ps1 mcp set-profile -Profile <name>" -ForegroundColor Cyan
Write-Host ""
Write-Host "Available: core, fullstack, testing, data, all" -ForegroundColor Gray
Write-Host ""
