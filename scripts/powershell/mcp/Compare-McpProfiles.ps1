# Compare-McpProfiles
# Compares tool counts and server configurations between MCP profiles

<#
.SYNOPSIS
    Compares MCP profiles to show differences in tool counts and server configurations.

.DESCRIPTION
    Analyzes profile configurations to display:
    - Tool count differences
    - Server inclusion/exclusion
    - Token usage estimates
    - Runtime distribution (Node.js vs Python)

.PARAMETER Profile1
    First profile to compare (default: core)

.PARAMETER Profile2
    Second profile to compare (default: fullstack)

.PARAMETER ShowServers
    Display detailed server-level comparison

.EXAMPLE
    .\Compare-McpProfiles.ps1
    Compares core vs fullstack profiles.

.EXAMPLE
    .\Compare-McpProfiles.ps1 -Profile1 testing -Profile2 data -ShowServers
    Compares testing vs data profiles with server details.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("core", "fullstack", "testing", "data", "all")]
    [string]$Profile1 = "core",
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("core", "fullstack", "testing", "data", "all")]
    [string]$Profile2 = "fullstack",
    
    [Parameter(Mandatory=$false)]
    [switch]$ShowServers
)

$ErrorActionPreference = "Stop"

$workspaceRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$profilesDir = Join-Path $workspaceRoot ".vscode\configs\mcp\profiles"

# Profile file mapping
$profileFiles = @{
    "core" = "core.json"
    "fullstack" = "fullstack.json"
    "testing" = "testing.json"
    "data" = "data.json"
    "all" = "../../mcp.json"
}

# Load profiles
function Get-ProfileData {
    param([string]$ProfileName)
    
    $filePath = if ($ProfileName -eq "all") {
        Join-Path $workspaceRoot ".vscode\mcp.json"
    } else {
        Join-Path $profilesDir $profileFiles[$ProfileName]
    }
    
    if (-not (Test-Path $filePath)) {
        Write-Host "✗ Profile not found: $ProfileName ($filePath)" -ForegroundColor Red
        exit 1
    }
    
    $config = Get-Content $filePath | ConvertFrom-Json
    $servers = $config.servers.PSObject.Properties.Name
    $metadata = if ($config.PSObject.Properties.Name -contains '_metadata') { $config._metadata } else { $null }
    
    return @{
        Name = $ProfileName
        Config = $config
        Servers = $servers
        ServerCount = $servers.Count
        Metadata = $metadata
    }
}

$prof1 = Get-ProfileData $Profile1
$prof2 = Get-ProfileData $Profile2

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  MCP PROFILE COMPARISON" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Profile summaries
Write-Host "Profile 1: " -NoNewline
Write-Host $prof1.Name.ToUpper() -ForegroundColor Green
if ($prof1.Metadata) {
    Write-Host "  Tools: $($prof1.Metadata.tool_count)" -ForegroundColor Gray
    Write-Host "  Tokens: $($prof1.Metadata.estimated_tokens)" -ForegroundColor Gray
}
Write-Host "  Servers: $($prof1.ServerCount)" -ForegroundColor Gray

Write-Host ""
Write-Host "Profile 2: " -NoNewline
Write-Host $prof2.Name.ToUpper() -ForegroundColor Green
if ($prof2.Metadata) {
    Write-Host "  Tools: $($prof2.Metadata.tool_count)" -ForegroundColor Gray
    Write-Host "  Tokens: $($prof2.Metadata.estimated_tokens)" -ForegroundColor Gray
}
Write-Host "  Servers: $($prof2.ServerCount)" -ForegroundColor Gray

Write-Host ""
Write-Host "───────────────────────────────────────────────────────────────" -ForegroundColor DarkGray
Write-Host ""

# Calculate differences
if ($prof1.Metadata -and $prof2.Metadata) {
    $toolDiff = $prof2.Metadata.tool_count - $prof1.Metadata.tool_count
    $toolDiffPercent = [math]::Round(($toolDiff / $prof1.Metadata.tool_count) * 100, 1)
    
    Write-Host "Tool Count Difference:" -ForegroundColor White
    if ($toolDiff -gt 0) {
        Write-Host "  $($prof2.Name) has $toolDiff more tools " -NoNewline -ForegroundColor Yellow
        Write-Host "(+$toolDiffPercent%)" -ForegroundColor Gray
    } elseif ($toolDiff -lt 0) {
        Write-Host "  $($prof2.Name) has $([math]::Abs($toolDiff)) fewer tools " -NoNewline -ForegroundColor Cyan
        Write-Host "($toolDiffPercent%)" -ForegroundColor Gray
    } else {
        Write-Host "  Same tool count" -ForegroundColor Gray
    }
    Write-Host ""
}

# Server comparison
$onlyInProf1 = $prof1.Servers | Where-Object { $_ -notin $prof2.Servers }
$onlyInProf2 = $prof2.Servers | Where-Object { $_ -notin $prof1.Servers }
$inBoth = $prof1.Servers | Where-Object { $_ -in $prof2.Servers }

Write-Host "Server Distribution:" -ForegroundColor White
Write-Host "  In both profiles: " -NoNewline -ForegroundColor Gray
Write-Host $inBoth.Count -ForegroundColor Cyan
if ($inBoth.Count -gt 0 -and $ShowServers) {
    foreach ($server in $inBoth | Sort-Object) {
        Write-Host "    • $server" -ForegroundColor Gray
    }
}

Write-Host "  Only in $($prof1.Name): " -NoNewline -ForegroundColor Gray
Write-Host $onlyInProf1.Count -ForegroundColor Yellow
if ($onlyInProf1.Count -gt 0) {
    foreach ($server in $onlyInProf1 | Sort-Object) {
        Write-Host "    • $server" -ForegroundColor Yellow
    }
}

Write-Host "  Only in $($prof2.Name): " -NoNewline -ForegroundColor Gray
Write-Host $onlyInProf2.Count -ForegroundColor Green
if ($onlyInProf2.Count -gt 0) {
    foreach ($server in $onlyInProf2 | Sort-Object) {
        Write-Host "    • $server" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
